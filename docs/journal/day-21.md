# Cicero — Rapport quotidien J21

## Réalisé aujourd'hui

- Story avancée: **ML-4 / Ops review** — préparation dry-run des payloads feedback avant réinjection API.
- Outil ajouté: `backend/tools/prepare_hard_case_feedback_payloads.py`.
- Tests ajoutés: génération uniquement des lignes annotées, absence d'écriture en cas de CSV invalide, contrat CLI compact.
- Runbook ops et spécification API mis à jour pour intégrer l'étape de payloads inspectables.

## Tests

- Commande depuis la racine du dépôt: `python -m pytest backend/tests/test_prepare_hard_case_feedback_payloads.py backend/tests/test_validate_hard_cases_csv.py -q` → `9 passed in 0.70s`.
- Premier passage a échoué sur import CLI (`ModuleNotFoundError: tools.validate_hard_cases_csv`); corrigé en ajoutant le parent `backend/` au `sys.path` quand le script est lancé directement.

## Blocages

- Mode léger appliqué: RAM libre basse au démarrage (`free=179 MiB`, `available=812 MiB`); pas d'appel modèle, pas d'embeddings, pas de veille web lourde.
- Disque racine à 70%; seuil strict `>70%` non franchi, mais `.cache` (~2.2G) et `/var/log` (~1.6G) sont des candidats de ménage non destructif si Henri valide.

## Suite proposée

1. Ajouter `--min-annotation-rate` au validateur pour accepter une revue partielle mais statistiquement suffisante (ex. 80%).
2. Préparer ensuite un script d'application réel en mode `--dry-run` par défaut et `--execute` explicite, avec validation humaine avant tout appel API.
