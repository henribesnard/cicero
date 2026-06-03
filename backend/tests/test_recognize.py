from fastapi.testclient import TestClient

from app.main import HARD_CASE_LOGGER, app


TOKEN_HEADER = {"Authorization": "Bearer dev-token"}


def recognize_payload(embedding: list[float] | None = None, model_version: str = "vision-lite-1.0.0") -> dict:
    return {
        "embedding": embedding if embedding is not None else [1.0] + [0.0] * 255,
        "model_version": model_version,
        "location": {"lat": 48.853, "lng": 2.3499, "accuracy_m": 8},
        "heading_deg": 215,
        "radius_m": 300,
        "city_id": "paris",
    }


def test_recognize_matched_contract() -> None:
    HARD_CASE_LOGGER.clear()
    client = TestClient(app)

    r = client.post("/v1/recognize", json=recognize_payload(), headers=TOKEN_HEADER)

    assert r.status_code == 200
    assert r.headers["x-request-id"]
    data = r.json()
    assert data["request_id"]
    assert data["status"] == "matched"
    assert data["matches"] == [
        {
            "monument_id": "notre-dame",
            "name": "Notre-Dame de Paris",
            "confidence": 1.0,
        }
    ]
    assert HARD_CASE_LOGGER.list_records() == []


def test_recognize_low_confidence_contract() -> None:
    HARD_CASE_LOGGER.clear()
    client = TestClient(app)
    embedding = [0.6, 0.8] + [0.0] * 254

    r = client.post("/v1/recognize", json=recognize_payload(embedding=embedding), headers=TOKEN_HEADER)

    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "low_confidence"
    assert data["matches"][0]["confidence"] == 0.6
    hard_cases = HARD_CASE_LOGGER.list_records()
    assert len(hard_cases) == 1
    assert hard_cases[0]["scan_id"] == data["request_id"]
    assert hard_cases[0]["status"] == "low_confidence"
    assert hard_cases[0]["score"] == 0.6
    assert hard_cases[0]["model_version"] == "vision-lite-1.0.0"
    assert hard_cases[0]["city_id"] == "paris"
    assert hard_cases[0]["candidate_monument_id"] == "notre-dame"


def test_recognize_not_found_contract() -> None:
    HARD_CASE_LOGGER.clear()
    client = TestClient(app)
    embedding = [0.0, 1.0] + [0.0] * 254

    r = client.post("/v1/recognize", json=recognize_payload(embedding=embedding), headers=TOKEN_HEADER)

    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "not_found"
    assert data["matches"] == []
    hard_cases = HARD_CASE_LOGGER.list_records()
    assert len(hard_cases) == 1
    assert hard_cases[0]["scan_id"] == data["request_id"]
    assert hard_cases[0]["status"] == "not_found"
    assert hard_cases[0]["score"] == 0.0
    assert hard_cases[0]["city_id"] == "paris"
    assert hard_cases[0]["candidate_monument_id"] is None


def test_recognize_rejects_incompatible_model_version_with_409() -> None:
    client = TestClient(app)

    r = client.post(
        "/v1/recognize",
        json=recognize_payload(model_version="vision-lite-2.0.0"),
        headers=TOKEN_HEADER,
    )

    assert r.status_code == 409
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["detail"] == "Incompatible model_version"


def test_recognize_rejects_invalid_embedding_with_400() -> None:
    client = TestClient(app)

    r = client.post("/v1/recognize", json=recognize_payload(embedding=[1.0, 0.0]), headers=TOKEN_HEADER)

    assert r.status_code == 400
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["detail"] == "embedding must contain 256 numbers"


def test_recognize_rejects_empty_city_id_with_400() -> None:
    client = TestClient(app)
    payload = recognize_payload()
    payload["city_id"] = "   "

    r = client.post("/v1/recognize", json=payload, headers=TOKEN_HEADER)

    assert r.status_code == 400
    assert r.json()["detail"] == "city_id must be a non-empty string when provided"
