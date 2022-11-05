from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_fetch_fibonacci_indx():
    response = client.get("/fibonacci/5")
    assert response.status_code == 200


def test_create_blacklist():
    response = client.post("/fibonacci/blacklist/5")
    print(response.json())
    assert response.status_code == 201
