# Day 38 — Intégration du plan de revue nettoyage dans ops guardrails

## Contexte

Run en mode léger: RAM disponible sous le seuil de 800 MiB. Objectif limité à une amélioration read-only et testée, sans build lourd ni nettoyage effectif.

## Actif produit

`backend/tools/report_ops_guardrails.py` expose maintenant un bloc `cleanup_review_plan` en plus de `health`, `cleanup` et `summary`.

Champs ajoutés:
- `cleanup_review_plan.schema_version = cleanup-review-plan-v1`
- `cleanup_review_plan.mode = report-only`
- `cleanup_review_plan.review_item_count`
- `cleanup_review_plan.review_items[]` avec `path`, `size_mb`, `category`, `cleanup_risk`, `urgency`, `manual_checks`, `allowed_automation`, `requires_human_validation`
- `summary.manual_review_item_count`

## Garde-fous

- Aucun fichier supprimé, compressé, tronqué ou déplacé.
- Le rapport reste `report-only`.
- Chaque item de revue conserve `allowed_automation=none` et `requires_human_validation=true`.
- Les chemins web/serveur restent exclus par le générateur de candidats conservateurs.

## Validation exécutée

```bash
python3 -m pytest backend/tests/test_report_ops_guardrails.py backend/tests/test_report_cleanup_review_plan.py -q
```

Résultat:

```text
6 passed in 0.06s
```

```bash
python3 backend/tools/report_ops_guardrails.py --top-cleanup 3 --min-cleanup-size-mb 100
```

Résultat observé:

```text
ops guardrails: status=light, ram_free=146 MiB, ram_available=710 MiB, disk=69.8% used, cleanup_candidates=4593 MiB, report-only
- Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds.
- Revoir 3 candidat(s) de nettoyage non destructif avant tout ménage manuel.
- cleanup 2181 MiB	/home/hermes/.cache	candidate: inspect before manual cleanup
- cleanup 1628 MiB	/var/log	candidate: inspect before manual cleanup
- cleanup 738 MiB	/home/hermes/.npm	candidate: inspect before manual cleanup
- review high	2181 MiB	/home/hermes/.cache	generic-cache	risk=low
- review medium	1628 MiB	/var/log	system-logs	risk=medium
- review medium	738 MiB	/home/hermes/.npm	node-cache	risk=low
```

## Utilité QA / ops

Le cron peut désormais afficher directement les actions manuelles recommandées et leur niveau d'urgence dans le rapport ops global, sans demander à Henri d'exécuter un second outil pour comprendre quoi inspecter.
