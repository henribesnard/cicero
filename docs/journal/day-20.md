# Cicero — Rapport quotidien J20

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops review** — ajout d'un mode de validation stricte pour les CSV hard-cases avant réinjection batch.
- Option CLI ajoutée: `--require-all-annotated` dans `backend/tools/validate_hard_cases_csv.py`.
- Tests ajoutés: couverture fonctionnelle Python + retour CLI non-zéro quand une ligne n'est pas annotée.
- Runbook ops mis à jour avec la commande stricte.

## Tests

- Commande depuis `backend/`: `python -m pytest -q tests/test_validate_hard_cases_csv.py` → `6 passed in 0.46s`.
- Démonstrateur CLI: CSV temporaire avec `user_feedback` vide + `--require-all-annotated --json` → `returncode=1`, `valid=false`, erreur `row 2: user_feedback must be annotated`.

## Blocages

- Mode léger appliqué: RAM libre basse au démarrage (`free=151 MiB`, `available=883 MiB`); pas d'appel modèle, pas d'embeddings, pas de veille web lourde.
- Disque racine à 70%; seuil strict `>70%` non franchi, mais marge faible à surveiller.

## Suite proposée

1. Ajouter un `--min-annotation-rate` au validateur pour bloquer uniquement si le taux de revue est insuffisant (ex. 80%), plus souple que le mode strict.
2. Préparer `apply_feedback_from_csv.py` en dry-run par défaut pour générer les payloads API sans les envoyer.
