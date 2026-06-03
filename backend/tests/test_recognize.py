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
            "distance_m": 0.0,
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


def test_recognize_filters_candidates_outside_requested_radius() -> None:
    HARD_CASE_LOGGER.clear()
    client = TestClient(app)
    payload = recognize_payload()
    payload["location"] = {"lat": 48.8584, "lng": 2.2945, "accuracy_m": 8}  # Eiffel Tower area
    payload["radius_m"] = 300

    r = client.post("/v1/recognize", json=payload, headers=TOKEN_HEADER)

    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "not_found"
    assert data["matches"] == []
    assert HARD_CASE_LOGGER.list_records()[0]["status"] == "not_found"


def test_hard_cases_export_endpoint_returns_privacy_safe_review_queue() -> None:
    HARD_CASE_LOGGER.clear()
    client = TestClient(app)
    low_confidence_embedding = [0.6, 0.8] + [0.0] * 254
    not_found_embedding = [0.0, 1.0] + [0.0] * 254

    client.post("/v1/recognize", json=recognize_payload(embedding=low_confidence_embedding), headers=TOKEN_HEADER)
    client.post("/v1/recognize", json=recognize_payload(embedding=not_found_embedding), headers=TOKEN_HEADER)
    r = client.get("/v1/hard-cases/export", headers=TOKEN_HEADER)

    assert r.status_code == 200
    assert r.headers["x-request-id"]
    data = r.json()
    assert data["request_id"]
    assert data["schema_version"] == "hard-cases-v1"
    assert data["record_count"] == 2
    assert data["counts_by_status"] == {"low_confidence": 1, "not_found": 1}
    assert data["privacy"] == {
        "stores_raw_image": False,
        "stores_raw_embedding": False,
        "stores_precise_location": False,
    }
    assert [record["status"] for record in data["records"]] == ["low_confidence", "not_found"]
    assert [record["status"] for record in data["review_queue"]] == ["not_found", "low_confidence"]


def test_hard_case_feedback_endpoint_annotates_existing_scan() -> None:
    HARD_CASE_LOGGER.clear()
    client = TestClient(app)
    low_confidence_embedding = [0.6, 0.8] + [0.0] * 254

    scan = client.post("/v1/recognize", json=recognize_payload(embedding=low_confidence_embedding), headers=TOKEN_HEADER)
    scan_id = scan.json()["request_id"]
    r = client.post(
        f"/v1/hard-cases/{scan_id}/feedback",
        json={"user_feedback": "wrong_monument", "notes": "confusion façade latérale"},
        headers=TOKEN_HEADER,
    )

    assert r.status_code == 200
    assert r.headers["x-request-id"]
    data = r.json()
    assert data["request_id"]
    assert data["record"]["scan_id"] == scan_id
    assert data["record"]["user_feedback"] == "wrong_monument"
    assert data["record"]["notes"] == "confusion façade latérale"
    assert HARD_CASE_LOGGER.export_retraining_batch()["counts_by_feedback"]["wrong_monument"] == 1


def test_hard_case_feedback_endpoint_rejects_missing_scan_and_invalid_payload() -> None:
    HARD_CASE_LOGGER.clear()
    client = TestClient(app)

    missing = client.post(
        "/v1/hard-cases/scan-missing/feedback",
        json={"user_feedback": "unknown"},
        headers=TOKEN_HEADER,
    )
    invalid = client.post(
        "/v1/hard-cases/scan-missing/feedback",
        json={"user_feedback": "invalid-label"},
        headers=TOKEN_HEADER,
    )

    assert missing.status_code == 404
    assert missing.json()["detail"] == "Hard case not found"
    assert invalid.status_code == 400
    assert invalid.json()["detail"] == "user_feedback is not an allowed label"


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
