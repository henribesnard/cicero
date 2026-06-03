# Cicero API — Spécification vivante

## Version
- v0.5 (API-4 `POST /v1/chat` RAG minimal sourcé)

## Règles transverses
- `GET /health` est public.
- Tous les endpoints `/v1/*` exigent un header `Authorization` avec un jeton Bearer.
  - Token local de développement: variable `CICERO_API_BEARER_TOKEN`, fallback `dev-token`.
- Rate limiting sur `/v1/*`:
  - `CICERO_RATE_LIMIT_WINDOW_SECONDS` (défaut `60`)
  - `CICERO_RATE_LIMIT_MAX_REQUESTS` (défaut `30`)
- Chaque réponse contient `request_id` et le header `X-Request-Id`.
- Les erreurs applicatives renvoient `{ "request_id": "<uuid>", "detail": "..." }`.

## Endpoints actifs

### `GET /health`
- Auth: non requise.
- Réponse 200:
```json
{
  "request_id": "<uuid>",
  "status": "ok"
}
```

### `GET /v1/monuments/{id}?lang=<code>`
- Auth: Bearer requise.
- Réponse 200: fiche monument complète.
```json
{
  "request_id": "<uuid>",
  "monument_id": "notre-dame",
  "name": "Notre-Dame de Paris",
  "type": "cathedral",
  "location": { "lat": 48.853, "lng": 2.3499 },
  "year_built": 1163,
  "architect": "Maurice de Sully",
  "description": "Cathédrale gothique emblématique de Paris.",
  "practical_info": { "opening_hours": "09:00-18:00", "ticket": "free" },
  "media": [{ "type": "image", "url": "https://example.com/notre-dame.jpg" }]
}
```
- Erreurs: `404 Monument not found`.

### `POST /v1/recognize`
- Story: API-2.
- Auth: Bearer requise.
- Modèle supporté: `vision-lite-1.0.0`.
- Dimension d'empreinte: `256`.
- Seuils actuels:
  - `matched`: meilleur score `>= 0.80`
  - `low_confidence`: meilleur score `>= 0.50` et `< 0.80`
  - `not_found`: aucun match `>= 0.50`
- Requête:
```json
{
  "embedding": [1.0, 0.0],
  "model_version": "vision-lite-1.0.0",
  "location": { "lat": 48.853, "lng": 2.3499, "accuracy_m": 8 },
  "heading_deg": 215,
  "radius_m": 300
}
```
> `embedding` doit contenir exactement 256 nombres; l'exemple ci-dessus est abrégé.
- Réponse 200:
```json
{
  "request_id": "<uuid>",
  "status": "matched",
  "matches": [
    {
      "monument_id": "notre-dame",
      "name": "Notre-Dame de Paris",
      "confidence": 1.0
    }
  ]
}
```
- Erreurs:
  - `400` payload/embedding/localisation/cap invalides.
  - `409 Incompatible model_version` si la version modèle n'est pas supportée.

### `GET /v1/cities/{id}/package`
- Story: API-5.
- Auth: Bearer requise.
- Réponse 200:
```json
{
  "request_id": "<uuid>",
  "city_id": "paris",
  "model_version": "vision-lite-1.0.0",
  "package_url": "https://static.cicero.local/packages/paris-vision-lite-1.0.0.zip",
  "size_bytes": 24576000,
  "checksum_sha256": "local-dev-placeholder",
  "monument_count": 1
}
```
- Erreurs: `404 City package not found`.

### `POST /v1/chat`
- Stories: API-4 / IA-1.
- Auth: Bearer requise.
- Implémentation actuelle: RAG déterministe minimal sur la fiche KB locale, sans appel LLM externe.
- Comportement garanti:
  - réponse fondée sur les champs récupérés du monument;
  - `sources` liste les champs utilisés;
  - si aucune donnée fiable ne correspond à la question, l'assistant le dit et renvoie `sources: []`.
- Requête:
```json
{
  "monument_id": "notre-dame",
  "message": "Que sais-tu de son architecture ?",
  "history": [
    { "role": "user", "content": "Parlons de la visite." },
    { "role": "assistant", "content": "..." }
  ],
  "lang": "fr"
}
```
- Réponse 200:
```json
{
  "request_id": "<uuid>",
  "answer": "Notre-Dame de Paris est une Cathédrale gothique emblématique de Paris. Son type référencé est: cathedral.",
  "sources": [
    { "monument_id": "notre-dame", "field": "description", "lang": "fr" },
    { "monument_id": "notre-dame", "field": "type", "lang": "fr" }
  ]
}
```
- Erreurs:
  - `400` payload/message/historique/lang invalides.
  - `404 Monument not found`.

## Endpoints à implémenter (ordre backlog)
- Aucun endpoint J2 restant avant intégration produit hors-ligne; enrichissements à venir: streaming réel et backend RAG/LLM externe pour API-4.
