# Tests — Day 02 — API request_id

## Portée
- Backend FastAPI
- Incrément API-1 (partiel): propagation `request_id` via middleware + header `X-Request-Id`
- Réponses d'erreur HTTP enrichies avec `request_id`

## Commande exécutée
```bash
pytest -q
```

## Résultat exact
```text
....                                                                     [100%]
4 passed in 0.91s
```

## Couverture fonctionnelle vérifiée
- `GET /health` retourne `request_id` + header `X-Request-Id`
- `GET /v1/monuments/{id}` retourne `request_id` + header `X-Request-Id`
- `GET /v1/monuments/{id}` (404) retourne `request_id` + `detail`
