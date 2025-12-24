"""
Chat endpoints
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatQueryRequest,
    ChatQueryResponse,
    ChatHistoryResponse,
    ChatSessionSummaryResponse,
    ChatSessionBase
)
from app.services.chat_service import ChatService


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(username: str, db: Session = Depends(get_db)):
    """Create new user"""
    user = ChatService.create_user(db, username)
    return {
        "id": user.id,
        "name": user.name,
        "message": f"User {username} created successfully"
    }


@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = ChatService.get_user(db, user_id)
    return {
        "id": user.id,
        "name": user.name,
        "sessions_count": len(user.chat_sessions)
    }


@router.get("/users/{user_id}/check")
async def check_user_exists(user_id: int, db: Session = Depends(get_db)):
    """Check if user exists"""
    try:
        ChatService.get_user(db, user_id)
        return {"exists": True, "user_id": user_id}
    except:
        return {"exists": False, "user_id": user_id}


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_create: ChatSessionCreate,
    db: Session = Depends(get_db)
):
    """Create new chat session"""
    session = ChatService.create_chat_session(
        db,
        user_id=session_create.user_id,
        title=session_create.title
    )
    return session


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get chat session by ID"""
    session = ChatService.get_chat_session(db, session_id)
    return session


@router.get("/users/{user_id}/sessions", response_model=List[ChatSessionResponse])
async def get_user_sessions(user_id: int, db: Session = Depends(get_db)):
    """Get all sessions for user"""
    sessions = ChatService.get_user_sessions(db, user_id)
    return sessions


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    """Delete chat session"""
    ChatService.delete_session(db, session_id, user_id)
    return None


@router.post("/messages", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def add_message(
    message_create: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """Add message to session"""
    message = ChatService.add_message(
        db,
        session_id=message_create.session_id,
        content=message_create.content,
        role=message_create.role
    )
    return message


@router.get("/sessions/{session_id}/messages", response_model=ChatHistoryResponse)
async def get_session_history(
    session_id: int,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get message history for session"""
    ChatService.get_chat_session(db, session_id)
    messages = ChatService.get_recent_messages(db, session_id, limit)
    
    return ChatHistoryResponse(
        session_id=session_id,
        messages=messages
    )


@router.post("/query", response_model=ChatQueryResponse)
async def chat_query(
    query: ChatQueryRequest,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint - handles user queries and creates/manages sessions
    """
    try:
        session_id = query.session_id
        
        # If no session ID, create new session
        if session_id is None:
            session = ChatService.create_chat_session(db, query.user_id)
            session_id = session.id
        else:
            # Verify user owns this session
            ChatService.get_chat_session(db, session_id, query.user_id)
        
        # Add user message
        user_msg = ChatService.add_message(
            db,
            session_id,
            query.message,
            "user"
        )
        
        # Generate AI response (placeholder - integrate with your LLM)
        ai_response = f"Response to: {query.message}"
        
        # Add AI message
        ai_msg = ChatService.add_message(
            db,
            session_id,
            ai_response,
            "assistant"
        )
        
        return ChatQueryResponse(
            session_id=session_id,
            message_id=ai_msg.id,
            response=ai_response,
            status="success"
        )
    
    except Exception as e:
        return ChatQueryResponse(
            session_id=query.session_id or -1,
            message_id=-1,
            response=str(e),
            status="error"
        )


@router.post("/sessions/{session_id}/summarize", response_model=ChatSessionSummaryResponse)
async def summarize_session(
    session_id: int,
    message_count: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Summarize latest messages in session"""
    ChatService.get_chat_session(db, session_id)
    
    summary = ChatService.summarize_latest_messages(db, session_id, message_count)
    
    messages = ChatService.get_session_history(db, session_id)
    
    return ChatSessionSummaryResponse(
        session_id=session_id,
        summary=summary,
        message_count=len(messages)
    )
