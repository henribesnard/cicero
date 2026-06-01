from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Cicero API", version="0.1.0")


MONUMENTS = {
    "notre-dame": {
        "monument_id": "notre-dame",
        "type": "cathedral",
        "location": {"lat": 48.853, "lng": 2.3499},
        "year_built": 1163,
        "architect": "Maurice de Sully",
        "practical_info": {
            "opening_hours": "09:00-18:00",
            "ticket": "free"
        },
        "media": [
            {
                "type": "image",
                "url": "https://example.com/notre-dame.jpg"
            }
        ],
        "translations": {
            "fr": {
                "name": "Notre-Dame de Paris",
                "description": "Cathédrale gothique emblématique de Paris."
            },
            "en": {
                "name": "Notre-Dame Cathedral",
                "description": "Iconic Gothic cathedral in Paris."
            },
        },
    }
}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/v1/monuments/{monument_id}")
def get_monument(monument_id: str, lang: str = Query(default="fr")) -> dict:
    monument = MONUMENTS.get(monument_id)
    if monument is None:
        raise HTTPException(status_code=404, detail="Monument not found")

    translation = monument["translations"].get(lang) or monument["translations"]["fr"]

    return {
        "request_id": str(uuid4()),
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
