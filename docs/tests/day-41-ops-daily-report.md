# Day 41 — Tests rapport quotidien ops guardrails

## Commande

```bash
python3 -m pytest backend/tests/test_report_ops_guardrails_daily.py backend/tests/test_report_ops_guardrails.py backend/tests/test_report_ops_guardrails_trend.py -q
```

## Résultat

```text
...........                                                              [100%]
11 passed in 0.09s
```

## Vérification manuelle légère

```bash
python3 backend/tools/report_ops_guardrails_daily.py --markdown --trend-input docs/ops/ops_guardrails_snapshots.jsonl --trend-limit 7 --top-cleanup 3 --min-cleanup-size-mb 100
```

Résultat observé: rapport Markdown quotidien généré avec statut combiné `light`, RAM/disque actuels, tendance snapshot, chemins de revue nettoyage et mention finale `report-only`.
