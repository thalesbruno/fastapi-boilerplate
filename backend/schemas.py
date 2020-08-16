from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    item_id: int
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "item_id": 302,
                "name": "Smartphone",
                "description": "A modern smartphone"
            }
        }
