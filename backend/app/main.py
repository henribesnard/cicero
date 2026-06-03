import math
import os
import time
from collections import defaultdict, deque
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Cicero API", version="0.1.0")

AUTH_BEARER_TOKEN = os.getenv("CICERO_API_BEARER_TOKEN", "dev-token")
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("CICERO_RATE_LIMIT_MAX_REQUESTS", "30"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("CICERO_RATE_LIMIT_WINDOW_SECONDS", "60"))
SUPPORTED_MODEL_VERSION = "vision-lite-1.0.0"
EMBEDDING_DIMENSION = 256
HIGH_CONFIDENCE_THRESHOLD = 0.80
LOW_CONFIDENCE_THRESHOLD = 0.50
DEFAULT_CONTENT_LANG = "fr"
SUPPORTED_CONTENT_LANGS = ("fr", "en")
_request_windows: dict[str, deque[float]] = defaultdict(deque)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = str(uuid4())
    request.state.request_id = request_id

    if request.url.path.startswith("/v1/"):
        auth_header = request.headers.get("authorization")
        expected_header = f"Bearer {AUTH_BEARER_TOKEN}"
        if auth_header != expected_header:
            return JSONResponse(
                status_code=401,
                content={"request_id": request_id, "detail": "Unauthorized"},
                headers={"X-Request-Id": request_id},
            )

        actor = auth_header
        now = time.time()
        window = _request_windows[actor]
        while window and window[0] <= now - RATE_LIMIT_WINDOW_SECONDS:
            window.popleft()

        if len(window) >= RATE_LIMIT_MAX_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"request_id": request_id, "detail": "Rate limit exceeded"},
                headers={"X-Request-Id": request_id},
            )

        window.append(now)

    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response


@app.exception_handler(HTTPException)
async def http_exception_with_request_id(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"request_id": request.state.request_id, "detail": exc.detail},
        headers={"X-Request-Id": request.state.request_id},
    )


MONUMENTS = {
    "notre-dame": {
        "monument_id": "notre-dame",
        "type": "cathedral",
        "location": {"lat": 48.853, "lng": 2.3499},
        "year_built": 1163,
        "architect": "Maurice de Sully",
        "practical_info": {"opening_hours": "09:00-18:00", "ticket": "free"},
        "media": [{"type": "image", "url": "https://example.com/notre-dame.jpg"}],
        "translations": {
            "fr": {
                "name": "Notre-Dame de Paris",
                "description": "Cathédrale gothique emblématique de Paris.",
            },
            "en": {
                "name": "Notre-Dame Cathedral",
                "description": "Iconic Gothic cathedral in Paris.",
            },
        },
    }
}

REFERENCE_EMBEDDINGS = {
    "notre-dame": [1.0] + [0.0] * (EMBEDDING_DIMENSION - 1),
}

CITY_PACKAGES = {
    "paris": {
        "city_id": "paris",
        "city_name": "Paris",
        "country": "FR",
        "package_version": "2026.06.03-1",
        "model_version": SUPPORTED_MODEL_VERSION,
        "package_url": "https://static.cicero.local/packages/paris-vision-lite-1.0.0.zip",
        "size_bytes": 24_576_000,
        "checksum_sha256": "f0b2d67ef13f7e759bba5b0916d2d8f56840db1e46b4e7d0f5d33c6b1f4b43b7",
        "monument_count": len(MONUMENTS),
        "generated_at": "2026-06-03T00:00:00Z",
        "components": [
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
        ],
    }
}


def _translated_monument(monument: dict, lang: str) -> dict:
    requested_lang = lang.strip().lower()
    translation = monument["translations"].get(requested_lang) or monument["translations"][DEFAULT_CONTENT_LANG]
    effective_lang = requested_lang if requested_lang in monument["translations"] else DEFAULT_CONTENT_LANG
    return {
        "name": translation["name"],
        "description": translation["description"],
        "lang": effective_lang,
        "fallback_lang": None if effective_lang == requested_lang else DEFAULT_CONTENT_LANG,
    }


@app.get("/health")
def health(request: Request) -> dict:
    return {"request_id": request.state.request_id, "status": "ok"}


@app.get("/v1/monuments/{monument_id}")
def get_monument(request: Request, monument_id: str, lang: str = Query(default="fr")) -> dict:
    monument = MONUMENTS.get(monument_id)
    if monument is None:
        raise HTTPException(status_code=404, detail="Monument not found")

    translation = _translated_monument(monument, lang)

    return {
        "request_id": request.state.request_id,
        "monument_id": monument["monument_id"],
        "name": translation["name"],
        "type": monument["type"],
        "location": monument["location"],
        "year_built": monument["year_built"],
        "architect": monument["architect"],
        "description": translation["description"],
        "lang": translation["lang"],
        "fallback_lang": translation["fallback_lang"],
        "available_langs": list(SUPPORTED_CONTENT_LANGS),
        "practical_info": monument["practical_info"],
        "media": monument["media"],
    }


def _validate_chat_payload(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Invalid chat payload")

    monument_id = payload.get("monument_id")
    if not isinstance(monument_id, str) or not monument_id.strip():
        raise HTTPException(status_code=400, detail="monument_id is required")

    message = payload.get("message")
    if not isinstance(message, str) or not message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    history = payload.get("history", [])
    if not isinstance(history, list):
        raise HTTPException(status_code=400, detail="history must be a list")

    for entry in history:
        if not isinstance(entry, dict) or entry.get("role") not in {"user", "assistant"}:
            raise HTTPException(status_code=400, detail="history entries must be user or assistant messages")
        content = entry.get("content")
        if not isinstance(content, str):
            raise HTTPException(status_code=400, detail="history entries must contain text content")

    lang = payload.get("lang", "fr")
    if not isinstance(lang, str) or not lang.strip():
        raise HTTPException(status_code=400, detail="lang must be a non-empty string")

    return payload


def _source(monument_id: str, field: str, lang: str) -> dict:
    return {"monument_id": monument_id, "field": field, "lang": lang}


def _build_grounded_chat_answer(
    monument_id: str, monument: dict, message: str, history: list[dict], lang: str
) -> tuple[str, list[dict]]:
    translated = _translated_monument(monument, lang)
    text = " ".join([entry["content"] for entry in history] + [message]).lower()
    name = translated["name"]
    effective_lang = translated["lang"]

    if any(keyword in text for keyword in ["architecture", "architect", "gothique", "style", "décrire", "decrire"]):
        answer = f"{name} est une {translated['description']} Son type référencé est: {monument['type']}."
        sources = [
            _source(monument_id, "description", effective_lang),
            _source(monument_id, "type", effective_lang),
        ]
        return answer, sources

    if any(keyword in text for keyword in ["visite", "visiter", "horaire", "horaires", "ticket", "billet", "prix", "pratique"]):
        practical_info = monument["practical_info"]
        answer = (
            f"Pour {name}, les horaires référencés sont {practical_info['opening_hours']} "
            f"et l'accès indiqué est: {practical_info['ticket']}."
        )
        sources = [
            _source(monument_id, "practical_info.opening_hours", effective_lang),
            _source(monument_id, "practical_info.ticket", effective_lang),
        ]
        return answer, sources

    if any(keyword in text for keyword in ["date", "construit", "construite", "année", "annee", "quand"]):
        answer = f"La date de construction référencée pour {name} est {monument['year_built']}."
        return answer, [_source(monument_id, "year_built", effective_lang)]

    return f"Je ne dispose pas de donnée fiable sur ce point pour {name}.", []


@app.post("/v1/chat")
async def chat(request: Request) -> dict:
    payload = _validate_chat_payload(await request.json())
    monument_id = payload["monument_id"]
    monument = MONUMENTS.get(monument_id)
    if monument is None:
        raise HTTPException(status_code=404, detail="Monument not found")

    answer, sources = _build_grounded_chat_answer(
        monument_id=monument_id,
        monument=monument,
        message=payload["message"],
        history=payload.get("history", []),
        lang=payload.get("lang", "fr"),
    )
    return {
        "request_id": request.state.request_id,
        "answer": answer,
        "sources": sources,
    }


def _validate_recognize_payload(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Invalid recognize payload")

    embedding = payload.get("embedding")
    model_version = payload.get("model_version")

    if model_version != SUPPORTED_MODEL_VERSION:
        raise HTTPException(status_code=409, detail="Incompatible model_version")

    if not isinstance(embedding, list) or len(embedding) != EMBEDDING_DIMENSION:
        raise HTTPException(status_code=400, detail="embedding must contain 256 numbers")

    if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in embedding):
        raise HTTPException(status_code=400, detail="embedding must contain only numbers")

    location = payload.get("location")
    if not isinstance(location, dict):
        raise HTTPException(status_code=400, detail="location is required")

    lat = location.get("lat")
    lng = location.get("lng")
    if (
        not isinstance(lat, (int, float))
        or isinstance(lat, bool)
        or not isinstance(lng, (int, float))
        or isinstance(lng, bool)
    ):
        raise HTTPException(status_code=400, detail="location.lat and location.lng must be numbers")

    heading_deg = payload.get("heading_deg")
    if not isinstance(heading_deg, (int, float)) or isinstance(heading_deg, bool) or not 0 <= heading_deg <= 360:
        raise HTTPException(status_code=400, detail="heading_deg must be between 0 and 360")

    radius_m = payload.get("radius_m", 300)
    if not isinstance(radius_m, (int, float)) or isinstance(radius_m, bool) or radius_m <= 0:
        raise HTTPException(status_code=400, detail="radius_m must be positive")

    return payload


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (norm_a * norm_b)))


@app.post("/v1/recognize")
async def recognize(request: Request) -> dict:
    payload = _validate_recognize_payload(await request.json())
    embedding = payload["embedding"]

    scored_matches = []
    for monument_id, reference_embedding in REFERENCE_EMBEDDINGS.items():
        confidence = _cosine_similarity(embedding, reference_embedding)
        if confidence >= LOW_CONFIDENCE_THRESHOLD:
            monument = MONUMENTS[monument_id]
            translation = monument["translations"]["fr"]
            scored_matches.append(
                {
                    "monument_id": monument_id,
                    "name": translation["name"],
                    "confidence": round(confidence, 4),
                }
            )

    scored_matches.sort(key=lambda match: match["confidence"], reverse=True)

    if not scored_matches:
        status = "not_found"
    elif scored_matches[0]["confidence"] >= HIGH_CONFIDENCE_THRESHOLD:
        status = "matched"
    else:
        status = "low_confidence"

    return {
        "request_id": request.state.request_id,
        "matches": scored_matches,
        "status": status,
    }


@app.get("/v1/cities/{city_id}/package")
def get_city_package(request: Request, city_id: str) -> dict:
    package = CITY_PACKAGES.get(city_id)
    if package is None:
        raise HTTPException(status_code=404, detail="City package not found")

    return {
        "request_id": request.state.request_id,
        **package,
    }
