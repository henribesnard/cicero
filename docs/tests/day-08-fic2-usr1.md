# Cicero — Rapport de tests J8

## Stories couvertes
- **FIC-2** — Fiche multilingue: `GET /v1/monuments/{id}` respecte `lang`, expose `available_langs`, et signale le fallback `fr` quand la langue demandée n'existe pas.
- **FIC-2 hors-ligne** — Le bundle local conserve les fiches en `fr`/`en` et applique le même fallback explicite.
- **USR-1** — Carnet local: chaque scan enregistre monument, date, score, statut; liste triable par date.

## Commande exécutée
```bash
pytest -q
```

## Résultat exact
```text
29 passed in 1.08s
```

## Verdict QA
Tests verts. Les critères automatisables de FIC-2 et l'incrément local USR-1 sont validés.
