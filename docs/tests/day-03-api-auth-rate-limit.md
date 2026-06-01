# Tests — J3 API-1 Auth + rate limiting

## Portée
- `GET /health`
- `GET /v1/monuments/{id}`
- Règles transverses API-1: `request_id`, Auth Bearer, limitation de débit

## Commande
- `pytest -q`

## Résultat
- `7 passed in 0.78s`

## Cas couverts ajoutés
- Refus 401 sans header `Authorization` sur endpoint `/v1/*`
- Endpoint `/health` accessible sans auth
- Refus 429 lorsque le quota de requêtes est dépassé
- Présence de `X-Request-Id` et `request_id` sur erreurs 401/429
