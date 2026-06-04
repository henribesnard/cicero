# Day 41 — Rapport quotidien ops guardrails combiné

## Décision du run

Mode léger: RAM libre/disponible sous le seuil opérationnel de 800 MiB. Aucun build lourd, téléchargement massif, nettoyage disque, publication ou action externe.

## Stories / actifs traités

- **OPS léger / QA-1**: ajout de `backend/tools/report_ops_guardrails_daily.py`.
- Le nouvel outil combine le résumé courant `report_ops_guardrails` et la tendance JSONL `report_ops_guardrails_trend` en un rapport quotidien compact.
- Sorties disponibles: texte synthétique par défaut, `--json`, `--markdown`.
- Tests ciblés ajoutés dans `backend/tests/test_report_ops_guardrails_daily.py`.

## Validation

- `python3 -m pytest backend/tests/test_report_ops_guardrails_daily.py backend/tests/test_report_ops_guardrails.py backend/tests/test_report_ops_guardrails_trend.py -q` → `11 passed in 0.09s`.
- `python3 backend/tools/report_ops_guardrails_daily.py --markdown --trend-input docs/ops/ops_guardrails_snapshots.jsonl --trend-limit 7 --top-cleanup 3 --min-cleanup-size-mb 100` → Markdown valide; statut combiné `light`; 4595 MiB de candidats nettoyage; chemins à revoir: `/home/hermes/.cache`, `/var/log`, `/home/hermes/.npm`; aucune mutation système.

## Documentation mise à jour

- `docs/api.md`: outil quotidien combiné documenté dans le diagnostic VPS non destructif.
- `docs/project-register.md`: D8/D9/D10 mis à jour au day-41.

## Prochain pas léger

Ajouter une option `--max-recommendations` ou un profil `--cron-compact` pour limiter automatiquement le rapport final aux champs obligatoires du cron Henri.
