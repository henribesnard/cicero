# Cicero — Rapport quotidien J15

## Réalisé aujourd'hui
- Story avancée: **ML-4** — persistance JSONL optionnelle de la file privacy-safe `hard-cases-v1`.
- `HardCaseLogger` accepte désormais un `storage_path` et recharge/réécrit les cas difficiles après ajout, annotation et purge.
- Le backend active cette persistance uniquement si `CICERO_HARD_CASES_JSONL_PATH` est défini; le comportement MVP par défaut reste volatile.
- Mise à jour de `docs/api.md`, `docs/project-register.md` et ajout du rapport QA `docs/tests/day-15-hard-case-jsonl-persistence.md`.

## Tests
- Commande ciblée: `pytest -q backend/tests/test_hard_case_logger.py backend/tests/test_recognize.py`
- Résultat: `19 passed in 0.96s`
- Commande complète backend: `pytest -q backend/tests`
- Résultat: `49 passed in 1.13s`

## Blocages
- Aucun blocage fonctionnel.
- Push distant à vérifier en fin de run selon l'authentification disponible.

## Suite proposée
1. Ajouter un mini export CSV/CLI des hard-cases annotés pour revue humaine sans exposer de signaux bruts.
2. Préparer les tests QA-3 hors-ligne bout-en-bout à partir du bundle local OFF-2/OFF-3.
