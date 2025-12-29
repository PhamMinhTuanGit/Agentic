from sqlalchemy.orm import Session as DBSession
from agent.retriever import retriever_with_rerank
from app.agent.db_models import Session, STM, LTM
from app.llm.ollama import call_ollama
from agent.prompt_template import *
from app.agent.schemas import MemoryItem, LongTermMemory
from typing import List, Generator
from agent.prompt_template import *
import requests
import json

SYSTEM_PROMPT = "You are a helpful assistant. Answer concisely."
OLLAMA_API = "http://localhost:11434/api/chat"

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

    def chat_stream(self, session_id: str, user_message: str) -> Generator[str, None, None]:
        """Stream tokens from the agent's response"""
        session = self._get_or_create_session(session_id)

        # 1️⃣ Build prompt using _build_prompt method
        prompt = self._build_prompt(user_message, session)
        messages = [{"role": "user", "content": prompt}]

        # 2️⃣ Stream from Ollama and collect full response
        full_reply = ""
        full_thinking = ""
        try:
            with requests.post(
                OLLAMA_API,
                json={"model": "qwen3:4b", "messages": messages, "stream": True},
                stream=True,
                timeout=120
            ) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode("utf-8"))
                            if "message" in data:
                                msg = data["message"]
                                # Capture thinking
                                if "thinking" in msg and msg["thinking"]:
                                    thinking = msg["thinking"]
                                    full_thinking += thinking
                                    yield thinking
                                # Capture content
                                if "content" in msg and msg["content"]:
                                    content = msg["content"]
                                    full_reply += content
                                    yield content
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            yield f"[ERROR] {error_msg}"
            full_reply = error_msg
            return

        # 3️⃣ Lưu STM (after streaming completes)
        self._add_stm(session, "user", user_message)
        self._add_stm(session, "assistant", full_reply)

        # 4️⃣ Summarize STM → LTM nếu cần
        if len(session.stm) >= self.max_stm:
            self._summarize_to_ltm(session)

        self.db.commit()

    def chat_stream_nothink(self, session_id: str, user_message: str) -> Generator[str, None, None]:
        """Stream tokens from the agent's response without thinking markers"""
        session = self._get_or_create_session(session_id)

        prompt = self._build_prompt(user_message, session)
        messages = [{"role": "user", "content": prompt}]

        # 4️⃣ Stream from Ollama and collect full response
        full_reply = ""
        try:
            with requests.post(
                OLLAMA_API,
                json={"model": "qwen3:4b", "messages": messages, "stream": True},
                stream=True,
                timeout=120
            ) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode("utf-8"))
                            if "message" in data:
                                msg = data["message"]
                                # Only yield content, skip thinking
                                if "content" in msg and msg["content"]:
                                    content = msg["content"]
                                    full_reply += content
                                    yield content
                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            yield error_msg
            full_reply = error_msg
            return

        # 5️⃣ Lưu STM (after streaming completes)
        self._add_stm(session, "user", user_message)
        self._add_stm(session, "assistant", full_reply)

        # 6️⃣ Summarize STM → LTM nếu cần
        if len(session.stm) >= self.max_stm:
            self._summarize_to_ltm(session)

        self.db.commit()


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
        prompt = [{"role": "system", "content": "Summarize important info to long-term memory. MAXIMUM 50 WORDS."}]
        prompt.extend(stm_msgs)
        summary = call_ollama(prompt)

        self.db.add(LTM(session_id=session.id, content=summary, tags="auto-summary"))
        # Xóa STM
        self.db.query(STM).filter_by(session_id=session.id).delete()
    def _build_prompt(self, query: str, session: Session) -> str:
        # Build context
        retrieved_context = retriever_with_rerank(query, top_k=25, rerank_top_k=10)
        
        # Create prompt template instance and build prompt
        prompt_template = PromptTemplate()
        prompt_no_history = prompt_template.create_search_augmented_prompt(
            query, retrieved_context, max_results=10
        )
        
        ltm = self._retrieve_ltm(session, query)
        stm = [{"role": s.role, "content": s.content} for s in session.stm]
        prompt = prompt_no_history.replace("{history_stm_context}", str(stm))
        prompt = prompt.replace("{history_ltm_context}", str(ltm))
        return prompt

    def _add_cache_docs(self, session: Session, cache_docs: str):
        self.db.add(Session(session_id=session.id, cache_docs=cache_docs))
        # Giới hạn số STM
    
    def _topic_detect(self, text: str) -> List[str]:
        prompt = [
            {"role": "system", "content": "Extract key topics from the following text. Return as a comma-separated list."},
            {"role": "user", "content": text}
        ]
        response = call_ollama(prompt)
        topics = [t.strip() for t in response.split(",")]
        return topics

