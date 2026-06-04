# Cicero — Rapport quotidien J23

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops review** — pipeline local dry-run pour la revue des cas difficiles.
- Outil ajouté: `backend/tools/run_hard_case_review_pipeline.py`.
- Tests ajoutés: écriture des artefacts dry-run, échec validation sans artefact métier, contrat CLI compact.
- Documentation mise à jour: `docs/ops/hard-case-review.md`, `docs/api.md`, `docs/tests/day-23-hard-case-review-pipeline.md`, `docs/project-register.md`.

## Tests

- Commande depuis `backend/`: `python -m pytest tests/test_run_hard_case_review_pipeline.py -q` → `3 passed in 0.21s`.
- Non-régression hard-case ops: `python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py -q` → `29 passed in 1.65s`.
- Démonstration CLI sur CSV synthétique: `pipeline ok: 2 row(s), 1 annotated, 1 selected, 1 payload(s) to /tmp/cicero-hardcase-pipeline-demo/out`.

## Blocages

- Mode léger appliqué: RAM libre basse au démarrage (`free=238 MiB`, `available=889 MiB`); pas d'appel modèle, pas d'embeddings, pas de veille web lourde.
- Disque racine à 70%; seuil strict `>70%` non franchi, mais marge faible. Ménage non destructif proposé si Henri valide: caches utilisateur, caches Python/pytest anciens, rotation/logs applicatifs hors serveur web.

## Suite proposée

1. Ajouter une estimation `review_effort_minutes` dans le batch pour piloter le coût humain.
2. Ajouter un export Markdown depuis le pipeline pour produire une fiche revue humaine imprimable/non technique.
