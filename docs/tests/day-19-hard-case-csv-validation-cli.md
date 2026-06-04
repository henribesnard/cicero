# Cicero — QA day-19 — Validation CSV hard-cases avant réinjection

## Périmètre

Ajout d'un préflight local pour valider un CSV de revue annoté avant tout appel `POST /v1/hard-cases/{scan_id}/feedback`.

## Actifs testés

- `backend/tools/validate_hard_cases_csv.py`
- `backend/tests/test_validate_hard_cases_csv.py`
- Non-régression: `test_summarize_hard_cases_csv.py`, `test_export_hard_cases_csv.py`

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest -q tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_export_hard_cases_csv.py
```

Résultat:

```text
........                                                                 [100%]
8 passed in 0.39s
```

Démonstrateur CLI léger:

```bash
python tools/validate_hard_cases_csv.py /tmp/<review.csv>
python tools/validate_hard_cases_csv.py /tmp/<review.csv> --json
```

Résultat observé:

```text
valid: 2 row(s), 2 annotated, 0 error(s), 0 warning(s)
invalid_returncode= 1
"schema_version": "hard-case-csv-validation-v1",
```

## Critères validés

- Header obligatoire contrôlé.
- `scan_id` non vide et unique.
- `review_priority` borné 0..100.
- `score` borné 0..1.
- `status` limité à `low_confidence` / `not_found`.
- `user_feedback` limité à `correct`, `wrong_monument`, `unknown`, `poor_angle`, `too_dark`, `other`.
- Notes longues signalées en warning, sans bloquer les lignes valides.
- Aucun effet de bord: pas d'appel API, pas d'écriture JSONL.
