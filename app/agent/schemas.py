from pydantic import BaseModel, Field
from typing import Literal, List, Union

class MemoryItem(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class LongTermMemory(BaseModel):
    content: str
    tags: List[str] = []

class ChatRequest(BaseModel):
    session_id: Union[str, int] = Field(...)
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "1",
                "message": "How to configure OSPF?"
            }
        }


class MessageRequest(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "How to configure OSPF?"
            }
        }
