from fastapi.testclient import TestClient

from app.main import app


def test_get_monument_200() -> None:
    client = TestClient(app)

    r = client.get("/v1/monuments/notre-dame", params={"lang": "en"})

    assert r.status_code == 200
    assert r.headers["x-request-id"]
    data = r.json()
    assert data["request_id"]
    assert data["monument_id"] == "notre-dame"
    assert data["name"] == "Notre-Dame Cathedral"
    assert data["type"] == "cathedral"
    assert data["location"] == {"lat": 48.853, "lng": 2.3499}
    assert data["year_built"] == 1163
    assert data["architect"] == "Maurice de Sully"
    assert data["description"] == "Iconic Gothic cathedral in Paris."
    assert "opening_hours" in data["practical_info"]
    assert isinstance(data["media"], list)


def test_get_monument_404() -> None:
    client = TestClient(app)

    r = client.get("/v1/monuments/unknown-id")

    assert r.status_code == 404
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["detail"] == "Monument not found"
