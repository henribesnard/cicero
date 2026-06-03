import math
from copy import deepcopy
from typing import Any

from app.main import (
    CITY_PACKAGES,
    EMBEDDING_DIMENSION,
    HIGH_CONFIDENCE_THRESHOLD,
    LOW_CONFIDENCE_THRESHOLD,
    MONUMENTS,
    REFERENCE_EMBEDDINGS,
    SUPPORTED_MODEL_VERSION,
)


def build_offline_bundle(city_id: str, lang: str = "fr") -> dict[str, Any]:
    """Build the deterministic local payload a mobile client stores after downloading a city.

    This is the OFF-2 contract foundation: recognition and monument cards can be read
    from the bundle without calling the API, while chat is explicitly marked as online-only.
    """
    package = CITY_PACKAGES.get(city_id)
    if package is None:
        raise KeyError("City package not found")

    cards = []
    embeddings = []
    for monument_id, monument in MONUMENTS.items():
        translation = monument["translations"].get(lang) or monument["translations"]["fr"]
        effective_lang = lang if lang in monument["translations"] else "fr"
        cards.append(
            {
                "monument_id": monument_id,
                "name": translation["name"],
                "type": monument["type"],
                "location": deepcopy(monument["location"]),
                "year_built": monument["year_built"],
                "architect": monument["architect"],
                "description": translation["description"],
                "practical_info": deepcopy(monument["practical_info"]),
                "media": deepcopy(monument["media"]),
                "lang": effective_lang,
            }
        )
        embeddings.append(
            {
                "monument_id": monument_id,
                "model_version": SUPPORTED_MODEL_VERSION,
                "embedding": list(REFERENCE_EMBEDDINGS[monument_id]),
            }
        )

    return {
        "city_id": package["city_id"],
        "package_version": package["package_version"],
        "model_version": SUPPORTED_MODEL_VERSION,
        "lang": lang,
        "capabilities": {
            "recognition": True,
            "monument_cards": True,
            "chat": False,
            "chat_unavailable_message": "Le chat nécessite une connexion réseau.",
        },
        "embeddings_index": embeddings,
        "monument_cards": cards,
    }


def get_offline_monument(bundle: dict[str, Any], monument_id: str) -> dict[str, Any]:
    for card in bundle.get("monument_cards", []):
        if card.get("monument_id") == monument_id:
            return deepcopy(card)
    raise KeyError("Monument not found in offline bundle")


def recognize_offline(bundle: dict[str, Any], embedding: list[float]) -> dict[str, Any]:
    if bundle.get("model_version") != SUPPORTED_MODEL_VERSION:
        raise ValueError("Incompatible model_version")
    if not isinstance(embedding, list) or len(embedding) != EMBEDDING_DIMENSION:
        raise ValueError("embedding must contain 256 numbers")
    if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in embedding):
        raise ValueError("embedding must contain only numbers")

    cards_by_id = {card["monument_id"]: card for card in bundle.get("monument_cards", [])}
    matches = []
    for reference in bundle.get("embeddings_index", []):
        confidence = _cosine_similarity(embedding, reference["embedding"])
        if confidence >= LOW_CONFIDENCE_THRESHOLD:
            card = cards_by_id[reference["monument_id"]]
            matches.append(
                {
                    "monument_id": reference["monument_id"],
                    "name": card["name"],
                    "confidence": round(confidence, 4),
                }
            )

    matches.sort(key=lambda match: match["confidence"], reverse=True)
    if not matches:
        status = "not_found"
    elif matches[0]["confidence"] >= HIGH_CONFIDENCE_THRESHOLD:
        status = "matched"
    else:
        status = "low_confidence"

    return {"status": status, "matches": matches}


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (norm_a * norm_b)))
