from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_ai_with_mock():
    # Teste com o mock implementado
    r = client.post("/ai/ask", json={"question": "Qual a capital da França?"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "capital" in data["answer"].lower() or "frança" in data["answer"]

def test_ask_ai_cache():
    # Primeira chamada
    r1 = client.post("/ai/ask", json={"question": "Teste cache?"})
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["cached"] is False

    # Segunda chamada deve vir do cache
    r2 = client.post("/ai/ask", json={"question": "Teste cache?"})
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["cached"] is True
