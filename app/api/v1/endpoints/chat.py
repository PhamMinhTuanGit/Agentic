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
    return StreamingResponse(
        agent.chat_stream(str(req.session_id), req.message),
        media_type="text/plain"
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
    return StreamingResponse(
        agent.chat_stream_nothink(str(req.session_id), f"{req.message}"),
        media_type="text/plain"
    )


