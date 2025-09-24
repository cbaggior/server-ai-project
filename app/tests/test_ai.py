<<<<<<< HEAD
def test_ai_smoke():
    """Teste smoke básico"""
    assert True

def test_ai_import():
    """Teste que as importações funcionam"""
    try:
        from app.routes import ai
        assert ai is not None
    except ImportError:
        assert False, "Erro na importação"
=======
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_ai_endpoint_exists():
    """Teste básico que o endpoint existe e retorna 200"""
    # Mock para evitar chamadas reais à OpenAI
    with patch('app.routes.ai.redis_client') as mock_redis:
        mock_redis.get.return_value = None  # Simula cache vazio
        mock_redis.set.return_value = True  # Simula salvar no cache
        
        response = client.post("/ai/ask", json={"question": "teste"})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "cached" in data

def test_ai_cache_behavior():
    """Teste o comportamento do cache"""
    with patch('app.routes.ai.redis_client') as mock_redis:
        # Primeira chamada - cache miss
        mock_redis.get.return_value = None
        response1 = client.post("/ai/ask", json={"question": "cache test"})
        assert response1.status_code == 200
        assert response1.json()["cached"] is False
        
        # Segunda chamada - cache hit
        mock_redis.get.return_value = "Resposta em cache"
        response2 = client.post("/ai/ask", json={"question": "cache test"})
        assert response2.status_code == 200
        assert response2.json()["cached"] is True
>>>>>>> c5d78f6f3b847c96a37051e73cf36d33957a180e
