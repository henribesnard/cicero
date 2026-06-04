# Day 40 — Rapport Markdown ops guardrails

## Périmètre

- Story traitée: OPS léger / QA-1.
- Incrément: ajout d'une sortie `--markdown` à `backend/tools/report_ops_guardrails.py` pour transformer le résumé compact cron en mini rapport Markdown lisible.
- Garantie: sortie strictement `report-only`, aucune suppression ni mutation système.

## Tests automatisés

Commande exécutée depuis la racine du dépôt:

```bash
python3 -m pytest backend/tests/test_report_ops_guardrails.py backend/tests/test_report_cleanup_review_plan.py backend/tests/test_report_ops_guardrails_trend.py backend/tests/test_archive_ops_guardrails.py -q
```

Résultat exact:

```text
..............                                                           [100%]
14 passed in 0.15s
```

## Validation CLI

Commande exécutée:

```bash
python3 backend/tools/report_ops_guardrails.py --markdown --top-cleanup 3 --min-cleanup-size-mb 100
```

Résultat observé:

```text
# Rapport ops guardrails

- Statut: `light`
- RAM: 155 MiB libres / 711 MiB disponibles
- Disque: 69.8% utilisé
- Revue nettoyage requise: oui
- Candidats nettoyage: 4594 MiB (3 actionnable(s), 3 à revoir manuellement)

## Chemins à revoir
- `/home/hermes/.cache`
- `/var/log`
- `/home/hermes/.npm`

## Recommandations
- Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds.
- Revoir 3 candidat(s) de nettoyage non destructif avant tout ménage manuel.

_Mode report-only: aucune suppression ni mutation système._
```
