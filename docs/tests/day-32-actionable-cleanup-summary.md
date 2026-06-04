# Day 32 — Rapport actionnable nettoyage disque (mode léger)

## Contexte

- Le VPS est en mode léger sur ce run : RAM disponible sous 800 MiB.
- Le disque racine est proche du seuil d'alerte 70%, donc l'objectif est de produire un diagnostic non destructif, compact et directement exploitable.

## Changement validé

`backend/tools/report_safe_cleanup_candidates.py` ajoute deux options CLI de filtrage en sortie texte :

- `--top N` : limite le nombre de candidats affichés.
- `--min-size-mb N` : masque les petits candidats dans la synthèse texte.

Le JSON complet reste inchangé : aucune perte d'information pour l'audit ou l'automatisation future.

## Preuves d'exécution

```bash
python3 -m pytest backend/tests/test_report_safe_cleanup_candidates.py -q
```

Résultat :

```text
.....                                                                    [100%]
5 passed in 0.05s
```

```bash
python3 backend/tools/report_safe_cleanup_candidates.py --top 3 --min-size-mb 100
```

Résultat :

```text
safe cleanup report: disk 69.7% used, 4581 MiB candidate(s), report-only
- 2181 MiB	/home/hermes/.cache	candidate: inspect before manual cleanup
- 1615 MiB	/var/log	candidate: inspect before manual cleanup
- 738 MiB	/home/hermes/.npm	candidate: inspect before manual cleanup
```

## Garde-fous

- Le script reste strictement `report-only` : aucune suppression.
- Les chemins web/serveur restent exclus des candidats.
- Toute suppression éventuelle doit rester manuelle et arbitrée.
