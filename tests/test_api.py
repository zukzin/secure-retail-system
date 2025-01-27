import pytest
from api import app
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_root_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Welcome to the Secure Retail System API" in response.json["message"]

@patch('auth.register', return_value="User registered successfully!")

def test_register(client): # Pass client as parameter
    data = {"username": "john_doe", "password": "secure_password", "email": "john@example.com"}
    response = client.post('/register', json=data)
    assert response.status_code == 200

def test_get_products(client):  # Pass client as a parameter
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)