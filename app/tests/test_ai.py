from fastapi.testclient import TestClient
from app.main import app
from app.routes import ai as ai_module

client = TestClient(app)

def test_ask_ai_with_mock(monkeypatch):
    # mock do chain.invoke para evitar chamada real ao LLM
    def fake_invoke(input_data):
        class R:
            content = "Paris é a capital da França."
        return R()

    monkeypatch.setattr(ai_module, "chain", type("C", (), {"invoke": staticmethod(fake_invoke)})())

    r = client.post("/ai/ask", json={"question": "Qual a capital da França?"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "Paris" in data["answer"]

    # segunda chamada deve vir do cache
    r2 = client.post("/ai/ask", json={"question": "Qual a capital da França?"})
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["cached"] is True
