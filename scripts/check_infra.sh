#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/infra/docker-compose.yml"
ENV_FILE="$ROOT_DIR/infra/.env"

if [ ! -f "$ENV_FILE" ]; then
  ENV_FILE="$ROOT_DIR/infra/.env.example"
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "[WARN] docker introuvable dans le PATH."
  echo "[INFO] Vérification docker compose ignorée."
  exit 0
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "[WARN] Docker Compose plugin indisponible (commande: docker compose)."
  echo "[INFO] Vérification de la syntaxe compose ignorée."
  exit 0
fi

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "[ERROR] Fichier compose introuvable: $COMPOSE_FILE"
  exit 1
fi

echo "[INFO] Docker Compose plugin détecté."
echo "[INFO] Validation du compose: $COMPOSE_FILE"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" config >/dev/null

echo "[OK] Validation réussie."
