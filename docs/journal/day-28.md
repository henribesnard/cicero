# Cicero — Rapport quotidien J28

## Réalisé aujourd'hui

- Story avancée: **Ops VPS / garde-fou disque** — ajout d'un diagnostic de ménage non destructif pour anticiper le seuil disque sans toucher au serveur web.
- Outil ajouté: `backend/tools/report_safe_cleanup_candidates.py`.
- Tests ajoutés: `backend/tests/test_report_safe_cleanup_candidates.py`.
- Documentation ajoutée: `docs/tests/day-28-safe-cleanup-candidates.md`.

## Tests

- Commande ciblée depuis `backend/`: `python -m pytest tests/test_report_safe_cleanup_candidates.py -q` → `3 passed in 0.06s`.
- Smoke test CLI depuis `backend/`: `python tools/report_safe_cleanup_candidates.py` → `safe cleanup report: disk 69.7% used, 4569 MiB candidate(s), report-only`.

## Résultat VPS observé

- Candidats principaux détectés, sans suppression: `/home/hermes/.cache` 2181 MiB, `/var/log` 1603 MiB, `/home/hermes/.npm` 738 MiB, `/home/hermes/.cache/pip` 38 MiB, `/tmp` 8 MiB.
- Garde-fous intégrés: exclusion chemins web/serveur courants, rapport uniquement, revue manuelle obligatoire.

## Blocages

- Disque racine proche du seuil opérationnel: `df -h` affiche 70% et le diagnostic script mesure 69.7% utilisé.
- RAM disponible au démarrage: 851 MiB, au-dessus du seuil 800 MiB mais marge faible; aucune tâche lourde lancée.

## Suite proposée

1. Si Henri valide un ménage non destructif, vider uniquement caches applicatifs sûrs (`~/.cache`, `~/.npm`, pip cache) et/ou rotation logs, sans toucher au serveur web.
2. Ajouter une commande dry-run de réinjection batch depuis `hard-case-feedback-payloads.jsonl`, sans secret en dur et avec mode `--dry-run` par défaut.
