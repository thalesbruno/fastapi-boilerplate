from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemSchema(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
