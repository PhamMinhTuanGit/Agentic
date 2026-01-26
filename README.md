# ZebOS Expert System - RAG Chatbot

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

## 📋 Tổng Quan (Overview)

**ZebOS Expert System** là một hệ thống AI chatbot chuyên biệt cho cấu hình và vận hành mạng ZebOS. Hệ thống sử dụng kiến trúc RAG (Retrieval-Augmented Generation) kết hợp với:

- **LLM**: Ollama (Qwen3:4b model)
- **Hybrid Search**: FAISS + BM25
- **Reranking**: Cross-encoder cho độ chính xác cao
- **Memory Management**: Hệ thống quản lý phiên chat với STM/LTM
- **Docker**: Deployment đơn giản với Docker Compose

### 🎯 Tính Năng Chính

✅ **Chỉ hỗ trợ ZebOS** - Không cung cấp lệnh cho Cisco IOS, Juniper, hay các platform khác  
✅ **CLI Commands** - Sinh CLI commands thực thi được, không có placeholder  
✅ **Context-Aware** - Dùng tài liệu ZebOS để trả lời chính xác  
✅ **Session Management** - Quản lý nhiều phiên chat với lịch sử  
✅ **Hybrid Search** - Kết hợp semantic search (FAISS) và keyword search (BM25)  
✅ **Intelligent Reranking** - Sắp xếp lại kết quả theo độ liên quan  

---

## 🏗️ Kiến Trúc Hệ Thống (System Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                            │
│  ┌──────────────┐        ┌──────────────┐                   │
│  │ Flask Client │  OR    │  API Client  │                   │
│  │  (Web UI)    │        │   (REST)     │                   │
│  └──────────────┘        └──────────────┘                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Router (v1)                         │   │
│  │  - /chat/users, /chat/sessions, /chat/query         │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Agent      │  │   Database   │  │  LLM Service │
│   Module     │  │   (MySQL)    │  │   (Ollama)   │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ • Retriever  │  │ • Users      │  │ • Qwen3:4b   │
│ • Reranker   │  │ • Sessions   │  │ • nomic-embed│
│ • Planning   │  │ • Messages   │  └──────────────┘
│ • Prompts    │  └──────────────┘
└──────────────┘
        │
        ▼
┌──────────────────────────────────┐
│    Hybrid Search System          │
│  ┌──────────────┐ ┌────────────┐ │
│  │    FAISS     │ │   BM25     │ │
│  │  (Semantic)  │ │ (Keyword)  │ │
│  └──────────────┘ └────────────┘ │
└──────────────────────────────────┘
```

---

## 📂 Cấu Trúc Thư Mục (Directory Structure)

```
Agentic/
├── agent/                          # Core Agent Logic
│   ├── chat_session_management.py  # Database models & session CRUD
│   ├── client.py                   # Agent client interface
│   ├── core.py                     # Agent decision-making engine
│   ├── planning.py                 # Task planning module
│   ├── prompt_template.py          # Prompt templates (SYSTEM_PROMPT)
│   ├── reranker.py                 # Cross-encoder reranking
│   └── retriever.py                # Hybrid search retriever
│
├── app/                            # FastAPI Application
│   ├── main.py                     # FastAPI app entry point
│   ├── api/v1/                     # API version 1
│   │   ├── router.py               # Main router
│   │   └── endpoints/              # Endpoint handlers
│   ├── core/                       # Core configs
│   │   └── config.py               # Settings & configurations
│   ├── db/                         # Database setup
│   │   ├── base.py                 # Base DB models
│   │   └── session.py              # Session management
│   ├── llm/                        # LLM integrations
│   │   └── ollama.py               # Ollama client wrapper
│   └── schemas/                    # Pydantic schemas
│       ├── chat.py                 # Chat request/response schemas
│       └── tool.py                 # Tool schemas
│
├── bm25/                           # BM25 Search Module
│   ├── bm25.py                     # BM25 implementation
│   ├── embedding.py                # Text embedding & chunking
│   ├── main.py                     # Index creation
│   ├── parse.py                    # HTML parsing
│   └── search.py                   # Hybrid search logic
│
├── client/                         # Flask Web Client
│   ├── app.py                      # Flask application
│   └── requirements.txt            # Client dependencies
│
├── telnet/                         # Telnet Module (Network Device Access)
│   ├── connect.py                  # Telnet connection handler
│   └── parse_and_telnet.py         # Parse commands & execute
│
├── docs/                           # Documentation
│   ├── API_DOCUMENTATION.md        # API endpoints documentation
│   ├── bm25_doc_en.md              # BM25 module documentation
│   └── memory_agent.md             # Memory agent documentation
│
├── ZebOS-XP_1.4_HTML/              # ZebOS Documentation (HTML)
├── indexes/                        # Search indexes
│   └── faiss.index                 # FAISS vector index
│
├── docker-compose.yaml             # Docker services definition
├── Dockerfile                      # Docker image build
├── requirements.txt                # Python dependencies
├── requirements-fastapi.txt        # FastAPI specific dependencies
│
├── init_ollama.py                  # Initialize Ollama models
├── download_model.py               # Download embedding models
├── setup.sh                        # Setup script
├── run_api.sh                      # Run API server
└── reset_db.py                     # Reset database

```

---

## 🚀 Cài Đặt & Chạy (Installation & Setup)

### Yêu Cầu Hệ Thống (Prerequisites)

- **Python**: 3.11+
- **Docker**: 20.10+ và Docker Compose
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB)
- **Disk**: ~10GB cho models và indexes

### Phương Pháp 1: Docker Compose (Khuyến Nghị)

```bash
# 1. Clone repository
git clone <repository-url>
cd Agentic

# 2. Build và start services
docker-compose up -d

# 3. Kiểm tra logs
docker-compose logs -f app

# 4. Truy cập API
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# MySQL: localhost:3306
# Ollama: localhost:11435
```

**Services được khởi chạy:**
- `app`: FastAPI backend (port 8000)
- `mysql`: Database (port 3306)
- `ollama`: LLM service (port 11435)

### Phương Pháp 2: Local Development

```bash
# 1. Tạo virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements-fastapi.txt

# 3. Setup database (MySQL)
# Tạo database 'chat_history_db'
mysql -u root -p -e "CREATE DATABASE chat_history_db;"

# 4. Setup environment variables
export DATABASE_URL="mysql+pymysql://root:password@localhost:3306/chat_history_db"
export OLLAMA_HOST="http://localhost:11434"

# 5. Download models
python init_ollama.py
python download_model.py

# 6. Build indexes
python bm25/main.py

# 7. Run API server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔧 Cấu Hình (Configuration)

### Environment Variables

```bash
# Database
DATABASE_URL=mysql+pymysql://root:123456@mysql:3306/chat_history_db

# Docker
RUNNING_IN_DOCKER=true  # Set to 'true' in Docker environment

# Ollama
OLLAMA_HOST=http://ollama:11434  # Docker
# OLLAMA_HOST=http://localhost:11434  # Local
```

### Model Configuration

Trong `init_ollama.py`:
```python
MODELS = [
    "qwen3:4b",        # Main LLM
    "nomic-embed-text" # Embedding model
]
```

### Search Configuration

Trong `agent/retriever.py`:
```python
results = search_with_indexes(
    query,
    index_dir="indexes",
    top_k=25,          # Số kết quả ban đầu
    alpha=0.4,         # Trọng số FAISS (0.4) vs BM25 (0.6)
    verbose=True
)
```

### Reranker Configuration

Trong `agent/reranker.py`:
```python
model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
top_k = 10  # Số documents sau rerank
```

---

## 📖 Sử Dụng (Usage)

### 1. Qua API (REST)

#### Tạo User
```bash
curl -X POST "http://localhost:8000/api/v1/chat/users?username=john"
```

#### Tạo Session
```bash
curl -X POST "http://localhost:8000/api/v1/chat/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "title": "OSPF Configuration"
  }'
```

#### Query (Chat)
```bash
curl -X POST "http://localhost:8000/api/v1/chat/query" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "session_id": 1,
    "message": "How to configure OSPF on interface xe1?"
  }'
```

#### Lấy History
```bash
curl "http://localhost:8000/api/v1/chat/sessions/1/messages?limit=10"
```

### 2. Qua Web Client (Flask)

```bash
cd client/
pip install -r requirements.txt
python app.py
# Truy cập: http://localhost:5000
```

### 3. Qua Python Code

```python
from agent.retriever import retriever_with_rerank
from agent.prompt_template import PromptTemplate
import ollama

# Query với reranking
query = "Configure OSPF on xe1"
results = retriever_with_rerank(query, top_k=25, rerank_top_k=10)

# Tạo prompt
template = PromptTemplate()
prompt = template.create_search_augmented_prompt(query, results, max_results=5)

# Generate response
client = ollama.Client(host='http://localhost:11434')
response = client.generate(prompt=prompt, model='qwen3:4b')
print(response['response'])
```

---

## 🧠 Các Module Chính (Core Modules)

### 1. **Agent Module** (`agent/`)

#### a. `prompt_template.py`
Quản lý các template prompt cho LLM.

**SYSTEM_PROMPT** - Prompt chính cho ZebOS Expert:
- Quy tắc ZEBOS-ONLY (không Cisco/Juniper)
- Format output bắt buộc (no placeholders)
- Verification commands
- Ví dụ configuration format

```python
from agent.prompt_template import PromptTemplate, SYSTEM_PROMPT

template = PromptTemplate()
prompt = template.create_query_prompt(
    query="Configure BGP on xe48",
    context="ZebOS documentation..."
)
```

#### b. `retriever.py`
Hybrid search retrieval với reranking.

**Functions:**
- `retriever(query, top_k)`: Hybrid search (FAISS + BM25)
- `retriever_with_rerank(query, top_k, rerank_top_k)`: Search + rerank
- `construct_prompt(query, results)`: Tạo prompt từ results
- `model_response(prompt)`: Call LLM

```python
from agent.retriever import retriever_with_rerank

results = retriever_with_rerank(
    query="Configure VLAN",
    top_k=25,
    rerank_top_k=10
)
```

#### c. `reranker.py`
Cross-encoder reranking để cải thiện độ chính xác.

```python
from agent.reranker import Reranker

reranker = Reranker()
reranked = reranker.rerank(
    query="OSPF configuration",
    documents=search_results,
    top_k=10
)
```

#### d. `chat_session_management.py`
SQLAlchemy models cho User, ChatSession, ChatMessage.

**Classes:**
- `User`: User account
- `ChatSession`: Chat session (1 user, nhiều sessions)
- `ChatMessage`: Individual message trong session

**CRUD Operations:**
- `create_user(engine, username)`
- `create_chat_session(engine, user_id, title)`
- `add_message(engine, session_id, role, content)`
- `get_session_messages(engine, session_id)`
- `summarize_memory(engine, session_id)`

### 2. **BM25 Module** (`bm25/`)

#### a. `main.py`
Tạo FAISS index và BM25 index từ HTML documents.

**Functions:**
- `process_documents(directory_path)`: Parse HTML files
- `create_faiss_index(documents, ...)`: Tạo FAISS index
- `save_indexes(faiss_index, chunks_data, bm25_index, output_dir)`: Lưu indexes

```python
from bm25.main import process_documents, create_faiss_index

# Process HTML docs
docs = process_documents("ZebOS-XP_1.4_HTML/")

# Create FAISS index
faiss_index, chunks_data, embeddings = create_faiss_index(
    docs,
    chunking_method='paragraphs',
    max_chunk_size=512,
    overlap=50
)
```

#### b. `search.py`
Hybrid search combining FAISS (semantic) và BM25 (keyword).

**Functions:**
- `hybrid_search_en(query, faiss_index, chunks_data, bm25_index, top_k, alpha)`
- `search_with_indexes(query, index_dir, top_k, alpha)`

```python
from bm25.search import search_with_indexes

results = search_with_indexes(
    query="OSPF configuration",
    index_dir="indexes",
    top_k=20,
    alpha=0.5  # 50% FAISS, 50% BM25
)
```

#### c. `embedding.py`
Text embedding và chunking strategies.

**Functions:**
- `embed_text(text)`: Embed single text với Ollama
- `embed_batch(texts, batch_size)`: Batch embedding
- `chunk_by_paragraphs(text)`: Chunk theo paragraphs
- `chunk_by_sentences(text, max_words)`: Chunk theo sentences
- `chunk_by_size(text, chunk_size, overlap)`: Fixed-size chunks

#### d. `parse.py`
Parse HTML documents từ ZebOS documentation.

**Functions:**
- `parse_html_and_normalize(file_path)`: Parse HTML to text
- `pipeline_html_extraction_and_normalization(file_path)`: Full pipeline

### 3. **FastAPI App** (`app/`)

#### a. `main.py`
FastAPI application entry point.

**Endpoints:**
- `GET /`: Welcome message
- `GET /health`: Health check
- `/api/v1/*`: API routes (via router)

#### b. `api/v1/router.py`
API routes definition.

**Route Groups:**
- `/chat/users`: User management
- `/chat/sessions`: Session management
- `/chat/messages`: Message operations
- `/chat/query`: Main chat query endpoint

#### c. API Endpoints Chi Tiết

**User Management:**
```
POST   /chat/users?username=<name>          # Create user
GET    /chat/users/{user_id}                # Get user info
GET    /chat/users/{user_id}/check          # Check exists
GET    /chat/users/{user_id}/sessions       # Get user sessions
DELETE /chat/users/{user_id}                # Delete user
```

**Session Management:**
```
POST   /chat/sessions                       # Create session
GET    /chat/sessions/{session_id}          # Get session
GET    /chat/sessions/{session_id}/messages # Get messages
DELETE /chat/sessions/{session_id}          # Delete session
```

**Chat Query:**
```
POST   /chat/query                          # Main chat endpoint
Body: {
  "user_id": 1,
  "session_id": 1,
  "message": "How to configure OSPF?"
}
```

---

## 🔍 Workflow Chi Tiết (Detailed Workflow)

### Query Processing Flow

```
1. User Input
   └─> POST /chat/query
       │
2. Hybrid Search (Retrieval)
   ├─> FAISS (Semantic Search)
   │   └─> Top 25 results (alpha=0.4)
   └─> BM25 (Keyword Search)
       └─> Top 25 results (alpha=0.6)
       │
3. Combine & Rank
   └─> 25 combined results
       │
4. Reranking (Cross-Encoder)
   └─> ms-marco-MiniLM-L-6-v2
   └─> Top 10 reranked results
       │
5. Prompt Construction
   └─> SYSTEM_PROMPT + Context + Query
       │
6. LLM Generation
   └─> Ollama (Qwen3:4b)
   └─> Response with CLI commands
       │
7. Save to Database
   └─> ChatMessage (role='user' + role='assistant')
       │
8. Return Response
   └─> JSON response to client
```

### Memory Management Flow

```
1. Short-Term Memory (STM)
   └─> Recent 5 messages in current session
       │
2. Long-Term Memory (LTM)
   └─> Summarized older messages
   └─> Triggered when messages > 10
       │
3. Summarization
   ├─> Take last 5 messages
   ├─> Generate summary via LLM
   └─> Store in ChatSession.summary
       │
4. Context Injection
   └─> {history_stm_context}: Recent messages
   └─> {history_ltm_context}: Summary
```

---

## 🧪 Testing

### Test Database Connection
```bash
python test_database.py
```

### Test Ollama
```bash
python test_ollama_refactor.py
```

### Test BM25 Search
```bash
cd bm25/
python main.py --test
```

### API Testing (Swagger)
Truy cập: `http://localhost:8000/docs`

---

## 🐛 Troubleshooting

### 1. Ollama Connection Error
```bash
# Check Ollama service
curl http://localhost:11434/api/tags

# Check Docker logs
docker-compose logs ollama

# Restart service
docker-compose restart ollama
```

### 2. MySQL Connection Error
```bash
# Check MySQL is running
docker-compose ps mysql

# Check connection
mysql -h localhost -u root -p123456 chat_history_db

# Reset database
python reset_db.py
```

### 3. FAISS Index Error
```bash
# Rebuild indexes
cd bm25/
python main.py

# Check index exists
ls -la indexes/
```

### 4. OpenMP Error (MacOS)
```bash
# Run fix script
bash fix_openmp.sh
```

---

## 📊 Performance Tuning

### 1. Search Performance

**Adjust alpha** (FAISS vs BM25 weight):
```python
# More semantic: alpha=0.7 (70% FAISS, 30% BM25)
# More keyword: alpha=0.3 (30% FAISS, 70% BM25)
# Balanced: alpha=0.5 (50% FAISS, 50% BM25)
```

**Adjust top_k**:
```python
# More results, slower but better recall
results = retriever(query, top_k=50)

# Fewer results, faster but may miss relevant docs
results = retriever(query, top_k=10)
```

### 2. Reranking

**Adjust rerank_top_k**:
```python
# More reranked, better precision but slower
results = retriever_with_rerank(query, top_k=25, rerank_top_k=15)

# Fewer reranked, faster but may miss best docs
results = retriever_with_rerank(query, top_k=25, rerank_top_k=5)
```

### 3. LLM Generation

**Model selection** trong `init_ollama.py`:
```python
# Faster, less accurate
MODELS = ["qwen3:4b"]

# Slower, more accurate
MODELS = ["qwen3:8b"]
```

---

## 🔐 Security Considerations

1. **Database Credentials**: Đổi mật khẩu mặc định trong production
   ```yaml
   # docker-compose.yaml
   MYSQL_ROOT_PASSWORD: <strong-password>
   ```

2. **API Authentication**: Thêm authentication middleware cho FastAPI
   ```python
   # app/main.py
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(CORSMiddleware, ...)
   ```

3. **Input Validation**: Validate user input để tránh injection
   ```python
   # schemas/chat.py
   class ChatRequest(BaseModel):
       message: str = Field(..., max_length=1000)
   ```

---

## 📈 Roadmap

- [ ] Add authentication & authorization
- [ ] Support multi-language (English + Vietnamese)
- [ ] Add more network device platforms
- [ ] Implement caching for search results
- [ ] Add telnet integration for live device testing
- [ ] WebSocket support for real-time chat
- [ ] Add monitoring & logging (Prometheus + Grafana)
- [ ] CLI tool for administration

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👥 Authors

- **Tuan PM** - Initial work

---

## 🙏 Acknowledgments

- **Ollama** - Local LLM runtime
- **FAISS** - Vector similarity search by Facebook AI
- **Sentence Transformers** - Cross-encoder models
- **FastAPI** - Modern web framework
- **SQLAlchemy** - Python SQL toolkit

---

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Email: support@example.com
- Documentation: `/docs/`

---

**Built with ❤️ for Network Engineers**
