# Cicero — Runbook revue des cas difficiles ML-4

Objectif: transformer la file locale `hard-cases-v1` en boucle d'amélioration exploitable sur VPS modeste, sans stocker d'image brute, d'embedding brut ni de position précise.

## Entrées

- JSONL local optionnel: chemin configuré par `CICERO_HARD_CASES_JSONL_PATH`.
- Schéma attendu par ligne: `scan_id`, `status`, `score`, `created_at`, `model_version`, `city_id` optionnel, `candidate_monument_id` optionnel, `user_feedback` optionnel, `notes` optionnel.
- Labels autorisés: `correct`, `wrong_monument`, `unknown`, `poor_angle`, `too_dark`, `other`.

## Export CSV de revue

Depuis `backend/`:

```bash
python tools/export_hard_cases_csv.py "$CICERO_HARD_CASES_JSONL_PATH" /tmp/cicero-hard-cases-review.csv
```

Colonnes CSV produites:

```text
review_priority,scan_id,status,score,created_at,model_version,city_id,candidate_monument_id,user_feedback,notes
```

Tri: priorité décroissante, puis `created_at`, puis `scan_id`. La priorité favorise les `not_found`, scores faibles, feedbacks ambigus/erreurs et cas rattachés à une ville/candidat.

## Revue humaine minimale

1. Ouvrir le CSV localement ou dans un tableur privé.
2. Traiter d'abord `review_priority >= 70`.
3. Renseigner `user_feedback` et `notes` avec une phrase courte et factuelle.
4. Ne pas ajouter d'image, d'URL personnelle, de coordonnées précises ni d'informations utilisateur.

## Synthèse actionnable post-revue

Après export CSV ou après annotation partielle, générer un résumé JSON local:

```bash
python tools/summarize_hard_cases_csv.py /tmp/cicero-hard-cases-review.csv /tmp/cicero-hard-cases-summary.json
```

Le résumé produit:

```text
record_count, counts_by_status, counts_by_feedback, top_cities, top_city_status_pairs, top_unresolved
```

Usage produit: identifier les villes/statuts qui concentrent les échecs, puis décider d'une correction légère avant toute réindexation coûteuse: enrichissement fiche monument, photos d'angles manquants, seuil de confiance local ou collecte terrain ciblée.

## Validation avant réinjection

Avant tout appel API de feedback, valider le CSV annoté localement:

```bash
python tools/validate_hard_cases_csv.py /tmp/cicero-hard-cases-review.csv
```

Sortie compacte attendue si le fichier est réinjectable:

```text
valid: 12 row(s), 8 annotated, 0 error(s), 0 warning(s)
```

Pour CI, automatisation locale sans effet de bord ou contrôle strict avant batch complet:

```bash
python tools/validate_hard_cases_csv.py /tmp/cicero-hard-cases-review.csv --json
python tools/validate_hard_cases_csv.py /tmp/cicero-hard-cases-review.csv --require-all-annotated --json
```

`--require-all-annotated` transforme toute ligne sans `user_feedback` en erreur bloquante; utile juste avant une réinjection batch pour éviter de croire qu'un CSV partiellement revu est complet.

Le validateur vérifie le header, les `scan_id` vides ou dupliqués, les statuts, les labels `user_feedback`, les scores/priorités bornés et signale les notes trop longues. Il ne modifie pas le JSONL et n'appelle pas l'API.

## Préparation dry-run des payloads feedback

Avant toute réinjection réelle, générer un JSONL inspectable contenant uniquement les lignes annotées:

```bash
python tools/prepare_hard_case_feedback_payloads.py /tmp/cicero-hard-cases-review.csv /tmp/cicero-feedback-payloads.jsonl
```

Sortie compacte attendue:

```text
prepared 8 feedback payload(s) to /tmp/cicero-feedback-payloads.jsonl
```

Chaque ligne JSON contient `scan_id`, `method`, `path` et `payload`; le script valide le CSV en amont, ignore les lignes non annotées par défaut et ne fait aucun appel réseau. Ajouter `--require-all-annotated` pour bloquer si une ligne reste sans label avant batch complet.

## Pipeline local complet sans effet API

Pour éviter les erreurs de manipulation entre les étapes ops, lancer toute la chaîne locale en dry-run:

```bash
python tools/run_hard_case_review_pipeline.py /tmp/cicero-hard-cases-review.csv /tmp/cicero-hardcase-ops
```

Artefacts produits dans le répertoire de sortie:

```text
hard-case-summary.json
hard-case-review-batch.json
hard-case-review-sheet.md
hard-case-feedback-payloads.jsonl
hard-case-review-capacity.json
```

Sortie compacte attendue:

```text
pipeline ok: 42 row(s), 18 annotated, 20 selected, capacity 24 unresolved, 18 payload(s) to /tmp/cicero-hardcase-ops
```

Le pipeline exécute `validate → summarize → select-batch → export-review-markdown → report-capacity → prepare-payloads`; si la validation échoue, aucun artefact métier n'est écrit. Le batch JSON inclut `review_effort_minutes` par cas et `estimated_review_effort_minutes` au total; le rapport capacité dimensionne les sessions 30/60/120 minutes par défaut sans inspecter d'image ni lancer de modèle. Il reste volontairement sans appel réseau, sans mutation du JSONL source et sans réinjection API. Options utiles: `--batch-limit`, `--max-per-city`, `--max-per-status`, `--capacity-budgets 45,90,180`, `--require-all-annotated`, `--json`.

## Fiche Markdown imprimable

Pour produire uniquement une fiche non technique à partir d'un batch JSON déjà sélectionné:

```bash
python tools/export_hard_case_review_markdown.py /tmp/cicero-hardcase-ops/hard-case-review-batch.json /tmp/cicero-hardcase-ops/hard-case-review-sheet.md
```

Sortie compacte attendue:

```text
review markdown: 20 item(s) to /tmp/cicero-hardcase-ops/hard-case-review-sheet.md
```

La fiche liste les labels autorisés, l'effort total estimé, un bloc par `scan_id`, la priorité, l'effort estimé du cas, le statut, la ville, le candidat modèle et une checklist de décision. Elle rappelle explicitement les garde-fous: aucune image brute, aucun embedding brut, aucune position précise.

## Import des décisions Markdown vers CSV annoté

Après revue de la fiche Markdown, appliquer les cases cochées au CSV source sans appel API:

```bash
python tools/import_hard_case_review_markdown.py \
  /tmp/cicero-hard-cases-review.csv \
  /tmp/cicero-hardcase-ops/hard-case-review-sheet.md \
  /tmp/cicero-hard-cases-review.annotated.csv
```

Sortie compacte attendue:

```text
imported 12 markdown decision(s) to /tmp/cicero-hard-cases-review.annotated.csv
```

Règles:
- une seule case cochée par `scan_id`; plusieurs cases cochées bloquent l'import;
- les sections non cochées sont ignorées par défaut;
- `--require-decision-for-each-section` rend obligatoire une décision pour chaque section Markdown;
- les `scan_id` absents du CSV source bloquent l'import;
- seules les colonnes `user_feedback` et `notes` sont enrichies, puis le CSV de sortie est revalidé.

## Rapport de capacité de revue

Pour planifier une session hebdomadaire de revue sans lancer de modèle:

```bash
python tools/report_hard_case_review_capacity.py \
  /tmp/cicero-hard-cases-review.csv \
  /tmp/cicero-hardcase-ops/hard-case-review-capacity.json
```

Sortie compacte attendue:

```text
review capacity: 30min=6 case(s), 60min=12 case(s), 120min=24 case(s) to /tmp/cicero-hardcase-ops/hard-case-review-capacity.json
```

Le rapport exclut les cas déjà résolus (`user_feedback` différent de vide ou `unknown`), trie les cas restants par priorité et estime l'effort avec le même calcul déterministe que le sélecteur de batch. Budgets personnalisés: `--budgets 45,90,180`.

## Réinjection feedback via API locale

Après génération de `/tmp/cicero-feedback-payloads.jsonl`, valider le batch en dry-run (aucun appel réseau, aucun effet API):

```bash
python tools/apply_hard_case_feedback_payloads.py /tmp/cicero-feedback-payloads.jsonl
```

Sortie compacte attendue:

```text
dry-run ok: 8 feedback payload(s) validated, 0 sent
```

Réinjection réelle uniquement sur action opérateur explicite, avec URL et jeton Bearer fournis:

```bash
python tools/apply_hard_case_feedback_payloads.py \
  /tmp/cicero-feedback-payloads.jsonl \
  --apply \
  --base-url http://localhost:8000 \
  --bearer-token "$CICERO_API_BEARER_TOKEN"
```

Le script refuse par défaut les champs sensibles (`image`, `embedding`, coordonnées), vérifie les labels, le couple `scan_id`/`path`, les doublons, et n'envoie rien sans `--apply`.

Appel manuel unitaire équivalent, à réserver au debug:

```bash
curl -sS -X POST "http://localhost:8000/v1/hard-cases/${SCAN_ID}/feedback" \
  -H "Content-Type: application/json" \
  -d '{"user_feedback":"wrong_monument","notes":"confusion façade latérale"}'
```

## Critères de passage MVP → produit

- Au moins 30 cas revus sans donnée sensible.
- Top 3 causes d'échec identifiées par ville ou monument.
- Une action d'amélioration définie: enrichir fiche, ajouter angles photos, ajuster index local ou seuils.

## Garde-fous VPS/quota

- Export CSV, revue, validation CSV et synthèse CSV → JSON: légers, acceptables en mode RAM basse.
- Réindexation, génération d'embeddings ou appels modèle payants: ne pas lancer automatiquement; noter `Besoin update quota manuel Henri` avant exécution.
- Si disque racine dépasse 70%, faire uniquement un ménage non destructif proposé/validé; ne pas toucher au serveur web.
