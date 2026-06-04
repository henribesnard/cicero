# Day 37 — Plan manuel nettoyage disque

## Décision du run

Mode léger maintenu: RAM disponible basse et disque racine proche de 70%. Aucun build lourd, téléchargement massif, suppression, rotation de logs, publication ou action externe destructive.

## Stories / actifs traités

- **OPS léger / QA-1**: création de `backend/tools/report_cleanup_review_plan.py`, outil read-only qui convertit les candidats conservateurs de nettoyage en plan manuel par chemin.
- Ajout de `backend/tests/test_report_cleanup_review_plan.py` pour valider classification, urgence, filtrage/limite et garde-fous humains.
- Documentation de preuve: `docs/tests/day-37-cleanup-review-plan.md`.

## Validation

- `python3 -m pytest backend/tests/test_report_cleanup_review_plan.py backend/tests/test_report_safe_cleanup_candidates.py backend/tests/test_report_ops_guardrails.py backend/tests/test_report_ops_guardrails_trend.py -q` → `15 passed in 0.12s`.
- `python3 backend/tools/report_cleanup_review_plan.py --limit 5 --min-size-mb 100` → `items=3`, disque `69.7%`, candidats: `/home/hermes/.cache` 2181 MiB, `/var/log` 1619 MiB, `/home/hermes/.npm` 738 MiB.
- `python3 backend/tools/report_cleanup_review_plan.py --limit 5 --min-size-mb 100 --json` → JSON `cleanup-review-plan-v1` vérifié, `mode=report-only`, `allowed_automation=none`.

## Documentation mise à jour

- `docs/api.md`: diagnostic VPS enrichi avec le plan de revue manuel des candidats de nettoyage.
- `docs/project-register.md`: D8/D9/D10 mis à jour au day-37.

## Prochain pas léger

Intégrer le plan de revue nettoyage dans la synthèse ops globale (`report_ops_guardrails.py`) pour que les rapports cron exposent directement les actions manuelles recommandées, toujours sans suppression automatique.
