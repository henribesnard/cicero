# Cicero — Tests J31 · Réserve disque du diagnostic VPS

## Objet

Renforcer le diagnostic disque non destructif livré en J28 avec une réserve opérationnelle explicite: calcul de 10% du disque racine et recommandations manuelles si `/` atteint le seuil 70% ou si l'espace libre passe sous cette réserve.

## Actifs livrés

- Outil enrichi: `backend/tools/report_safe_cleanup_candidates.py`.
- Tests enrichis: `backend/tests/test_report_safe_cleanup_candidates.py`.
- Documentation ops: `docs/ops/hard-case-review.md`.

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_report_privacy_retention_controls.py tests/test_report_safe_cleanup_candidates.py -q
```

Résultat:

```text
5 passed in 0.75s
```

Smoke CLI JSON:

```bash
python tools/report_safe_cleanup_candidates.py --json
```

Résultat observé sur le VPS:

```text
schema_version = safe-cleanup-candidates-v1
mode = report-only
disk.used_percent = 69.7
disk.free_gb = 14.33
reserve_10_percent_free_gb = 4.74
recommended_manual_actions = []
total_candidate_size_mb = 4580
```

## Couverture

- Calcul de `reserve_10_percent_free_gb` depuis la taille du disque racine.
- Recommandation quand le disque est à 70% ou plus.
- Recommandation distincte quand l'espace libre est sous la réserve de 10%.
- Garde-fou inchangé: rapport uniquement, aucune suppression automatique, chemins web/serveur exclus.
