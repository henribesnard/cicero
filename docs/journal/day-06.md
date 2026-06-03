# Cicero — Rapport quotidien J6

## Réalisé aujourd'hui
- Story traitée: **OFF-1** (incrément backend du téléchargement paquet ville).
- `GET /v1/cities/{id}/package` enrichi en manifeste hors-ligne: métadonnées ville, version de paquet, checksum SHA-256, date de génération et composants.
- Le manifeste expose les deux composants attendus pour le stockage local: `embeddings_index` et `monument_cards`.
- La taille totale du paquet reste affichable avant téléchargement et est vérifiée par test comme somme des composants.
- Mise à jour de `docs/api.md` et création du rapport de test J6.

## Tests
- Commande: `pytest -q`
- Résultat: `20 passed in 1.62s`

## Blocages
- Aucun blocage technique pour cet incrément.

## Suite proposée (ordre backlog)
1. Démarrer **OFF-2** côté logique de cache/contrats: lecture reconnaissance + fiche depuis paquet local.
2. Préparer ensuite **FIC-2** ou **USR-1** selon disponibilité du socle client/cache.
