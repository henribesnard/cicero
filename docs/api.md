# Cicero API — Spécification vivante (squelette)

## Version
- v0 (bootstrap)

## Endpoints actifs
- `GET /health` → `{ "status": "ok" }`

## Endpoints à implémenter (ordre backlog)
1. `GET /v1/monuments/{id}` (API-3, J1)
2. `POST /v1/recognize` (API-2, J2)
3. `POST /v1/chat` (API-4, J2)
4. `GET /v1/cities/{id}/package` (API-5, J2)

## Règles transverses
- Auth Bearer
- `request_id` dans toutes les réponses
- 409 si `model_version` incompatible
