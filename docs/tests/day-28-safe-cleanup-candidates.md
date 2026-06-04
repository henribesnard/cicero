# Cicero — Test J28 diagnostic disque non destructif

## Objectif

Ajouter un outil léger pour identifier des candidats de ménage disque sans suppression automatique, sans toucher aux chemins serveur web, et utilisable quand le disque racine approche le seuil opérationnel.

## Commandes exécutées

Depuis `backend/`:

```bash
python -m pytest tests/test_report_safe_cleanup_candidates.py -q
```

Résultat:

```text
3 passed in 0.06s
```

Smoke test CLI:

```bash
python tools/report_safe_cleanup_candidates.py
```

Résultat observé sur le VPS:

```text
safe cleanup report: disk 69.7% used, 4569 MiB candidate(s), report-only
- 2181 MiB	/home/hermes/.cache	candidate: inspect before manual cleanup
- 1603 MiB	/var/log	candidate: inspect before manual cleanup
- 738 MiB	/home/hermes/.npm	candidate: inspect before manual cleanup
- 38 MiB	/home/hermes/.cache/pip	candidate: inspect before manual cleanup
- 8 MiB	/tmp	candidate: inspect before manual cleanup
```

## Couverture

- Exclusion explicite des chemins web/serveur communs (`/var/www`, `/srv/www`, `/srv/http`, `/etc/nginx`, `/etc/apache2`).
- Mode rapport uniquement: aucune suppression.
- Tri décroissant par taille estimée.
- Résilience aux répertoires larges contenant des fichiers non lisibles: taille `du` exploitée quand disponible.

## Décision

Outil validé pour proposer un ménage manuel non destructif lorsque `/` dépasse 70%, sans action irréversible ni impact serveur web.
