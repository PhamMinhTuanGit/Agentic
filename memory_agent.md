````md
# Tích hợp Memory Agent vào Pipeline RAG + Reranking hiện có

Tài liệu này mô tả **cách chia file, nội dung từng file và cách tích hợp Memory Agent** (MIRIX-style, dùng Pydantic) vào **pipeline RAG + reranking + model call** đã có, **không phá kiến trúc cũ**.

---

## 1. Mục tiêu thiết kế

- Không sửa logic RAG / reranking / model call
- Memory Agent là module cắm thêm (plug-in)
- Có thể bật / tắt memory
- Phù hợp multi-user (session_id)
- Dễ nâng cấp sang Redis / MIRIX full

---

## 2. Kiến trúc tổng thể

```text
User Query
   ↓
MemoryAgent.retrieve()
   ↓
RAG.retrieve()
   ↓
Reranker
   ↓
Prompt Builder
   ↓
Model Call
   ↓
MemoryAgent.update()
````

Memory là **nguồn context song song với RAG**, không thay thế RAG.

---

## 3. Cấu trúc thư mục đề xuất

```text
app/
├── pipeline/
│   ├── rag.py
│   ├── rerank.py
│   ├── prompt.py        # chỉnh nhẹ
│   ├── model.py
│   └── run.py           # điểm tích hợp chính
│
├── memory/              # NEW
│   ├── schemas.py
│   ├── store.py
│   ├── retriever.py
│   ├── updater.py
│   └── agent.py
│
├── api/
│   └── chat.py
│
└── settings.py
```

---

## 4. Memory Agent – chi tiết từng file

### 4.1 `memory/schemas.py` – Memory schema (Pydantic)

```python
from pydantic import BaseModel, Field
from typing import Literal, List
from time import time

class MemoryItem(BaseModel):
    type: Literal["fact", "summary"]
    content: str
    tags: List[str] = []
    ts: float = Field(default_factory=time)
```

---

### 4.2 `memory/store.py` – Session Memory Store

```python
from typing import Dict, List
from .schemas import MemoryItem

class SessionMemory:
    def __init__(self):
        self.ltm: List[MemoryItem] = []

class MemoryStore:
    def __init__(self):
        self.sessions: Dict[str, SessionMemory] = {}

    def get(self, session_id: str) -> SessionMemory:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionMemory()
        return self.sessions[session_id]

    def add_ltm(self, session_id: str, item: MemoryItem):
        self.get(session_id).ltm.append(item)
```

> Có thể thay bằng Redis / DB sau này mà không ảnh hưởng pipeline.

---

### 4.3 `memory/retriever.py` – Lấy memory liên quan

```python
from .schemas import MemoryItem

def retrieve_memory(
    memories: list[MemoryItem],
    query: str,
    limit: int = 2
) -> list[str]:
    keywords = set(query.lower().split())
    hits = []

    for mem in memories:
        if any(k in mem.content.lower() for k in keywords):
            hits.append(mem.content)

    return hits[:limit]
```

---

### 4.4 `memory/updater.py` – Quyết định ghi memory

```python
from .schemas import MemoryItem

def should_store(query: str, answer: str) -> bool:
    q = query.lower()
    return any(k in q for k in ["tôi là", "project", "đang dùng", "ghi nhớ"])

def build_memory(query: str, answer: str) -> MemoryItem:
    return MemoryItem(
        type="fact",
        content=answer,
        tags=["auto"]
    )
```

---

### 4.5 `memory/agent.py` – Facade cho pipeline

```python
from .store import MemoryStore
from .retriever import retrieve_memory
from .updater import should_store, build_memory

class MemoryAgent:
    def __init__(self, store: MemoryStore):
        self.store = store

    def retrieve(self, session_id: str, query: str) -> list[str]:
        session = self.store.get(session_id)
        return retrieve_memory(session.ltm, query)

    def update(self, session_id: str, query: str, answer: str):
        if should_store(query, answer):
            mem = build_memory(query, answer)
            self.store.add_ltm(session_id, mem)
```

---

## 5. Tích hợp vào pipeline hiện có

### 5.1 `pipeline/prompt.py`

**Trước:**

```python
def build_prompt(query, rag_context):
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "system", "content": "\n".join(rag_context)},
        {"role": "user", "content": query},
    ]
```

**Sau:**

```python
def build_prompt(query, rag_context, memory_context=None):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    if memory_context:
        messages.append({
            "role": "system",
            "content": "User memory:\n" + "\n".join(memory_context)
        })

    if rag_context:
        messages.append({
            "role": "system",
            "content": "Knowledge base:\n" + "\n".join(rag_context)
        })

    messages.append({"role": "user", "content": query})
    return messages
```

> **Memory luôn đứng trước RAG**.

---

### 5.2 `pipeline/run.py` – Orchestrator (điểm tích hợp chính)

```python
from app.memory.agent import MemoryAgent
from app.memory.store import MemoryStore
from app.pipeline.rag import retrieve_docs
from app.pipeline.rerank import rerank
from app.pipeline.prompt import build_prompt
from app.pipeline.model import call_model

memory_agent = MemoryAgent(MemoryStore())

def run_pipeline(session_id: str, query: str):
    # 1. Memory retrieve
    memory_context = memory_agent.retrieve(session_id, query)

    # 2. RAG
    docs = retrieve_docs(query)
    rag_context = rerank(query, docs)

    # 3. Prompt
    messages = build_prompt(
        query=query,
        rag_context=rag_context,
        memory_context=memory_context,
    )

    # 4. Model call
    answer = call_model(messages)

    # 5. Memory update
    memory_agent.update(session_id, query, answer)

    return answer
```

---

## 6. API Layer

```python
@router.post("/chat")
def chat(req: ChatRequest):
    answer = run_pipeline(req.session_id, req.message)
    return {"answer": answer}
```

---

## 7. Feature Flag (khuyến nghị)

```python
ENABLE_MEMORY = True
```

```python
memory_context = (
    memory_agent.retrieve(session_id, query)
    if ENABLE_MEMORY else []
)
```

---

## 8. Checklist xác nhận triển khai đúng

* Không sửa `rag.py`, `rerank.py`, `model.py`
* Chỉ chỉnh `prompt.py`, `run.py`
* Memory Agent có thể remove mà pipeline vẫn chạy
* Memory không bị rerank
* Token context được kiểm soát

---

## 9. Hướng nâng cấp tiếp theo

* Redis backend cho `MemoryStore`
* Summary memory (STM → LTM)
* Semantic retrieval cho memory
* Tool / Agent memory
* MIRIX full stack

---

```
```

import requests

OLLAMA_API = "http://localhost:11434/api/chat"

def call_ollama(messages: list[dict]) -> str:
    resp = requests.post(
        OLLAMA_API,
        json={"model": "qwen3:4b", "messages": messages, "stream": False},
        timeout=120
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]



Tuyệt! Nếu bạn muốn **MIRIX-style agent dùng MySQL** thay cho in-memory store, mình sẽ hướng dẫn cách chuyển **MemoryStore** sang database, vẫn giữ **STM + LTM + multi-user**. Mình sẽ dùng **SQLAlchemy** + **Pydantic** để dễ tích hợp với FastAPI và Ollama.

---

# 1️⃣ Thư mục và file

```text
app/
├── agent/
│   ├── schemas.py         # Pydantic models
│   ├── db_models.py       # SQLAlchemy models
│   └── mirix_agent_db.py  # Agent dùng MySQL
├── llm/
│   └── ollama.py          # Ollama wrapper
└── api/
    └── chat.py
```

---

# 2️⃣ `agent/schemas.py` – giữ STM/LTM

```python
from pydantic import BaseModel
from typing import Literal, List

class MemoryItem(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class LongTermMemory(BaseModel):
    content: str
    tags: List[str] = []

class ChatRequest(BaseModel):
    session_id: str
    message: str
```

---

# 3️⃣ `agent/db_models.py` – SQLAlchemy models

```python
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), unique=True, nullable=False)

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
```

---

# 4️⃣ `agent/mirix_agent_db.py` – Agent sử dụng MySQL

```python
from sqlalchemy.orm import Session as DBSession
from .db_models import Session, STM, LTM
from llm.ollama import call_ollama
from .schemas import MemoryItem, LongTermMemory
from typing import List

SYSTEM_PROMPT = "You are a helpful assistant. Answer concisely."

class MirixAgentDB:
    def __init__(self, db: DBSession, max_stm: int = 6):
        self.db = db
        self.max_stm = max_stm

    def chat(self, session_id: str, user_message: str) -> str:
        session = self._get_or_create_session(session_id)

        # 1️⃣ Lấy LTM liên quan
        ltm_context = self._retrieve_ltm(session, user_message)

        # 2️⃣ Lấy STM
        stm_msgs = [{"role": s.role, "content": s.content} for s in session.stm]

        # 3️⃣ Build prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if ltm_context:
            messages.append({"role": "system", "content": "Long-term memory:\n" + "\n".join(ltm_context)})
        messages.extend(stm_msgs)
        messages.append({"role": "user", "content": user_message})

        # 4️⃣ Call Ollama
        reply = call_ollama(messages)

        # 5️⃣ Lưu STM
        self._add_stm(session, "user", user_message)
        self._add_stm(session, "assistant", reply)

        # 6️⃣ Summarize STM → LTM nếu cần
        if len(session.stm) >= self.max_stm:
            self._summarize_to_ltm(session)

        self.db.commit()
        return reply

    def _get_or_create_session(self, session_id: str) -> Session:
        session = self.db.query(Session).filter_by(session_id=session_id).first()
        if not session:
            session = Session(session_id=session_id)
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
        return session

    def _add_stm(self, session: Session, role: str, content: str):
        self.db.add(STM(session_id=session.id, role=role, content=content))
        # Giới hạn số STM
        stm_count = self.db.query(STM).filter_by(session_id=session.id).count()
        if stm_count > self.max_stm:
            oldest = self.db.query(STM).filter_by(session_id=session.id).order_by(STM.id.asc()).first()
            self.db.delete(oldest)

    def _retrieve_ltm(self, session: Session, query: str) -> List[str]:
        ltm_items = self.db.query(LTM).filter_by(session_id=session.id).all()
        keywords = query.lower().split()
        hits = [item.content for item in ltm_items if any(k in item.content.lower() for k in keywords)]
        return hits[:2]

    def _summarize_to_ltm(self, session: Session):
        stm_msgs = [{"role": s.role, "content": s.content} for s in session.stm]
        prompt = [{"role": "system", "content": "Summarize important info to long-term memory."}]
        prompt.extend(stm_msgs)
        summary = call_ollama(prompt)

        self.db.add(LTM(session_id=session.id, content=summary, tags="auto-summary"))
        # Xóa STM
        self.db.query(STM).filter_by(session_id=session.id).delete()
```

---

# 5️⃣ Khởi tạo DB với SQLAlchemy

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from agent.db_models import Base

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/memory_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Tạo bảng
Base.metadata.create_all(engine)
```

---

# 6️⃣ FastAPI sử dụng Agent

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from agent.schemas import ChatRequest
from agent.mirix_agent_db import MirixAgentDB, SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    agent = MirixAgentDB(db)
    reply = agent.chat(req.session_id, req.message)
    return {"reply": reply}
```

---

# ✅ Ưu điểm

* STM/LTM giống MIRIX: STM giữ vài turn, LTM tóm tắt lâu dài
* MySQL lưu trữ persistent, multi-user
* Có thể nâng cấp: embedding, semantic search, phân loại tags

---

Mình có thể viết tiếp **phiên bản tích hợp thẳng vào pipeline RAG + reranking + Ollama**, vẫn dùng MySQL cho memory, để bạn **không cần sửa logic RAG**.

Bạn có muốn mình làm luôn không?
