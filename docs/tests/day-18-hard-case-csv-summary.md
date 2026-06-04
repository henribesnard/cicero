# Cicero — Rapport QA J18: synthèse CSV des hard cases

## Objectif

Valider un outil léger qui transforme le CSV de revue `hard-cases-v1` en résumé JSON exploitable par l'équipe produit/ops, sans image, embedding brut ni localisation précise.

## Actifs validés

- `backend/tools/summarize_hard_cases_csv.py`
- `backend/tests/test_summarize_hard_cases_csv.py`

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest -q tests/test_summarize_hard_cases_csv.py tests/test_export_hard_cases_csv.py
```

Résultat:

```text
4 passed in 0.22s
```

Démonstrateur local:

```bash
python tools/export_hard_cases_csv.py /tmp/cicero-hard-cases-sample-day18.jsonl /tmp/cicero-hard-cases-review-day18.csv
python tools/summarize_hard_cases_csv.py /tmp/cicero-hard-cases-review-day18.csv /tmp/cicero-hard-cases-summary-day18.json
```

Résultat:

```text
exported 3 hard-case record(s) to /tmp/cicero-hard-cases-review-day18.csv
summarized 3 hard-case record(s) to /tmp/cicero-hard-cases-summary-day18.json
```

Extrait vérifié:

```json
{
  "record_count": 3,
  "counts_by_status": {"low_confidence": 1, "not_found": 2},
  "counts_by_feedback": {"poor_angle": 1, "unknown": 1, "unlabeled": 1},
  "top_cities": [["paris", 2], ["lyon", 1]],
  "top_unresolved": ["scan-miss", "scan-empty-feedback"]
}
```

## Conclusion

L'outil est compatible mode léger VPS et complète la boucle ML-4: JSONL → CSV revue → synthèse priorisée → décision de correction avant actions coûteuses.
