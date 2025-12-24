from fastapi import FastAPI
from app.api.v1.router import api_router
from app.api.v1.endpoints import users, items, chat 
app = FastAPI(
    title="ZebOS CLI Expert API",
    version="1.0.0",
    description="API for ZebOS CLI Expert System",
)


app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/")  # Root endpoint
def read_root():
    return {"message": "Welcome to the ZebOS CLI Expert API"}



 