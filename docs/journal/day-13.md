# Cicero — Rapport quotidien J13

## Réalisé aujourd'hui
- Story avancée: **ML-4** — ajout d'un endpoint backend authentifié `GET /v1/hard-cases/export`.
- L'endpoint expose l'export `hard-cases-v1` déjà produit par `HardCaseLogger`: agrégats, file de revue priorisée, records chronologiques et garanties privacy.
- Ajout d'un test d'intégration couvrant deux reconnaissances difficiles (`low_confidence`, `not_found`) puis l'export sécurisé.
- Mise à jour de `docs/api.md` avec le contrat de réponse et ajout du rapport QA `docs/tests/day-13-hard-cases-export-endpoint.md`.

## Tests
- Commande ciblée: `pytest -q backend/tests/test_hard_case_logger.py backend/tests/test_recognize.py`
- Résultat: `12 passed in 0.95s`
- Commande complète backend: `pytest -q backend/tests`
- Résultat: `42 passed in 1.04s`

## Blocages
- Aucun blocage fonctionnel.
- Point VPS: disque racine à 71%; ménage non destructif possible côté caches/logs uniquement, sans toucher au serveur web.

## Suite proposée
1. Ajouter une route de feedback interne pour annoter un hard case (`correct`, `wrong_monument`, `poor_angle`, etc.) avant réindexation.
2. Décider la persistance cible de la file hard-cases: mémoire volatile MVP, fichier JSONL local, ou stockage applicatif léger.
