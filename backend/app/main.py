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


@app.get("/health")
def health(request: Request) -> dict:
    return {"request_id": request.state.request_id, "status": "ok"}


@app.get("/v1/monuments/{monument_id}")
def get_monument(request: Request, monument_id: str, lang: str = Query(default="fr")) -> dict:
    monument = MONUMENTS.get(monument_id)
    if monument is None:
        raise HTTPException(status_code=404, detail="Monument not found")

    translation = monument["translations"].get(lang) or monument["translations"]["fr"]

    return {
        "request_id": request.state.request_id,
        "monument_id": monument["monument_id"],
        "name": translation["name"],
        "type": monument["type"],
        "location": monument["location"],
        "year_built": monument["year_built"],
        "architect": monument["architect"],
        "description": translation["description"],
        "practical_info": monument["practical_info"],
        "media": monument["media"],
    }
