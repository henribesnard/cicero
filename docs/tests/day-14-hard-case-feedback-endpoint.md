# Cicero — QA J14: endpoint feedback hard-cases

## Objet
Validation de ML-5: annotation interne d'un cas difficile existant via `POST /v1/hard-cases/{scan_id}/feedback`.

## Couverture ajoutée
- `HardCaseLogger.annotate(...)` met à jour `user_feedback` et `notes` sans stocker image, embedding brut ni position précise.
- Rejet d'un `scan_id` inconnu.
- Rejet d'un label non autorisé.
- Test d'intégration FastAPI: génération d'un hard case `low_confidence`, annotation via endpoint authentifié, puis vérification des agrégats `counts_by_feedback`.

## Commandes exécutées
- `pytest -q backend/tests/test_hard_case_logger.py backend/tests/test_recognize.py`
  - Résultat: `17 passed in 0.96s`
- `pytest -q backend/tests`
  - Résultat: `47 passed in 1.21s`

## Conclusion
ML-5 est validé côté MVP backend: la boucle reconnaissance difficile → revue humaine → export priorisé est maintenant exploitable sans collecte de données sensibles lourdes.
