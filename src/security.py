# Time module imported for handling time-related functions e.g. tracking when failed attempts occur.
import time
from cryptography.fernet import Fernet

# Generate encryption keys for secure data handling
SECRET_KEY = Fernet.generate_key()
fernet = Fernet(SECRET_KEY)

ENCRYPTION_KEY = Fernet.generate_key().decode()

# Dictionary to track failed login attempts
failed_attempts = {}

# This function is to check if a user has exceeded the allowed number of failed login attempts.
def check_brute_force(username):
    if username in failed_attempts: # This retrieves the number of attempts and the time of the attempt.
        attempts, last_attempt_time = failed_attempts[username]
        if attempts >= 3 and time.time() - last_attempt_time < 30:
            return  "Too many failed attempts! Try again later."
        if time.time() - last_attempt_time > 30:
            failed_attempts[username] = (0, time.time())
    return None

# This function updates the count of failed login attempts for a given username.
def track_failed_attempt(username):
    if username in failed_attempts:
        attempts, _ = failed_attempts[username]
        failed_attempts[username] = (attempts + 1, time.time())
    else:
        failed_attempts[username] = (1, time.time())


# Checks if the input data contains any restricted characters that could lead to SQL inject attacks.
def sanitize_input(data):

    restricted_chars = ["'", '"', ";", "__", "/*", "*/"]
    return all(char not in data for char in restricted_chars)

"""
      Validates the input to ensure it doesn't contain restricted characters.
      Args:
          data (str): The user-provides input.
      Returns:
          bool: True if the input is valid, False if it contains restricted characters.
"""
# Returns True if none of the restricted characters are found in the input, or it returns False.

def encrypt_data(data: str) -> str:
    """Encrypt the data provided"""
    data_bytes = data.encode()
    encrypted_data = fernet.encrypt(data_bytes)
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt the provided encrypted data."""
    encrypted_data_bytes = encrypted_data.encode()
    decrypted_data = fernet.decrypt(encrypted_data_bytes)
    return decrypted_data.decode()
