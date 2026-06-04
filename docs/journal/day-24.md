# Cicero — Rapport quotidien J24

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops review** — fiche Markdown imprimable pour revue humaine des cas difficiles.
- Outil ajouté: `backend/tools/export_hard_case_review_markdown.py`.
- Pipeline enrichi: `backend/tools/run_hard_case_review_pipeline.py` génère maintenant `hard-case-review-sheet.md` en plus des artefacts JSON/JSONL.
- Tests ajoutés: rendu Markdown, écriture, rejet de mauvais schéma, contrat CLI et intégration pipeline.
- Documentation mise à jour: `docs/ops/hard-case-review.md`, `docs/api.md`, `docs/tests/day-24-hard-case-review-markdown.md`, `docs/project-register.md`.

## Tests

- Commande depuis `backend/`: `python -m pytest tests/test_export_hard_case_review_markdown.py tests/test_run_hard_case_review_pipeline.py -q` → `7 passed in 0.40s`.
- Non-régression hard-case ops: `python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py -q` → `33 passed in 1.71s`.
- Démonstration CLI sur CSV synthétique: `pipeline ok: 2 row(s), 1 annotated, 1 selected, 1 payload(s) to /tmp/cicero-hardcase-md-demo-out`; export standalone: `review markdown: 1 item(s) to /tmp/cicero-hardcase-md-demo-out/review-sheet-standalone.md`.

## Blocages

- Mode léger appliqué: RAM libre basse au démarrage (`free=197 MiB`, `available=856 MiB`); pas d'appel modèle, pas d'embeddings, pas de veille web lourde.
- Disque racine à 70%; seuil strict `>70%` non franchi, mais marge faible. Ménage non destructif proposé si Henri valide: caches utilisateur, caches Python/pytest anciens, rotation/logs applicatifs hors serveur web.

## Suite proposée

1. Ajouter une estimation `review_effort_minutes` dans le batch pour piloter le coût humain.
2. Ajouter un import contrôlé de décisions depuis la fiche Markdown vers CSV annoté, sans appel API.
