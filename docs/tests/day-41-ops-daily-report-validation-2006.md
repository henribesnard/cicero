# Day 41 — Validation légère rapport quotidien ops guardrails (20:06 CEST)

## Contexte VPS

Mode léger requis: RAM libre sous 800 MiB au début du run; aucune action lourde ni suppression.

## Commande exécutée

```bash
python3 -m pytest backend/tests/test_report_ops_guardrails_daily.py backend/tests/test_report_ops_guardrails.py backend/tests/test_report_ops_guardrails_trend.py -q && \
python3 backend/tools/report_ops_guardrails_daily.py --markdown --trend-input docs/ops/ops_guardrails_snapshots.jsonl --trend-limit 7 --top-cleanup 3 --min-cleanup-size-mb 100
```

## Résultat vérifié

```text
...........                                                              [100%]
11 passed in 0.07s
```

Le rendu Markdown généré inclut:

- statut combiné `light`;
- RAM actuelle: 144 MiB libres / 725 MiB disponibles;
- disque actuel: 69.8% utilisé;
- revue nettoyage: oui, 4596 MiB candidats, 3 revues manuelles;
- chemins proposés en revue uniquement: `/home/hermes/.cache`, `/var/log`, `/home/hermes/.npm`;
- mention finale `report-only`, sans suppression ni mutation système.

## Décision

Validation OK pour usage cron/reporting: le rapport quotidien agrège bien état courant, tendance et recommandations sans effet de bord.
