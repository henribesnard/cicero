# Cicero — Team Operations

## Rôles actifs
- Hermès (orchestrateur)
- Architecte
- Données & Vision
- Backend/API (+ IA)
- Mobile Flutter
- QA
- DevOps

## Règles de livraison
1. Une story ne passe DONE que si tests verts + critères d'acceptation validés.
2. PR obligatoire, CI verte obligatoire avant merge.
3. Commit conventionnel (`feat:`, `fix:`, `chore:`).
4. Tag jalon à chaque sortie majeure (`v0.1.0-j0`, `v0.2.0-j1-mvp`, ...).

## Démarrage quotidien
1. Lire `docs/source/*` + `docs/project-register.md`.
2. Lire dernier `docs/journal/day-*.md`.
3. Exécuter les tests de la zone modifiée.
4. Mettre à jour `docs/tests/` et `docs/journal/`.

## Plan J2 prioritaire
- API-3 (`GET /v1/monuments/{id}`)
- DATA-1 + KB-1 (seed Paris minimal)
- QA-1 (pipeline tests unitaire+intégration)
- INFRA-1 baseline locale
