from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.agent.schemas import ChatRequest, MessageRequest
from app.agent.agent import MirixAgentDB
from app.db.session import get_db
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/chat_stream")
def chat_stream(req: ChatRequest, db: Session = Depends(get_db)):
    """Stream tokens from the agent with memory management"""
    agent = MirixAgentDB(db)
    
    def generate():
        for token in agent.chat_stream(str(req.session_id), req.message):
            yield token
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/sessions/{session_id}/messages/stream")
def stream_session_message(
    session_id: str,
    req: MessageRequest,
    db: Session = Depends(get_db),
):
    """REST endpoint: stream model output for a message in a session."""
    agent = MirixAgentDB(db)

    def generate():
        for token in agent.chat_stream(str(session_id), req.message):
            yield token

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    agent = MirixAgentDB(db)
    reply = agent.chat(str(req.session_id), req.message)
    return {"reply": reply}


@router.post("/sessions/{session_id}/messages")
def create_session_message(
    session_id: str,
    req: MessageRequest,
    db: Session = Depends(get_db),
):
    """REST endpoint: create a message and return the assistant response."""
    agent = MirixAgentDB(db)
    reply = agent.chat(str(session_id), req.message)
    return {"reply": reply}

@router.post("/chat_stream/nothink")
def chat_stream_nothink(req: ChatRequest, db: Session = Depends(get_db)):
    """Stream tokens from the agent without thinking markers"""
    agent = MirixAgentDB(db)
    
    def generate():
        for token in agent.chat_stream_nothink(str(req.session_id), req.message):
            yield token
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/sessions/{session_id}/messages/stream/no-think")
def stream_session_message_without_thinking(
    session_id: str,
    req: MessageRequest,
    db: Session = Depends(get_db),
):
    """REST endpoint: stream output without think markers for a session message."""
    agent = MirixAgentDB(db)

    def generate():
        for token in agent.chat_stream_nothink(str(session_id), req.message):
            yield token

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/chat/only_config")
def chat_only_config(req: ChatRequest, db: Session = Depends(get_db)):
    agent = MirixAgentDB(db)
    def generate():
        for token in agent.full_configuration(str(req.session_id), req.message):
            yield token
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/sessions/{session_id}/configurations/stream")
def stream_session_configuration(
    session_id: str,
    req: MessageRequest,
    db: Session = Depends(get_db),
):
    """REST endpoint: stream full device configuration output for a session."""
    agent = MirixAgentDB(db)

    def generate():
        for token in agent.full_configuration(str(session_id), req.message):
            yield token

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
    
