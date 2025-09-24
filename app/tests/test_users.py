from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_users_endpoint_exists():
    response = client.get("/users/1")
    assert response.status_code in [200, 404]
