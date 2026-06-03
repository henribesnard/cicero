# Tests — J6 OFF-1 manifeste paquet hors-ligne

## Portée
- `GET /v1/cities/{id}/package`
- Enrichissement OFF-1 du manifeste de téléchargement ville
- Non-régression des endpoints API J1/J2 existants

## Commande
- `pytest -q`

## Résultat
- `20 passed in 1.62s`

## Cas couverts ajoutés
- Le contrat paquet ville expose les métadonnées nécessaires à l'affichage avant téléchargement: ville, pays, version paquet, version modèle, URL, taille totale, checksum, nombre de monuments, date de génération.
- Le manifeste liste les composants stockables localement: index d'empreintes et fiches monument.
- La somme des tailles de composants égale `size_bytes`, pour permettre un affichage fiable de la taille avant téléchargement.
