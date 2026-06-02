from fastapi.testclient import TestClient

from app.main import app


TOKEN_HEADER = {"Authorization": "Bearer dev-token"}


def test_get_city_package_contract() -> None:
    client = TestClient(app)

    r = client.get("/v1/cities/paris/package", headers=TOKEN_HEADER)

    assert r.status_code == 200
    assert r.headers["x-request-id"]
    data = r.json()
    assert data["request_id"]
    assert data["city_id"] == "paris"
    assert data["model_version"] == "vision-lite-1.0.0"
    assert data["package_url"].endswith("/paris-vision-lite-1.0.0.zip")
    assert data["size_bytes"] == 24_576_000
    assert data["checksum_sha256"] == "local-dev-placeholder"
    assert data["monument_count"] == 1


def test_get_city_package_404_contract() -> None:
    client = TestClient(app)

    r = client.get("/v1/cities/unknown/package", headers=TOKEN_HEADER)

    assert r.status_code == 404
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["detail"] == "City package not found"
