import bcrypt  # For hashing passwords securely
import jwt  # For creating JSON Web Tokens for session management
import datetime  # To handle date and time for token expiration
import json  # For reading and writing user data in JSON format
import random  # To generate random OTPs
import smtplib  # For sending emails with OTP
from email.message import EmailMessage
from cryptography.fernet import Fernet
from config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT, ENCRYPTION_KEY

# Config variables are imported from the separate config file
USER_DB_FILE = "src/users.json"  # Path to JSON file where user data is stored
MFA_TOKENS = {}  # A dictionary to temporarily store OTPs associated with users
cipher = Fernet(ENCRYPTION_KEY)

# Reads user data from JSON file
def load_users():
    try:
        with open(USER_DB_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Saves user data back to JSON file, formatting it for readability
def save_users(users):
    try:
        with open(USER_DB_FILE, "w") as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        print(f"Error saving user: {e}")

# Registers a new user by hashing password and storing their details
def register(username, password, role="customer", email=""):
    users = load_users()
    if username in users:
        return "User already exists!"

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = {
        "password": hashed_pw.decode(),
        "role": role,
        "email": encrypt_data(email),
    }
    save_users(users)
    return "User registered successfully!"

# Generates a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Sends the generated OTP to the user's email address
def send_otp(email, otp):
    try:
        msg = EmailMessage()
        msg.set_content(f"Your MFA OTP Code is: {otp}")
        msg["Subject"] = "Your Secure Retail MFA OTP"
        msg["From"] = SMTP_EMAIL
        msg["To"] = email

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        return "OTP sent successfully!"
    except Exception as e:
        return f"Error sending OTP: {e}"

# Authenticates the user by checking credentials
def login(username, password):
    users = load_users()
    if username not in users:
        return "User not found!"

    stored_password = users[username]["password"].encode()
    if bcrypt.checkpw(password.encode(), stored_password):
        otp = generate_otp()
        MFA_TOKENS[username] = otp
        email = decrypt_data(users[username]["email"])  # Decrypt email before sending OTP
        return send_otp(email, otp)
    return "Invalid credentials!"

# Defines secret key
SECRET_KEY = "your_secret_key"

# Validates the OTP entered by the user
def verify_otp(username, otp):
    if username in MFA_TOKENS and MFA_TOKENS[username] == otp:
        token = jwt.encode(
            {"user": username, "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)},
            SECRET_KEY, algorithm="HS256",
        )
        del MFA_TOKENS[username]
        return f"Login successful! Token: {token}"
    return "Invalid OTP!"

# Authenticates a JWT token
def authenticate(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user"]
    except jwt.ExpiredSignatureError:
        return "Token has expired!"
    except jwt.InvalidTokenError:
        return "Invalid token"

# Encrypt data
def encrypt_data(data):
    try:
        return cipher.encrypt(data.encode()).decode()
    except Exception as e:
        return f"Encryption error: {e}"

# Decrypt data
def decrypt_data(data):
    try:
        return cipher.decrypt(data.encode()).decode()
    except Exception as e:
        return f"Decryption error: {e}"
