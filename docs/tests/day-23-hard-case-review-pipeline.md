# Cicero — QA J23 — Pipeline local revue hard cases

## Périmètre

Story avancée: **ML-4 / Ops review** — chaînage local dry-run des étapes de revue des cas difficiles.

Nouveau script testé: `backend/tools/run_hard_case_review_pipeline.py`.

Le pipeline exécute, sans appel réseau ni mutation du JSONL source:

1. validation du CSV annoté;
2. synthèse JSON actionnable;
3. sélection bornée/diversifiée des cas non résolus;
4. préparation JSONL des payloads feedback déjà annotés.

## Tests automatisés

Commande depuis `backend/`:

```bash
python -m pytest tests/test_run_hard_case_review_pipeline.py -q
```

Résultat réel:

```text
3 passed in 0.21s
```

Contrôles couverts:

- écriture des 3 artefacts dry-run (`summary`, `review-batch`, `feedback-payloads`);
- blocage validation invalide sans artefact métier;
- contrat CLI compact.

## Non-régression hard-case ops

Commande depuis `backend/`:

```bash
python -m pytest tests/test_*hard_case*.py tests/test_validate_hard_cases_csv.py tests/test_summarize_hard_cases_csv.py tests/test_prepare_hard_case_feedback_payloads.py tests/test_select_hard_case_review_batch.py tests/test_run_hard_case_review_pipeline.py -q
```

Résultat réel:

```text
29 passed in 1.65s
```

## Démonstration CLI

Commande exécutée sur CSV synthétique local:

```bash
python tools/run_hard_case_review_pipeline.py /tmp/cicero-hardcase-pipeline-demo/review.csv /tmp/cicero-hardcase-pipeline-demo/out --batch-limit 5
```

Résultat réel:

```text
pipeline ok: 2 row(s), 1 annotated, 1 selected, 1 payload(s) to /tmp/cicero-hardcase-pipeline-demo/out
['hard-case-feedback-payloads.jsonl', 'hard-case-review-batch.json', 'hard-case-summary.json']
1
1
```

## Verdict

OK pour usage ops local: la chaîne réduit le risque d'oubli d'étape avant revue/réinjection, tout en restant compatible VPS modeste et privacy-safe.
