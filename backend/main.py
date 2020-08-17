from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.setup import SessionLocal, engine
from models import models
from schemas import schemas
from crud import crud


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependecy


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"Response": "Hello World"}
