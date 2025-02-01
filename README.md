# Secure Retail System

A Python-based retail system demonstrating secure user authentication (with MFA), brute-force prevention, input sanitisation, and product management. 
The system is split into two primary interfaces: 
1. Command-Line Interface (CLI) 
2. REST API using Flask.

## Table of Contents
- Overview
- Features
- Project Structure
- Getting Started
- Prerequisites
- Installation
- Running the CLI
- Running the Flask API
- Usage Examples
- CLI Usage
- API Usage
- Security Highlights
- Testing

## Overview

This Secure Retail System is designed to illustrate best practices in Python for:

1. Authentication & MFA: Users authenticate with a username, password, and a one-time code (OTP) sent via email.
2. Brute-Force Prevention: Automatically locks out users after consecutive failed login attempts within a short timeframe.
3. Role-Based Access: Differentiates between admin and customer functionalities. Admins can add/update/delete products, while customers can only view.
4. Data Encryption: Uses Fernet to encrypt sensitive data (e.g., email addresses) at rest.
5. Logging & Auditing: Logs critical user actions for security audits.
6. Input Sanitisation: Checks user inputs for restricted characters to mitigate injection attacks.

## Features

**CLI Interface** (main.py):

- Register new users (with role and email for MFA).
- Login with password; receive OTP for second-factor authentication.
- Add or view products (admin-only vs. customer).

**REST API** (api.py):

- Endpoints for registration, login, OTP verification, product CRUD operations.
- Rate-limited using flask_limiter (prevents excessive requests).
- Returns JSON responses for easy integration with front-end or other services.

**Modular Design:**

- auth.py for authentication logic (register, login, OTP verification, JWT).
- database.py for product-related CRUD operations.
- security.py for brute-force check, tracking failed attempts, input sanitisation, and data encryption.
- config.py for centralized configuration of SMTP credentials, encryption keys, etc.

**Testing:**

- test_api.py and test_auth.py unit/integration tests for the Flask API and authentication logic.
- test_security.py for verifying brute-force checks, sanitisation, and encryption.


# Project Structure

Below is a simplified directory layout.

SecureRetailSystem/

├── src/
├── README.md
├── requirements.txt
├── config.py
├── main.py                # CLI entry point
├── api.py                 # Flask API
├── auth.py                # User auth, MFA logic
├── database.py            # Product CRUD operations
├── security.py            # Brute force, encryption, sanitization
├── logger.py              # User action logging
├── tests/
│   ├── test_api.py
│   ├── test_auth.py
│   └── test_security.py

│   ├── users.json         # Local user data (or users.jason.py placeholder)
└── └── __init__.py
 

# Getting Started

## Prerequisites

**- Python 3.13+**
- (Optional) A local or virtual environment management tool (e.g., venv)
- SMTP Email Account: For sending OTPs (e.g., Gmail). Adjust the settings in config.py

## Installation

- 1. ""Clone""
git clone https://github.com/zukzin/SecureRetailSystem.git
cd SecureRetailSystem

- 2. **Create and activate a Virtual Environment (recommended)
python3 -m venv venv
source venv\Scripts\activate

- 3. **Install Dependencies**
Ensure you set SMTP_EMAIL, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT, etc.

## Running the CLI
From the project root, run:

python main.py

You should see a welcome message:

Welcome to the Secure Retail System CLI
Options:
- 1. Register
- 2. Login
- 3. Verify OTP & Get Token
- 4. Add Product (Admin Only)
- 5. View Products
- 6. Exit

## Running the Flask API

python api.py

- By default the server runs at http://127.0.0.1:5000/.
- Check the root endpoint (GET /) for a brief welcome and list of available endpoints.

## Usage Examples

**CLI Usage

- **1. Register New User**
- **2. Login + OTP
- **3. Add/View Products**

**API Usage
**Register (POST/register):
**Login (POST/Login)
**Verify OTP (POST/verify_otp)

**Products:**
GET /products
POST /products (admin only)
PUT /products/<id>
DELETE /products/<id>

## Security Highlights

**MFA (OTP)**: Enhances security by requiring a one-time code sent via email.
**Password Hashing:** Uses bcrypt to store salted, hashed passwords.
**Brute-Force Protection:** Lock out accounts for 30 seconds after 3 failed login attempts.
**Input Sanitisation:** security.py ensures restricted characters aren’t passed to potentially vulnerable endpoints.
**Encryption:** Email addresses (or other sensitive data) encrypted with Fernet in auth.py.

## Testing
All tests are located in the test/ folder
- API Tests: test_api.py
- Auth Tests: test_auth.py
- Security Tests: test_security.py

To run all tests:

pytest

Ensure you have pytest installed

Thank you, for any improvements, feel free to open an issue or submit a pull request!
