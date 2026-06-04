# Cicero — Rapport quotidien J25

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops review** — estimation du coût humain de revue des cas difficiles.
- Outil enrichi: `backend/tools/select_hard_case_review_batch.py` ajoute `review_effort_minutes` par item et `estimated_review_effort_minutes` au batch.
- Fiche Markdown enrichie: `backend/tools/export_hard_case_review_markdown.py` affiche l'effort total et l'effort par cas.
- Tests ajoutés: calcul déterministe, plafond des cas complexes, rendu Markdown de l'effort.
- Documentation mise à jour: `docs/ops/hard-case-review.md`, `docs/api.md`, `docs/tests/day-25-hard-case-review-effort.md`, `docs/project-register.md`.

## Tests

- Commande ciblée depuis `backend/`: `python -m pytest tests/test_select_hard_case_review_batch.py tests/test_export_hard_case_review_markdown.py -q` → `9 passed in 0.39s`.
- Non-régression hard-case ops: `python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py tests/test_export_hard_case_review_markdown.py -q` → `34 passed in 1.52s`.

## Blocages

- Mode léger appliqué: RAM libre basse au démarrage (`free=207 MiB`, `available=856 MiB`); pas d'appel modèle, pas d'embeddings, pas de veille web lourde.
- Disque racine à 70%; seuil strict `>70%` non franchi, mais marge faible. Ménage non destructif à prévoir si ça dépasse: caches utilisateur, caches Python/pytest anciens, logs applicatifs hors serveur web.

## Suite proposée

1. Ajouter un import contrôlé de décisions depuis la fiche Markdown vers CSV annoté, sans appel API.
2. Ajouter un rapport hebdo `review_capacity`: nombre de cas traitables en 30/60/120 minutes selon l'estimation.
