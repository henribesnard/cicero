# ADR-001 — Backbone vision, dimension d'empreinte et versioning

- **Statut**: Accepté
- **Date**: 2026-06-01
- **Décideurs**: Architecte + Hermès

## Contexte
Le cahier des charges impose la cohérence stricte entre modèle embarqué, cache local et base vectorielle (`D` + `model_version`).

## Décision
1. **Backbone initial**: `MobileNetV3-Large` (priorité vitesse on-device Android).
2. **Dimension embedding (`D`)**: `256`.
3. **Version modèle**: format semver `vision-lite-<major>.<minor>.<patch>` ; version initiale `vision-lite-1.0.0`.
4. **Compatibilité API**:
   - `POST /v1/recognize` refuse les versions incompatibles avec **409**.
   - Payload obligatoire: `model_version`.
5. **Migration index**:
   - En cas de changement de `D` => nouvelle collection vectorielle et reindex complet.
   - En cas de patch mineur conservant `D` => double-lecture temporaire autorisée (fenêtre de migration).

## Conséquences
- Simplifie le MVP Android (latence cible prioritaire).
- Rend explicite la stratégie de migration pour éviter la dérive des embeddings.
