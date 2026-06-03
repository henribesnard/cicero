# Cicero — QA J13 — endpoint export hard-cases ML-4

## Périmètre
- Vérification de l'endpoint authentifié `GET /v1/hard-cases/export`.
- Validation que deux scans incertains (`low_confidence`, `not_found`) alimentent l'export `hard-cases-v1`.
- Contrôle des garanties privacy: aucune image brute, aucun embedding brut, aucune position précise.

## Commandes exécutées
```bash
pytest -q backend/tests/test_hard_case_logger.py backend/tests/test_recognize.py
pytest -q backend/tests
```

## Résultats
- `12 passed in 0.95s`
- `42 passed in 1.04s`

## Points validés
1. L'endpoint renvoie `request_id`, `schema_version`, `record_count`, agrégats par statut et file de revue priorisée.
2. L'ordre `review_queue` priorise le `not_found` avant le `low_confidence` dans le scénario testé.
3. L'export reste exploitable pour revue/réindexation sans stockage d'image, embedding brut ni localisation précise.
4. La suite backend complète reste verte après ajout de l'endpoint.
