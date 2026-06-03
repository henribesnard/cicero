# Tests — J10 OFF-3 gestion des paquets hors-ligne

## Périmètre
- Story: **OFF-3 · Gestion et mise à jour des paquets**.
- Module local client simulé: `backend/app/offline_package_registry.py`.
- Contrat validé: liste des villes téléchargées, suppression locale possible, usage stockage, indicateur de mise à jour disponible.

## Commandes exécutées

```bash
pytest -q backend/tests/test_offline_package_registry.py backend/tests/test_offline_bundle.py
```

Résultat:

```text
9 passed in 0.63s
```

```bash
pytest -q
```

depuis `backend/`.

Résultat:

```text
35 passed in 1.01s
```

## Verdict QA
- Critères OFF-3 automatisés couverts:
  - liste des villes téléchargées;
  - suppression locale d'un paquet;
  - stockage utilisé/quota affichable;
  - notification logique si une version plus récente est disponible.
- Aucun endpoint serveur nouveau requis pour cet incrément; le registre local consomme le bundle OFF-2 / manifeste API-5 existant.
