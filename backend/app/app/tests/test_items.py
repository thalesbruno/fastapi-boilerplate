from app.tests.setup import client


def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200
