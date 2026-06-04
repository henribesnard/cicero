# Cicero — Tests J27: capacité revue intégrée au pipeline hard-case

## Périmètre

Story avancée: **ML-4 / Ops pipeline** — le pipeline dry-run hard-case génère désormais aussi `hard-case-review-capacity.json` pour planifier une session de revue humaine sans commande séparée.

## Changements vérifiés

- `tools/run_hard_case_review_pipeline.py` ajoute l'artefact `hard-case-review-capacity.json`.
- La sortie compacte indique le nombre de cas non résolus pris en compte par le rapport capacité.
- Option CLI ajoutée: `--capacity-budgets`, valeurs positives séparées par virgules.
- Rejet contrôlé des budgets invalides avant création du répertoire de sortie.

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_run_hard_case_review_pipeline.py tests/test_report_hard_case_review_capacity.py -q
```

Résultat:

```text
8 passed in 0.95s
```

Non-régression hard-case ops:

```bash
python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py tests/test_export_hard_case_review_markdown.py tests/test_import_hard_case_review_markdown.py tests/test_report_hard_case_review_capacity.py -q
```

Résultat:

```text
45 passed in 2.51s
```

Suite backend complète:

```bash
python -m pytest -q
```

Résultat:

```text
85 passed in 5.12s
```

## Décision QA

OK pour continuer: évolution légère, sans appel réseau, sans modèle, sans mutation de la file JSONL source.
