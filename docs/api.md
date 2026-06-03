# Cicero API — Spécification vivante

## Version
- v1.0 (ML-4 hard-cases feedback + persistance JSONL optionnelle)

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
- Réponse 200: fiche monument complète dans la langue demandée si disponible.
- Langues de contenu supportées actuellement: `fr`, `en`.
- Fallback: si `lang` n'est pas disponible, la fiche est renvoyée en `fr` avec `fallback_lang: "fr"`.
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
  "lang": "fr",
  "fallback_lang": null,
  "available_langs": ["fr", "en"],
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
  - `not_found`: aucun match `>= 0.50`, ou aucun candidat dans `radius_m`
- Entonnoir géographique REC-3: les candidats sont préfiltrés par distance haversine entre `location` et la position du monument; `distance_m` est retourné pour chaque match.
- Requête:
```json
{
  "embedding": [1.0, 0.0],
  "model_version": "vision-lite-1.0.0",
  "location": { "lat": 48.853, "lng": 2.3499, "accuracy_m": 8 },
  "heading_deg": 215,
  "radius_m": 300,
  "city_id": "paris"
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
      "confidence": 1.0,
      "distance_m": 0.0
    }
  ]
}
```
- `city_id` est optionnel mais, s'il est fourni, il doit être non vide; il sert uniquement à la journalisation agrégée des cas difficiles.
- Journalisation ML-4: les réponses `low_confidence` et `not_found` sont ajoutées à une file locale `hard-cases-v1` avec `request_id`, statut, score, `model_version`, `city_id` optionnel et candidat éventuel. Aucune image, embedding brut ni position précise n'est stocké.
- Persistance ML-4 optionnelle: si `CICERO_HARD_CASES_JSONL_PATH` est défini, la file `hard-cases-v1` est rechargée au démarrage et réécrite en JSONL après chaque ajout, annotation ou purge; par défaut elle reste volatile en mémoire pour le MVP.
- Erreurs:
  - `400` payload/embedding/localisation/cap invalides.
  - `409 Incompatible model_version` si la version modèle n'est pas supportée.

### `GET /v1/hard-cases/export`
- Story: ML-4.
- Auth: Bearer requise.
- Exporte la file locale de cas difficiles pour revue humaine et préparation de réindexation, sans image brute, embedding brut ni position précise.
- Réponse 200:
```json
{
  "request_id": "<uuid>",
  "schema_version": "hard-cases-v1",
  "record_count": 2,
  "counts_by_status": { "low_confidence": 1, "not_found": 1 },
  "counts_by_feedback": { "correct": 0, "other": 0, "poor_angle": 0, "too_dark": 0, "unknown": 0, "wrong_monument": 0 },
  "review_queue": [
    {
      "scan_id": "<request_id>",
      "status": "not_found",
      "score": 0.0,
      "created_at": "2026-06-03T00:00:00Z",
      "model_version": "vision-lite-1.0.0",
      "city_id": "paris",
      "candidate_monument_id": null,
      "user_feedback": null,
      "notes": null,
      "review_priority": 75
    }
  ],
  "privacy": {
    "stores_raw_image": false,
    "stores_raw_embedding": false,
    "stores_precise_location": false
  },
  "records": []
}
```
> `records` contient la file chronologique complète; `review_queue` est triée par priorité de revue.

### `POST /v1/hard-cases/{scan_id}/feedback`
- Story: ML-5.
- Auth: Bearer requise.
- Annote un cas difficile existant avec un retour humain pour prioriser la revue et préparer une réindexation, sans ajouter d'image brute, d'empreinte brute ni de position précise.
- Labels autorisés: `correct`, `wrong_monument`, `unknown`, `poor_angle`, `too_dark`, `other`.
- Requête:
```json
{
  "user_feedback": "wrong_monument",
  "notes": "confusion façade latérale"
}
```
- Réponse 200:
```json
{
  "request_id": "<uuid>",
  "record": {
    "scan_id": "<request_id reconnaissance>",
    "status": "low_confidence",
    "score": 0.6,
    "created_at": "2026-06-03T00:00:00Z",
    "model_version": "vision-lite-1.0.0",
    "city_id": "paris",
    "candidate_monument_id": "notre-dame",
    "user_feedback": "wrong_monument",
    "notes": "confusion façade latérale"
  }
}
```
- Erreurs: `400` payload/label invalides; `404 Hard case not found`.

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
  "requested_lang": "fr",
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
      "lang": "fr",
      "fallback_lang": null
    }
  ]
}
```
> L'exemple abrège `embedding`; le bundle réel conserve 256 dimensions.

Comportements locaux validés:
- reconnaissance depuis `embeddings_index` avec les mêmes statuts que `POST /v1/recognize`: `matched`, `low_confidence`, `not_found`;
- lecture de fiche depuis `monument_cards` sans appel API;
- fiches locales multilingues: `lang` demandé respecté si disponible, sinon fallback explicite en `fr`;
- chat explicitement indisponible hors-ligne via `capabilities.chat=false`.

## Contrat gestion locale des paquets OFF-3

Le client maintient un registre local des paquets ville téléchargés à partir du bundle OFF-2.

Entrée logique installée:
```json
{
  "city_id": "paris",
  "package_version": "2026.06.03-1",
  "model_version": "vision-lite-1.0.0",
  "lang": "fr",
  "size_bytes": 24576000,
  "installed_at": "2026-06-03T09:00:00Z",
  "monument_count": 1,
  "update_available": false
}
```

Comportements locaux validés:
- liste triée des villes téléchargées;
- calcul de `used_bytes`, `quota_bytes`, `available_bytes` pour affichage stockage;
- suppression locale d'un paquet ville par `city_id`;
- marquage `update_available=true` avec `latest_package_version` si le manifeste serveur annonce une version plus récente;
- rejet explicite si le paquet dépasse le quota local ou si la ville n'est pas installée.

## Contrat carnet local USR-1

Le carnet de voyage est un modèle local côté client, validé pour enregistrer chaque scan et lister l'historique.

Entrée logique créée à chaque scan:
```json
{
  "monument_id": "notre-dame",
  "scanned_at": "2026-06-03T08:30:00Z",
  "score": 0.9235,
  "status": "matched"
}
```

Contraintes validées:
- `score` borné entre `0` et `1`, arrondi à 4 décimales;
- `status` dans `matched`, `low_confidence`, `not_found`;
- liste consultable triée par date en ordre descendant par défaut, ou ascendant sur demande;
- politique SEC-2 locale: conservation cible `365` jours, `purge_before(cutoff)` supprime les entrées antérieures, `clear()` supprime tout le carnet utilisateur.

### `POST /v1/chat`
- Stories: API-4 / IA-1.
- Auth: Bearer requise.
- Implémentation actuelle: RAG déterministe minimal sur la fiche KB locale, sans appel LLM externe.
- Comportement garanti:
  - réponse fondée sur les champs récupérés du monument;
  - `sources` liste les champs utilisés;
  - si aucune donnée fiable ne correspond à la question, l'assistant le dit et renvoie `sources: []`;
  - SEC-2: historique non persisté serveur, seulement les 12 derniers messages client sont utilisés, métadonnées `privacy` renvoyées.
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
  ],
  "privacy": {
    "history_retention": "session_only_client_side",
    "history_received": 2,
    "history_used": 2,
    "history_max_messages": 12
  }
}
```
- Erreurs:
  - `400` payload/message/historique/lang invalides.
  - `404 Monument not found`.

## Endpoints à implémenter (ordre backlog)
- Aucun endpoint J2 restant avant intégration produit hors-ligne; enrichissements à venir: streaming réel et backend RAG/LLM externe pour API-4.
