# Cicero — Rapport quotidien J26

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops review** — import contrôlé des décisions cochées dans la fiche Markdown vers un CSV annoté, sans appel API.
- Story avancée: **ML-4 / Ops capacity** — rapport de capacité de revue indiquant combien de cas difficiles non résolus tiennent dans des budgets 30/60/120 minutes (budgets personnalisables).
- Outils ajoutés:
  - `backend/tools/import_hard_case_review_markdown.py`
  - `backend/tools/report_hard_case_review_capacity.py`
- Tests ajoutés: parsing Markdown, import CSV par `scan_id`, rejets labels multiples / `scan_id` inconnu, rapport de capacité, CLI compactes.
- Documentation mise à jour: `docs/ops/hard-case-review.md`, `docs/api.md`, `docs/tests/day-26-hard-case-markdown-import-capacity.md`, `docs/project-register.md`.

## Tests

- Commande ciblée depuis `backend/`: `python -m pytest tests/test_import_hard_case_review_markdown.py tests/test_report_hard_case_review_capacity.py -q` → `10 passed in 0.74s`.
- Non-régression hard-case ops depuis `backend/`: `python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py tests/test_export_hard_case_review_markdown.py tests/test_import_hard_case_review_markdown.py tests/test_report_hard_case_review_capacity.py -q` → `44 passed in 2.29s`.
- Suite backend complète depuis `backend/`: `python -m pytest -q` → `84 passed in 4.97s`.

## Blocages

- Mode léger maintenu: RAM disponible basse au démarrage du run (`available=800 MiB`); aucun modèle, embedding ou appel lourd lancé.
- Disque racine à 70%; seuil strict `>70%` non franchi, mais marge toujours faible.

## Suite proposée

1. Intégrer le rapport de capacité dans le pipeline dry-run pour générer l'artefact `hard-case-review-capacity.json` automatiquement.
2. Ajouter une commande dry-run de réinjection batch depuis `hard-case-feedback-payloads.jsonl`, sans secret en dur et avec mode `--dry-run` par défaut.
