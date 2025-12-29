from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Tạo bảng



Base = declarative_base()


def init_db():
    """Initialize database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), unique=True, nullable=False)
    cache_docs = Column(Text, nullable=True)
    ext_dir = Column(String(256), nullable=True)
    stm = relationship("STM", back_populates="session", cascade="all, delete-orphan")
    ltm = relationship("LTM", back_populates="session", cascade="all, delete-orphan")

class STM(Base):
    __tablename__ = "stm"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    role = Column(String(16))
    content = Column(Text)
    ts = Column(Float, default=datetime.utcnow().timestamp)

    session = relationship("Session", back_populates="stm")

class LTM(Base):
    __tablename__ = "ltm"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    content = Column(Text)
    tags = Column(String(256))
    ts = Column(Float, default=datetime.utcnow().timestamp)

    session = relationship("Session", back_populates="ltm")



init_db()