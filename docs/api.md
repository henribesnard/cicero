# Cicero API — Spécification vivante

## Version
- v0.3 (API-1 complétée sur endpoints actifs: `request_id` + Auth Bearer + rate limiting)

## Endpoints actifs
- `GET /health`
  - Réponse: `{ "request_id": "<uuid>", "status": "ok" }`
  - Header: `X-Request-Id`
  - Auth: non requise (sonde technique)

- `GET /v1/monuments/{id}?lang=<code>`
  - Réponse 200: fiche monument + `request_id`
  - Header: `X-Request-Id`
  - Auth: **Bearer requise**

## Gestion d'erreurs
Toutes les erreurs applicatives renvoient:
- `request_id`
- `detail`
- header `X-Request-Id`

Exemple 401:
```json
{
  "request_id": "f8fdb62b-8d78-4d2d-9f3a-9fb76f01c1f4",
  "detail": "Unauthorized"
}
```

Exemple 429:
```json
{
  "request_id": "a7a1f758-4ac1-4313-97e5-10ef5f58b618",
  "detail": "Rate limit exceeded"
}
```

## Règles transverses
- Auth Bearer: header `Authorization: Bearer <token>`
  - Token actuel: via variable d'environnement `CICERO_API_BEARER_TOKEN` (fallback dev local: `dev-token`)
- Rate limiting (endpoints `/v1/*`):
  - Fenêtre: `CICERO_RATE_LIMIT_WINDOW_SECONDS` (défaut `60`)
  - Max requêtes: `CICERO_RATE_LIMIT_MAX_REQUESTS` (défaut `30`)
- `request_id` dans toutes les réponses des endpoints actifs
- 409 si `model_version` incompatible: non implémenté (porté par API-2)

## Endpoints à implémenter (ordre backlog)
1. `POST /v1/recognize` (API-2, J2)
2. `POST /v1/chat` (API-4, J2)
3. `GET /v1/cities/{id}/package` (API-5, J2)
