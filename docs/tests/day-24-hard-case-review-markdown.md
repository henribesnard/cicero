# Cicero — Tests J24 — export Markdown revue cas difficiles

## Objet

Valider l'ajout d'une fiche Markdown imprimable et non technique pour la revue humaine des cas difficiles ML-4, intégrée au pipeline local dry-run.

## Couverture

- `backend/tools/export_hard_case_review_markdown.py`:
  - rendu Markdown avec contexte confidentialité et checklist de labels;
  - écriture du fichier de sortie;
  - rejet d'un mauvais `schema_version`;
  - contrat CLI compact.
- `backend/tools/run_hard_case_review_pipeline.py`:
  - génération automatique de `hard-case-review-sheet.md` en plus des artefacts JSON/JSONL existants;
  - présence du `scan_id` sélectionné et du rappel confidentialité dans la fiche.

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_export_hard_case_review_markdown.py tests/test_run_hard_case_review_pipeline.py -q
```

Résultat:

```text
7 passed in 0.40s
```

Non-régression ops hard cases:

```bash
python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py -q
```

Résultat:

```text
33 passed in 1.71s
```

## Démonstration CLI

```bash
python tools/run_hard_case_review_pipeline.py /tmp/cicero-hardcase-md-demo-review.csv /tmp/cicero-hardcase-md-demo-out
python tools/export_hard_case_review_markdown.py /tmp/cicero-hardcase-md-demo-out/hard-case-review-batch.json /tmp/cicero-hardcase-md-demo-out/review-sheet-standalone.md
```

Résultat:

```text
pipeline ok: 2 row(s), 1 annotated, 1 selected, 1 payload(s) to /tmp/cicero-hardcase-md-demo-out
review markdown: 1 item(s) to /tmp/cicero-hardcase-md-demo-out/review-sheet-standalone.md
```

Extrait vérifié de `hard-case-review-sheet.md`:

```text
# Cicero — Fiche de revue cas difficiles
- Cas sélectionnés: 1 / non résolus: 1 / total CSV: 2
- Confidentialité: aucune image brute, aucun embedding brut, aucune position précise dans cette fiche.
### 1. `scan-demo-open` — priorité 92
```
