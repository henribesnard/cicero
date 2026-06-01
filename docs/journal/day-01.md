# Cicero — Rapport quotidien J1

## Décisions validées par le responsable
- Repo GitHub: https://github.com/henribesnard/cicero.git
- Stack mobile: Flutter
- LLM applicatif (V1): DeepSeek
- OS prioritaire de test: Android
- Handoff design reçu et extrait (D5)

## Réalisé aujourd'hui
- Documents source importés dans `docs/source/`.
- Handoff design extrait dans `docs/design/`.
- Registre documentaire créé et D5 passé à **Reçu et extrait**.
- ADR-001 validé (`MobileNetV3-Large`, `D=256`, `vision-lite-1.0.0`).
- Socle backend FastAPI créé (`/health`) + test unitaire.
- CI GitHub Actions minimale ajoutée (tests backend).

## Blocages
- SDK Flutter absent sur l'environnement agent actuel (`flutter: command not found`).

## Plan J2 (démarrage équipe)
1. Backend: implémenter `GET /v1/monuments/{id}` + tests (API-3).
2. Data: créer schéma Postgres initial + jeu Paris minimal (DATA-1/KB-1).
3. QA: pipeline tests unitaires/intégration (QA-1).
4. DevOps: préparer Docker compose (Postgres+PostGIS+Qdrant) et secrets baseline (SEC-3).

## Décisions attendues du responsable
- Autoriser l'installation Flutter sur l'environnement de build agent, ou fournir runner Android dédié.
