# ZebOS Expert System - Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Technology Stack](#technology-stack)

---

## System Overview

ZebOS Expert System là một ứng dụng AI-powered chatbot được thiết kế đặc biệt cho network configuration và troubleshooting trên hệ thống ZebOS. Kiến trúc hệ thống tuân theo mô hình **RAG (Retrieval-Augmented Generation)** để đảm bảo responses được hỗ trợ bởi tài liệu chính thức.

### Core Principles

1. **Accuracy First**: Chỉ cung cấp thông tin từ tài liệu ZebOS chính thức
2. **No Hallucination**: Sử dụng RAG để giảm thiểu hallucination
3. **Production-Ready**: CLI commands thực thi được, không có placeholders
4. **Scalable**: Microservices architecture với Docker
5. **Maintainable**: Modular design với separation of concerns

---

## Architecture Layers

### 1. Presentation Layer (Client)

```
┌─────────────────────────────────────────────┐
│         Presentation Layer                   │
├─────────────────────────────────────────────┤
│  ┌──────────────┐      ┌─────────────────┐ │
│  │ Flask Web UI │      │  REST API       │ │
│  │  (Port 5000) │      │  Clients        │ │
│  └──────────────┘      └─────────────────┘ │
└─────────────────────────────────────────────┘
```

**Components:**
- **Flask Web Client** (`client/app.py`): Web-based chat interface
- **REST API Clients**: Third-party integrations via HTTP

**Responsibilities:**
- User interaction và input collection
- Response rendering và visualization
- Session management (frontend)

### 2. API Gateway Layer

```
┌─────────────────────────────────────────────┐
│           API Gateway Layer                  │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐   │
│  │    FastAPI Application              │   │
│  │    (Port 8000)                      │   │
│  ├─────────────────────────────────────┤   │
│  │  • Request Validation (Pydantic)    │   │
│  │  • Routing (/api/v1/*)              │   │
│  │  • Error Handling                   │   │
│  │  • CORS Management                  │   │
│  │  • OpenAPI/Swagger Docs             │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Components:**
- **FastAPI App** (`app/main.py`): Main application
- **API Router** (`app/api/v1/router.py`): Route definitions
- **Schemas** (`app/schemas/`): Request/response validation

**Responsibilities:**
- API endpoint exposure
- Request validation và serialization
- Authentication/Authorization (future)
- Rate limiting (future)

### 3. Business Logic Layer (Agent)

```
┌──────────────────────────────────────────────────────┐
│              Business Logic Layer                     │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────┐│
│  │   Retriever   │  │   Reranker    │  │ Planning ││
│  │   Module      │  │   Module      │  │  Module  ││
│  └───────────────┘  └───────────────┘  └──────────┘│
│           │                 │                │       │
│           └─────────────────┴────────────────┘       │
│                          │                           │
│                 ┌────────▼────────┐                  │
│                 │  Agent Core     │                  │
│                 │  (Decision)     │                  │
│                 └────────┬────────┘                  │
│                          │                           │
│                 ┌────────▼────────┐                  │
│                 │ Prompt Builder  │                  │
│                 └─────────────────┘                  │
└──────────────────────────────────────────────────────┘
```

**Components:**

#### a. Retriever Module (`agent/retriever.py`)
- **Function**: Hybrid document retrieval
- **Methods**:
  - `retriever(query, top_k)`: Basic hybrid search
  - `retriever_with_rerank(query, top_k, rerank_top_k)`: Search + reranking
- **Dependencies**: BM25 module, FAISS

#### b. Reranker Module (`agent/reranker.py`)
- **Function**: Cross-encoder reranking
- **Model**: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- **Purpose**: Improve precision of search results

#### c. Prompt Template (`agent/prompt_template.py`)
- **Function**: Prompt engineering và management
- **Templates**:
  - `SYSTEM_PROMPT`: Main ZebOS expert prompt
  - `RERANK_PROMPT`: Reranking evaluation prompt
  - `INTENT_PARSING_PROMPT`: Intent classification
- **Classes**:
  - `PromptTemplate`: Base template manager
  - `RerankPromptTemplate`: Reranking specific

#### d. Chat Session Management (`agent/chat_session_management.py`)
- **Function**: Database models và CRUD operations
- **Models**:
  - `User`: User accounts
  - `ChatSession`: Chat sessions
  - `ChatMessage`: Individual messages
- **Operations**:
  - Create/Read/Update/Delete users, sessions, messages
  - Memory summarization

### 4. Data Access Layer

```
┌─────────────────────────────────────────────┐
│          Data Access Layer                   │
├─────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  │
│  │  SQLAlchemy ORM │  │  Database Pool  │  │
│  └─────────────────┘  └─────────────────┘  │
│           │                     │            │
│           └──────────┬──────────┘            │
│                      ▼                       │
│           ┌─────────────────────┐            │
│           │   MySQL Database    │            │
│           │   (Port 3306)       │            │
│           └─────────────────────┘            │
└─────────────────────────────────────────────┘
```

**Components:**
- **SQLAlchemy**: ORM layer
- **MySQL**: Persistent storage
- **Connection Pool**: Efficient DB connections

**Tables:**
- `user_account`: User information
- `chat_session`: Session metadata
- `chat_message`: Conversation history

### 5. Search & Retrieval Layer

```
┌─────────────────────────────────────────────────────┐
│         Search & Retrieval Layer                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐              ┌──────────────┐    │
│  │    FAISS     │              │     BM25     │    │
│  │   (Vector)   │              │  (Keyword)   │    │
│  └──────┬───────┘              └──────┬───────┘    │
│         │                             │             │
│         │     ┌───────────────┐       │             │
│         └────▶│ Hybrid Search │◀──────┘             │
│               │   (α-blend)   │                     │
│               └───────┬───────┘                     │
│                       │                             │
│                       ▼                             │
│              ┌─────────────────┐                    │
│              │  Search Results │                    │
│              └─────────────────┘                    │
└─────────────────────────────────────────────────────┘
```

**Components:**

#### a. FAISS Index (`indexes/faiss.index`)
- **Type**: Flat L2 index
- **Dimension**: 768 (nomic-embed-text)
- **Purpose**: Semantic similarity search
- **Advantages**: Fast, GPU-accelerated, handles synonyms

#### b. BM25 Index (`indexes/bm25.pkl`)
- **Algorithm**: Okapi BM25
- **Purpose**: Keyword-based search
- **Advantages**: Exact match, no embedding needed, fast

#### c. Hybrid Search (`bm25/search.py`)
- **Formula**: `final_score = α × faiss_score + (1-α) × bm25_score`
- **Default α**: 0.4 (40% FAISS, 60% BM25)
- **Advantage**: Best of both worlds

### 6. LLM Service Layer

```
┌─────────────────────────────────────────────┐
│           LLM Service Layer                  │
├─────────────────────────────────────────────┤
│  ┌──────────────────────────────────────┐  │
│  │       Ollama Server                  │  │
│  │       (Port 11434)                   │  │
│  ├──────────────────────────────────────┤  │
│  │  Models:                             │  │
│  │  • qwen3:4b (Generation)             │  │
│  │  • nomic-embed-text (Embedding)      │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

**Components:**
- **Ollama**: Local LLM runtime
- **qwen3:4b**: Text generation model (4B parameters)
- **nomic-embed-text**: Embedding model (768 dimensions)

---

## Component Details

### Agent Core Decision Engine

```python
class AgentCore:
    """
    Central decision-making engine.
    Orchestrates retrieval, reasoning, and response generation.
    """
    
    def __init__(self, llm_client, tools, memory_module):
        self.llm = llm_client          # Ollama client
        self.tools = tools              # Available tools
        self.memory = memory_module     # Session memory
        self.objectives = []            # Goal management
        
    async def execute_cycle(self, user_input: str):
        """
        Main decision loop:
        1. Retrieve context from memory
        2. LLM reasoning with tools
        3. Tool execution if needed
        4. Recursive loop until completion
        5. Return final response
        """
        # Step 1: Get context
        context = self.memory.get_context(user_input)
        
        # Step 2: LLM reasoning
        response = await self.llm.chat(
            messages=context,
            tools=self.tools,
            tool_choice="auto"
        )
        
        # Step 3: Handle tool calls
        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = await self._dispatch_tool(tool_call)
                self.memory.add_tool_result(tool_call.id, result)
                return await self.execute_cycle(user_input)
        
        return response.content
```

### Hybrid Search Algorithm

```python
def hybrid_search(query, faiss_index, bm25_index, alpha=0.4, top_k=10):
    """
    Combine FAISS (semantic) and BM25 (keyword) search.
    
    Formula:
        score = α × normalize(faiss_score) + (1-α) × normalize(bm25_score)
    
    Args:
        query: Search query string
        faiss_index: FAISS index object
        bm25_index: BM25 index object
        alpha: Weight for FAISS (0-1)
        top_k: Number of results to return
        
    Returns:
        List of top_k results sorted by combined score
    """
    # 1. FAISS search
    query_embedding = embed_text(query)
    faiss_distances, faiss_indices = faiss_index.search(
        query_embedding, top_k * 2
    )
    faiss_results = normalize_scores(faiss_distances)
    
    # 2. BM25 search
    bm25_scores = bm25_index.get_scores(tokenize(query))
    bm25_results = normalize_scores(bm25_scores)
    
    # 3. Combine scores
    combined = {}
    for idx, score in faiss_results:
        combined[idx] = alpha * score
    
    for idx, score in bm25_results:
        combined[idx] = combined.get(idx, 0) + (1 - alpha) * score
    
    # 4. Sort and return top_k
    sorted_results = sorted(
        combined.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:top_k]
    
    return sorted_results
```

### Reranking Process

```python
class Reranker:
    """
    Cross-encoder based reranking.
    Improves precision by scoring query-document pairs.
    """
    
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)
    
    def rerank(self, query: str, documents: List[Dict], top_k: int = 10):
        """
        Rerank documents using cross-encoder.
        
        Process:
        1. Create (query, doc) pairs
        2. Score each pair with cross-encoder
        3. Sort by score
        4. Return top_k
        """
        # Create pairs
        pairs = [(query, doc['text']) for doc in documents]
        
        # Score with cross-encoder
        scores = self.model.predict(pairs)
        
        # Sort and return top_k
        reranked = [
            {**doc, 'rerank_score': score}
            for doc, score in zip(documents, scores)
        ]
        reranked.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        return reranked[:top_k]
```

---

## Data Flow

### End-to-End Query Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    1. User Query Input                        │
│   POST /api/v1/chat/query                                     │
│   Body: {"user_id": 1, "session_id": 1, "message": "..."}    │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│              2. Request Validation (FastAPI)                  │
│   • Validate JSON schema                                      │
│   • Check user_id and session_id exist                        │
│   • Sanitize input                                            │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                3. Retrieve Chat History                       │
│   • Query MySQL for session messages                          │
│   • Get last 5 messages (STM)                                 │
│   • Get summary if exists (LTM)                               │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│              4. Hybrid Search (Retrieval)                     │
│   ┌────────────────┐         ┌────────────────┐             │
│   │ FAISS Search   │         │  BM25 Search   │             │
│   │ (Semantic)     │         │  (Keyword)     │             │
│   │ • Embed query  │         │ • Tokenize     │             │
│   │ • Vector search│         │ • Score docs   │             │
│   │ • Top 25       │         │ • Top 25       │             │
│   └───────┬────────┘         └───────┬────────┘             │
│           │                          │                       │
│           └────────┬─────────────────┘                       │
│                    ▼                                          │
│           ┌─────────────────┐                                │
│           │ Combine Results │                                │
│           │ α=0.4 (FAISS)   │                                │
│           │ 1-α=0.6 (BM25)  │                                │
│           └────────┬────────┘                                │
│                    │                                          │
│                    ▼                                          │
│           ┌─────────────────┐                                │
│           │  Top 25 Docs    │                                │
│           └─────────────────┘                                │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                  5. Reranking (Cross-Encoder)                 │
│   • Create (query, doc) pairs                                 │
│   • Score with cross-encoder model                            │
│   • Sort by rerank score                                      │
│   • Select top 10                                             │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                 6. Prompt Construction                        │
│   Components:                                                 │
│   • SYSTEM_PROMPT (ZebOS rules)                               │
│   • Retrieved context (top 10 docs)                           │
│   • Chat history (STM + LTM)                                  │
│   • User question                                             │
│   Format: <|im_start|>...<|im_end|>                          │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│              7. LLM Generation (Ollama/Qwen3:4b)              │
│   • Send prompt to Ollama                                     │
│   • Stream or wait for complete response                      │
│   • Parse response (extract CLI commands)                     │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                 8. Save to Database                           │
│   • Save user message (role='user')                           │
│   • Save assistant response (role='assistant')                │
│   • Update session timestamp                                  │
│   • Trigger summarization if needed (>10 messages)            │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                    9. Return Response                         │
│   JSON: {                                                     │
│     "response": "...",                                        │
│     "session_id": 1,                                          │
│     "timestamp": "2026-01-26T10:30:00"                        │
│   }                                                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Design Patterns

### 1. Repository Pattern
- **Location**: `agent/chat_session_management.py`
- **Purpose**: Separate data access logic from business logic
- **Implementation**: CRUD functions for User, ChatSession, ChatMessage

### 2. Strategy Pattern
- **Location**: `bm25/embedding.py`
- **Purpose**: Different chunking strategies
- **Strategies**: `chunk_by_paragraphs`, `chunk_by_sentences`, `chunk_by_size`

### 3. Template Method Pattern
- **Location**: `agent/prompt_template.py`
- **Purpose**: Define prompt structure with customizable parts
- **Implementation**: `PromptTemplate.create_query_prompt()`

### 4. Factory Pattern
- **Location**: `agent/retriever.py`
- **Purpose**: Create retriever instances with different configurations
- **Implementation**: `retriever()` vs `retriever_with_rerank()`

### 5. Facade Pattern
- **Location**: `bm25/main.py`
- **Purpose**: Simplify complex index creation process
- **Implementation**: `pipeline_html_extraction_and_normalization()`

---

## Technology Stack

### Backend
- **Python 3.11+**: Core language
- **FastAPI**: Web framework
- **SQLAlchemy 2.0**: ORM
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### AI/ML
- **Ollama**: LLM runtime
- **Qwen3:4b**: Generation model
- **nomic-embed-text**: Embedding model
- **Sentence Transformers**: Cross-encoder
- **FAISS**: Vector search
- **BM25**: Keyword search

### Database
- **MySQL 8.0**: Primary database
- **PyMySQL**: MySQL driver

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

### Frontend (Client)
- **Flask**: Web framework
- **Jinja2**: Templating
- **Bootstrap**: UI framework (assumed)

---

## Scalability Considerations

### Horizontal Scaling
1. **Stateless API**: FastAPI instances can be scaled horizontally
2. **Load Balancer**: Nginx/HAProxy for distributing requests
3. **Database Replication**: MySQL read replicas

### Performance Optimization
1. **Caching**: Redis for search results and embeddings
2. **Connection Pooling**: SQLAlchemy pool for database connections
3. **Async Operations**: FastAPI async endpoints for I/O operations

### Future Enhancements
1. **Message Queue**: RabbitMQ/Kafka for async processing
2. **Monitoring**: Prometheus + Grafana
3. **Distributed Tracing**: Jaeger/Zipkin
4. **API Gateway**: Kong/Tyk for advanced routing

---

## Security Architecture

### Current Implementation
- Basic input validation via Pydantic
- SQL injection prevention via SQLAlchemy ORM
- CORS configuration in FastAPI

### Recommended Additions
1. **Authentication**: JWT tokens, OAuth2
2. **Authorization**: Role-based access control (RBAC)
3. **Rate Limiting**: Per-user request limits
4. **Input Sanitization**: Advanced XSS prevention
5. **Secrets Management**: Vault for credentials
6. **HTTPS**: TLS/SSL certificates

---

This architecture provides a solid foundation for a production RAG system with room for growth and optimization.
