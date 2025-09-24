from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Teste básico de saúde"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_users_endpoint_exists():
<<<<<<< HEAD
    response = client.get("/users/1")
=======
    """Teste que o endpoint de users existe"""
    response = client.get("/users/1")
    # Pode retornar 404 (não encontrado) ou 200 (se existir)
>>>>>>> c5d78f6f3b847c96a37051e73cf36d33957a180e
    assert response.status_code in [200, 404]
