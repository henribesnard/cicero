# Infrastructure locale (INFRA-1)

Cette baseline locale démarre **Postgres + PostGIS** et **Qdrant** via Docker Compose.

## Prérequis

- Docker Engine
- Docker Compose Plugin (`docker compose`)

## Configuration

```bash
cp infra/.env.example infra/.env
```

Adaptez ensuite les variables dans `infra/.env` si nécessaire.

## Commandes utiles

Depuis la racine du repo :

```bash
# Démarrer les services
cd infra && docker compose up -d

# Voir les logs
cd infra && docker compose logs -f

# Arrêter et supprimer les conteneurs/réseau
cd infra && docker compose down
```

## Vérification rapide de la configuration

```bash
./scripts/check_infra.sh
```
