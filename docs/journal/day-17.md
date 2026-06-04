# Cicero — Rapport quotidien J17

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops review** — formalisation d'un runbook de revue des cas difficiles persistés.
- Nouveau document: `docs/ops/hard-case-review.md`.
- Spécification API reliée au runbook via `docs/api.md`.
- Nouveau rapport QA: `docs/tests/day-17-hard-case-review-runbook.md`.

## Tests

- Commande ciblée: `python -m pytest -q backend/tests/test_export_hard_cases_csv.py backend/tests/test_hard_case_logger.py` → `11 passed in 0.14s`.
- Démonstrateur CLI: `python backend/tools/export_hard_cases_csv.py /tmp/cicero-hard-cases-sample.jsonl /tmp/cicero-hard-cases-review.csv` → `exported 2 hard-case record(s)`; priorités CSV 75 puis 65.

## Blocages

- Mode léger appliqué: RAM libre basse au démarrage; pas de génération d'embeddings, pas d'appel modèle, pas de veille web coûteuse.
- Disque racine à 70%; surveillance nécessaire, ménage non destructif à proposer si dépassement strict de 70%.

## Suite proposée

1. Ajouter un mini script de synthèse CSV: top causes par `city_id`, `status`, `user_feedback`.
2. Préparer le workflow annoté complet: CSV revu → appels `/feedback` locaux → export de synthèse.
