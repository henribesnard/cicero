# Cicero — Rapport QA J17: runbook revue hard-cases

## Périmètre

Validation légère de la documentation ops `docs/ops/hard-case-review.md` et non-régression ciblée de l'outil CSV ML-4.

## Commandes exécutées

```bash
python -m pytest -q backend/tests/test_export_hard_cases_csv.py backend/tests/test_hard_case_logger.py
python backend/tools/export_hard_cases_csv.py /tmp/cicero-hard-cases-sample.jsonl /tmp/cicero-hard-cases-review.csv
```

## Résultats observés

- `11 passed in 0.14s`.
- `exported 2 hard-case record(s) to /tmp/cicero-hard-cases-review.csv`.
- CSV trié par priorité: `scan-none-1` priorité 75 avant `scan-low-1` priorité 65.

## Notes sécurité

- Aucune donnée réelle utilisée.
- Le runbook interdit explicitement image brute, embedding brut, position précise, URL personnelle et informations utilisateur.
- Pas d'appel modèle, pas de réindexation, pas de publication.
