# Cicero — Tests J29 — Réinjection batch feedback ML-4

Date: 2026-06-04

## Story / incrément

- Story avancée: **ML-4 · Boucle d'amélioration continue**.
- Incrément: outil ops `backend/tools/apply_hard_case_feedback_payloads.py` pour valider et, seulement avec `--apply`, réinjecter un JSONL de feedbacks hard-cases.
- Garde-fou produit: le mode par défaut est un dry-run sans réseau; les appels API exigent `--apply`, `--base-url` et un Bearer token explicite ou `CICERO_API_BEARER_TOKEN`.

## Couverture ajoutée

Fichier: `backend/tests/test_apply_hard_case_feedback_payloads.py`

Cas validés:

1. Chargement d'un JSONL préparé, comptage par label et promesses privacy.
2. Dry-run par défaut sans appel réseau.
3. Rejet de champs sensibles (`raw_embedding`) et champs payload non supportés.
4. Rejet d'un `--apply` sans prérequis URL/token.
5. Envoi uniquement quand `--apply` + URL + token sont présents (HTTP mocké).
6. Smoke CLI dry-run compact.

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_apply_hard_case_feedback_payloads.py -q
```

Résultat exact:

```text
......                                                                   [100%]
6 passed in 0.44s
```

Suite élargie exécutée ensuite:

```bash
python -m pytest tests/test_apply_hard_case_feedback_payloads.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_run_hard_case_review_pipeline.py -q
```

Résultat exact:

```text
.............                                                            [100%]
13 passed in 1.29s
```

Suite backend complète exécutée avant commit:

```bash
python -m pytest -q
```

Résultat exact:

```text
........................................................................ [ 76%]
......................                                                   [100%]
94 passed in 4.69s
```
