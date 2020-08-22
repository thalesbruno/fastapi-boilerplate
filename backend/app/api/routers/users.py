from fastapi import APIRouter, HTTPException, Depends
from crud import crud
from api.deps import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from typing import List
from api.deps import oauth2_scheme, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


def fake_hash_password(password: str):
    return password + "notreallyhashed"


@router.post("/token", tags=['auth'])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me", response_model=schemas.User, tags=['auth'])
def read_users_me(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user


@router.get("/users", response_model=List[schemas.User], tags=['users'])
def read_users(
        skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@ router.post("/users", response_model=schemas.User, tags=['users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="Email already registered")
    return crud.create_user(db=db, user=user)


@ router.get("/users/{user_id}", response_model=schemas.User, tags=['users'])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@ router.post("/users/{user_id}/items", response_model=schemas.Item, tags=['users'])
def create_item_for_user(item: schemas.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@ router.delete("/users/{user_id}", tags=['users'])
def remove_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    crud.delete_user(db=db, user=db_user)
    return {"detail": f"User with id {db_user.id} successfully deleted"}
