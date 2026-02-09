# Deployment Guide - ZebOS Expert System

## Table of Contents
1. [Deployment Options](#deployment-options)
2. [Docker Deployment](#docker-deployment)
3. [Production Configuration](#production-configuration)
4. [Monitoring & Logging](#monitoring--logging)
5. [Backup & Recovery](#backup--recovery)
6. [Scaling](#scaling)
7. [Security Hardening](#security-hardening)

---

## Deployment Options

### 1. Docker Compose (Recommended for Development/Small Scale)
- Single server deployment
- Easy setup and management
- Suitable for up to 100 concurrent users

### 2. Kubernetes (Production/Large Scale)
- Multi-server deployment
- Auto-scaling capabilities
- High availability
- Suitable for 1000+ concurrent users

### 3. Cloud Platforms
- AWS ECS/EKS
- Google Cloud Run/GKE
- Azure Container Instances/AKS

---

## Docker Deployment

### Prerequisites

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Quick Start

```bash
# 1. Clone repository
git clone <repository-url>
cd Agentic

# 2. Build and start services
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f

# 5. Access services
# API: http://localhost:8000
# MySQL: localhost:3306
# Ollama: localhost:11435
```

### Production Docker Compose

Create `docker-compose.prod.yaml`:

```yaml
version: '3.8'

services:
  app:
    image: agentic:${VERSION:-latest}
    build:
      context: .
      dockerfile: Dockerfile
      args:
        BUILD_DATE: ${BUILD_DATE}
        VERSION: ${VERSION}
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@mysql:3306/chat_history_db
      - RUNNING_IN_DOCKER=true
      - OLLAMA_HOST=http://ollama:11434
      - LOG_LEVEL=INFO
    depends_on:
      mysql:
        condition: service_healthy
      ollama:
        condition: service_started
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    volumes:
      - ./logs:/app/logs
    networks:
      - agentic_network

  mysql:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: chat_history_db
      MYSQL_INITDB_SKIP_TZINFO: "true"
    ports:
      - "3306:3306"
    command: --bind-address=0.0.0.0 --max-connections=200
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql/conf.d:/etc/mysql/conf.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 10
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    networks:
      - agentic_network

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
      - OLLAMA_NUM_PARALLEL=4
      - OLLAMA_MAX_LOADED_MODELS=2
    volumes:
      - ollama_data:/data
      - ollama_models:/root/.ollama
    restart: always
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - agentic_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - app
    restart: always
    networks:
      - agentic_network

volumes:
  mysql_data:
    driver: local
  ollama_data:
    driver: local
  ollama_models:
    driver: local

networks:
  agentic_network:
    driver: bridge
```

### Environment Configuration

Create `.env.prod`:

```bash
# Version
VERSION=1.0.0
BUILD_DATE=2026-01-26

# MySQL
MYSQL_ROOT_PASSWORD=<strong-random-password>
MYSQL_DATABASE=chat_history_db

# Application
DATABASE_URL=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@mysql:3306/chat_history_db
RUNNING_IN_DOCKER=true
LOG_LEVEL=INFO

# Ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_NUM_PARALLEL=4
OLLAMA_MAX_LOADED_MODELS=2

# Security
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Deploy to Production

```bash
# 1. Set environment variables
export $(cat .env.prod | xargs)

# 2. Build images
docker-compose -f docker-compose.prod.yaml build

# 3. Start services
docker-compose -f docker-compose.prod.yaml up -d

# 4. Initialize database
docker-compose -f docker-compose.prod.yaml exec app python reset_db.py

# 5. Download models
docker-compose -f docker-compose.prod.yaml exec app python init_ollama.py

# 6. Build indexes
docker-compose -f docker-compose.prod.yaml exec app python bm25/main.py

# 7. Verify deployment
curl http://localhost:8000/health
```

---


docker compose exec ollama bash -c '
ollama list | grep -q qwen3:4b || ollama pull qwen3:4b
ollama list | grep -q nomic-embed-text || ollama pull nomic-embed-text
'


## Production Configuration

### Nginx Configuration

`nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api_backend {
        least_conn;
        server app:8000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security Headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Logging
        access_log /var/log/nginx/access.log combined;
        error_log /var/log/nginx/error.log warn;

        # API Proxy
        location /api/ {
            # Rate limiting
            limit_req zone=api_limit burst=20 nodelay;
            limit_conn addr 10;

            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Health Check
        location /health {
            proxy_pass http://api_backend;
            access_log off;
        }

        # Static files (if any)
        location /static/ {
            alias /app/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### MySQL Optimization

`mysql/conf.d/custom.cnf`:

```ini
[mysqld]
# Connection Settings
max_connections = 200
max_connect_errors = 100
wait_timeout = 600
interactive_timeout = 600

# Buffer Settings
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_log_buffer_size = 16M
innodb_flush_log_at_trx_commit = 2

# Query Cache (MySQL 5.7)
query_cache_type = 1
query_cache_size = 64M
query_cache_limit = 2M

# Performance Schema
performance_schema = ON

# Logging
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow-query.log
long_query_time = 2

# Character Set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

### Application Configuration

`app/core/config.py`:

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App
    APP_NAME: str = "ZebOS Expert System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_PRE_PING: bool = True
    
    # Ollama
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_TIMEOUT: int = 120
    
    # Search
    SEARCH_TOP_K: int = 25
    SEARCH_ALPHA: float = 0.4
    RERANK_TOP_K: int = 10
    
    # Security
    SECRET_KEY: str
    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = ["*"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## Monitoring & Logging

### Application Logging

`app/core/logging.py`:

```python
import logging
import sys
from logging.handlers import RotatingFileHandler
from app.core.config import settings

def setup_logging():
    """Configure application logging."""
    # Create logger
    logger = logging.getLogger("agentic")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # File handler
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()
```

### Prometheus Metrics (Optional)

Install:
```bash
pip install prometheus-fastapi-instrumentator
```

`app/main.py`:
```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(...)

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)
```

Access metrics: `http://localhost:8000/metrics`

### Log Aggregation with ELK Stack

`docker-compose.monitoring.yaml`:

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash/config:/usr/share/logstash/pipeline
    ports:
      - "5000:5000"
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

---

## Backup & Recovery

### Database Backup

Automated backup script `scripts/backup_db.sh`:

```bash
#!/bin/bash

# Configuration
BACKUP_DIR="/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
MYSQL_CONTAINER="agentic-mysql-1"
DB_NAME="chat_history_db"
RETENTION_DAYS=7

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker exec $MYSQL_CONTAINER mysqldump \
    -u root -p$MYSQL_ROOT_PASSWORD \
    --single-transaction \
    --quick \
    --lock-tables=false \
    $DB_NAME > $BACKUP_DIR/backup_${DATE}.sql

# Compress backup
gzip $BACKUP_DIR/backup_${DATE}.sql

# Remove old backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: backup_${DATE}.sql.gz"
```

Setup cron job:
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/scripts/backup_db.sh >> /var/log/backup.log 2>&1
```

### Database Restore

```bash
# Restore from backup
gunzip -c /backups/mysql/backup_20260126_020000.sql.gz | \
docker exec -i agentic-mysql-1 mysql \
    -u root -p$MYSQL_ROOT_PASSWORD \
    chat_history_db
```

### Index Backup

```bash
# Backup indexes
tar -czf indexes_backup_$(date +%Y%m%d).tar.gz indexes/

# Restore indexes
tar -xzf indexes_backup_20260126.tar.gz
```

---

## Scaling

### Vertical Scaling (Single Server)

Increase resources in `docker-compose.prod.yaml`:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
  
  ollama:
    deploy:
      resources:
        limits:
          cpus: '8'
          memory: 16G
```

### Horizontal Scaling (Multiple Servers)

Use Docker Swarm or Kubernetes.

#### Docker Swarm Example

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yaml agentic

# Scale API service
docker service scale agentic_app=3

# View services
docker service ls
```

#### Kubernetes Example

`k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentic-api
  template:
    metadata:
      labels:
        app: agentic-api
    spec:
      containers:
      - name: api
        image: agentic:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: agentic-secrets
              key: database-url
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: agentic-api-service
spec:
  type: LoadBalancer
  selector:
    app: agentic-api
  ports:
  - port: 80
    targetPort: 8000
```

Deploy:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
kubectl get services
```

---

## Security Hardening

### 1. Application Security

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trusted Hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)
```

### 2. Database Security

- Use strong passwords
- Enable SSL/TLS connections
- Restrict network access
- Regular security updates

### 3. Docker Security

```dockerfile
# Use non-root user
FROM python:3.11-slim

RUN useradd -m -u 1000 appuser
USER appuser

# Copy only necessary files
COPY --chown=appuser:appuser . /app

# Don't run as root
WORKDIR /app
```

### 4. SSL/TLS Configuration

```bash
# Generate SSL certificate (Let's Encrypt)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com
```

### 5. Secrets Management

Use Docker secrets or environment variables:

```bash
# Create secret
echo "supersecretpassword" | docker secret create mysql_password -

# Use in compose file
services:
  mysql:
    secrets:
      - mysql_password
    environment:
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/mysql_password

secrets:
  mysql_password:
    external: true
```

---

## Health Checks & Monitoring

### Application Health Check

```python
# app/api/v1/endpoints/health.py
from fastapi import APIRouter, status
import ollama
from sqlalchemy import text
from app.db.session import engine

router = APIRouter()

@router.get("/health")
async def health_check():
    """Comprehensive health check."""
    health_status = {
        "status": "healthy",
        "components": {}
    }
    
    # Check database
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health_status["components"]["database"] = "healthy"
    except Exception as e:
        health_status["components"]["database"] = f"unhealthy: {e}"
        health_status["status"] = "unhealthy"
    
    # Check Ollama
    try:
        client = ollama.Client()
        client.list()
        health_status["components"]["ollama"] = "healthy"
    except Exception as e:
        health_status["components"]["ollama"] = f"unhealthy: {e}"
        health_status["status"] = "unhealthy"
    
    # Check indexes
    import os
    if os.path.exists("indexes/faiss.index"):
        health_status["components"]["indexes"] = "healthy"
    else:
        health_status["components"]["indexes"] = "unhealthy: indexes not found"
        health_status["status"] = "degraded"
    
    status_code = status.HTTP_200_OK if health_status["status"] == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return health_status, status_code
```

---

## Maintenance Tasks

### Regular Maintenance Checklist

- [ ] Daily: Check logs for errors
- [ ] Daily: Database backup
- [ ] Weekly: Update Docker images
- [ ] Weekly: Review disk usage
- [ ] Monthly: Security patches
- [ ] Monthly: Performance review
- [ ] Quarterly: Dependency updates

### Useful Commands

```bash
# View logs
docker-compose logs -f --tail=100 app

# Restart service
docker-compose restart app

# Update images
docker-compose pull
docker-compose up -d

# Clean up
docker system prune -a --volumes

# Database shell
docker-compose exec mysql mysql -u root -p chat_history_db

# Application shell
docker-compose exec app /bin/bash
```

---

Production deployment complete! Your ZebOS Expert System is ready to serve users at scale. 🚀
