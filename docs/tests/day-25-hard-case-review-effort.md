# Cicero — QA day-25 — Estimation effort revue hard-cases

## Périmètre

Ajout d'une estimation locale et privacy-safe de l'effort humain de revue pour chaque cas difficile sélectionné. Objectif: transformer un batch ML-4 en charge opérateur prévisible, sans appel modèle, sans image brute, sans embedding et sans donnée de localisation précise.

## Actifs modifiés

- `backend/tools/select_hard_case_review_batch.py`
- `backend/tools/export_hard_case_review_markdown.py`
- `backend/tests/test_select_hard_case_review_batch.py`
- `backend/tests/test_export_hard_case_review_markdown.py`
- `docs/ops/hard-case-review.md`
- `docs/api.md`
- `docs/journal/day-25.md`
- `docs/project-register.md`

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_select_hard_case_review_batch.py tests/test_export_hard_case_review_markdown.py -q
python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py tests/test_export_hard_case_review_markdown.py -q
```

Résultats finaux observés:

```text
.........                                                                [100%]
9 passed in 0.39s
..................................                                       [100%]
34 passed in 1.52s
```

## Critères validés

- Chaque item de `hard-case-review-batch-v1` expose `review_effort_minutes`.
- Le batch expose `estimated_review_effort_minutes`, somme des efforts sélectionnés.
- L'estimation reste déterministe et légère: base 3 minutes, surcoûts bornés selon statut, feedback `unknown`, candidat modèle et notes existantes; plafond à 8 minutes par cas.
- La fiche Markdown imprimable affiche l'effort total et l'effort par cas pour planifier une session de revue.
- Aucun appel réseau, aucun modèle, aucune mutation API.
