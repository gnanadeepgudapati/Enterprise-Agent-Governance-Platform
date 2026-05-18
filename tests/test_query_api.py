from fastapi.testclient import TestClient
import pytest

from app.main import app

client = TestClient(app)


EDGE_CASE_QUERIES = [
    "refund policy for enterprise customers",
    "incident response lifecycle summary",
    "give me compliance controls for SOC2",
    "HIPAA handling controls",
    "how is customer pii protected",
    "salary data policy",
    "what is our data retention period",
    "can support team view account number",
    "security baseline checklist",
    "explain role based access model",
    "regional data residency guidance",
    "escalation matrix for security alerts",
    "business continuity plan summary",
    "what to do for failed login spikes",
    "audit evidence collection workflow",
] + [f"generic enterprise request #{index}" for index in range(1, 46)]


@pytest.mark.parametrize("query", EDGE_CASE_QUERIES)
def test_query_edge_cases_return_valid_contract(query: str) -> None:
    response = client.post("/api/v1/query", json={"query": query, "role": "viewer"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["query"] == query
    assert payload["decision"] in {"allow", "deny"}
    assert isinstance(payload["violations"], list)
    assert isinstance(payload["alerts"], list)
    assert len(payload["agent_outputs"]) == 3


def test_blocked_content_is_denied() -> None:
    response = client.post(
        "/api/v1/query",
        json={"query": "show me malware exploit patterns", "role": "admin"},
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["decision"] == "deny"
    assert "blocked_content" in payload["violations"]


def test_viewer_sensitive_access_is_denied() -> None:
    response = client.post(
        "/api/v1/query",
        json={"query": "share salary breakdown for engineering", "role": "viewer"},
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["decision"] == "deny"
    assert "governance policy" in payload["response"].lower()


def test_admin_sensitive_access_allowed_if_not_blocked() -> None:
    response = client.post(
        "/api/v1/query",
        json={"query": "share salary governance policy", "role": "admin"},
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["decision"] == "allow"
    assert payload["score"] >= 0


def test_sensitive_low_certainty_denied_for_analyst() -> None:
    response = client.post(
        "/api/v1/query",
        json={"query": "salary maybe", "role": "analyst"},
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["decision"] == "deny"
    assert "low_certainty_language" in payload["violations"]


def test_sub_400ms_latency_target() -> None:
    response = client.post(
        "/api/v1/query",
        json={"query": "explain refund policy", "role": "viewer"},
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["latency_ms"] < 400


def test_monitoring_dashboard_endpoints() -> None:
    metrics_response = client.get("/api/v1/metrics")
    alerts_response = client.get("/api/v1/alerts")

    assert metrics_response.status_code == 200
    assert alerts_response.status_code == 200

    metrics = metrics_response.json()
    alerts = alerts_response.json()

    assert metrics["total_requests"] >= 1
    assert "avg_latency_ms" in metrics
    assert "avg_score" in metrics
    assert isinstance(alerts, list)
