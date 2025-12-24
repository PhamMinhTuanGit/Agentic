from banks import ChatMessage
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.user import User

class ChatSession(Base):
    __tablename__ = "chat_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id")
    )

    user: Mapped["User"] = relationship(back_populates="chat_sessions")

    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ChatSession(id={self.id!r}, title={self.title!r}, user_created={self.user_id!r}, messages_count={len(self.messages)!r})"

class ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_summary: Mapped[bool] = mapped_column(default=False)
    content: Mapped[str] = mapped_column(String(500))
    role: Mapped[str] = mapped_column(String(10))  # user / assistant

    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_session.id")
    )

    session: Mapped["ChatSession"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return (
            f"ChatMessage(id={self.id!r}, role={self.role!r}, "
            f"content={self.content!r})"
        )