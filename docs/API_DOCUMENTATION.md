# FastAPI Chat Endpoints Documentation

## Overview
API endpoints for managing chat sessions và messages using `chat_session_management` module.

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### Users

#### Create User
```
POST /chat/users?username=<username>
```

**Response:**
```json
{
  "id": 1,
  "name": "username",
  "message": "User username created successfully"
}
```

#### Get User
```
GET /chat/users/{user_id}
```

**Response:**
```json
{
  "id": 1,
  "name": "username",
  "sessions_count": 3
}
```

#### Check User Exists
```
GET /chat/users/{user_id}/check
```

---

### Chat Sessions

#### Create Session
```
POST /chat/sessions
Content-Type: application/json

{
  "user_id": 1,
  "title": "My Chat Session"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "My Chat Session",
  "messages": []
}
```

#### Get Session
```
GET /chat/sessions/{session_id}
```

#### Get User Sessions
```
GET /chat/users/{user_id}/sessions
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Session 1",
    "messages": [...]
  }
]
```

#### Delete Session
```
DELETE /chat/sessions/{session_id}?user_id={user_id}
```

---

### Messages

#### Add Message
```
POST /chat/messages
Content-Type: application/json

{
  "session_id": 1,
  "content": "Hello AI!",
  "role": "user"
}
```

**Role values:** `user` hoặc `assistant`

**Response:**
```json
{
  "id": 1,
  "session_id": 1,
  "content": "Hello AI!",
  "role": "user",
  "is_summary": false
}
```

#### Get Session History
```
GET /chat/sessions/{session_id}/messages?limit=10
```

**Query Parameters:**
- `limit`: Number of messages to retrieve (1-100, default: 10)

**Response:**
```json
{
  "session_id": 1,
  "messages": [
    {
      "id": 1,
      "session_id": 1,
      "content": "Hello",
      "role": "user",
      "is_summary": false
    }
  ]
}
```

---

### Chat Operations

#### Chat Query
```
POST /chat/query
Content-Type: application/json

{
  "user_id": 1,
  "session_id": 1,
  "message": "What is BGP?",
  "use_rag": true
}
```

**Parameters:**
- `user_id`: ID người dùng (bắt buộc)
- `session_id`: ID session (nếu None, tạo session mới)
- `message`: Nội dung tin nhắn
- `use_rag`: Có dùng RAG không (optional, default: true)

**Response:**
```json
{
  "session_id": 1,
  "message_id": 2,
  "response": "BGP is a Border Gateway Protocol...",
  "status": "success"
}
```

#### Summarize Session
```
POST /chat/sessions/{session_id}/summarize?message_count=5
```

**Query Parameters:**
- `message_count`: Số message để summarize (1-20, default: 5)

**Response:**
```json
{
  "session_id": 1,
  "summary": "Summary of the last 5 messages...",
  "message_count": 10
}
```

---

## Example Usage

### Python
```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Create user
user_res = requests.post(f"{BASE_URL}/chat/users?username=john")
user_id = user_res.json()["id"]

# Create session
session_res = requests.post(
    f"{BASE_URL}/chat/sessions",
    json={"user_id": user_id, "title": "ZebOS Chat"}
)
session_id = session_res.json()["id"]

# Send query
query_res = requests.post(
    f"{BASE_URL}/chat/query",
    json={
        "user_id": user_id,
        "session_id": session_id,
        "message": "How to configure OSPF?",
        "use_rag": True
    }
)
print(query_res.json())

# Get history
history_res = requests.get(
    f"{BASE_URL}/chat/sessions/{session_id}/messages?limit=10"
)
print(history_res.json())
```

### cURL
```bash
# Create user
curl -X POST "http://localhost:8000/api/v1/chat/users?username=john"

# Create session
curl -X POST "http://localhost:8000/api/v1/chat/sessions" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "title": "ZebOS Chat"}'

# Send query
curl -X POST "http://localhost:8000/api/v1/chat/query" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "session_id": 1,
    "message": "How to configure OSPF?",
    "use_rag": true
  }'

# Get history
curl "http://localhost:8000/api/v1/chat/sessions/1/messages?limit=10"
```

---

## Error Handling

### Common Status Codes
- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `403`: Forbidden
- `404`: Not Found
- `500`: Server Error

### Error Response Format
```json
{
  "detail": "Error message"
}
```

---

## Database Models

### User
- `id`: Integer (Primary Key)
- `name`: String (Unique)
- `chat_sessions`: Relationship to ChatSession

### ChatSession
- `id`: Integer (Primary Key)
- `title`: String
- `user_id`: Integer (Foreign Key)
- `user`: Relationship to User
- `messages`: Relationship to ChatMessage

### ChatMessage
- `id`: Integer (Primary Key)
- `session_id`: Integer (Foreign Key)
- `content`: String (Max 500 chars)
- `role`: String (user/assistant)
- `is_summary`: Boolean
- `session`: Relationship to ChatSession
