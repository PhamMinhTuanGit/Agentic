"""
Chat service with business logic
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status
from typing import List, Dict, Optional

# Import từ agent module
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent.chat_session_management import (
    User, ChatSession, ChatMessage
)
from agent.retriever import model_response
from agent.prompt_template import build_summarize_prompt


class ChatService:
    """Chat service for business logic"""
    
    @staticmethod
    def create_user(db: Session, username: str) -> User:
        """Create new user"""
        # Check if user exists
        existing_user = db.query(User).filter(User.name == username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {username} already exists"
            )
        
        user = User(name=username)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """Get user by ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found"
            )
        return user
    
    @staticmethod
    def user_exists(db: Session, username: str) -> bool:
        """Check if user exists"""
        user = db.query(User).filter(User.name == username).first()
        return user is not None
    
    @staticmethod
    def create_chat_session(db: Session, user_id: int, title: str = None) -> ChatSession:
        """Create new chat session"""
        # Verify user exists
        ChatService.get_user(db, user_id)
        
        if title is None:
            title = f"Chat Session {ChatSession.__table__.select().count() + 1}"
        
        session = ChatSession(user_id=user_id, title=title)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_chat_session(db: Session, session_id: int, user_id: int = None) -> ChatSession:
        """Get chat session by ID"""
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chat session {session_id} not found"
            )
        
        # Check if user owns this session
        if user_id and session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this session"
            )
        
        return session
    
    @staticmethod
    def get_user_sessions(db: Session, user_id: int) -> List[ChatSession]:
        """Get all chat sessions for user"""
        ChatService.get_user(db, user_id)
        
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == user_id
        ).all()
        return sessions
    
    @staticmethod
    def add_message(
        db: Session,
        session_id: int,
        content: str,
        role: str,
        is_summary: bool = False
    ) -> ChatMessage:
        """Add message to chat session"""
        # Verify session exists
        ChatService.get_chat_session(db, session_id)
        
        message = ChatMessage(
            session_id=session_id,
            content=content,
            role=role,
            is_summary=is_summary
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    @staticmethod
    def get_recent_messages(
        db: Session,
        session_id: int,
        limit: int = 10
    ) -> List[ChatMessage]:
        """Get recent messages from session"""
        ChatService.get_chat_session(db, session_id)
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.id.desc()).limit(limit).all()
        
        return list(reversed(messages))
    
    @staticmethod
    def get_session_history(db: Session, session_id: int) -> List[ChatMessage]:
        """Get full message history"""
        ChatService.get_chat_session(db, session_id)
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.id.asc()).all()
        
        return messages
    
    @staticmethod
    def summarize_latest_messages(
        db: Session,
        session_id: int,
        message_count: int = 5
    ) -> Optional[str]:
        """Summarize latest messages"""
        ChatService.get_chat_session(db, session_id)
        
        # Get latest messages
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.id.desc()).limit(message_count).all()
        
        if not messages:
            return None
        
        # Extract message contents
        message_contents = [msg.content for msg in reversed(messages)]
        
        # Generate summary using LLM
        try:
            prompt = build_summarize_prompt(message_contents)
            summary = model_response(prompt)
            return summary
        except Exception as e:
            return f"Error summarizing: {str(e)}"
    
    @staticmethod
    def delete_session(db: Session, session_id: int, user_id: int = None) -> None:
        """Delete chat session"""
        session = ChatService.get_chat_session(db, session_id, user_id)
        db.delete(session)
        db.commit()
