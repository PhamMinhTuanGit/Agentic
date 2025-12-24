"""
Tests for user endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    """Test user registration"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]


def test_login_user():
    """Test user login"""
    # First register
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "full_name": "Login User",
        "password": "testpassword123"
    }
    client.post("/api/v1/users/register", json=user_data)
    
    # Then login
    login_data = {
        "username": "loginuser",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
