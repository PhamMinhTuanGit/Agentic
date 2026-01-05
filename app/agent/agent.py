from sqlalchemy.orm import Session as DBSession
from app.agent.db_models import Session, STM, LTM
from app.llm.ollama import call_ollama, stream_ollama_with_collection
from agent.retriever import retriever_with_rerank
from agent.prompt_template import *
from app.agent.schemas import MemoryItem, LongTermMemory
from typing import List, Generator
import json

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

    def chat_stream(self, session_id: str, user_message: str) -> Generator[str, None, None]:
        """Stream tokens from the agent's response"""
        session = self._get_or_create_session(session_id)

        # 1️⃣ Lấy LTM liên quan
        prompt = self._build_prompt(user_message, session)
        messages = [{"role": "user", "content": prompt}]

        # 2️⃣ Stream from Ollama using centralized function
        stream_generator, get_full_response = stream_ollama_with_collection(
            messages=messages,
            include_thinking=True
        )
        
        # Yield all tokens from stream
        try:
            for token in stream_generator:
                yield token
        finally:
            # This runs after generator is consumed or closed
            # 3️⃣ Get full response after streaming
            full_reply = get_full_response()

            # 4️⃣ Lưu STM (after streaming completes)
            self._add_stm(session, "user", user_message)
            self._add_stm(session, "assistant", full_reply)

            # 5️⃣ Summarize STM → LTM nếu cần
            if len(session.stm) >= self.max_stm:
                self._summarize_to_ltm(session)

            self.db.commit()

    def chat_stream_nothink(self, session_id: str, user_message: str) -> Generator[str, None, None]:
        """Stream tokens from the agent's response without thinking markers"""
        session = self._get_or_create_session(session_id)

        prompt = self._build_prompt(user_message, session)
        messages = [{"role": "user", "content": prompt}]

        # Stream from Ollama without thinking tokens
        stream_generator, get_full_response = stream_ollama_with_collection(
            messages=messages,
            include_thinking=False  # Skip thinking tokens
        )
        
        # Yield all content tokens
        try:
            for token in stream_generator:
                yield token
        finally:
            # Get full response after streaming
            full_reply = get_full_response()

            # Lưu STM (after streaming completes)
            self._add_stm(session, "user", user_message)
            self._add_stm(session, "assistant", full_reply)

            # Summarize STM → LTM nếu cần
            if len(session.stm) >= self.max_stm:
                self._summarize_to_ltm(session)

            self.db.commit()

        # Summarize STM → LTM nếu cần
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


    def full_configuration(self, answer) -> str:
        """Return full configuration as JSON string for debugging"""
        prompt = EXTRACT_CONFIG_PROMPT
        prompt = prompt.replace("{full_configuration}", answer)
        config =  call_ollama(prompt=prompt, model = "qwen2.5-coder:1.5b-base")
        return config
    
        
class AgentOrchestration:
    def __init__(self, db: DBSession):
        self.db = db
        self.agent_db = MirixAgentDB(db)

    def _intent_parsed(self, user_message: str) -> str:
        prompt = INTENT_PARSING_PROMPT.replace("{user_query}", user_message)
        print("Optimizing tool selection")
        intent = call_ollama([{"role": "user", "content": prompt}])
        print("Tool selection result:", intent["intent"])
        return intent["intent"]


if __name__ == "__main__":
    query = "Configure OSPF on router with ID 10"
    # print("Testing AgentOrchestration intent parsing...")
    # agent = AgentOrchestration(None)  # Assuming None for DBSession for testing
    # intent = agent._intent_parsed(query)
    # print(intent)
    
    agent = MirixAgentDB(db=)  # Assuming None for DBSession for testing
    print(agent._build_prompt(query, Session(id=1, session_id="test")))