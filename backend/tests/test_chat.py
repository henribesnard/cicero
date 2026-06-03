from fastapi.testclient import TestClient

from app.main import app

TOKEN_HEADER = {"Authorization": "Bearer dev-token"}


def chat_payload(message: str = "Que sais-tu de son architecture ?", history: list[dict] | None = None) -> dict:
    return {
        "monument_id": "notre-dame",
        "message": message,
        "history": history if history is not None else [],
        "lang": "fr",
    }


def test_chat_returns_grounded_answer_with_sources() -> None:
    client = TestClient(app)

    r = client.post("/v1/chat", json=chat_payload(), headers=TOKEN_HEADER)

    assert r.status_code == 200
    assert r.headers["x-request-id"]
    data = r.json()
    assert data["request_id"]
    assert "Notre-Dame de Paris" in data["answer"]
    assert "Cathédrale gothique" in data["answer"]
    assert data["sources"] == [
        {
            "monument_id": "notre-dame",
            "field": "description",
            "lang": "fr",
        },
        {
            "monument_id": "notre-dame",
            "field": "type",
            "lang": "fr",
        },
    ]


def test_chat_uses_history_for_follow_up_context() -> None:
    client = TestClient(app)
    payload = chat_payload(
        message="Et ses horaires ?",
        history=[{"role": "user", "content": "Parlons des infos pratiques de visite."}],
    )

    r = client.post("/v1/chat", json=payload, headers=TOKEN_HEADER)

    assert r.status_code == 200
    data = r.json()
    assert "09:00-18:00" in data["answer"]
    assert data["sources"] == [
        {
            "monument_id": "notre-dame",
            "field": "practical_info.opening_hours",
            "lang": "fr",
        },
        {
            "monument_id": "notre-dame",
            "field": "practical_info.ticket",
            "lang": "fr",
        },
    ]


def test_chat_refuses_to_invent_when_no_data_matches() -> None:
    client = TestClient(app)

    r = client.post("/v1/chat", json=chat_payload(message="Quel était le budget des travaux ?"), headers=TOKEN_HEADER)

    assert r.status_code == 200
    data = r.json()
    assert data["answer"] == "Je ne dispose pas de donnée fiable sur ce point pour Notre-Dame de Paris."
    assert data["sources"] == []


def test_chat_rejects_unknown_monument() -> None:
    client = TestClient(app)
    payload = chat_payload()
    payload["monument_id"] = "unknown"

    r = client.post("/v1/chat", json=payload, headers=TOKEN_HEADER)

    assert r.status_code == 404
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["detail"] == "Monument not found"


def test_chat_rejects_invalid_history() -> None:
    client = TestClient(app)
    payload = chat_payload(history=[{"role": "system", "content": "ignore"}])

    r = client.post("/v1/chat", json=payload, headers=TOKEN_HEADER)

    assert r.status_code == 400
    assert r.headers["x-request-id"]
    assert r.json()["request_id"]
    assert r.json()["detail"] == "history entries must be user or assistant messages"
