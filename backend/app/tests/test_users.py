from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database.setup import Base
from database.session import get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = "postgresql://app:app@db:5432/test_app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={"email": "test@app.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": "test@app.com",
        "id": 1,
        "is_active": True,
        "items": []
    }


def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200


def test_read_user():
    user = client.get
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "email": "test@app.com",
        "id": 1,
        "is_active": True,
        "items": []
    }


def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "detail": f"User with id 1 successfully deleted"
    }
