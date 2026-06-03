# Cicero — Rapport quotidien J12

## Réalisé aujourd'hui
- Story avancée: **ML-4 / INFRA-2** — branchement du `HardCaseLogger` sur `POST /v1/recognize`.
- Les réponses `low_confidence` et `not_found` créent désormais automatiquement un enregistrement `hard-cases-v1` avec métadonnées sûres: `request_id`/`scan_id`, statut, score, `model_version`, `city_id` optionnel, candidat éventuel.
- Les reconnaissances `matched` ne sont pas journalisées.
- Validation de `city_id` optionnel côté payload de reconnaissance.
- Mise à jour de `docs/api.md` et ajout du rapport QA `docs/tests/day-12-recognize-hard-case-integration.md`.

## Tests
- Commande ciblée: `pytest -q backend/tests/test_hard_case_logger.py backend/tests/test_recognize.py`
- Résultat: `11 passed in 0.91s`
- Commande complète backend: `pytest -q backend/tests`
- Résultat: `41 passed in 1.05s`

## Blocages
- Aucun blocage fonctionnel.
- Point de vigilance hébergement déjà observé: VPS contraint en RAM/disque; éviter les jobs ML lourds sur cette machine.

## Suite proposée
1. Documenter le processus ML-4 de réindexation: revue humaine des cas difficiles → enrichissement dataset → recalcul embeddings → bump `package_version`.
2. Ajouter une petite interface/export sécurisé pour consulter la file `hard-cases-v1` lorsque la persistance serveur sera choisie.
