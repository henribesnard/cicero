import pytest

from app.offline import build_offline_bundle, get_offline_monument, recognize_offline


def test_build_offline_bundle_contains_local_recognition_and_cards() -> None:
    bundle = build_offline_bundle("paris", lang="fr")

    assert bundle["city_id"] == "paris"
    assert bundle["package_version"] == "2026.06.03-1"
    assert bundle["model_version"] == "vision-lite-1.0.0"
    assert bundle["capabilities"] == {
        "recognition": True,
        "monument_cards": True,
        "chat": False,
        "chat_unavailable_message": "Le chat nécessite une connexion réseau.",
    }
    assert bundle["embeddings_index"] == [
        {
            "monument_id": "notre-dame",
            "model_version": "vision-lite-1.0.0",
            "embedding": [1.0] + [0.0] * 255,
        }
    ]
    assert bundle["monument_cards"][0]["monument_id"] == "notre-dame"
    assert bundle["monument_cards"][0]["name"] == "Notre-Dame de Paris"
    assert bundle["monument_cards"][0]["description"] == "Cathédrale gothique emblématique de Paris."


def test_build_offline_bundle_respects_language_and_fallback() -> None:
    english = build_offline_bundle("paris", lang="en")
    fallback = build_offline_bundle("paris", lang="es")

    assert english["monument_cards"][0]["name"] == "Notre-Dame Cathedral"
    assert english["monument_cards"][0]["description"] == "Iconic Gothic cathedral in Paris."
    assert english["monument_cards"][0]["lang"] == "en"
    assert english["monument_cards"][0]["fallback_lang"] is None

    assert fallback["lang"] == "es"
    assert fallback["monument_cards"][0]["name"] == "Notre-Dame de Paris"
    assert fallback["monument_cards"][0]["lang"] == "fr"
    assert fallback["monument_cards"][0]["fallback_lang"] == "fr"


def test_offline_recognition_and_card_read_work_without_api_client() -> None:
    bundle = build_offline_bundle("paris")

    recognition = recognize_offline(bundle, [1.0] + [0.0] * 255)
    card = get_offline_monument(bundle, recognition["matches"][0]["monument_id"])

    assert recognition == {
        "status": "matched",
        "matches": [
            {
                "monument_id": "notre-dame",
                "name": "Notre-Dame de Paris",
                "confidence": 1.0,
            }
        ],
    }
    assert card["name"] == "Notre-Dame de Paris"
    assert card["practical_info"]["opening_hours"] == "09:00-18:00"


def test_offline_recognition_exposes_low_confidence_and_not_found_states() -> None:
    bundle = build_offline_bundle("paris")

    low_confidence = recognize_offline(bundle, [0.6, 0.8] + [0.0] * 254)
    not_found = recognize_offline(bundle, [0.0, 1.0] + [0.0] * 254)

    assert low_confidence["status"] == "low_confidence"
    assert low_confidence["matches"][0]["confidence"] == 0.6
    assert not_found == {"status": "not_found", "matches": []}


def test_offline_bundle_unknown_city_and_invalid_embedding_are_rejected() -> None:
    with pytest.raises(KeyError, match="City package not found"):
        build_offline_bundle("unknown")

    with pytest.raises(ValueError, match="embedding must contain 256 numbers"):
        recognize_offline(build_offline_bundle("paris"), [1.0, 0.0])
