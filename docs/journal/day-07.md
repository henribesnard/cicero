# Cicero — Rapport quotidien J7

## Réalisé aujourd'hui
- Story traitée: **OFF-2** (incrément logique hors-ligne).
- Ajout d'un module de bundle local permettant au client de stocker `embeddings_index` + `monument_cards` après téléchargement ville.
- Reconnaissance locale disponible sans appel API avec statuts `matched`, `low_confidence`, `not_found` et mêmes seuils que le serveur.
- Lecture de fiche monument depuis le bundle local sans réseau.
- Chat marqué explicitement indisponible hors-ligne: `Le chat nécessite une connexion réseau.`
- Mise à jour de `docs/api.md` et création du rapport de test J7.

## Tests
- Commande: `pytest -q`
- Résultat: `24 passed in 0.96s`

## Blocages
- Aucun blocage technique pour cet incrément.

## Suite proposée (ordre backlog)
1. Démarrer **FIC-2**: fallback multilingue complet et contrat documenté/testé côté fiches.
2. Préparer ensuite **USR-1** ou **SEC-2** selon disponibilité du socle client.
