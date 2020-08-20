from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# With Docker
SQLALCHEMY_DATABASE_URL = "postgresql://app:app@db:5432/app"

# Local
# SQLALCHEMY_DATABASE_URL = "postgresql://app:app@localhost:5432/app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
