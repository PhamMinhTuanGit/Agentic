"""
FastAPI application entry point
"""
from fastapi import FastAPI
from app.api.v1.router import api_router

# Create FastAPI instance
app = FastAPI(
    title="RAG Chatbot API",
    description="Vietnamese RAG Chatbot with Session Management and Memory Agent",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to RAG Chatbot API",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}