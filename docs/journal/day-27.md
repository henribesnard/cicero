# Cicero — Rapport quotidien J27

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops pipeline** — intégration du rapport de capacité de revue directement dans le pipeline dry-run hard-case.
- Outil modifié: `backend/tools/run_hard_case_review_pipeline.py`.
- Artefact pipeline ajouté: `hard-case-review-capacity.json`.
- Option CLI ajoutée: `--capacity-budgets` pour personnaliser les budgets minute (`30,60,120` par défaut).
- Tests ajoutés: présence de l'artefact capacité dans le pipeline, exposition des budgets dans le rapport retourné, rejet CLI des budgets invalides.
- Documentation mise à jour: `docs/ops/hard-case-review.md`, `docs/api.md`, `docs/tests/day-27-hard-case-pipeline-capacity.md`, `docs/project-register.md`.

## Tests

- Commande ciblée depuis `backend/`: `python -m pytest tests/test_run_hard_case_review_pipeline.py tests/test_report_hard_case_review_capacity.py -q` → `8 passed in 0.95s`.
- Non-régression hard-case ops depuis `backend/`: `python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py tests/test_export_hard_case_review_markdown.py tests/test_import_hard_case_review_markdown.py tests/test_report_hard_case_review_capacity.py -q` → `45 passed in 2.51s`.
- Suite backend complète depuis `backend/`: `python -m pytest -q` → `85 passed in 5.12s`.

## Blocages

- RAM disponible proche du seuil au démarrage (`available=858 MiB`): aucune tâche lourde lancée.
- Disque racine à 70%: seuil strict `>70%` non franchi, mais marge faible; proposer uniquement ménage non destructif si dépassement.

## Suite proposée

1. Ajouter une commande dry-run de réinjection batch depuis `hard-case-feedback-payloads.jsonl`, sans secret en dur et avec mode `--dry-run` par défaut.
2. Ajouter un mini script de diagnostic disque non destructif listant caches/logs volumineux candidats au ménage, sans suppression automatique et sans toucher au serveur web.
