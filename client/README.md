# ZebOS Expert Chatbot

Full-stack RAG chatbot với session management, retrieval, reranking, và LLM integration.

## 🚀 Tính năng

- ✅ **RAG Pipeline**: BM25 + FAISS hybrid search → BGE reranking
- ✅ **Session Management**: PostgreSQL/SQLite với auto-summary
- ✅ **Context Management**: Tự động tóm tắt khi vượt token limit
- ✅ **Multi-user Support**: Session tracking per user
- ✅ **Beautiful UI**: Responsive chat interface
- ✅ **LLM Integration**: Ollama với Qwen2.5

## 📦 Cài đặt

### 1. Install dependencies

```bash
cd client
pip install -r requirements.txt
```

### 2. Setup Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### 3. Build indexes (nếu chưa có)

```bash
cd ..
python3 -m bm25.main
```

## 🎯 Chạy ứng dụng

### Development mode

```bash
python3 app.py
```

Mở browser: http://localhost:5000

### Production mode

```bash
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:pass@localhost/dbname
export OLLAMA_MODEL=qwen2.5:7b
export CONTEXT_LIMIT=8000
export RETRIEVAL_TOP_K=25
export RERANK_TOP_K=5

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔧 Configuration

Environment variables:

- `DATABASE_URL`: Database connection (default: sqlite:///chat_sessions.db)
- `OLLAMA_MODEL`: LLM model name (default: qwen2.5:7b)
- `CONTEXT_LIMIT`: Max context window (default: 8000)
- `SAFETY_RATIO`: Trigger summary ratio (default: 0.8)
- `RETRIEVAL_TOP_K`: Initial retrieval count (default: 25)
- `RERANK_TOP_K`: Final reranked count (default: 5)
- `SECRET_KEY`: Flask session secret (required for production)
- `PORT`: Server port (default: 5000)

## 📚 API Endpoints

### POST /api/chat
Chat with the bot
```json
{
  "message": "How to configure BGP?",
  "use_rag": true
}
```

### GET /api/sessions
Get all user sessions

### POST /api/sessions/new
Create new chat session

### GET /api/sessions/<id>
Get session history

### GET /api/health
Health check

## 🗄️ Database Schema

### chat_sessions
- id (UUID)
- user_id (UUID)
- title (String)
- is_active (Boolean)
- created_at, updated_at

### chat_messages
- id (UUID)
- session_id (UUID)
- role (String: user/assistant/system)
- content (Text)
- token_count (Integer)
- created_at

### chat_summaries
- id (UUID)
- session_id (UUID)
- summary (Text)
- from_message_id, to_message_id (UUID)
- token_count (Integer)
- created_at

## 🧪 Testing

```bash
# Run the app
python3 app.py

# In another terminal, test API
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is BGP?"}'
```

## 📝 Project Structure

```
client/
├── app.py                 # Flask application
├── requirements.txt       # Dependencies
├── templates/
│   └── index.html        # Chat UI
└── static/               # Static assets (if needed)
```

## 🔍 How it works

1. **User sends message** → API endpoint receives
2. **RAG Pipeline**:
   - Hybrid search (BM25 + FAISS) retrieves top 25 docs
   - BGE reranker selects top 5 most relevant
   - Context built from documents
3. **Session Management**:
   - Message saved to database with token count
   - Context built from history + summary (if exists)
   - Check token limit → auto-summary if needed
4. **LLM Generation**:
   - Prompt with context sent to Ollama
   - Response generated and saved
5. **Return to user** with response + source documents

## 🚨 Troubleshooting

**Database connection error:**
- Check DATABASE_URL
- For SQLite: ensure write permissions
- For PostgreSQL: verify credentials and database exists

**Ollama not responding:**
```bash
ollama serve
ollama list  # Check models
```

**BGE reranker slow/OOM:**
- Use CPU mode (automatic fallback)
- Reduce RERANK_TOP_K
- Or skip reranking: modify retriever.py

**Context overflow:**
- Reduce CONTEXT_LIMIT
- Increase SAFETY_RATIO (triggers summary earlier)

## 📖 License

MIT License
