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
    assert data["city_name"] == "Paris"
    assert data["country"] == "FR"
    assert data["package_version"] == "2026.06.03-1"
    assert data["model_version"] == "vision-lite-1.0.0"
    assert data["package_url"].endswith("/paris-vision-lite-1.0.0.zip")
    assert data["size_bytes"] == 24_576_000
    assert len(data["checksum_sha256"]) == 64
    assert data["monument_count"] == 1
    assert data["generated_at"] == "2026-06-03T00:00:00Z"


def test_get_city_package_lists_offline_components() -> None:
    client = TestClient(app)

    r = client.get("/v1/cities/paris/package", headers=TOKEN_HEADER)

    assert r.status_code == 200
    data = r.json()
    assert data["components"] == [
        {
            "kind": "embeddings_index",
            "schema_version": "embeddings-index-v1",
            "path": "index/embeddings.jsonl",
            "size_bytes": 8_192_000,
            "checksum_sha256": "c580fb7f299af3aa6c1dbe315ab2d609c871d0bde4fe2fc999c7ba5091f8b55f",
        },
        {
            "kind": "monument_cards",
            "schema_version": "monument-cards-v1",
            "path": "content/monuments.fr.json",
            "size_bytes": 16_384_000,
            "checksum_sha256": "ee67659b3b2d994de528e3ad920fc96f35594d0a8044c2b1075c34eb12f8f9ba",
        },
    ]
    assert sum(component["size_bytes"] for component in data["components"]) == data["size_bytes"]


def test_get_city_package_404_contract() -> None:
    client = TestClient(app)

    r = client.get("/v1/cities/unknown/package", headers=TOKEN_HEADER)

    assert r.status_code == 404
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["detail"] == "City package not found"
