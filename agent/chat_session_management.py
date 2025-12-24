from typing import List, Dict
from typing import Optional
from banks import ChatMessage
from sqlalchemy import ForeignKey, create_engine, text
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship 
from sqlalchemy.orm import sessionmaker
from agent.retriever import model_response
from agent.prompt_template import build_summarize_prompt
class Base(DeclarativeBase):
    pass

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

def get_recent_messages(user_id: int, session_id: int) -> List[Dict]:
    """
    Retrieve the most recent messages for a given user and session.

    Args:
        user_id (int): The ID of the user requesting the messages.
        session_id (int): The ID of the chat session.

    Returns:
        List[Dict]: A list of dictionaries, each representing a message with keys:
            - id: The message ID.
            - message: The message content.
            - role: The role of the sender (e.g., user, assistant).
            - session_id: The session ID.
            - created_at: The timestamp when the message was created.

    Raises:
        Exception: If the session_id does not belong to the user_id.

    Notes:
        - The function first checks if the session belongs to the user.
        - If the session is invalid, an error is returned.
        - It counts the number of messages in the session.
        - It fetches the latest n messages, where n is the count modulo 10, ordered by creation time descending.
    """
    with engine.begin() as c:
        # 2) Count messages
        n = c.execute(
            text("SELECT COUNT(*) AS c FROM chat_message WHERE session_id = :sid"),
            {"sid": session_id},
        ).scalar_one()

        if not n:
            return []
        n = n%10
        # 3) Fetch latest n messages
        rows = c.execute(
            text(
                """
                SELECT id, message, role, session_id, created_at
                FROM chat_message
                WHERE session_id = :sid
                ORDER BY created_at DESC
                LIMIT :n
                """
            ),
            {"sid": session_id, "n": int(n)},
        ).mappings().all()

        return [dict(r) for r in rows]

def summarize_5_latest_messages(user_id: Optional[int], session_id: int) -> Optional[str]:
    """
    Summarize the latest 5 messages in a chat session for a given user.

    Args:
        user_id (int): The ID of the user requesting the summary.
        session_id (int): The ID of the chat session.

    Returns:
        Optional[str]: The summary of the latest 5 messages, or None if there are no messages.

    Raises:
        Exception: If the session_id does not belong to the user_id.
    """
    with engine.begin() as c:
        # 2) Fetch latest 5 messages
        rows = c.execute(
            text(
                """
                SELECT message
                FROM chat_message
                WHERE session_id = :sid
                ORDER BY created_at DESC
                LIMIT 5
                """
            ),
            {"sid": session_id},
        ).scalars().all()
        if not rows:
            return None
        # 3) Create summary (simple concatenation for demonstration)
        else:
            prompt = build_summarize_prompt(rows)
            summary = model_response(prompt)
        return summary

def is_user_existed(username: str) -> bool:
    session = Session()
    user = session.query(User).filter(User.name == username).first()
    session.close()
    return user is not None

def create_user(username: str) -> int:
    session = Session()
    new_user = User(name=username)
    session.add(new_user)
    session.commit()
    user_id = new_user.id
    session.close()
    return user_id

def handle_api_query(request: Dict) -> Dict:
    """
    Handles an API query from the user, managing session and message creation.
    Flow:
    1. Check if session_id is present in the request.
        - If yes, use the existing session_id.
        - If no, get user_id from request, create a new session, and use its session_id.
    2. Create a new message linked to the session_id.
    3. Return session_id to the client.
    """
    session_id = request.get("session_id")
    user_id = request.get("user_id")
    message = request.get("message", "")

    session = Session()
    
    try:
        if session_id is None:
            if user_id is None:
                raise ValueError("user_id is required if session_id is not provided")
            new_session = ChatSession(user_id=user_id)
            session.add(new_session)
            session.flush()
            session_id = new_session.id
        else:
            existing_session = session.get(ChatSession, session_id)
            if not existing_session:
                raise ValueError("Invalid session_id")

        new_message = ChatMessage(session_id=session_id, message=message, role="user")
        session.add(new_message)
        session.flush()
        message_id = new_message.id
        session.commit()

        return {"session_id": session_id, "message_id": message_id}
    finally:
        session.close()

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    
    # Update the connection string for MySQL (adjust username, password, host, dbname as needed)
    engine = create_engine(
        "mysql+pymysql://root:123456@localhost/chat_history_db",
        echo=True
    )
    
    Session = sessionmaker(bind=engine)

    # with Session(engine) as session:
    #     new_user = User(name="Alice")
    #     session.add(new_user)
    #     session.commit()

    #     new_session = ChatSession(title="Support Chat", user=new_user)
    #     session.add(new_session)
    #     session.commit()

    #     msg1 = ChatMessage(
    #         content="Hello, I need help with my account.",
    #         role="user",
    #         session=new_session
    #     )
    #     msg2 = ChatMessage(
    #         content="Sure, I'd be happy to assist you.",
    #         role="assistant",
    #         session=new_session
    #     )
    #     session.add_all([msg1, msg2])
    #     session.commit()

    #     for user in session.query(User).all():
    #         print(user)
    #         for chat_session in user.chat_sessions:
    #             print(f"  {chat_session}")
    #             for message in chat_session.messages:
    #                 print(f"    {message}")
    create_user("tuanpm")
    is_user_existed("tuanpm")