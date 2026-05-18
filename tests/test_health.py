from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["version"] == "1.0.0"


def test_query_contract_smoke():
    r = client.post("/api/v1/query", json={"query": "What is our refund policy?"})
    assert r.status_code == 200
    payload = r.json()
    assert "trace_id" in payload
    assert payload["decision"] in {"allow", "deny"}
    assert isinstance(payload["score"], float)
    assert isinstance(payload["latency_ms"], float)
    assert isinstance(payload["agent_outputs"], list)