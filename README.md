# Cicero

Application mobile de reconnaissance de monuments touristiques.

## Sources de vérité
Voir `docs/source/` pour les documents fournis par le responsable produit.

## Structure initiale
- `backend/` : API FastAPI (socle)
- `mobile/` : app Flutter (à initialiser)
- `docs/` : ADR, journal, tests, design

## Lancer les tests backend
```bash
cd backend
pip install -r requirements.txt
pytest -q
```
