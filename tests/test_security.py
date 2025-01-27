import sys
import os

sys.path.append(src_secure_retail_system(src_secure_retail_system(secure_retail_system(__file__), '../src')))
from security import check_brute_force, track_failed_attempt, sanitize_input

def test_check_brute_force():
    username = "test_user"

    # Simulate failed login attempts
    track_failed_attempt(username)
    track_failed_attempt(username)
    track_failed_attempt(username)

    # Test  lockout message after 3 failed attempts
    result = check_brute_force(username)
    assert result == "Too many failed attempts! Try again later."

def test_sanitize_input():
    # Test valid input
    assert sanitize_input("validInput123") is True

    # Test inout with restricted characters
    assert  sanitize_input("Invalid'; DROP TABLE users; __") is False
    assert sanitize_input("normalString") is True

