# Development Guide - ZebOS Expert System

## Table of Contents
1. [Setup Development Environment](#setup-development-environment)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Testing](#testing)
5. [Debugging](#debugging)
6. [Common Tasks](#common-tasks)
7. [Best Practices](#best-practices)

---

## Setup Development Environment

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- MySQL 8.0 (if running locally)
- Git
- IDE (VS Code recommended)

### Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd Agentic

# 2. Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-fastapi.txt

# 4. Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy

# 5. Setup environment variables
cp .env.example .env  # Create if not exists
# Edit .env with your configurations
```

### VS Code Setup

Recommended extensions:
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-azuretools.vscode-docker",
    "redhat.vscode-yaml",
    "ms-python.black-formatter"
  ]
}
```

`.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.analysis.typeCheckingMode": "basic"
}
```

---

## Project Structure

### Module Organization

```
agent/              # Core business logic
├── __init__.py
├── core.py         # Agent decision engine
├── retriever.py    # Hybrid search retrieval
├── reranker.py     # Cross-encoder reranking
├── prompt_template.py  # Prompt management
├── planning.py     # Task planning
└── chat_session_management.py  # DB models & CRUD

app/                # FastAPI application
├── __init__.py
├── main.py         # App entry point
├── api/
│   └── v1/
│       ├── router.py      # API routes
│       └── endpoints/     # Endpoint handlers
├── core/
│   └── config.py          # Configuration
├── db/
│   ├── base.py            # DB base
│   └── session.py         # Session factory
├── schemas/
│   ├── chat.py            # Chat schemas
│   └── tool.py            # Tool schemas
└── llm/
    └── ollama.py          # Ollama client

bm25/               # Search & indexing
├── __init__.py
├── main.py         # Index creation
├── bm25.py         # BM25 implementation
├── embedding.py    # Embedding & chunking
├── parse.py        # HTML parsing
└── search.py       # Hybrid search

client/             # Flask web client
├── app.py
└── requirements.txt

telnet/             # Device connectivity
├── __init__.py
├── connect.py
└── parse_and_telnet.py

docs/               # Documentation
├── API_DOCUMENTATION.md
├── ARCHITECTURE.md
├── DEVELOPMENT.md
└── bm25_doc_en.md
```

### File Naming Conventions

- **Python files**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase`
- **Functions**: `lowercase_with_underscores`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore`

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) with these specifics:

**Line Length**: 88 characters (Black default)

**Imports**:
```python
# Standard library
import os
import sys
from typing import List, Dict, Optional

# Third-party
import faiss
import numpy as np
from sqlalchemy import create_engine

# Local
from agent.retriever import retriever
from agent.prompt_template import PromptTemplate
```

**Type Hints**:
```python
def hybrid_search(
    query: str,
    faiss_index: faiss.Index,
    bm25_index: BM25Okapi,
    top_k: int = 10,
    alpha: float = 0.4
) -> List[Dict[str, Any]]:
    """
    Perform hybrid search combining FAISS and BM25.
    
    Args:
        query: Search query string
        faiss_index: FAISS index object
        bm25_index: BM25 index object
        top_k: Number of results to return
        alpha: Weight for FAISS (0-1)
        
    Returns:
        List of search results with scores
        
    Raises:
        ValueError: If alpha not in [0, 1]
    """
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be between 0 and 1")
    
    # Implementation...
    return results
```

**Docstrings**: Google style
```python
def create_user(engine, username: str) -> User:
    """Create a new user in the database.
    
    Args:
        engine: SQLAlchemy engine instance
        username: Username for the new user
        
    Returns:
        Created User object
        
    Raises:
        IntegrityError: If username already exists
        
    Example:
        >>> engine = create_engine("mysql://...")
        >>> user = create_user(engine, "john_doe")
        >>> print(user.id)
        1
    """
    with Session(engine) as session:
        user = User(name=username)
        session.add(user)
        session.commit()
        return user
```

### Formatting

Use **Black** for code formatting:
```bash
# Format single file
black agent/retriever.py

# Format entire project
black .

# Check without modifying
black --check .
```

### Linting

Use **Flake8** for linting:
```bash
# Lint single file
flake8 agent/retriever.py

# Lint entire project
flake8 .

# Configuration in .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,.venv
```

### Type Checking

Use **mypy** for static type checking:
```bash
# Type check single file
mypy agent/retriever.py

# Type check entire project
mypy .

# Configuration in mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

---

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── unit/
│   ├── test_retriever.py
│   ├── test_reranker.py
│   └── test_prompt_template.py
├── integration/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_search.py
└── e2e/
    └── test_chat_flow.py
```

### Unit Tests

```python
# tests/unit/test_retriever.py
import pytest
from agent.retriever import retriever
from unittest.mock import Mock, patch

def test_retriever_returns_results():
    """Test that retriever returns expected results."""
    with patch('agent.retriever.search_with_indexes') as mock_search:
        mock_search.return_value = [
            {'text': 'Result 1', 'score': 0.9},
            {'text': 'Result 2', 'score': 0.8}
        ]
        
        results = retriever("test query", top_k=2)
        
        assert len(results) == 2
        assert results[0]['score'] == 0.9
        mock_search.assert_called_once_with(
            "test query",
            index_dir="indexes",
            top_k=2,
            alpha=0.4,
            verbose=True
        )

def test_retriever_handles_empty_results():
    """Test retriever with no results."""
    with patch('agent.retriever.search_with_indexes') as mock_search:
        mock_search.return_value = []
        
        results = retriever("test query")
        
        assert results == []
```

### Integration Tests

```python
# tests/integration/test_database.py
import pytest
from sqlalchemy import create_engine
from agent.chat_session_management import create_user, create_chat_session

@pytest.fixture
def test_engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

def test_create_user_and_session(test_engine):
    """Test creating user and session."""
    # Create user
    user = create_user(test_engine, "test_user")
    assert user.id is not None
    assert user.name == "test_user"
    
    # Create session
    session = create_chat_session(test_engine, user.id, "Test Chat")
    assert session.id is not None
    assert session.user_id == user.id
    assert session.title == "Test Chat"
```

### API Tests

```python
# tests/integration/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_user():
    """Test user creation endpoint."""
    response = client.post("/api/v1/chat/users?username=testuser")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "testuser"
    assert "id" in data

def test_chat_query():
    """Test chat query endpoint."""
    # Create user first
    user_response = client.post("/api/v1/chat/users?username=testuser2")
    user_id = user_response.json()["id"]
    
    # Create session
    session_response = client.post(
        "/api/v1/chat/sessions",
        json={"user_id": user_id, "title": "Test"}
    )
    session_id = session_response.json()["id"]
    
    # Send query
    query_response = client.post(
        "/api/v1/chat/query",
        json={
            "user_id": user_id,
            "session_id": session_id,
            "message": "Configure OSPF on xe1"
        }
    )
    assert query_response.status_code == 200
    assert "response" in query_response.json()
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_retriever.py

# Run with coverage
pytest --cov=agent --cov=app --cov-report=html

# Run with verbose output
pytest -v

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

---

## Debugging

### Logging Setup

```python
# agent/logger.py
import logging
import sys

def setup_logger(name: str, level=logging.INFO):
    """Setup logger with consistent format."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

# Usage in modules
logger = setup_logger(__name__)
logger.info("Starting retrieval...")
logger.debug(f"Query: {query}")
logger.error(f"Error occurred: {e}")
```

### Debug FastAPI

```python
# app/main.py
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Or use FastAPI debug mode
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
```

### Debug with VS Code

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": false
    },
    {
      "name": "Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Debug Ollama Connections

```python
import ollama
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    client = ollama.Client(host='http://localhost:11434')
    response = client.list()
    print("Available models:", response)
except Exception as e:
    print(f"Connection error: {e}")
```

### Debug Database Queries

```python
from sqlalchemy import create_engine
import logging

# Enable SQL logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(
    "mysql+pymysql://root:password@localhost:3306/chat_history_db",
    echo=True  # Print all SQL statements
)
```

---

## Common Tasks

### Adding a New API Endpoint

1. **Define Schema** (`app/schemas/chat.py`):
```python
from pydantic import BaseModel, Field

class NewFeatureRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    param: str = Field(..., max_length=100)

class NewFeatureResponse(BaseModel):
    result: str
    status: str
```

2. **Create Endpoint** (`app/api/v1/endpoints/new_feature.py`):
```python
from fastapi import APIRouter, HTTPException
from app.schemas.chat import NewFeatureRequest, NewFeatureResponse

router = APIRouter()

@router.post("/new-feature", response_model=NewFeatureResponse)
async def new_feature(request: NewFeatureRequest):
    """Process new feature request."""
    try:
        # Implementation
        result = process_feature(request)
        return NewFeatureResponse(
            result=result,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

3. **Register Router** (`app/api/v1/router.py`):
```python
from app.api.v1.endpoints import new_feature

api_router.include_router(
    new_feature.router,
    prefix="/feature",
    tags=["feature"]
)
```

### Adding a New Prompt Template

```python
# agent/prompt_template.py

NEW_FEATURE_PROMPT = """<|im_start|>system
You are an expert in...

{context}
<|im_end|>

<|im_start|>user
{user_question}
<|im_end|>

<|im_start|>assistant
"""

class NewFeaturePromptTemplate(PromptTemplate):
    """Template for new feature."""
    
    def __init__(self):
        super().__init__(NEW_FEATURE_PROMPT)
    
    def create_prompt(self, question: str, context: str) -> str:
        """Create formatted prompt."""
        prompt = self.system_prompt
        prompt = prompt.replace("{context}", context)
        prompt = prompt.replace("{user_question}", question)
        return prompt
```

### Rebuilding Indexes

```bash
# Full rebuild
python bm25/main.py

# Or programmatically
python -c "
from bm25.main import process_documents, create_faiss_index, save_indexes

docs = process_documents('ZebOS-XP_1.4_HTML/')
faiss_idx, chunks, embeddings = create_faiss_index(docs)
save_indexes(faiss_idx, chunks, None, 'indexes/')
"
```

### Database Migrations

```bash
# Reset database (development only)
python reset_db.py

# Manual migration
python -c "
from sqlalchemy import create_engine
from agent.chat_session_management import Base

engine = create_engine('mysql+pymysql://...')
Base.metadata.create_all(engine)
"
```

### Adding a New Model

```bash
# 1. Add model to init_ollama.py
MODELS = [
    "qwen3:4b",
    "qwen3:8b",  # New model
    "nomic-embed-text"
]

# 2. Pull model
python init_ollama.py

# Or manually
docker exec -it agentic-ollama-1 ollama pull qwen3:8b
```

---

## Best Practices

### Code Organization

1. **Single Responsibility**: One function = one purpose
2. **DRY**: Don't Repeat Yourself - extract common code
3. **Modularity**: Keep modules independent
4. **Configuration**: Use environment variables, not hardcoded values

### Error Handling

```python
# Good: Specific exception handling
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise HTTPException(status_code=400, detail="Invalid input")
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise HTTPException(status_code=503, detail="Service unavailable")

# Bad: Catch-all exception
try:
    result = risky_operation()
except Exception as e:
    pass  # Silent failure
```

### Async Best Practices

```python
# Good: Use async for I/O operations
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Bad: Blocking I/O in async function
async def fetch_data_bad(url: str) -> dict:
    import requests
    response = requests.get(url)  # Blocks event loop!
    return response.json()
```

### Database Best Practices

```python
# Good: Context manager
from contextlib import contextmanager

@contextmanager
def get_session(engine):
    """Provide session with automatic cleanup."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
with get_session(engine) as session:
    user = session.query(User).filter_by(id=1).first()
```

### Performance Tips

1. **Batch Operations**: Process multiple items at once
```python
# Good: Batch embedding
embeddings = embed_batch(texts, batch_size=32)

# Bad: One at a time
embeddings = [embed_text(text) for text in texts]
```

2. **Caching**: Cache expensive operations
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def embed_text_cached(text: str):
    """Cache embeddings for repeated queries."""
    return embed_text(text)
```

3. **Connection Pooling**: Reuse database connections
```python
engine = create_engine(
    "mysql+pymysql://...",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### Security Best Practices

1. **Input Validation**: Always validate user input
2. **SQL Injection**: Use parameterized queries (ORM handles this)
3. **Secrets**: Never commit credentials to git
4. **Dependencies**: Keep dependencies updated

```bash
# Check for security vulnerabilities
pip install safety
safety check

# Update dependencies
pip list --outdated
pip install --upgrade <package>
```

---

## Troubleshooting

### Common Issues

**Issue: Import errors**
```bash
# Solution: Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install in editable mode
pip install -e .
```

**Issue: Ollama connection refused**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama (Docker)
docker-compose up ollama

# Check logs
docker-compose logs ollama
```

**Issue: MySQL connection error**
```bash
# Check MySQL is running
docker-compose ps mysql

# Check connection
mysql -h localhost -u root -p123456 -e "SELECT 1"

# Reset database
python reset_db.py
```

---

## Contributing Workflow

1. **Create Branch**: `git checkout -b feature/your-feature`
2. **Make Changes**: Follow coding standards
3. **Run Tests**: `pytest`
4. **Format Code**: `black .`
5. **Lint**: `flake8 .`
6. **Type Check**: `mypy .`
7. **Commit**: `git commit -m "feat: add new feature"`
8. **Push**: `git push origin feature/your-feature`
9. **Pull Request**: Open PR on GitHub

### Commit Message Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Examples**:
```
feat(retriever): add reranking support
fix(api): handle empty query gracefully
docs(readme): update installation instructions
```

---

Happy coding! 🚀
