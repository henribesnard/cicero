# Day 36 — Tendance légère archive ops

## Objectif

Exploiter l'archive JSONL des guardrails VPS pour produire un signal de tendance RAM/disque utilisable en mode léger, sans dépendance externe ni action destructive.

## Actif créé

- `backend/tools/report_ops_guardrails_trend.py`
  - lit les dernières lignes valides `ops-guardrails-snapshot-v1` depuis `docs/ops/ops_guardrails_snapshots.jsonl`;
  - ignore les lignes vides/invalides ou d'autre schéma;
  - calcule fenêtre observée, min/moyenne/delta RAM libre, min RAM disponible, max/delta disque, candidats de nettoyage;
  - expose sortie texte compacte ou JSON via `--json`.

## Validation

```bash
python3 -m pytest backend/tests/test_report_ops_guardrails_trend.py backend/tests/test_archive_ops_guardrails.py -q
```

Résultat réel: `6 passed in 0.10s`.

```bash
python3 backend/tools/report_ops_guardrails_trend.py --input docs/ops/ops_guardrails_snapshots.jsonl --limit 7
```

Résultat réel: `ops trend: status=light, snapshots=1, ram_free=120 MiB (min=120, delta=0), disk=69.7% (max=69.7, delta=0.0), cleanup_candidates=4582 MiB`.

Recommandations émises:
- `Mode léger recommandé: dernier snapshot RAM libre < 800 MiB.`
- `Candidats de nettoyage présents: revue manuelle uniquement, aucune suppression automatique.`

```bash
python3 backend/tools/report_ops_guardrails_trend.py --input docs/ops/ops_guardrails_snapshots.jsonl --limit 7 --json
```

Résultat: JSON `ops-guardrails-trend-v1` vérifié avec `snapshot_count=1`, `status=light`, `memory.last_free_mb=120`, `disk.last_used_percent=69.7`, `cleanup.last_total_candidate_size_mb=4582`.

## Garde-fous

- Lecture seule de l'archive JSONL existante.
- Aucun nettoyage, suppression, publication, téléchargement lourd ou dépense.
- Adapté au mode léger quand RAM libre < 800 MiB.
