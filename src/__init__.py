from cryptography.fernet import Fernet
import bcrypt
from .auth import register, login, verify_otp, authenticate, MFA_TOKENS, load_users

# Shared encryption key and Fernet object

def hash_password(password: str) -> bytes:
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_pw = bcrypt.hashpw(password.encode(), salt)  # Hash the password
    return hashed_pw

def generate_salt() -> bytes:
    """
    Generates a salt for bcrypt hashing.

    Returns:
        bytes: A randomly generated salt.
    """
    return bcrypt.gensalt()

def verify_password(plaintext: str, hashed: bytes) -> bool:
    """
    Verifies a plaintext password against a hashed password.
    """
    return bcrypt.checkpw(plaintext.encode(), hashed)

# Exposing for external modules
__all__ = ["register", "login", "verify_otp", "authenticate", "MFA_TOKENS", "hash_password", "verify_password", "generate_salt"]
