"""
User ORM model
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from agent.chat_session_management import Base, User
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.models.chat import ChatSession

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    chat_sessions: Mapped[list["ChatSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, sessions_count={len(self.chat_sessions)}, created_sessions={[session.id for session in self.chat_sessions]!r})"



