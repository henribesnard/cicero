# Cicero — Rapport quotidien J16

## Réalisé aujourd'hui
- Story avancée: **ML-4 / Ops review** — ajout d'un export CSV local des cas difficiles persistés en JSONL.
- Nouveau script: `backend/tools/export_hard_cases_csv.py`.
- Nouveau test: `backend/tests/test_export_hard_cases_csv.py`.
- Nouveau rapport QA: `docs/tests/day-16-hard-case-csv-export-cli.md`.

## Tests
- Commande ciblée: `pytest -q backend/tests/test_export_hard_cases_csv.py backend/tests/test_hard_case_logger.py`
- Résultat: `11 passed in 0.17s`
- Démonstrateur CLI exécuté avec un JSONL temporaire; CSV généré avec colonnes `review_priority,scan_id,status,score,created_at,model_version,city_id,candidate_monument_id,user_feedback,notes`.

## Blocages
- Mode léger appliqué: RAM `free` basse au démarrage; pas d'exécution lourde ni veille web coûteuse.
- Disque racine à 70%; à surveiller, ménage non destructif à prévoir si >70%.

## Suite proposée
1. Ajouter une courte section d'usage CLI dans `docs/api.md` ou un `docs/ops.md` dédié.
2. Préparer un mini workflow offline: export CSV → annotation manuelle → réimport feedback via endpoint local.
