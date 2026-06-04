# Cicero — Rapport quotidien J22

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops review** — sélection bornée et diversifiée des cas difficiles à annoter.
- Outil ajouté: `backend/tools/select_hard_case_review_batch.py`.
- Tests ajoutés: priorisation des non-résolus, plafonds par ville/statut, rejet des paramètres invalides, contrat CLI.
- Documentation QA ajoutée: `docs/tests/day-22-hard-case-review-batch-selection.md`.

## Tests

- Commande depuis `backend/`: `python -m pytest tests/test_select_hard_case_review_batch.py -q` → `4 passed in 0.34s`.
- Démonstration CLI sur CSV synthétique: `selected 2 of 2 unresolved hard-case row(s) to /tmp/cicero-hardcase-demo/batch.json`.

## Blocages

- Mode léger appliqué: RAM libre basse au démarrage (`free=189 MiB`, `available=844 MiB`); pas d'appel modèle, pas d'embeddings, pas de veille web lourde.
- Disque racine à 70%; seuil strict `>70%` non franchi, mais marge faible. Ménage non destructif proposé si Henri valide: caches utilisateur, caches Python/pytest anciens, rotation/logs applicatifs hors serveur web.

## Suite proposée

1. Chaîner `export → validate → summarize → select-batch → prepare-payloads` dans un runbook/CLI unique en dry-run par défaut.
2. Ajouter une métrique `annotation_effort_minutes` estimée par batch pour piloter le coût humain de ML-4.
