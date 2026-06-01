# SQL schema (KB-1 minimal)

Ce dossier contient le schéma PostgreSQL initial de Cicero.

## Appliquer le script

Depuis la racine du repo :

```bash
psql "$DATABASE_URL" -f backend/sql/001_init.sql
```

Ou avec des paramètres explicites :

```bash
psql -h <host> -U <user> -d <database> -f backend/sql/001_init.sql
```
