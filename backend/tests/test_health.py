from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["status"] == "ok"
