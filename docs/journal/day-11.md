# Cicero — Rapport quotidien J11

## Réalisé aujourd'hui
- Story préparée: **ML-4** (boucle d'amélioration continue) avec un prototype léger de journalisation des scans difficiles.
- Ajout de `HardCaseLogger` pour stocker uniquement des métadonnées de cas `low_confidence` / `not_found`: score, modèle, ville optionnelle, candidat optionnel, feedback taxonomisé, notes.
- Ajout d'un export `hard-cases-v1` exploitable pour revue/retraining, avec garanties explicites: aucune image brute, aucun embedding brut, aucune position précise.
- Ajout du rapport QA `docs/tests/day-11-hard-case-logger.md`.

## Tests
- Commande ciblée: `pytest -q backend/tests/test_hard_case_logger.py`
- Résultat: `5 passed in 0.04s`

## Blocages
- VPS en mode léger au démarrage du run: RAM libre stricte sous 800 Mo.
- Disque racine à 71%: proposer ménage non destructif de caches/temp/logs sûrs, sans toucher au serveur web.

## Suite proposée
1. Brancher `HardCaseLogger` à `POST /v1/recognize` pour enregistrer uniquement les statuts `low_confidence` et `not_found`.
2. Documenter le processus de réindexation ML-4: revue humaine -> enrichissement dataset -> recalcul embeddings -> bump `package_version`.
