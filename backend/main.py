from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.setup import SessionLocal, engine
from models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependecy


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
