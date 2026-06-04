# Day 33 — Rapport santé VPS automatisé (mode léger)

## Contexte

- Le VPS est en mode léger sur ce run : RAM libre sous 800 MiB.
- Le disque racine est proche mais pas au-dessus du seuil strict de 70% selon le script (`69.7%`).
- Objectif : produire un actif léger qui rend les prochains runs cron plus fiables et auditables.

## Changement validé

`backend/tools/report_vps_health.py` ajoute un diagnostic `report-only` des garde-fous d'exécution :

- charge système 1/5/15 min ;
- RAM libre et disponible ;
- occupation disque racine ;
- statut `normal` ou `light` selon les seuils cron ;
- recommandations compactes sans action destructive.

## Preuves d'exécution

```bash
python3 -m pytest backend/tests/test_report_vps_health.py -q
```

Résultat :

```text
....                                                                     [100%]
4 passed in 0.05s
```

```bash
python3 backend/tools/report_vps_health.py
```

Résultat :

```text
vps health: status=light, load=0.0/0.0/0.0, ram_free=177 MiB, ram_available=774 MiB, disk=69.7% used, report-only
- Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds.
```

## Garde-fous

- Le script ne modifie rien : diagnostic uniquement.
- Le seuil disque de ménage est strictement `>70%`, aligné avec la consigne cron.
- La réserve disque 10% est calculée et signalée si entamée.
