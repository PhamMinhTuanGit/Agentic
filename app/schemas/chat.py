"""
Pydantic schemas for Chat
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ChatMessageBase(BaseModel):
    """Base chat message schema"""
    content: str = Field(..., min_length=1, max_length=500)
    role: str = Field(..., pattern="^(user|assistant)$")


class ChatMessageCreate(ChatMessageBase):
    """Create chat message"""
    session_id: int


class ChatMessageResponse(ChatMessageBase):
    """Chat message response"""
    id: int
    session_id: int
    is_summary: bool
    
    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    """Base chat session schema"""
    title: str = Field(..., min_length=1, max_length=100)


class ChatSessionCreate(ChatSessionBase):
    """Create chat session"""
    user_id: int


class ChatSessionResponse(ChatSessionBase):
    """Chat session response"""
    id: int
    user_id: int
    messages: List[ChatMessageResponse] = []
    
    class Config:
        from_attributes = True


class ChatQueryRequest(BaseModel):
    """Chat query request"""
    user_id: int
    session_id: Optional[int] = None
    message: str = Field(..., min_length=1, max_length=500)
    use_rag: bool = True


class ChatQueryResponse(BaseModel):
    """Chat query response"""
    session_id: int
    message_id: int
    response: Optional[str] = None
    status: str = "success"


class ChatHistoryResponse(BaseModel):
    """Chat history response"""
    session_id: int
    messages: List[ChatMessageResponse]


class ChatSessionSummaryResponse(BaseModel):
    """Chat session summary response"""
    session_id: int
    summary: Optional[str] = None
    message_count: int
