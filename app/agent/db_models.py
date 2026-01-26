from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from app.db.session import engine, SessionLocal
from app.core.config import settings

def utc_now_no_microseconds():
    """Return current UTC datetime without microseconds"""
    return datetime.utcnow().replace(microsecond=0)

Base = declarative_base()


def init_db():
    """Initialize database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), unique=True, nullable=False)

    stm = relationship("STM", back_populates="session", cascade="all, delete-orphan")
    ltm = relationship("LTM", back_populates="session", cascade="all, delete-orphan")

class STM(Base):
    __tablename__ = "stm"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    role = Column(String(16), nullable=False)
    content = Column(Text, nullable=False)
    ts = Column(DateTime, default=utc_now_no_microseconds, nullable=False)

    session = relationship("Session", back_populates="stm")

class LTM(Base):
    __tablename__ = "ltm"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(256))
    ts = Column(DateTime, default=utc_now_no_microseconds, nullable=False)

    session = relationship("Session", back_populates="ltm")


def init_db():
    """Initialize database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables initialized successfully")


if __name__ == "__main__":
    init_db()





