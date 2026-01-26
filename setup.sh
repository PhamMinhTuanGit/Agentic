#!/bin/bash

# ============================================
# ZebOS Expert - Complete Project Setup Script
# ============================================
# This script sets up everything needed to run the project from scratch
# Usage: bash setup.sh

set -e  # Exit on error

echo "=========================================="
echo "ZebOS Expert - Project Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================
# 1. Check Prerequisites
# ============================================
echo -e "${YELLOW}[1/7] Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"
echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"
echo ""

# ============================================
# 2. Create Virtual Environment
# ============================================
echo -e "${YELLOW}[2/7] Setting up Python virtual environment...${NC}"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# ============================================
# 3. Install Dependencies
# ============================================
echo -e "${YELLOW}[3/7] Installing Python dependencies...${NC}"

pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Core dependencies installed${NC}"

pip install -r requirements-fastapi.txt > /dev/null 2>&1
echo -e "${GREEN}✓ FastAPI dependencies installed${NC}"

# Additional MySQL driver
pip install pymysql > /dev/null 2>&1
echo -e "${GREEN}✓ MySQL driver installed${NC}"
echo ""

# ============================================
# 4. Setup MySQL Database
# ============================================
echo -e "${YELLOW}[4/7] Setting up MySQL database...${NC}"

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q '^mysql-server$'; then
    echo -e "${GREEN}✓ MySQL container exists${NC}"
    if ! docker ps --format '{{.Names}}' | grep -q '^mysql-server$'; then
        echo "Starting MySQL container..."
        docker start mysql-server > /dev/null 2>&1
        sleep 5
    else
        echo -e "${GREEN}✓ MySQL container is already running${NC}"
    fi
else
    echo "Creating MySQL 8.0 container..."
    docker run --name mysql-server \
      -e MYSQL_ROOT_PASSWORD=123456 \
      -e MYSQL_DATABASE=chat_history_db \
      -p 3306:3306 \
      -d mysql:8.0 \
      --default-authentication-plugin=mysql_native_password \
      --character-set-server=utf8mb4 \
      --collation-server=utf8mb4_unicode_ci > /dev/null 2>&1
    
    echo "Waiting for MySQL to start..."
    sleep 10
    echo -e "${GREEN}✓ MySQL container created and started${NC}"
fi

# Verify MySQL connection
if docker exec mysql-server mysql -uroot -p123456 -e "SELECT 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ MySQL is running and accessible${NC}"
else
    echo -e "${RED}Error: Cannot connect to MySQL${NC}"
    exit 1
fi
echo ""

# ============================================
# 5. Create .env File
# ============================================
echo -e "${YELLOW}[5/7] Setting up environment variables...${NC}"

if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# FastAPI Configuration
DEBUG=True
FLASK_ENV=development

# Database
DATABASE_URL=mysql+pymysql://root:123456@localhost/chat_history_db

# CORS
CORS_ORIGINS=["*"]

# API
API_V1_STR=/api/v1

# Server
PORT=8000
HOST=0.0.0.0
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi
echo ""

# ============================================
# 6. Initialize Database
# ============================================
echo -e "${YELLOW}[6/7] Initializing database tables...${NC}"

python3 << 'PYTHON_SCRIPT'
import sys
from sqlalchemy import create_engine
from agent.chat_session_management import Base

try:
    engine = create_engine(
        "mysql+pymysql://root:123456@localhost/chat_history_db",
        echo=False
    )
    
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")
except Exception as e:
    print(f"Error creating tables: {e}")
    sys.exit(1)
PYTHON_SCRIPT

echo ""

# ============================================
# 7. Summary
# ============================================
echo -e "${YELLOW}[7/7] Setup complete!${NC}"
echo ""
echo -e "${GREEN}=========================================="
echo "✓ Project Setup Successfully Completed"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate virtual environment (if not already activated):"
echo "   source .venv/bin/activate"
echo ""
echo "2. Run the FastAPI server:"
echo "   bash run_api.sh"
echo ""
echo "3. Access the API:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo ""
echo "Database Information:"
echo "   - Host: localhost"
echo "   - Port: 3306"
echo "   - User: root"
echo "   - Password: 123456"
echo "   - Database: chat_history_db"
echo ""
echo "Useful commands:"
echo "   - Stop MySQL: docker stop mysql-server"
echo "   - Start MySQL: docker start mysql-server"
echo "   - Remove MySQL: docker rm -f mysql-server"
echo ""


