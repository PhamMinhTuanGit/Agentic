#!/bin/bash

# FastAPI Startup Script
# Cài đặt dependencies và chạy server

# Fix OpenMP duplicate library error on macOS
export KMP_DUPLICATE_LIB_OK=TRUE
export OMP_NUM_THREADS=1

echo "Installing dependencies..."
pip install -r requirements-fastapi.txt

echo ""
echo "Creating database tables..."
python -c "from app.db.session import engine; from app.db.base import Base; Base.metadata.create_all(bind=engine)"

echo ""
echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "Documentation at: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
