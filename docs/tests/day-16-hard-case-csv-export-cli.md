# Cicero — QA J16 — export CSV des hard-cases

## Objectif
Valider un outil CLI léger qui transforme la persistance JSONL optionnelle `hard-cases-v1` en feuille CSV privacy-safe pour revue humaine.

## Périmètre vérifié
- Entrée: fichier JSONL produit par `HardCaseLogger` (`CICERO_HARD_CASES_JSONL_PATH`).
- Sortie: CSV trié par priorité de revue décroissante.
- Données exportées: métadonnées uniquement (`scan_id`, statut, score, version modèle, ville, candidat, feedback, notes) + `review_priority`.
- Données explicitement absentes: image brute, embedding brut, position GPS précise.

## Commandes exécutées
```bash
pytest -q backend/tests/test_export_hard_cases_csv.py backend/tests/test_hard_case_logger.py
```
Résultat:
```text
11 passed in 0.17s
```

```bash
python tools/export_hard_cases_csv.py "$tmpdir/hard-cases.jsonl" "$tmpdir/review.csv"
```
Résultat démonstrateur:
```text
exported 1 hard-case record(s) to /tmp/tmp.HWjWZZOBEA/review.csv
review_priority,scan_id,status,score,created_at,model_version,city_id,candidate_monument_id,user_feedback,notes
92,scan-demo,not_found,0.12,2026-06-03T14:05:00Z,vision-lite-1.0.0,paris,,unknown,
```

## Conclusion
Validation OK: l'outil permet une revue terrain/opérations sans backend lourd ni dépendance externe, avec conservation de la posture privacy-safe ML-4.
