from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from database.setup import SessionLocal
from sqlalchemy.orm import Session
from schemas import schemas
from crud import crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token: str, db: Session):
    user = crud.get_user_by_username(db=db, username=token)
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
