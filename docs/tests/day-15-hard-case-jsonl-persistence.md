# QA — Day 15 — Persistance JSONL des hard-cases ML-4

## Périmètre
- Story avancée: **ML-4** — boucle d'amélioration continue des cas difficiles.
- Objectif: rendre la file `hard-cases-v1` persistable sans changer le comportement MVP par défaut.

## Changements validés
- `HardCaseLogger(max_records=..., storage_path=...)` recharge les records JSONL existants.
- Chaque `record(...)`, `annotate(...)` et `clear()` réécrit la file JSONL configurée.
- La borne `max_records` est respectée au rechargement comme en mémoire.
- Le mode par défaut reste volatile si aucun `storage_path` / `CICERO_HARD_CASES_JSONL_PATH` n'est fourni.
- Les garanties privacy restent inchangées: pas d'image brute, pas d'empreinte brute, pas de localisation précise.

## Tests exécutés

```bash
pytest -q backend/tests/test_hard_case_logger.py backend/tests/test_recognize.py
```

Résultat:

```text
19 passed in 0.96s
```

```bash
pytest -q backend/tests
```

Résultat:

```text
49 passed in 1.13s
```

## Verdict
- Tests ciblés: verts.
- Suite backend complète: verte.
- Documentation API mise à jour.
