# Cicero — QA day-21 — Payloads feedback hard-cases en dry-run

## Périmètre

Ajout d'un préflight local entre CSV annoté et réinjection API: générer un JSONL inspectable de payloads feedback, sans appel réseau ni mutation serveur.

## Actifs modifiés

- `backend/tools/prepare_hard_case_feedback_payloads.py`
- `backend/tests/test_prepare_hard_case_feedback_payloads.py`
- `docs/ops/hard-case-review.md`
- `docs/api.md`
- `docs/project-register.md`

## Commandes exécutées

Depuis la racine du dépôt:

```bash
python -m pytest backend/tests/test_prepare_hard_case_feedback_payloads.py backend/tests/test_validate_hard_cases_csv.py -q
```

Résultat final observé:

```text
.........                                                                [100%]
9 passed in 0.70s
```

## Critères validés

- Le script valide le CSV via `validate_hard_cases_csv.py` avant d'écrire les payloads.
- Les lignes sans `user_feedback` sont ignorées par défaut, ce qui permet une revue progressive.
- Un CSV invalide retourne un rapport `valid=false` et n'écrit pas de JSONL.
- Le JSONL contient uniquement `scan_id`, `method`, `path` et `payload`; aucune image, embedding ou position précise.
- La CLI reste dry-run: aucun appel API, aucune publication, aucun coût modèle.
