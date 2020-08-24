from fastapi import APIRouter, Depends
from crud import crud
from typing import List
from api.schemas import schemas
from api.deps import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/items", response_model=List[schemas.Item], tags=['items'])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db=db, skip=skip, limit=limit)
    return items
