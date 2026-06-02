# Tests — J4 API-2 Recognize + API-5 City package

## Portée
- `POST /v1/recognize`
- `GET /v1/cities/{id}/package`
- Règles transverses conservées: Auth Bearer, rate limiting, `request_id`

## Commande
- `pytest -q`

## Résultat
- `14 passed in 0.91s`

## Cas couverts ajoutés
- Reconnaissance `matched` avec score de confiance exposé.
- Reconnaissance `low_confidence` entre seuil bas et seuil haut.
- Reconnaissance `not_found` sous seuil bas.
- Rejet `409` d'un `model_version` incompatible.
- Rejet `400` d'une empreinte invalide.
- Contrat paquet ville `GET /v1/cities/paris/package` (URL + taille + version modèle + checksum placeholder).
- Erreur `404` si paquet de ville inconnu.
