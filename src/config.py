# SMTP (Simple Mail Transfer Protocol) email configuration for Multi-Factor Authentication (MFA).
import os
from cryptography.fernet import Fernet

from secure_retail_system.src.security import SECRET_KEY

#SMTP Email Config for MFA
SMTP_EMAIL = "your-email@example.com" # The email address used to send emails (e.g. for MFA codes).
SMTP_PASSWORD = "your-email-password" # The password for the SMTP email account, used to authenticate sending emails.
SMTP_SERVER = "smtp.gmail.com" # The server address for connecting to the GMail SMTP service.
SMTP_PORT = 465 # The port number used for secure email transmission (SSL).
ENCRYPTION_KEY = Fernet.generate_key().decode()

class Fernet:
    pass

if __name__ == "main__":
    new_secret_key = SECRET_KEY()
    print(f"Generated Secret Key: {new_secret_key}")


