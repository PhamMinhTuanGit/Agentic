"""
Database session management for agent module
"""
import sys
from pathlib import Path

# Add agent module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import sessionmaker, Session
from agent.chat_session_management import engine

# Session factory using agent's engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_agent_db() -> Session:
    """Dependency for getting agent database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
