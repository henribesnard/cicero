# Cicero — Tests J30 · Rapport de contrôles SEC-2

## Objet

Ajouter un contrôle read-only des garde-fous RGPD/SEC-2 déjà présents dans le backend MVP: non-persistance du chat, purge/effacement du carnet local, file hard-cases bornée et sans signaux sensibles.

## Actifs livrés

- Script: `backend/tools/report_privacy_retention_controls.py`.
- Test: `backend/tests/test_report_privacy_retention_controls.py`.
- Documentation: `docs/api.md` section "Rapport de contrôles SEC-2".

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_report_privacy_retention_controls.py -q
```

Résultat:

```text
1 passed in 1.37s
```

Smoke CLI:

```bash
python tools/report_privacy_retention_controls.py --pretty
```

Résultat vérifié:

- `schema_version = privacy-retention-controls-v1`;
- `readiness.sec_2_minimum_controls_present = true`;
- chat: `retention = session_only_client_side`, `server_persists_conversation_history = false`, `max_context_messages_used = 12`;
- carnet: `retention_days = 365`, purge sélective et effacement complet disponibles;
- hard-cases: `max_records = 500`, effacement complet disponible, `stores_metadata_only = true`.

## Limites connues

- Ce rapport prouve les garde-fous code MVP, pas la conformité juridique finale.
- Avant production: aligner wording politique de confidentialité, identité utilisateur pour compte/sync, SLA d'effacement.
