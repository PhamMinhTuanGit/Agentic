"""
Tests for chat endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    """Test user creation"""
    response = client.post("/api/v1/chat/users?username=testuser")
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "testuser"


def test_get_user():
    """Test get user"""
    # Create user first
    create_response = client.post("/api/v1/chat/users?username=getuser")
    user_id = create_response.json()["id"]
    
    # Get user
    response = client.get(f"/api/v1/chat/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "getuser"


def test_create_session():
    """Test session creation"""
    # Create user first
    user_response = client.post("/api/v1/chat/users?username=sessionuser")
    user_id = user_response.json()["id"]
    
    # Create session
    session_data = {
        "user_id": user_id,
        "title": "Test Chat Session"
    }
    response = client.post("/api/v1/chat/sessions", json=session_data)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Chat Session"


def test_add_message():
    """Test adding message"""
    # Setup
    user_response = client.post("/api/v1/chat/users?username=msguser")
    user_id = user_response.json()["id"]
    
    session_data = {"user_id": user_id, "title": "Message Test"}
    session_response = client.post("/api/v1/chat/sessions", json=session_data)
    session_id = session_response.json()["id"]
    
    # Add message
    message_data = {
        "session_id": session_id,
        "content": "Hello AI!",
        "role": "user"
    }
    response = client.post("/api/v1/chat/messages", json=message_data)
    assert response.status_code == 201
    assert response.json()["content"] == "Hello AI!"


def test_get_session_history():
    """Test get session history"""
    # Setup
    user_response = client.post("/api/v1/chat/users?username=historyuser")
    user_id = user_response.json()["id"]
    
    session_data = {"user_id": user_id, "title": "History Test"}
    session_response = client.post("/api/v1/chat/sessions", json=session_data)
    session_id = session_response.json()["id"]
    
    # Add message
    message_data = {
        "session_id": session_id,
        "content": "Test message",
        "role": "user"
    }
    client.post("/api/v1/chat/messages", json=message_data)
    
    # Get history
    response = client.get(f"/api/v1/chat/sessions/{session_id}/messages")
    assert response.status_code == 200
    assert len(response.json()["messages"]) > 0
