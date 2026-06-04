# Day 35 — Archive JSONL ops guardrails

## Objectif

Ajouter un actif léger pour historiser les signaux VPS utiles aux runs cron sans build lourd ni action destructive.

## Actif créé

- `backend/tools/archive_ops_guardrails.py`
  - construit un snapshot compact `ops-guardrails-snapshot-v1` à partir de `report_ops_guardrails.py`;
  - écrit une ligne JSONL append-only dans `docs/ops/ops_guardrails_snapshots.jsonl`;
  - supporte `--dry-run`, `--output`, `--disk-path`, `--cleanup-path`, `--top-cleanup`, `--min-cleanup-size-mb`.

## Validation

```bash
python3 -m pytest backend/tests/test_archive_ops_guardrails.py backend/tests/test_report_ops_guardrails.py -q
```

Résultat: `4 passed in 0.07s`.

```bash
python3 backend/tools/archive_ops_guardrails.py --output docs/ops/ops_guardrails_snapshots.jsonl --top-cleanup 3 --min-cleanup-size-mb 100
```

Résultat réel du run: `ops snapshot archived: path=docs/ops/ops_guardrails_snapshots.jsonl, status=light, ram_free=120 MiB, disk=69.7% used, cleanup_candidates=4582 MiB`.

```bash
python3 backend/tools/archive_ops_guardrails.py --dry-run --top-cleanup 1 --min-cleanup-size-mb 100
```

Résultat: snapshot JSON compact imprimé, avec `schema_version=ops-guardrails-snapshot-v1`, `status=light`, `memory.available_mb=765`, `disk.used_percent=69.7`, `cleanup.total_candidate_size_mb=4582`.

## Garde-fous

- Aucun nettoyage, suppression, publication ou dépense.
- Écriture limitée à un artefact JSONL local append-only dans `docs/ops/`.
- Utilisable en mode léger RAM basse.
