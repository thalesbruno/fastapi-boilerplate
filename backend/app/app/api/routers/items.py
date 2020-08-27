from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.api.schemas.item import ItemSchema
from app.api.deps import get_db
from app.crud import crud_item


router = APIRouter()


@router.get("/items", response_model=List[ItemSchema], tags=['items'])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud_item.get_items(db=db, skip=skip, limit=limit)
    return items
