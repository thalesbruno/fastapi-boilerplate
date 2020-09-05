from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.crud import crud_user
from app.api.deps import get_db, oauth2_scheme, get_current_user
from app.api.auth import auth
from app.api.schemas.user import UserSchema, UserCreate
from app.api.schemas.item import ItemCreate, ItemSchema
from app.services.messaging.email import send_email
from app.core.config import settings


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


@router.get("/users",
            response_model=List[UserSchema], tags=['admin'],
            dependencies=[Depends(get_current_user)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/users/me", response_model=UserSchema, tags=['users'])
def read_users_me(
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user


@router.get("/users/{user_id}", response_model=UserSchema, tags=['users'])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.post("/users", response_model=UserSchema, tags=['users'])
def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="Email already registered")
    if settings.SMTP_SERVER != "your_stmp_server_here":
        background_tasks.add_task(send_email, user.email,
                                  message=f"You've created your account!")
    return crud_user.create_user(db=db, user=user)


@router.delete("/users/{user_id}", tags=['admin'])
def remove_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    crud_user.delete_user(db=db, user=db_user)
    return {"detail": f"User with id {db_user.id} successfully deleted"}
