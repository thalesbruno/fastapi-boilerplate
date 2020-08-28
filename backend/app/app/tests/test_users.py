from app.tests.setup import client


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


def test_user_authenticate(username: str = "test", password: str = "password"):
    response = client.post(
        "/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": f"{username}", "password": f"{password}"}
    )
    return response.json()["access_token"]
    assert response.status_code == 200


def test_read_user_me():
    token = test_user_authenticate()
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_read_users():
    token = test_user_authenticate()
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


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
