# Cicero — QA J11 — ML-4 Hard Case Logger

## Objectif
Valider un premier actif léger pour **ML-4 / INFRA-2**: journaliser les scans difficiles (`low_confidence`, `not_found`) sans collecter d'image, d'empreinte brute ni de position précise.

## Périmètre testé
- Module: `backend/app/hard_case_logger.py`
- Tests: `backend/tests/test_hard_case_logger.py`

## Cas couverts
1. Enregistrement d'un cas `low_confidence` avec métadonnées utiles au tri/retraining.
2. Rejet explicite des statuts non difficiles (`matched`) et feedbacks hors taxonomie.
3. Export batch `hard-cases-v1` avec agrégats par statut/feedback.
4. File de revue priorisée (`review_queue`) pour sélectionner les cas à corriger/réindexer en premier.
5. Garanties privacy dans l'export: pas d'image brute, pas d'embedding brut, pas de GPS précis.
6. File bornée + purge locale.
7. Filtrage par statut pour revue humaine.

## Commande exécutée
```bash
pytest -q backend/tests/test_hard_case_logger.py
```

## Résultat
```text
5 passed in 0.04s
```

## Décision QA
Incrément accepté pour prototype local. Prochaine étape recommandée: brancher ce logger sur la réponse `POST /v1/recognize` uniquement si statut `low_confidence` ou `not_found`, avec stockage local/serveur configurable et opt-in utilisateur à documenter.
