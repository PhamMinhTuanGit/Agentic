"""
API v1 router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import users, items, chat

api_router = APIRouter()

# Include routers
api_router.include_router(users.router)
api_router.include_router(items.router)
api_router.include_router(chat.router)
