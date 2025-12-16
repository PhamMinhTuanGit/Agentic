"""
ZebOS Expert Chatbot Web Application
Full-stack chatbot with RAG, reranking, and session management
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import uuid
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Import components
from agent.chat_session_management import (
    ChatSessionManager,
    DatabaseManager,
    TokenCounter
)
from agent.retriever import retriever_with_rerank, model_response
from agent.prompt_template import PromptTemplate
from agent.reranker import Reranker
import ollama

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Flask App Configuration
# ============================================================================

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# ============================================================================
# LLM Client Wrapper
# ============================================================================

class OllamaLLMClient:
    """
    Wrapper for Ollama client compatible with ChatSessionManager.
    """
    
    def __init__(self, model_name: str = "qwen3:4b"):
        self.client = ollama.Client()
        self.model_name = model_name
        logger.info(f"Initialized Ollama client with model: {model_name}")
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Chat completion compatible with session manager.
        
        Args:
            messages: List of message dicts with role and content
        
        Returns:
            Assistant response text
        """
        try:
            # Convert to Ollama format and call
            response = self.client.chat(
                model=self.model_name,
                messages=messages
            )
            
            return response['message']['content']
        
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return f"Error: Failed to generate response. {str(e)}"


# ============================================================================
# RAG Pipeline
# ============================================================================

class RAGPipeline:
    """
    Full RAG pipeline: retrieval → reranking → context building.
    """
    
    def __init__(
        self,
        reranker: Optional[Reranker] = None,
        top_k: int = 25,
        rerank_top_k: int = 5
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            reranker: Reranker instance (optional, loads if None)
            top_k: Initial retrieval count
            rerank_top_k: Final reranked count
        """
        self.top_k = top_k
        self.rerank_top_k = rerank_top_k
        self.reranker = reranker
        
        logger.info(f"RAG pipeline initialized: top_k={top_k}, rerank_top_k={rerank_top_k}")
    
    def retrieve_and_rerank(self, query: str) -> List[Dict]:
        """
        Execute full RAG pipeline.
        
        Args:
            query: User query
        
        Returns:
            List of reranked documents
        """
        try:
            # Use the retriever_with_rerank function
            results = retriever_with_rerank(
                query,
                top_k=self.top_k,
                rerank_top_k=self.rerank_top_k
            )
            
            logger.info(f"RAG pipeline completed: {len(results)} documents")
            return results
        
        except Exception as e:
            logger.error(f"RAG pipeline error: {e}")
            return []
    
    def build_context(self, documents: List[Dict]) -> str:
        """
        Build context string from documents.
        
        Args:
            documents: List of document dicts
        
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant documentation found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            doc_name = doc.get('doc_name', 'Unknown')
            text = doc.get('text', '')
            rerank_score = doc.get('rerank_score', 0)
            
            context_parts.append(
                f"[Document {i}] {doc_name} (Relevance: {rerank_score})\n{text}"
            )
        
        return "\n\n---\n\n".join(context_parts)


# ============================================================================
# Application State
# ============================================================================

# Database setup (SQLite for development)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///chat_sessions.db')
db_manager = DatabaseManager(DATABASE_URL)
db_manager.create_tables()

# LLM client
llm_client = OllamaLLMClient(
    model_name=os.environ.get('OLLAMA_MODEL', 'qwen2.5:7b')
)

# Chat session manager
chat_manager = ChatSessionManager(
    db_manager=db_manager,
    llm_client=llm_client,
    context_limit=int(os.environ.get('CONTEXT_LIMIT', 8000)),
    safety_ratio=float(os.environ.get('SAFETY_RATIO', 0.8)),
    system_prompt=os.environ.get('SYSTEM_PROMPT', PromptTemplate().system_prompt)
)

# RAG pipeline
rag_pipeline = RAGPipeline(
    top_k=int(os.environ.get('RETRIEVAL_TOP_K', 25)),
    rerank_top_k=int(os.environ.get('RERANK_TOP_K', 5))
)

logger.info("Application initialized successfully")


# ============================================================================
# Helper Functions
# ============================================================================

def get_or_create_user_id() -> uuid.UUID:
    """
    Get user ID from session or create new one.
    
    Returns:
        User UUID
    """
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    return uuid.UUID(session['user_id'])


def get_current_session_id() -> Optional[uuid.UUID]:
    """
    Get current chat session ID from Flask session.
    
    Returns:
        Session UUID or None
    """
    if 'chat_session_id' in session:
        return uuid.UUID(session['chat_session_id'])
    return None


def create_new_chat_session(user_id: uuid.UUID, title: str = None) -> uuid.UUID:
    """
    Create new chat session and store in Flask session.
    
    Args:
        user_id: User UUID
        title: Optional session title
    
    Returns:
        New session UUID
    """
    session_id = chat_manager.create_session(user_id, title)
    session['chat_session_id'] = str(session_id)
    logger.info(f"Created new chat session: {session_id}")
    return session_id


# ============================================================================
# Routes
# ============================================================================

@app.route('/')
def index():
    """Home page with chat interface."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint with RAG.
    
    Request JSON:
        {
            "message": "user message",
            "use_rag": true/false (optional, default true)
        }
    
    Response JSON:
        {
            "response": "assistant response",
            "session_id": "uuid",
            "documents_used": [...] (if RAG enabled)
        }
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        use_rag = data.get('use_rag', True)
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create user
        user_id = get_or_create_user_id()
        
        # Get or create session
        session_id = get_current_session_id()
        if not session_id:
            session_id = create_new_chat_session(user_id)
        
        # RAG pipeline (if enabled)
        documents = []
        if use_rag:
            logger.info(f"Running RAG for query: {user_message[:50]}...")
            documents = rag_pipeline.retrieve_and_rerank(user_message)
            
            # Build context from documents
            if documents:
                context = rag_pipeline.build_context(documents)
                
                # Inject context into the session's system prompt temporarily
                # This is done by using the prompt template directly
                template = PromptTemplate()
                
                # We'll manually handle this turn with context
                # Get the conversation context first
                with db_manager.get_session() as db:
                    from agent.chat_session_management import ChatMessage
                    from sqlalchemy import asc
                    
                    # Get recent messages
                    recent_messages = (
                        db.query(ChatMessage)
                        .filter(ChatMessage.session_id == session_id)
                        .order_by(asc(ChatMessage.created_at))
                        .limit(10)
                        .all()
                    )
                    
                    # Build messages array
                    messages = []
                    
                    # Add system prompt with context
                    prompt_with_context = template.format(
                        retrieved_context=context,
                        user_question=user_message
                    )
                    
                    # For this turn, we'll use direct LLM call with context
                    # Then save to session manager
                    logger.info("Generating response with RAG context...")
                    response_text = llm_client.client.generate(
                        model=llm_client.model_name,
                        prompt=prompt_with_context
                    )['response']
                    
                    # Save both messages to session
                    chat_manager._save_message(db, session_id, "user", user_message)
                    chat_manager._save_message(db, session_id, "assistant", response_text)
                    
                    return jsonify({
                        'response': response_text,
                        'session_id': str(session_id),
                        'documents_used': [
                            {
                                'doc_name': doc.get('doc_name'),
                                'rerank_score': doc.get('rerank_score'),
                                'preview': doc.get('text', '')[:200]
                            }
                            for doc in documents[:3]
                        ]
                    })
        
        # Normal chat without RAG (or RAG returned no documents)
        logger.info("Generating response without RAG context...")
        response_text = chat_manager.chat(session_id, user_message)
        
        return jsonify({
            'response': response_text,
            'session_id': str(session_id),
            'documents_used': [] if not use_rag else documents[:3]
        })
    
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """
    Get all chat sessions for current user.
    
    Response JSON:
        {
            "sessions": [
                {
                    "id": "uuid",
                    "title": "Chat title",
                    "created_at": "ISO datetime",
                    "updated_at": "ISO datetime"
                }
            ]
        }
    """
    try:
        user_id = get_or_create_user_id()
        sessions = chat_manager.get_user_sessions(user_id, active_only=True)
        
        return jsonify({
            'sessions': [
                {
                    'id': str(s.id),
                    'title': s.title,
                    'created_at': s.created_at.isoformat(),
                    'updated_at': s.updated_at.isoformat()
                }
                for s in sessions
            ]
        })
    
    except Exception as e:
        logger.error(f"Get sessions error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sessions/new', methods=['POST'])
def new_session():
    """
    Create a new chat session.
    
    Request JSON:
        {
            "title": "Optional title"
        }
    
    Response JSON:
        {
            "session_id": "uuid"
        }
    """
    try:
        user_id = get_or_create_user_id()
        data = request.get_json() or {}
        title = data.get('title')
        
        session_id = create_new_chat_session(user_id, title)
        
        return jsonify({'session_id': str(session_id)})
    
    except Exception as e:
        logger.error(f"New session error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session_history(session_id):
    """
    Get message history for a session.
    
    Response JSON:
        {
            "messages": [
                {
                    "role": "user/assistant",
                    "content": "message text",
                    "created_at": "ISO datetime"
                }
            ]
        }
    """
    try:
        history = chat_manager.get_session_history(uuid.UUID(session_id))
        
        return jsonify({
            'messages': history
        })
    
    except Exception as e:
        logger.error(f"Get history error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sessions/<session_id>/switch', methods=['POST'])
def switch_session(session_id):
    """
    Switch to a different session.
    
    Response JSON:
        {
            "session_id": "uuid"
        }
    """
    try:
        session['chat_session_id'] = session_id
        return jsonify({'session_id': session_id})
    
    except Exception as e:
        logger.error(f"Switch session error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'database': DATABASE_URL.split('://')[0],
        'model': llm_client.model_name
    })


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask server on port {port}...")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
