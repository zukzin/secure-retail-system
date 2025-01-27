import datetime
import pytest
from secure_retail_system.src import verify_otp, authenticate, MFA_TOKENS
from secure_retail_system.src import register, login

def test_register():
    # Test successful registration
    result = register("test_user", "password123", "customer", "test_user@example.com")
    assert result == "User registered successfully!"

    # Test duplicate registration
    result = register("test_user", "password123", "customer", "test_user@example.com")
    assert result == "User already exists!"

def test_login():
    # Register a user
    register("test_user", "password123", "customer", "test_user@example.com")

    # Test successful login
    result = login("test_user", "password123")
    assert "OTP sent successfully!" in result

    # Test login with invalid password
    result = login("test_user", "wrong_password")
    assert result == "Invalid credentials!"

    # Test login for non-existent user
    result = login("unknown_user", "password123")
    assert result == "User not found!"

def test_verify_otp():
    # Register and login to generate OTP
    register("test_user", "password123", "customer", "test_user@example.com")
    login("test_user", "password123")

    # Retrieve OTP from the MFA tokens
    otp = MFA_TOKENS["test_user"]

    # Test correct OTP verification
    result = verify_otp("test_user", otp)
    assert "Login successful!" in result

    # Test invalid OTP
    result = verify_otp("test_user", "000000")
    assert result == "Invalid OTP!"

    # Test valid token
    result = authenticate(token)
    assert result == "test_user"

    # Test expired token
    expired_token = jwt.encode(
        {"user": "test_user", "exp": datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)},
        algorithm="HS256",
    )
    result = authenticate(expired_token)
    assert result == "Token has expired!"

    # Test invalid token
    result = authenticate("invalid_token")
    assert result == "Invalid token"
