# Cicero — QA day-20 — Validation stricte CSV hard-cases

## Périmètre

Amélioration légère du préflight local `validate_hard_cases_csv.py`: ajout d'un mode strict pour bloquer les CSV partiellement annotés avant une réinjection batch de feedback.

## Actifs modifiés

- `backend/tools/validate_hard_cases_csv.py`
- `backend/tests/test_validate_hard_cases_csv.py`
- `docs/ops/hard-case-review.md`

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest -q tests/test_validate_hard_cases_csv.py
```

Résultat:

```text
......                                                                   [100%]
6 passed in 0.46s
```

Démonstrateur CLI strict sur CSV temporaire avec `user_feedback` vide:

```bash
python tools/validate_hard_cases_csv.py /tmp/<review.csv> --require-all-annotated --json
```

Résultat observé:

```text
returncode= 1
"valid": false
"row 2: user_feedback must be annotated"
```

## Critères validés

- Le comportement par défaut reste compatible avec les revues partielles: lignes non annotées comptées comme `unlabeled`.
- `--require-all-annotated` rend chaque `user_feedback` vide bloquant.
- Le rapport JSON conserve le schéma `hard-case-csv-validation-v1`.
- Aucun effet de bord: pas d'appel API, pas d'écriture JSONL.
