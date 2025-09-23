from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_user():
    # cria
    r = client.post("/users/", json={"name": "Teste", "email": "teste@example.com"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["name"] == "Teste"
    assert data["email"] == "teste@example.com"
    user_id = data["id"]

    # busca
    r2 = client.get(f"/users/{user_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["id"] == user_id
