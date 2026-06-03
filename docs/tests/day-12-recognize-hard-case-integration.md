# Cicero — Rapport QA J12 — Intégration HardCaseLogger / Recognize

## Objectif
Valider l'intégration **ML-4 / INFRA-2** entre `POST /v1/recognize` et `HardCaseLogger`: seuls les cas `low_confidence` et `not_found` doivent être journalisés, sous forme de métadonnées sûres pour la confidentialité.

## Périmètre testé
- Contrat existant `POST /v1/recognize` inchangé côté réponse publique (`request_id`, `status`, `matches`).
- Journalisation automatique des cas difficiles avec `scan_id = request_id`.
- Non-journalisation des reconnaissances `matched`.
- Conservation de métadonnées uniquement: statut, score, `model_version`, `city_id` optionnel, candidat éventuel.
- Validation de `city_id` optionnel non vide.
- Non-régression du logger autonome.

## Commandes exécutées
```bash
pytest -q backend/tests/test_hard_case_logger.py backend/tests/test_recognize.py
pytest -q backend/tests
```

## Résultats exacts
```text
...........                                                              [100%]
11 passed in 0.91s
```

```text
.........................................                                [100%]
41 passed in 1.05s
```

## Verdict
Incrément accepté. Le prototype ML-4 dispose maintenant d'une capture automatique des cas difficiles depuis le flux serveur de reconnaissance, sans stockage d'image, d'embedding brut ni de position précise.
