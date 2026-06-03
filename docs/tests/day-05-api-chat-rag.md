# Tests — J5 API-4 Chat RAG minimal

## Portée
- `POST /v1/chat`
- Règles transverses conservées: Auth Bearer, rate limiting, `request_id`

## Commande
- `pytest -q`

## Résultat
- `19 passed in 1.83s`

## Cas couverts ajoutés
- Réponse RAG fondée sur la fiche monument avec `sources` explicites.
- Prise en compte de l'historique pour une question de suivi.
- Refus d'inventer quand aucune donnée fiable ne correspond à la question (`sources: []`).
- Erreur `404` si monument inconnu.
- Erreur `400` si l'historique contient un rôle invalide.
