import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database.setup import Base
from app.api.deps import get_db
from main import app


def get_url():
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db_test")
    db = os.getenv("POSTGRES_DB", "test_app")
    return f"postgres://{user}:{password}@{server}/{db}"


SQLALCHEMY_DATABASE_URL = get_url()

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
        json={"username": "test", "email": "test@app.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": "test",
        "email": "test@app.com",
        "id": 1,
        "is_active": True,
        "items": []
    }


def test_create_existent_user():
    response = client.post(
        "/users",
        json={"username": "test", "email": "test@app.com", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email already registered"
    }


# Now, this needs authentication
# def test_read_users():
#     response = client.get("/users")
#     assert response.status_code == 200


def test_read_user():
    user = client.get
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "username": "test",
        "email": "test@app.com",
        "id": 1,
        "is_active": True,
        "items": []
    }


def test_read_inexistent_user():
    response = client.delete("/users/1000")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "User not found"
    }


def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "detail": f"User with id 1 successfully deleted"
    }


def test_delete_inexistent_user():
    response = client.delete("/users/1")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "User not found"
    }
