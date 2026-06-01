# Cicero — Backlog produit

*Application de reconnaissance de monuments touristiques*
*Epics et user stories prêts pour un outil de gestion (Jira, Linear, GitHub Projects) · Version 0.1*

---

## Conventions

- **Format des stories :** « En tant que **rôle**, je veux **action**, afin de **bénéfice**. »
- **Identifiants :** préfixe par epic (ex. `REC-1`).
- **Priorité :** Must / Should / Could (MoSCoW).
- **Estimation :** points relatifs (suite de Fibonacci : 1, 2, 3, 5, 8, 13).
- **Jalon :** J1 (MVP) · J2 (V1) · J3 (V2) · J0 (préparation/enabler).
- **Type :** Story (valeur utilisateur) · Enabler (technique/infra) · Spike (recherche).

### Definition of Ready (story prête à entrer en sprint)
- [ ] Valeur et bénéfice clairs
- [ ] Critères d'acceptation rédigés et testables
- [ ] Dépendances identifiées
- [ ] Estimée par l'équipe
- [ ] Maquette / contrat d'API disponible si nécessaire

### Definition of Done (story terminée)
- [ ] Code revu et mergé
- [ ] Tests unitaires et d'intégration passants
- [ ] Critères d'acceptation validés
- [ ] Documentation / API à jour
- [ ] Build installable mis à jour

---

## EPIC 1 — Reconnaissance visuelle
*Objectif : identifier un monument en moins d'une seconde via l'entonnoir géographique et le modèle embarqué.*
*Réf. cahier : EF-1 à EF-6.*

### REC-1 · Capture caméra et lecture des capteurs · **Must** · 5 pts · J1
En tant que visiteur, je veux que l'app active la caméra et lise ma position et mon orientation, afin que le système sache où je suis et ce que je regarde.
**Critères d'acceptation :**
- [ ] La caméra s'affiche en viseur plein écran.
- [ ] GPS, boussole et IMU sont lus en continu.
- [ ] La précision de localisation est affichée à l'utilisateur.
- [ ] Le consentement de localisation est demandé explicitement.
**Dépendances :** APP-1.

### REC-2 · Détection de stabilité pour le déclenchement · **Should** · 3 pts · J1
En tant que visiteur, je veux que l'analyse se déclenche quand mon téléphone est stable, afin d'éviter les images floues.
**Critères :**
- [ ] L'analyse ne se lance pas pendant un mouvement franc.
- [ ] Un indicateur visuel montre l'état (recherche / stable).
**Dépendances :** REC-1.

### REC-3 · Entonnoir géographique (filtrage des candidats) · **Must** · 8 pts · J1
En tant que système, je veux restreindre les candidats aux monuments proches et dans la direction visée, afin de rendre la reconnaissance rapide et fiable.
**Critères :**
- [ ] Renvoie uniquement les monuments dans un rayon paramétrable (défaut 300 m).
- [ ] Filtre selon un cône d'orientation paramétrable.
- [ ] Fonctionne sur l'index local (hors-ligne) comme côté serveur.
**Dépendances :** DATA-2, REC-1.

### REC-4 · Calcul de l'empreinte on-device · **Must** · 8 pts · J1
En tant que système, je veux convertir l'image en empreinte sur le téléphone, afin d'être instantané et de préserver la vie privée.
**Critères :**
- [ ] Le modèle TFLite/Core ML est embarqué et chargé.
- [ ] Extraction < ~200 ms sur appareil milieu de gamme.
- [ ] La photo ne quitte jamais l'appareil dans le flux nominal.
**Dépendances :** ML-3.

### REC-5 · Matching local et score de confiance · **Must** · 5 pts · J1
En tant que visiteur, je veux obtenir le monument le plus probable avec un niveau de confiance, afin de savoir si je peux me fier au résultat.
**Critères :**
- [ ] Renvoie le meilleur candidat + score [0–1].
- [ ] `score ≥ seuil_haut` → affichage normal.
- [ ] `seuil_bas ≤ score < seuil_haut` → affichage « probablement… ».
- [ ] `score < seuil_bas` → « non reconnu » + suggestions.
**Dépendances :** REC-3, REC-4.

### REC-6 · Repli serveur (monument hors cache) · **Should** · 5 pts · J2
En tant que visiteur, je veux que l'app interroge le serveur si le monument n'est pas dans mon cache, afin d'élargir la couverture.
**Critères :**
- [ ] Si aucun match local satisfaisant, appel à `POST /v1/recognize` avec l'empreinte.
- [ ] Gestion des cas hors-ligne (message clair).
**Dépendances :** API-2, REC-5.

### REC-7 · Repli modèle généraliste / multimodal · **Could** · 8 pts · J3
En tant que visiteur, je veux une tentative d'identification même pour un monument absent de la base, afin d'avoir une réponse utile (« probablement… »).
**Critères :**
- [ ] Déclenché en dernier recours.
- [ ] Réponse toujours assortie d'un doute explicite.

### REC-8 · Vérification géométrique (re-ranking) · **Should** · 5 pts · J2
En tant que système, je veux confirmer les matchs au score intermédiaire par les détails locaux, afin de départager les bâtiments similaires.
**Critères :**
- [ ] Appliquée pour les scores entre seuils.
- [ ] Améliore la précision mesurée sur le jeu de test terrain.
**Dépendances :** REC-5.

---

## EPIC 2 — Fiche d'information et contenu
*Réf. cahier : EF-7 à EF-9.*

### FIC-1 · Affichage de la fiche monument · **Must** · 3 pts · J1
En tant que visiteur, je veux voir les infos clés d'un monument identifié, afin d'en apprendre davantage.
**Critères :**
- [ ] Affiche nom, type, localisation, date, architecte, description, infos pratiques.
- [ ] Données récupérées via `GET /v1/monuments/{id}`.
**Dépendances :** API-3, REC-5.

### FIC-2 · Fiche multilingue · **Should** · 5 pts · J2
En tant que visiteur étranger, je veux la fiche dans ma langue, afin de comprendre le contenu.
**Critères :**
- [ ] Paramètre `lang` respecté ; fallback langue par défaut.
- [ ] Au moins 2 langues au lancement (à définir).
**Dépendances :** FIC-1, DATA-3.

### FIC-3 · Audioguide (lecture vocale) · **Could** · 3 pts · J3
En tant que visiteur, je veux écouter la fiche, afin de garder les yeux sur le monument.
**Critères :**
- [ ] Lecture/pause de la fiche.
- [ ] Disponible dans les langues du contenu.

---

## EPIC 3 — Assistant IA conversationnel
*Réf. cahier : EF-10 à EF-12.*

### IA-1 · Chat contextuel via RAG · **Must (V1)** · 8 pts · J2
En tant que visiteur, je veux poser des questions libres sur le monument, afin d'obtenir des réponses précises comme avec un guide.
**Critères :**
- [ ] `POST /v1/chat` avec `monument_id`, message, historique.
- [ ] Réponse fondée sur les faits récupérés (RAG) ; champ `sources` renseigné.
- [ ] En l'absence de donnée, l'assistant le dit sans inventer.
- [ ] Première réponse < 3 s (streaming souhaité).
**Dépendances :** API-4, KB-1.

### IA-2 · Questions suggérées · **Should** · 2 pts · J2
En tant que visiteur, je veux des suggestions de questions, afin de démarrer facilement la conversation.
**Critères :**
- [ ] 2 à 3 suggestions contextuelles affichées sous la fiche.

### IA-3 · Adaptation du registre de réponse · **Could** · 3 pts · J3
En tant que visiteur, je veux choisir un ton (enfant / expert / synthétique), afin d'adapter l'explication.
**Critères :**
- [ ] Sélecteur de registre ; le ton de la réponse change en conséquence.

### IA-4 · Mémoire de session de conversation · **Should** · 3 pts · J2
En tant que visiteur, je veux que l'assistant garde le fil, afin d'enchaîner les questions naturellement.
**Critères :**
- [ ] L'historique est transmis et pris en compte.
- [ ] Conservation limitée dans le temps (conformité).

---

## EPIC 4 — Mode hors-ligne et cache
*Réf. cahier : EF-13.*

### OFF-1 · Téléchargement du paquet d'une ville · **Must (V1)** · 8 pts · J2
En tant que visiteur, je veux télécharger une ville, afin d'utiliser l'app sans réseau.
**Critères :**
- [ ] `GET /v1/cities/{id}/package` fournit URL + taille.
- [ ] Taille affichée avant téléchargement ; progression visible.
- [ ] Index d'empreintes + fiches stockés localement.
**Dépendances :** API-5, DATA-2.

### OFF-2 · Reconnaissance et fiche hors-ligne · **Must (V1)** · 5 pts · J2
En tant que visiteur sans réseau, je veux scanner et lire les fiches, afin de visiter sans data.
**Critères :**
- [ ] Reconnaissance fonctionnelle en mode avion sur une ville téléchargée.
- [ ] Le chat indique clairement qu'il nécessite une connexion.
**Dépendances :** OFF-1, REC-3, REC-5.

### OFF-3 · Gestion et mise à jour des paquets · **Should** · 3 pts · J2
En tant que visiteur, je veux gérer mes villes téléchargées, afin de libérer de l'espace et rester à jour.
**Critères :**
- [ ] Liste des villes téléchargées ; suppression possible.
- [ ] Notification si une mise à jour de l'index est disponible.

---

## EPIC 5 — Compte utilisateur et carnet
*Réf. cahier : EF-14, EF-15.*

### USR-1 · Carnet de voyage · **Should** · 3 pts · J2
En tant que visiteur, je veux retrouver les monuments scannés, afin de revivre mon parcours.
**Critères :**
- [ ] Chaque scan enregistre monument, date, score.
- [ ] Liste consultable, triable par date.

### USR-2 · Compte et préférences · **Could** · 5 pts · J3
En tant que visiteur, je veux un compte, afin de synchroniser mes données et préférences.
**Critères :**
- [ ] Création de compte ; langue et abonnement mémorisés.
- [ ] Synchronisation du carnet entre appareils.

---

## EPIC 6 — Données et pipeline ML (enabler)
*Réf. cahier : §10. Préalable au MVP.*

### ML-1 · Spike : choix du backbone et de la dimension d'empreinte · **Must** · 3 pts · J0 · *Spike*
En tant qu'équipe, nous voulons figer le backbone et la dimension `D`, afin de contraindre correctement le modèle embarqué et la base vectorielle.
**Critères :**
- [ ] Comparatif de backbones légers documenté.
- [ ] Dimension `D` et `model_version` arrêtées.

### ML-2 · Entraînement du modèle (metric learning) · **Must** · 13 pts · J0 · *Enabler*
En tant qu'équipe, nous voulons entraîner le modèle avec tête ArcFace, afin de produire des empreintes discriminantes.
**Critères :**
- [ ] Données réunies (jeux publics + collecte) et augmentées.
- [ ] Métriques de validation atteintes (à définir).
**Dépendances :** ML-1, DATA-1.

### ML-3 · Distillation et export mobile · **Must** · 5 pts · J0 · *Enabler*
En tant qu'équipe, nous voulons un modèle léger TFLite/Core ML, afin de l'embarquer.
**Critères :**
- [ ] Modèle exporté aux deux formats.
- [ ] Performance on-device conforme à ENF-1.
**Dépendances :** ML-2.

### DATA-1 · Constitution de la base de la ville pilote · **Must** · 8 pts · J0 · *Enabler*
En tant qu'équipe, nous voulons rassembler positions, faits et images de la ville pilote, afin d'alimenter le modèle et les fiches.
**Critères :**
- [ ] Sources intégrées (OpenStreetMap, Wikidata, Wikimedia).
- [ ] Quelques centaines de monuments documentés.

### DATA-2 · Indexation des empreintes de référence · **Must** · 5 pts · J0 · *Enabler*
En tant qu'équipe, nous voulons indexer les empreintes par monument, afin de permettre le matching.
**Critères :**
- [ ] Empreintes multi-angles calculées et insérées en base vectorielle.
- [ ] Filtrage par `city_id` opérationnel.
**Dépendances :** ML-3, DATA-1, API-2.

### DATA-3 · Traductions du contenu · **Should** · 5 pts · J2 · *Enabler*
En tant qu'équipe, nous voulons traduire les fiches, afin de servir les visiteurs étrangers.
**Dépendances :** DATA-1.

### ML-4 · Boucle d'amélioration continue · **Should** · 5 pts · J2 · *Enabler*
En tant qu'équipe, nous voulons journaliser les scans à faible confiance et les retours, afin de réentraîner périodiquement.
**Critères :**
- [ ] Pipeline de collecte des cas difficiles.
- [ ] Processus de réindexation documenté.

---

## EPIC 7 — Backend, API et infrastructure (enabler)
*Réf. cahier : §7, §8.*

### API-1 · Socle API + authentification · **Must** · 5 pts · J1 · *Enabler*
En tant qu'équipe, nous voulons une API sécurisée, afin d'exposer les services serveur.
**Critères :**
- [ ] HTTPS/TLS, jetons Bearer, rate limiting.
- [ ] `request_id` dans chaque réponse.

### API-2 · Endpoint `POST /v1/recognize` · **Should** · 5 pts · J2 · *Enabler*
**Critères :** contrat respecté ; statuts `matched`/`low_confidence`/`not_found` ; rejet si `model_version` incompatible (409).
**Dépendances :** API-1, DATA-2.

### API-3 · Endpoint `GET /v1/monuments/{id}` · **Must** · 3 pts · J1 · *Enabler*
**Critères :** renvoie la fiche complète ; paramètre `lang`.
**Dépendances :** API-1, KB-1.

### API-4 · Endpoint `POST /v1/chat` (RAG) · **Must (V1)** · 8 pts · J2 · *Enabler*
**Critères :** récupération des faits + appel LLM ; streaming ; champ `sources`.
**Dépendances :** API-1, KB-1.

### API-5 · Endpoint `GET /v1/cities/{id}/package` · **Must (V1)** · 3 pts · J2 · *Enabler*
**Critères :** URL + taille du paquet hors-ligne.
**Dépendances :** API-1, DATA-2.

### INFRA-1 · Base vectorielle déployée · **Must** · 5 pts · J0 · *Enabler*
**Critères :** Qdrant (ou équivalent) opérationnel, filtrable par `city_id`.

### KB-1 · Base de connaissances (PostgreSQL + PostGIS) · **Must** · 5 pts · J0 · *Enabler*
**Critères :** schéma des tables créé ; requêtes géospatiales (rayon, cône) fonctionnelles.

### INFRA-2 · Observabilité et journalisation · **Should** · 3 pts · J1 · *Enabler*
**Critères :** logs structurés ; suivi des scores faibles et des erreurs.

---

## EPIC 8 — Application mobile : socle et expérience (enabler)

### APP-1 · Squelette de l'app mobile · **Must** · 5 pts · J1 · *Enabler*
**Critères :** projet Flutter/RN initialisé ; navigation de base ; build Android + iOS.

### APP-2 · Internationalisation (i18n) · **Should** · 3 pts · J2 · *Enabler*
**Critères :** UI multilingue ; au moins 2 langues.

### APP-3 · Accessibilité · **Should** · 3 pts · J2
**Critères :** contrastes, tailles de police, compatibilité lecteur d'écran, alternatives textuelles.

### APP-4 · Écran de résultat et fiche (UI) · **Must** · 5 pts · J1
**Critères :** maquette implémentée ; états « reconnu / probablement / non reconnu ».
**Dépendances :** REC-5, FIC-1.

---

## EPIC 9 — Sécurité et conformité RGPD
*Réf. cahier : §12, ENF-5 à ENF-7.*

### SEC-1 · Gestion du consentement et confidentialité · **Must** · 3 pts · J1
**Critères :** consentement localisation ; politique de confidentialité accessible ; photo non transmise.

### SEC-2 · Droits RGPD (effacement, conservation) · **Should** · 5 pts · J2
**Critères :** suppression des données sur demande ; durée de conservation des conversations bornée.

### SEC-3 · Gestion des secrets et chiffrement · **Must** · 3 pts · J0 · *Enabler*
**Critères :** secrets dans un coffre ; données sensibles chiffrées ; aucun secret en dur.

---

## EPIC 10 — Tests et qualité
*Réf. cahier : §13.*

### QA-1 · Suite de tests unitaires et d'intégration · **Must** · 5 pts · J1 · *Enabler*
**Critères :** couverture des modules clés ; CI exécutant les tests.

### QA-2 · Campagne de tests terrain · **Must** · 8 pts · J1
**Critères :** scans réels (jour/nuit, angles, occlusion) ; mesure précision et temps ; jeu de test de référence constitué.

### QA-3 · Tests hors-ligne · **Should** · 3 pts · J2
**Critères :** reconnaissance + fiche validées en mode avion.
**Dépendances :** OFF-2.

### QA-4 · Tests de charge API et base vectorielle · **Should** · 5 pts · J2
**Critères :** tenue sous trafic simulé ; latences conformes.

---

## Ordre de réalisation conseillé

1. **J0 (enablers)** : ML-1, DATA-1, KB-1, INFRA-1, SEC-3 → ML-2 → ML-3 → DATA-2.
2. **J1 (MVP)** : APP-1, API-1, REC-1 → REC-3 → REC-4 → REC-5, API-3, FIC-1, APP-4, SEC-1, QA-1, QA-2.
3. **J2 (V1)** : API-2/4/5, IA-1, OFF-1 → OFF-2, FIC-2, USR-1, SEC-2, ML-4.
4. **J3 (V2)** : REC-7, IA-3, FIC-3, USR-2, nouvelles villes.

---

*Fin du backlog — version 0.1. Les estimations sont indicatives et à recalibrer avec l'équipe lors du planning poker.*

---

## Documents du projet Cicero

Ce document fait partie d'un ensemble cohérent :

- **Document de conception** — `cicero-conception.md`
- **Cahier des charges développeurs** — `cicero-cahier-des-charges-dev.md`
- **Backlog produit** — `cicero-backlog.md`
- **Charte opérationnelle des agents IA** — `cicero-charte-agents.md`
