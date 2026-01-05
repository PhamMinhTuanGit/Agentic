from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.agent.schemas import ChatRequest
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


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    agent = MirixAgentDB(db)
    reply = agent.chat(str(req.session_id), req.message)
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


@router.post("/chat/only_config")
def chat_only_config(req: ChatRequest, db: Session = Depends(get_db)):
    agent = MirixAgentDB(db)
    def generate():
        for token in agent.chat(str(req.session_id), req.message):
            yield token

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )