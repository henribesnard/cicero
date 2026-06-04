# Cicero — Tests J26 — Import Markdown revue + capacité ML-4

## Périmètre

- Import sans effet API de décisions cochées dans une fiche Markdown de revue vers un CSV annoté.
- Rapport local de capacité de revue: cas difficiles traitables en budgets 30/60/120 minutes (ou budgets personnalisés).

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_import_hard_case_review_markdown.py tests/test_report_hard_case_review_capacity.py -q
```

Résultat:

```text
10 passed in 0.74s
```

## Couverture ajoutée

- Parsing Markdown: extraction d'un seul label coché par `scan_id` et notes optionnelles.
- Import CSV: mise à jour par `scan_id`, préservation des lignes non cochées, rejet des labels multiples et des `scan_id` inconnus.
- CLI d'import: rapport compact + mode JSON d'erreur.
- Capacité: calcul déterministe par budgets, exclusion des cas déjà résolus, validation CSV préalable, CLI compact.

## Garde-fous validés

- Aucun appel réseau/API.
- Aucune mutation du JSONL source.
- Pas d'image brute, pas d'embedding brut, pas de position précise ajoutés aux artefacts.
