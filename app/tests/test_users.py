from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_user():
    # Teste de criação de usuário
    user_data = {
        "name": "Teste User",
        "email": "teste@example.com"
    }
    
    # Cria usuário
    r = client.post("/users/", json=user_data)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    user_id = data["id"]

    # Busca usuário
    r2 = client.get(f"/users/{user_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["id"] == user_id
    assert data2["name"] == user_data["name"]

def test_create_duplicate_user():
    # Teste de usuário duplicado
    user_data = {
        "name": "Teste Duplicado",
        "email": "duplicado@example.com"
    }
    
    # Primeira criação
    r1 = client.post("/users/", json=user_data)
    assert r1.status_code == 200

    # Segunda criação deve falhar
    r2 = client.post("/users/", json=user_data)
    assert r2.status_code == 409  # Conflict
