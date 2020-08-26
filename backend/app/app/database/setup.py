from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


def get_url():
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgres://{user}:{password}@{server}/{db}"


# With Docker
SQLALCHEMY_DATABASE_URL = get_url()

# Local
# SQLALCHEMY_DATABASE_URL = "postgresql://app:app@localhost:5432/app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
