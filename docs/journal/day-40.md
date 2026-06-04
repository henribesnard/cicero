# Day 40 — Mini rapport Markdown ops guardrails

## Décision du run

Mode léger: RAM libre/disponible sous le seuil opérationnel de 800 MiB. Aucun build lourd, téléchargement massif, nettoyage disque, publication ou action externe.

## Stories / actifs traités

- **OPS léger / QA-1**: ajout d'une sortie `--markdown` à `backend/tools/report_ops_guardrails.py`.
- Le mini rapport réutilise les champs décisionnels du résumé compact: statut, RAM, disque, besoin de revue nettoyage, chemins à revoir et recommandations.
- Tests ciblés enrichis dans `backend/tests/test_report_ops_guardrails.py`.
- Documentation de preuve: `docs/tests/day-40-ops-markdown-summary.md`.

## Validation

- `python3 -m pytest backend/tests/test_report_ops_guardrails.py backend/tests/test_report_cleanup_review_plan.py backend/tests/test_report_ops_guardrails_trend.py backend/tests/test_archive_ops_guardrails.py -q` → `14 passed in 0.15s`.
- `python3 backend/tools/report_ops_guardrails.py --markdown --top-cleanup 3 --min-cleanup-size-mb 100` → Markdown valide, statut `light`, `cleanup_review_needed=oui`, 3 chemins de revue: `/home/hermes/.cache`, `/var/log`, `/home/hermes/.npm`.

## Documentation mise à jour

- `docs/api.md`: option `--markdown` documentée dans le diagnostic VPS non destructif.
- `docs/project-register.md`: D8/D9/D10 mis à jour au day-40.

## Prochain pas léger

Créer un export Markdown combiné `compact + trend` ou un résumé journalier prêt à coller dans les rapports cron, toujours en mode report-only.
