# Day 35 — Archive légère des signaux VPS

## Décision du run

Mode léger maintenu: RAM libre observée sous 800 MiB, charge faible, disque racine à ~70%. Aucun build lourd, téléchargement massif, publication, suppression ou action externe.

## Stories / actifs traités

- **OPS léger / QA-1**: création de `backend/tools/archive_ops_guardrails.py`, wrapper JSONL append-only pour historiser les snapshots cron `health + cleanup`.
- Ajout de `backend/tests/test_archive_ops_guardrails.py` pour verrouiller le format compact et l'écriture JSONL.
- Création du premier artefact local `docs/ops/ops_guardrails_snapshots.jsonl`.

## Validation

- `python3 -m pytest backend/tests/test_archive_ops_guardrails.py backend/tests/test_report_ops_guardrails.py -q` → `4 passed in 0.07s`.
- `python3 backend/tools/archive_ops_guardrails.py --output docs/ops/ops_guardrails_snapshots.jsonl --top-cleanup 3 --min-cleanup-size-mb 100` → snapshot archivé, statut `light`, RAM libre `120 MiB`, disque `69.7%`, candidats nettoyage report-only `4582 MiB`.
- `python3 backend/tools/archive_ops_guardrails.py --dry-run --top-cleanup 1 --min-cleanup-size-mb 100` → JSON compact vérifié à l'écran.

## Documentation mise à jour

- `docs/tests/day-35-ops-snapshot-archive.md`: preuve du run.
- `docs/api.md`: diagnostic VPS enrichi avec l'archive JSONL.
- `docs/project-register.md`: D8/D9/D10 mis à jour au day-35.

## Prochain pas léger

Exploiter le JSONL pour produire un mini rapport de tendance RAM/disque sur les 7 derniers snapshots, sans dépendance externe.
