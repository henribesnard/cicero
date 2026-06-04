# Day 37 — Plan de revue nettoyage disque (mode léger)

## Contexte

- Le VPS reste en mode léger: RAM disponible sous le seuil opérationnel et disque racine proche de 70%.
- Le run précédent demandait une revue critique des candidats de nettoyage sans suppression automatique ni action sur le serveur web.

## Changement validé

`backend/tools/report_cleanup_review_plan.py` transforme le rapport conservateur `safe-cleanup-candidates-v1` en plan manuel par chemin:

- classification du candidat (`generic-cache`, `system-logs`, `node-cache`, etc.);
- niveau d'urgence selon taille et pression disque;
- risque de nettoyage;
- contrôles manuels recommandés;
- garde-fou explicite `allowed_automation=none` et `requires_human_validation=true`.

Le script reste strictement `report-only`: aucune suppression, aucune compression, aucune rotation, aucun changement système.

## Preuves d'exécution

```bash
python3 -m pytest backend/tests/test_report_cleanup_review_plan.py backend/tests/test_report_safe_cleanup_candidates.py backend/tests/test_report_ops_guardrails.py backend/tests/test_report_ops_guardrails_trend.py -q
```

Résultat:

```text
...............                                                          [100%]
15 passed in 0.12s
```

```bash
python3 backend/tools/report_cleanup_review_plan.py --limit 5 --min-size-mb 100
```

Résultat:

```text
cleanup review plan: disk=69.7% used, items=3, mode=report-only
- high	2181 MiB	/home/hermes/.cache	generic-cache	risk=low
- medium	1619 MiB	/var/log	system-logs	risk=medium
- medium	738 MiB	/home/hermes/.npm	node-cache	risk=low
```

## Plan manuel produit

1. `/home/hermes/.cache` — 2181 MiB — urgence haute, risque faible: inspecter les plus gros sous-dossiers et nettoyer uniquement les caches identifiés.
2. `/var/log` — 1619 MiB — urgence moyenne, risque moyen: privilégier `journalctl --disk-usage`, `logrotate -d` et vacuum contrôlé après validation humaine plutôt qu'une suppression brute.
3. `/home/hermes/.npm` — 738 MiB — urgence moyenne, risque faible: vérifier le cache npm puis envisager un nettoyage npm contrôlé après validation humaine.

## Garde-fous

- Aucune action destructive effectuée.
- Chemins web/serveur exclus par le rapport source.
- Toute action de nettoyage réelle nécessite validation humaine.
