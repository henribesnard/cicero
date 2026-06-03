# Tests — J7 OFF-2 bundle local hors-ligne

## Portée
- Contrat de bundle local OFF-2 dérivé du paquet ville.
- Reconnaissance locale sans client API.
- Lecture de fiche monument locale sans client API.
- Signalement explicite du chat indisponible hors-ligne.
- Non-régression des endpoints API existants.

## Commande
- `pytest -q`

## Résultat
- `24 passed in 0.96s`

## Cas couverts ajoutés
- Le bundle local contient `embeddings_index` et `monument_cards`, avec `model_version`, `package_version` et capacités hors-ligne.
- Le parcours reconnaissance locale → fiche locale fonctionne sans `TestClient` ni appel réseau.
- Les états `matched`, `low_confidence` et `not_found` sont conservés en mode hors-ligne.
- Une ville inconnue et une empreinte invalide sont rejetées explicitement.
