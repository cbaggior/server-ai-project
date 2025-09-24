from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ai_endpoint_exists():
    response = client.post("/ai/ask", json={"question": "test"})
    assert response.status_code == 200
