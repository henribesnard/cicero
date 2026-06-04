# Day 34 — Synthèse ops guardrails (mode léger)

## Contexte

- Le VPS est encore en mode léger : RAM libre/disponible sous le seuil de confort cron.
- Objectif du run : brancher le diagnostic santé VPS dans les rapports de candidats de nettoyage pour produire une synthèse unique `health + cleanup candidates`, sans action destructive.

## Changement validé

`backend/tools/report_ops_guardrails.py` ajoute un rapport `report-only` combinant :

- santé cron (`status=normal|light`, charge, RAM, disque) ;
- volume total des candidats conservateurs de nettoyage ;
- top candidats actionnables filtrés par taille ;
- recommandations compactes pour le rapport quotidien.

## Preuves d'exécution

```bash
python3 -m pytest backend/tests/test_report_ops_guardrails.py backend/tests/test_report_vps_health.py backend/tests/test_report_safe_cleanup_candidates.py -q
```

Résultat ciblé :

```text
...........                                                              [100%]
11 passed in 0.11s
```

```bash
python3 -m pytest backend/tests -q
```

Résultat suite backend :

```text
........................................................................ [ 69%]
...............................                                          [100%]
103 passed in 2.84s
```

```bash
python3 backend/tools/report_ops_guardrails.py --top-cleanup 3 --min-cleanup-size-mb 100
```

Résultat :

```text
ops guardrails: status=light, ram_free=137 MiB, ram_available=737 MiB, disk=69.7% used, cleanup_candidates=4581 MiB, report-only
- Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds.
- Revoir 3 candidat(s) de nettoyage non destructif avant tout ménage manuel.
- cleanup 2181 MiB	/home/hermes/.cache	candidate: inspect before manual cleanup
- cleanup 1617 MiB	/var/log	candidate: inspect before manual cleanup
- cleanup 738 MiB	/home/hermes/.npm	candidate: inspect before manual cleanup
```

## Garde-fous

- Rapport strictement non destructif (`report-only`).
- Les chemins web/serveur restent exclus par le rapport de nettoyage sous-jacent.
- La synthèse recommande une revue manuelle, pas une suppression automatique.
