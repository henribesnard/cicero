from fastapi.testclient import TestClient

from app import main
from app.main import app


TOKEN_HEADER = {"Authorization": "Bearer dev-token"}


def setup_function() -> None:
    main._request_windows.clear()


def test_v1_requires_bearer_token() -> None:
    client = TestClient(app)

    r = client.get("/v1/monuments/notre-dame")

    assert r.status_code == 401
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["detail"] == "Unauthorized"


def test_health_does_not_require_auth() -> None:
    client = TestClient(app)

    r = client.get("/health")

    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_v1_rate_limit_exceeded_returns_429() -> None:
    client = TestClient(app)

    original_limit = main.RATE_LIMIT_MAX_REQUESTS
    original_window = main.RATE_LIMIT_WINDOW_SECONDS
    main.RATE_LIMIT_MAX_REQUESTS = 2
    main.RATE_LIMIT_WINDOW_SECONDS = 60

    try:
        r1 = client.get("/v1/monuments/notre-dame", headers=TOKEN_HEADER)
        r2 = client.get("/v1/monuments/notre-dame", headers=TOKEN_HEADER)
        r3 = client.get("/v1/monuments/notre-dame", headers=TOKEN_HEADER)
    finally:
        main.RATE_LIMIT_MAX_REQUESTS = original_limit
        main.RATE_LIMIT_WINDOW_SECONDS = original_window

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 429
    assert r3.headers["x-request-id"]
    assert r3.json()["request_id"]
    assert r3.json()["detail"] == "Rate limit exceeded"
