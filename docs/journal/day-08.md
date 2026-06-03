# Cicero — Rapport quotidien J8

## Réalisé aujourd'hui
- Stories traitées: **FIC-2** et **USR-1**.
- FIC-2: fiche monument multilingue renforcée sur `GET /v1/monuments/{id}` avec `lang`, `available_langs` et fallback explicite vers `fr`.
- FIC-2 hors-ligne: le bundle local respecte la langue demandée (`fr`/`en`) et indique le fallback quand nécessaire.
- USR-1: ajout d'un modèle local de carnet de voyage enregistrant monument, date, score et statut, avec consultation triable par date.
- Mise à jour de `docs/api.md` et création du rapport de test J8.

## Tests
- Commande: `pytest -q`
- Résultat: `29 passed in 1.08s`

## Blocages
- Aucun blocage technique pour cet incrément.

## Suite proposée (ordre backlog)
1. Démarrer **SEC-2**: bornage de conservation/suppression des données de conversation et carnet.
2. Préparer ensuite **ML-4** ou les enrichissements OFF-3 selon dépendances disponibles.
