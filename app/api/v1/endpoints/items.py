"""
Items endpoints (example)
"""
from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    """Item model"""
    id: int
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@router.get("", response_model=list[Item])
async def get_items():
    """Get items list"""
    return [
        {
            "id": 1,
            "name": "Item 1",
            "description": "Description 1",
            "price": 100.0
        }
    ]


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """Create new item"""
    return item
