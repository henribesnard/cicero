# Day 39 — Ops guardrails compact JSON

## Objectif

Ajouter une sortie JSON compacte à `backend/tools/report_ops_guardrails.py` pour les runs cron: uniquement les champs décisionnels, sans le JSON complet.

## Changements validés

- Nouvelle fonction `build_compact_summary(report)`.
- Nouvelle option CLI `--compact-json`.
- Le JSON compact expose: `status`, RAM libre/disponible, disque utilisé, besoin de revue nettoyage, compte de candidats actionnables, compte d'items manuels, chemins de revue, recommandations.
- Le mode reste strictement `report-only`: aucune suppression, aucune rotation, aucune compression.

## Preuves

```bash
python3 -m pytest backend/tests/test_report_ops_guardrails.py backend/tests/test_report_cleanup_review_plan.py -q
```

Résultat:

```text
7 passed in 0.07s
```

```bash
python3 backend/tools/report_ops_guardrails.py --compact-json --top-cleanup 3 --min-cleanup-size-mb 100
```

Résultat observé:

```json
{"schema_version":"ops-guardrails-compact-v1","mode":"report-only","status":"light","vps":{"ram_free_mb":152,"ram_available_mb":702,"disk_used_percent":69.8,"cleanup_review_needed":true},"cleanup":{"total_candidate_size_mb":4594,"actionable_count":3,"manual_review_item_count":3,"top_review_paths":["/home/hermes/.cache","/var/log","/home/hermes/.npm"]},"recommendations":["Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds.","Revoir 3 candidat(s) de nettoyage non destructif avant tout ménage manuel."]}
```
