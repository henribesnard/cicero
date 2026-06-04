# Day 36 — Tendance légère archive ops

## Décision du run

Mode léger activé: RAM disponible/free sous le seuil opérationnel, charge basse, disque racine à 70%. Aucun build lourd, téléchargement massif, publication, suppression ou action externe.

## Stories / actifs traités

- **OPS léger / QA-1**: création de `backend/tools/report_ops_guardrails_trend.py`, rapport read-only de tendance sur les snapshots JSONL ops.
- Ajout de `backend/tests/test_report_ops_guardrails_trend.py` pour valider parsing robuste, limites, deltas et cas archive vide.
- Documentation de preuve: `docs/tests/day-36-ops-guardrails-trend.md`.

## Validation

- `python3 -m pytest backend/tests/test_report_ops_guardrails_trend.py backend/tests/test_archive_ops_guardrails.py -q` → `6 passed in 0.10s`.
- `python3 backend/tools/report_ops_guardrails_trend.py --input docs/ops/ops_guardrails_snapshots.jsonl --limit 7` → `status=light`, `snapshots=1`, `ram_free=120 MiB`, `disk=69.7%`, `cleanup_candidates=4582 MiB`.
- `python3 backend/tools/report_ops_guardrails_trend.py --input docs/ops/ops_guardrails_snapshots.jsonl --limit 7 --json` → JSON `ops-guardrails-trend-v1` vérifié.

## Documentation mise à jour

- `docs/api.md`: diagnostic VPS enrichi avec le rapport de tendance JSONL.
- `docs/project-register.md`: D8/D9/D10 mis à jour au day-36.

## Prochain pas léger

Faire une revue critique des candidats de nettoyage déjà détectés et produire un plan manuel sûr par chemin, sans suppression automatique ni toucher au serveur web.
