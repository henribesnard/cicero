# Day 33 — Santé VPS et mode léger

## Décision du run

Le run reste en mode léger car la RAM libre est sous 800 MiB. Aucun build lourd, téléchargement massif, publication ou suppression n'a été lancé.

## Actif produit

Création de `backend/tools/report_vps_health.py`, un outil léger de diagnostic des garde-fous cron : charge, mémoire, disque, réserve 10%, statut d'exécution et recommandations.

## Validation

- `python3 -m pytest backend/tests/test_report_vps_health.py -q` → `4 passed in 0.05s`
- `python3 backend/tools/report_vps_health.py` → statut réel `light`, disque `69.7% used`, recommandation mode léger.

## Intérêt produit/business

Cet outil transforme une règle opérationnelle manuelle en contrôle réutilisable. Il réduit le risque de lancer des actions coûteuses sur un VPS contraint et prépare une base propre pour automatiser les rapports d'exploitation sans toucher au serveur web.

## Prochain pas léger

Brancher ce diagnostic dans les scripts de reporting existants pour générer un résumé unique `health + cleanup candidates`, toujours en `report-only`.
