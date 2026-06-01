# Cicero API — Spécification vivante (squelette)

## Version
- v0.2 (incrément API-1 partiel: `request_id`)

## Endpoints actifs
- `GET /health` → `{ "request_id": "<uuid>", "status": "ok" }` + header `X-Request-Id`
- `GET /v1/monuments/{id}` → fiche monument + `request_id` + header `X-Request-Id`

## Gestion d'erreurs
- Les erreurs HTTP applicatives renvoient maintenant:
  - `request_id`
  - `detail`

Exemple 404:

```json
{
  "request_id": "f8fdb62b-8d78-4d2d-9f3a-9fb76f01c1f4",
  "detail": "Monument not found"
}
```

## Endpoints à implémenter (ordre backlog)
1. `POST /v1/recognize` (API-2, J2)
2. `POST /v1/chat` (API-4, J2)
3. `GET /v1/cities/{id}/package` (API-5, J2)

## Règles transverses
- Auth Bearer
- `request_id` dans toutes les réponses
- 409 si `model_version` incompatible

## Statut des règles transverses
- Auth Bearer: non implémenté
- `request_id` dans les endpoints actifs: implémenté
- 409 `model_version` incompatible: non implémenté
