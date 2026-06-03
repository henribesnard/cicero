# Cicero API — Spécification vivante

## Version
- v0.7 (OFF-2 contrat de bundle local hors-ligne)

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
- Stories: API-5 / OFF-1.
- Auth: Bearer requise.
- Le manifeste permet au client d'afficher la taille avant téléchargement et de stocker localement l'index d'empreintes + les fiches.
- Réponse 200:
```json
{
  "request_id": "<uuid>",
  "city_id": "paris",
  "city_name": "Paris",
  "country": "FR",
  "package_version": "2026.06.03-1",
  "model_version": "vision-lite-1.0.0",
  "package_url": "https://static.cicero.local/packages/paris-vision-lite-1.0.0.zip",
  "size_bytes": 24576000,
  "checksum_sha256": "f0b2d67ef13f7e759bba5b0916d2d8f56840db1e46b4e7d0f5d33c6b1f4b43b7",
  "monument_count": 1,
  "generated_at": "2026-06-03T00:00:00Z",
  "components": [
    {
      "kind": "embeddings_index",
      "schema_version": "embeddings-index-v1",
      "path": "index/embeddings.jsonl",
      "size_bytes": 8192000,
      "checksum_sha256": "c580fb7f299af3aa6c1dbe315ab2d609c871d0bde4fe2fc999c7ba5091f8b55f"
    },
    {
      "kind": "monument_cards",
      "schema_version": "monument-cards-v1",
      "path": "content/monuments.fr.json",
      "size_bytes": 16384000,
      "checksum_sha256": "ee67659b3b2d994de528e3ad920fc96f35594d0a8044c2b1075c34eb12f8f9ba"
    }
  ]
}
```
- Erreurs: `404 City package not found`.

## Contrat client hors-ligne OFF-2

Le téléchargement d'un paquet ville produit un bundle local dérivé du manifeste `GET /v1/cities/{id}/package`.
Ce bundle est conçu pour être lu sans réseau par le client mobile.

Structure logique validée par tests:
```json
{
  "city_id": "paris",
  "package_version": "2026.06.03-1",
  "model_version": "vision-lite-1.0.0",
  "lang": "fr",
  "capabilities": {
    "recognition": true,
    "monument_cards": true,
    "chat": false,
    "chat_unavailable_message": "Le chat nécessite une connexion réseau."
  },
  "embeddings_index": [
    {
      "monument_id": "notre-dame",
      "model_version": "vision-lite-1.0.0",
      "embedding": [1.0]
    }
  ],
  "monument_cards": [
    {
      "monument_id": "notre-dame",
      "name": "Notre-Dame de Paris",
      "type": "cathedral",
      "location": { "lat": 48.853, "lng": 2.3499 },
      "year_built": 1163,
      "architect": "Maurice de Sully",
      "description": "Cathédrale gothique emblématique de Paris.",
      "practical_info": { "opening_hours": "09:00-18:00", "ticket": "free" },
      "media": [{ "type": "image", "url": "https://example.com/notre-dame.jpg" }],
      "lang": "fr"
    }
  ]
}
```
> L'exemple abrège `embedding`; le bundle réel conserve 256 dimensions.

Comportements locaux validés:
- reconnaissance depuis `embeddings_index` avec les mêmes statuts que `POST /v1/recognize`: `matched`, `low_confidence`, `not_found`;
- lecture de fiche depuis `monument_cards` sans appel API;
- chat explicitement indisponible hors-ligne via `capabilities.chat=false`.

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
