# Cicero — Rapport quotidien J29

## Réalisé aujourd'hui

- Story avancée: **ML-4 · Boucle d'amélioration continue** — sécurisation de la dernière étape ops de réinjection des feedbacks hard-cases.
- Outil ajouté: `backend/tools/apply_hard_case_feedback_payloads.py`.
- Tests ajoutés: `backend/tests/test_apply_hard_case_feedback_payloads.py`.
- Documentation mise à jour: `docs/ops/hard-case-review.md`, `docs/api.md`, `docs/tests/day-29-hard-case-feedback-batch-apply.md`, `docs/project-register.md`.

## Comportement livré

- Le batch JSONL préparé par `prepare_hard_case_feedback_payloads.py` est validé avant toute réinjection.
- Mode par défaut: dry-run sans réseau, `0 sent`.
- Réinjection réelle seulement avec `--apply`, `--base-url` et token Bearer explicite ou `CICERO_API_BEARER_TOKEN`.
- Garde-fous: rejet des doublons, labels invalides, mismatch `scan_id`/`path`, champs payload non supportés et champs sensibles (`image`, `embedding`, coordonnées).

## Tests

- Commande ciblée depuis `backend/`: `python -m pytest tests/test_apply_hard_case_feedback_payloads.py -q` → `6 passed in 0.44s`.
- Suite ops élargie depuis `backend/`: `python -m pytest tests/test_apply_hard_case_feedback_payloads.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_run_hard_case_review_pipeline.py -q` → `13 passed in 1.29s`.
- Suite backend complète depuis `backend/`: `python -m pytest -q` → `94 passed in 4.69s`.
- Smoke CLI dry-run: `python tools/apply_hard_case_feedback_payloads.py <payloads.jsonl>` → `dry-run ok: 1 feedback payload(s) validated, 0 sent`.

## Blocages

- Aucun blocage produit.
- Le push peut rester dépendant de l'authentification Git distante du VPS.

## Suite proposée

1. Démarrer le prochain incrément J2 restant selon ordre backlog: enrichir SEC-2 côté API (endpoint/export/suppression données utilisateur si périmètre disponible) ou passer au premier correctif QA prioritaire si un retour terrain apparaît.
2. Conserver les opérations ML lourdes (réindexation, modèle, embeddings) en action manuelle/planifiée, pas en cron automatique.
