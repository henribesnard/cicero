# Cicero — QA day-22 — Sélection batch de revue hard-cases

## Périmètre

Ajout d'un outil local, léger et privacy-safe pour transformer un export CSV de cas difficiles en file de revue bornée et diversifiée. Objectif: éviter qu'un opérateur passe son temps sur un seul couple ville/statut et accélérer l'annotation utile pour ML-4.

## Actifs modifiés

- `backend/tools/select_hard_case_review_batch.py`
- `backend/tests/test_select_hard_case_review_batch.py`
- `docs/journal/day-22.md`
- `docs/project-register.md`

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_select_hard_case_review_batch.py -q
```

Résultat final observé:

```text
....                                                                     [100%]
4 passed in 0.34s
```

Démonstration CLI sur CSV synthétique privacy-safe:

```bash
python tools/select_hard_case_review_batch.py /tmp/cicero-hardcase-demo/review.csv /tmp/cicero-hardcase-demo/batch.json --limit 2 --max-per-city 1 --max-per-status 2
```

Résultat observé:

```text
selected 2 of 2 unresolved hard-case row(s) to /tmp/cicero-hardcase-demo/batch.json
```

Extrait JSON produit:

```json
{
  "schema_version": "hard-case-review-batch-v1",
  "selected_count": 2,
  "counts_by_city": {"lyon": 1, "paris": 1},
  "counts_by_status": {"low_confidence": 1, "not_found": 1}
}
```

## Critères validés

- Sélectionne uniquement les lignes non résolues (`user_feedback` vide ou `unknown`).
- Trie par priorité décroissante puis ancienneté/scan_id pour une file déterministe.
- Applique des plafonds `--max-per-city` et `--max-per-status` pour diversifier la revue humaine.
- Produit un JSON compact sans image, embedding, coordonnées précises ni appel réseau.
- Rejette les limites non positives avant écriture.
