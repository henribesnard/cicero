# Day 38 — Ops guardrails avec plan de revue intégré

## Décision du run

Mode léger: RAM libre/disponible sous le seuil opérationnel de 800 MiB. Aucun build lourd, téléchargement massif, nettoyage disque, publication ou action externe.

## Stories / actifs traités

- **OPS léger / QA-1**: intégration de `report_cleanup_review_plan.py` dans `backend/tools/report_ops_guardrails.py`.
- Le rapport ops global expose maintenant `cleanup_review_plan` et `summary.manual_review_item_count`.
- Tests ciblés enrichis dans `backend/tests/test_report_ops_guardrails.py`.
- Documentation de preuve: `docs/tests/day-38-ops-guardrails-review-plan.md`.

## Validation

- `python3 -m pytest backend/tests/test_report_ops_guardrails.py backend/tests/test_report_cleanup_review_plan.py -q` → `6 passed in 0.06s`.
- `python3 backend/tools/report_ops_guardrails.py --top-cleanup 3 --min-cleanup-size-mb 100` → statut `light`, `cleanup_candidates=4593 MiB`, 3 candidats actionnables et 3 items de revue manuelle: `/home/hermes/.cache`, `/var/log`, `/home/hermes/.npm`.

## Documentation mise à jour

- `docs/api.md`: le diagnostic VPS documente désormais le bloc `cleanup_review_plan` dans la synthèse ops globale.
- `docs/project-register.md`: D8/D9/D10 mis à jour au day-38.

## Prochain pas léger

Ajouter une option JSON compacte à `report_ops_guardrails.py` ou à la tendance pour ne sortir que les champs décisionnels cron (`status`, RAM, disque, items de revue, arbitrage humain), sans dupliquer le JSON complet.
