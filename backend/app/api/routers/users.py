from fastapi import APIRouter, HTTPException, Depends, status
from crud import crud
from api.deps import get_db
from sqlalchemy.orm import Session
from api.schemas import schemas
from typing import List
from api.deps import oauth2_scheme, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import auth
from datetime import timedelta


router = APIRouter()


@router.post("/token", tags=['auth'])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(
        db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


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


@router.post("/users", response_model=schemas.User, tags=['users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.User, tags=['users'])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items", response_model=schemas.Item, tags=['users'])
def create_item_for_user(item: schemas.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.delete("/users/{user_id}", tags=['users'])
def remove_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    crud.delete_user(db=db, user=db_user)
    return {"detail": f"User with id {db_user.id} successfully deleted"}
