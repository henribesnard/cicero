# Cicero — Rapport quotidien J14

## Réalisé aujourd'hui
- Story avancée: **ML-5** — ajout d'un endpoint backend authentifié `POST /v1/hard-cases/{scan_id}/feedback`.
- Ajout de `HardCaseLogger.annotate(...)` pour annoter un cas difficile existant avec `user_feedback` et `notes`.
- Mise à jour de `docs/api.md` avec le contrat de l'endpoint feedback.
- Ajout du rapport QA `docs/tests/day-14-hard-case-feedback-endpoint.md`.

## Tests
- Commande ciblée: `pytest -q backend/tests/test_hard_case_logger.py backend/tests/test_recognize.py`
- Résultat: `17 passed in 0.96s`
- Commande complète backend: `pytest -q backend/tests`
- Résultat: `47 passed in 1.21s`

## Blocages
- Mode léger appliqué: RAM libre stricte mesurée à 213 Mo au début du run, même si RAM disponible Linux à 946 Mo.
- Disque racine à 70%; seuil de ménage à surveiller, sans toucher au serveur web.

## Suite proposée
1. Décider si la file hard-cases reste volatile MVP ou passe en JSONL local avec rotation.
2. Ajouter un mini tableau CLI/export CSV pour revue humaine des hard-cases annotés.
