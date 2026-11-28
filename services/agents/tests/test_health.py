from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

client = TestClient(app)


def test_health_reports_ok() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert res.json()["service"] == "agents"


def test_health_never_exposes_service_token(monkeypatch) -> None:
    monkeypatch.setenv("AGENTS_SERVICE_TOKEN", "super-secret-value")
    get_settings.cache_clear()
    try:
        assert "super-secret-value" not in client.get("/health").text
    finally:
        get_settings.cache_clear()
