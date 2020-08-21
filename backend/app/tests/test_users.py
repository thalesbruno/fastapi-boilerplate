from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


# Get the last user id created on db and instatiate it +1 in the tests

def test_create_user():
    response = client.post(
        "/users",
        json={"email": "test@app.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": "test@app.com",
        "id": 10,
        "is_active": True,
        "items": []
    }


def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200


def test_read_user():
    response = client.get("/users/10")
    assert response.status_code == 200
    assert response.json() == {
        "email": "test@app.com",
        "id": 10,
        "is_active": True,
        "items": []
    }
