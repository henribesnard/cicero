# Cicero — Cahier des charges développeurs

*Application de reconnaissance de monuments touristiques*
*Document technique à destination de l'équipe de développement · Version 0.1*

---

## 1. Contexte et objectifs

Développer **Cicero**, une application mobile (Android + iOS) qui identifie un monument ou un site touristique via la caméra, affiche une fiche d'information, et permet de dialoguer avec un assistant IA à son sujet.

**Objectifs mesurables (cibles de référence à valider) :**

- Reconnaissance d'un monument présent en base en **moins de 1 s** (perçu utilisateur), traitement on-device.
- Fonctionnement **hors-ligne** pour toute ville préalablement téléchargée.
- Précision top-1 **élevée** sur les monuments en base, grâce au préfiltre géographique.
- L'app ne **prétend jamais** identifier avec certitude un monument incertain : un score de confiance est toujours exposé.

---

## 2. Périmètre

### 2.1 Inclus dans le MVP
- Capture caméra + lecture des capteurs (GPS, boussole, IMU).
- Reconnaissance on-device avec entonnoir géographique.
- Fiche d'information statique.
- Une ville pilote (Paris), quelques centaines de monuments.

### 2.2 Inclus en V1
- Assistant IA conversationnel (RAG).
- Mode hors-ligne (cache local par ville).
- Carnet de voyage, traduction du contenu.

### 2.3 Hors périmètre (à ce stade)
- Réalité augmentée avancée (overlay 3D), audioguide généré, social/partage avancé.
- Couverture mondiale automatique.

---

## 3. Glossaire

| Terme | Définition |
|---|---|
| Empreinte (embedding) | Vecteur de nombres résumant une image, produit par le modèle de vision. |
| Entonnoir géographique | Réduction des candidats via GPS + boussole avant l'analyse visuelle. |
| ANN | Recherche approximative du plus proche voisin dans la base vectorielle. |
| RAG | Retrieval-augmented generation : on fournit au LLM des faits récupérés avant qu'il réponde. |
| Cache local | Index d'empreintes + fiches d'une ville stockées sur le téléphone. |
| Score de confiance | Mesure [0–1] de la fiabilité d'un match. |

---

## 4. Acteurs

- **Visiteur (utilisateur final)** : scanne, lit, discute.
- **Système de reconnaissance** : on-device + serveur.
- **Service IA** : répond aux questions via RAG.
- **Administrateur de contenu** : gère les monuments, fiches et médias (back-office, hors périmètre MVP mais à prévoir).

---

## 5. Exigences fonctionnelles

Priorisation **MoSCoW** : M = Must, S = Should, C = Could.

### 5.1 Module Reconnaissance

**EF-1 (M) — Capture et capteurs.**
L'app active la caméra et lit en continu GPS, boussole et IMU.
*Critères d'acceptation :*
- la position est obtenue avec une précision affichée ;
- si le GPS est indisponible, l'app le signale et tente le repli Wi-Fi/réseau ;
- la capture d'analyse se déclenche quand l'appareil est stable.

**EF-2 (M) — Entonnoir géographique.**
Avant toute analyse visuelle, le système restreint les candidats aux monuments proches dans la direction visée.
*Critères :* la liste de candidats renvoyée ne contient que des monuments dans un rayon paramétrable (par défaut ~300 m) et dans un cône d'orientation paramétrable.

**EF-3 (M) — Calcul de l'empreinte on-device.**
Le modèle embarqué convertit l'image en empreinte sans envoi de la photo au serveur.
*Critères :* la photo ne quitte jamais l'appareil dans le flux nominal ; seule l'empreinte (+ métadonnées) peut être transmise.

**EF-4 (M) — Matching et score.**
Le système compare l'empreinte aux candidats et renvoie le meilleur match avec un score [0–1].
*Critères :*
- si `score ≥ seuil_haut` → résultat affiché normalement ;
- si `seuil_bas ≤ score < seuil_haut` → résultat affiché avec mention « probablement… » ;
- si `score < seuil_bas` → message « non reconnu » + suggestions.

**EF-5 (S) — Repli serveur.**
Si aucun candidat local ne convient, l'app interroge la base vectorielle serveur, puis en dernier recours un modèle généraliste/multimodal.

**EF-6 (S) — Vérification géométrique.**
Pour les scores intermédiaires, une vérification par points d'intérêt locaux confirme le match.

### 5.2 Module Fiche d'information

**EF-7 (M)** — Afficher nom, type, localisation, date, architecte, description, infos pratiques.
**EF-8 (S)** — Afficher la fiche dans la langue de l'utilisateur (fallback langue par défaut).
**EF-9 (C)** — Lecture audio de la fiche (audioguide).

### 5.3 Module Assistant IA (chat)

**EF-10 (M, V1) — Dialogue contextuel.**
L'utilisateur pose des questions libres sur le monument identifié ; l'assistant répond via RAG.
*Critères :*
- chaque réponse s'appuie sur les faits récupérés en base de connaissances (RAG) ;
- l'assistant n'invente pas : en l'absence de donnée, il le dit ;
- l'historique de la conversation est conservé pour le contexte.

**EF-11 (S)** — Questions suggérées (« pourquoi a-t-il été construit ? », « comment le visiter ? »).
**EF-12 (C)** — Adaptation du registre (enfant, expert, pressé).

### 5.4 Module Hors-ligne

**EF-13 (M, V1) — Téléchargement d'une ville.**
L'utilisateur télécharge l'index d'empreintes + fiches d'une ville ; la reconnaissance et la fiche fonctionnent ensuite sans réseau.
*Critères :* taille du paquet affichée avant téléchargement ; reconnaissance fonctionnelle en mode avion ; le chat IA indique qu'il nécessite une connexion.

### 5.5 Module Compte et carnet

**EF-14 (S)** — Carnet : chaque monument scanné est enregistré (date, score).
**EF-15 (C)** — Compte utilisateur (langue, abonnement, synchronisation).

---

## 6. Exigences non-fonctionnelles

| Réf. | Catégorie | Exigence |
|---|---|---|
| ENF-1 | Performance | Reconnaissance on-device perçue < 1 s ; extraction d'empreinte < ~200 ms sur appareil milieu de gamme. |
| ENF-2 | Latence chat | Première réponse de l'assistant < 3 s (streaming des tokens souhaité). |
| ENF-3 | Disponibilité | API serveur cible 99,5 %. |
| ENF-4 | Hors-ligne | Reconnaissance + fiche sans réseau pour toute ville téléchargée. |
| ENF-5 | Sécurité | Communications en HTTPS/TLS ; authentification des appels API. |
| ENF-6 | Vie privée | La photo ne quitte pas l'appareil dans le flux nominal ; consentement explicite pour la localisation. |
| ENF-7 | RGPD | Données personnelles minimisées ; droit à l'effacement ; conservation limitée des conversations. |
| ENF-8 | Accessibilité | Contrastes, tailles de police, lecteur d'écran ; alternatives textuelles. |
| ENF-9 | i18n | Architecture multilingue dès le départ (UI + contenu). |
| ENF-10 | Compatibilité | Android 9+ / iOS 15+ (à confirmer). |
| ENF-11 | Observabilité | Journalisation des scores faibles et erreurs pour amélioration continue. |

---

## 7. Architecture technique cible

Découpage **client / serveur** :

- **Client (téléphone)** : caméra + capteurs, modèle embarqué (empreinte), cache local (hors-ligne), interface + chat.
- **Serveur (cloud)** : API passerelle, base vectorielle (ANN), base de connaissances, service IA (LLM + RAG).

Flux nominal : reconnaissance entièrement on-device si la ville est en cache. Le serveur n'est appelé que pour (a) un monument hors cache, (b) une interaction de chat.

---

## 8. Spécification des API (REST)

Format : JSON. Authentification : jeton (Bearer). Toutes les réponses incluent un `request_id`.

### 8.1 `POST /v1/recognize`
Reconnaissance serveur (repli, ou ville non cachée). Le client envoie l'**empreinte**, pas l'image.

Requête :
```json
{
  "embedding": [0.012, -0.45, 0.98, "..."],
  "model_version": "vision-lite-2.1",
  "location": { "lat": 48.8584, "lng": 2.2945, "accuracy_m": 8 },
  "heading_deg": 215,
  "radius_m": 300
}
```

Réponse `200` :
```json
{
  "request_id": "req_abc123",
  "matches": [
    { "monument_id": "mon_eiffel", "name": "Tour Eiffel", "confidence": 0.98 },
    { "monument_id": "mon_champ", "name": "Champ-de-Mars", "confidence": 0.21 }
  ],
  "status": "matched"
}
```
`status` ∈ `matched` | `low_confidence` | `not_found`.
Codes : `200` OK, `400` requête invalide, `401` non authentifié, `429` quota, `500` erreur serveur.

### 8.2 `GET /v1/monuments/{id}`
Récupère la fiche d'un monument.

Paramètre query : `lang` (ex. `fr`).
Réponse `200` :
```json
{
  "monument_id": "mon_eiffel",
  "name": "Tour Eiffel",
  "type": "edifice",
  "location": { "lat": 48.8584, "lng": 2.2945 },
  "year_built": 1889,
  "architect": "Gustave Eiffel",
  "description": "...",
  "practical_info": { "hours": "...", "ticket_url": "..." },
  "media": [ { "type": "audio", "lang": "fr", "url": "..." } ]
}
```

### 8.3 `POST /v1/chat`
Dialogue avec l'assistant (RAG côté serveur).

Requête :
```json
{
  "monument_id": "mon_eiffel",
  "message": "Pourquoi a-t-elle été construite ?",
  "history": [
    { "role": "user", "content": "..." },
    { "role": "assistant", "content": "..." }
  ],
  "lang": "fr"
}
```
Réponse : flux (streaming) de tokens, ou `200` avec `{ "request_id": "...", "answer": "..." , "sources": ["..."] }`. Le champ `sources` liste les faits utilisés (traçabilité RAG).

### 8.4 `GET /v1/cities/{id}/package`
Renvoie l'URL et la taille du paquet hors-ligne (index d'empreintes + fiches) d'une ville.

---

## 9. Modèle de données

### 9.1 PostgreSQL

**monuments**
| Champ | Type | Notes |
|---|---|---|
| id | uuid (PK) | |
| name | text | |
| city_id | uuid (FK → cities) | |
| type | enum | edifice, statue, fontaine, street_art… |
| lat | double | |
| lng | double | |
| year_built | int | nullable |
| architect | text | nullable |
| description | text | i18n via table dédiée |
| practical_info | jsonb | |
| created_at | timestamptz | |

**cities** : `id`, `name`, `country`, `bbox (geometry)`, `package_size_mb`, `package_url`.
**media** : `id`, `monument_id (FK)`, `type` (photo/audio), `lang`, `url`.
**monument_i18n** : `monument_id (FK)`, `lang`, `name`, `description` (contenu traduit).
**users** : `id`, `lang`, `subscription`, `created_at`.
**logbook** : `id`, `user_id (FK)`, `monument_id (FK)`, `scanned_at`, `confidence`.
**conversations** : `id`, `user_id (FK)`, `monument_id (FK)`, `messages (jsonb)`, `created_at`.

*Recommandation : extension PostGIS pour les requêtes géospatiales (rayon, cône d'orientation).*

### 9.2 Base vectorielle
Collection `embeddings` : `vector` (dimension fixée par le modèle), payload `{ monument_id, city_id, conditions, model_version }`. Filtrage par `city_id` pour l'entonnoir géographique côté serveur.

---

## 10. Pipeline ML

- **Entraînement** : metric learning (tête ArcFace/CosFace) sur jeux publics (Google Landmarks) + collecte ciblée + augmentation.
- **Format de sortie** : empreinte de dimension `D` (à figer ; impacte la base vectorielle et le modèle embarqué).
- **Distillation** : production d'un modèle léger TFLite / Core ML pour le téléphone.
- **Indexation** : calcul des empreintes de référence par monument (multi-angles) et insertion en base vectorielle.
- **Versioning** : chaque empreinte porte `model_version` ; le serveur refuse de comparer des empreintes de versions incompatibles.
- **Boucle d'amélioration** : journalisation des scans à faible confiance et des retours utilisateurs → ré-entraînement périodique.

**Contrainte critique :** la dimension `D` et la `model_version` doivent être cohérentes entre le modèle embarqué, le cache local et la base vectorielle. Toute mise à jour du modèle implique une stratégie de migration des index.

---

## 11. Contraintes techniques (stack recommandée)

| Couche | Recommandé | Alternatives |
|---|---|---|
| App mobile | Flutter / React Native | Natif Kotlin / Swift |
| Modèle embarqué | TFLite (Android), Core ML (iOS) | ONNX Runtime Mobile |
| Backbone | EfficientNet-Lite / MobileNetV3 | ViT distillé |
| Entraînement | PyTorch + ArcFace | TensorFlow |
| API | Python / FastAPI | Node.js / NestJS |
| Base vectorielle | Qdrant | Pinecone / Weaviate / FAISS |
| BDD | PostgreSQL + PostGIS | — |
| LLM / chat | API LLM (ex. Claude) + RAG | modèle auto-hébergé |
| Médias | stockage objet + CDN | — |
| Données sources | OpenStreetMap, Wikidata, Wikimedia | contenu propriétaire |

---

## 12. Sécurité et conformité

- HTTPS/TLS obligatoire ; jetons d'authentification ; limitation de débit (rate limiting).
- Photo non transmise dans le flux nominal ; consentement localisation explicite.
- RGPD : minimisation, conservation limitée des conversations, droit à l'effacement, politique de confidentialité claire.
- Stockage chiffré des données sensibles ; secrets gérés via un coffre (vault), jamais en dur.

---

## 13. Tests et critères de recette

- **Unitaires** : extraction d'empreinte, filtrage géographique, matching, parsing API.
- **Intégration** : flux complet scan → fiche, scan → repli serveur, chat → RAG.
- **Terrain** : campagne de scans réels (jour/nuit, angles, occlusion) avec mesure de la précision et du temps.
- **Hors-ligne** : reconnaissance en mode avion sur une ville téléchargée.
- **Charge** : tenue de l'API et de la base vectorielle sous trafic simulé.
- **Recette fonctionnelle** : chaque exigence M et S validée par ses critères d'acceptation.

---

## 14. Livrables et jalons

| Jalon | Contenu | Critère de sortie |
|---|---|---|
| J0 — Données | Base + index d'une ville pilote | Index requêtable, fiches complètes |
| J1 — MVP | EF-1 à EF-4, EF-7 | Reconnaissance terrain validée |
| J2 — V1 | EF-10, EF-13, EF-8, EF-14 | Chat + hors-ligne fonctionnels |
| J3 — V2 | Repli généralisé, audioguide, nouvelles villes | Passage à l'échelle |

Livrables attendus à chaque jalon : code source documenté, jeu de tests, documentation API à jour, build installable.

---

## 15. Annexes

### 15.1 Codes d'erreur API
| Code | Signification |
|---|---|
| 400 | Requête invalide (payload, version de modèle) |
| 401 | Authentification manquante/invalide |
| 404 | Ressource introuvable (monument, ville) |
| 409 | Version de modèle incompatible |
| 429 | Quota dépassé |
| 500 | Erreur serveur |

### 15.2 Paramètres configurables
`radius_m` (défaut 300), `cone_orientation_deg`, `seuil_haut`, `seuil_bas`, `model_version`, taille max du paquet hors-ligne.

---

*Fin du cahier des charges — version 0.1, à amender lors du cadrage avec l'équipe technique.*

---

## Documents du projet Cicero

Ce document fait partie d'un ensemble cohérent :

- **Document de conception** — `cicero-conception.md`
- **Cahier des charges développeurs** — `cicero-cahier-des-charges-dev.md`
- **Backlog produit** — `cicero-backlog.md`
- **Charte opérationnelle des agents IA** — `cicero-charte-agents.md`
