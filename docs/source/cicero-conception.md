# Cicero — Document de conception

*Application de reconnaissance de monuments touristiques*
*Concept, marché, positionnement, technique et architecture · Version 0.1*

---

## 1. Résumé exécutif

L'idée : **Cicero**, une application mobile qui, en pointant simplement la caméra du téléphone vers un monument ou un site touristique, l'identifie en une fraction de seconde, affiche une fiche d'information précise, et permet de **discuter avec un assistant IA** pour en savoir plus.

Le marché existe déjà (Google Lens, Whatizis, Smartify…), mais **aucun acteur ne réunit les trois piliers** de ce projet : reconnaissance de monuments en extérieur + couverture géographique large + assistant IA réellement conversationnel. C'est précisément cet espace vide qui constitue l'opportunité.

Techniquement, le secret de la rapidité et de la fiabilité n'est pas un modèle de vision surpuissant, mais un **entonnoir géographique** : le GPS et la boussole réduisent d'emblée les candidats de plusieurs millions à une trentaine, ce qui rend la reconnaissance à la fois instantanée et précise.

---

## 2. Le concept

L'utilisateur ouvre l'app, qui active la caméra comme un scanner. En la passant sur un monument, une statue ou un site, il obtient :

- une **identification instantanée** avec un score de confiance,
- une **fiche d'information** (nom, date, architecte, histoire, infos pratiques),
- un **assistant IA conversationnel** pour poser des questions libres (« pourquoi ce style ? », « que voir à côté ? », « explique-le à un enfant »).

Fonctions complémentaires qui renforcent l'utilité :

- mode **hors-ligne** (essentiel pour les touristes sans réseau),
- **traduction** dans la langue de l'utilisateur,
- mode **audioguide** (lecture vocale du contenu),
- **carnet de voyage** : sauvegarde des monuments scannés pour revivre le parcours.

---

## 3. Le marché et les concurrents

Le secteur est actif. On peut regrouper les acteurs en quatre familles.

| Application (éditeur) | Reconnaissance | Couverture géo. | Profondeur du contenu | Chat IA ouvert | Audioguide | Modèle économique |
|---|---|---|---|---|---|---|
| Google Lens (Google) | Généraliste | Mondiale | Faible à moyenne | Partiel (Gemini) | Non | Gratuit |
| Visual Look Up (Apple) | Généraliste, intégré iOS | Mondiale | Faible | Non | Non | Gratuit |
| Whatizis | Monuments extérieurs | ~8 villes | Élevée (guides-conférenciers) | Non (audio figé) | Oui | Payant par ville / freemium |
| Smartify | Œuvres en musée | 2 000+ musées partenaires | Élevée mais limitée aux partenaires | Non | Oui | Gratuit + premium |
| Google Arts & Culture | Œuvres / musée virtuel | Mondiale (numérique) | Moyenne à élevée | Non | Partiel | Gratuit |
| Chance AI | Œuvres d'art | Mondiale (sur photo) | Élevée, explicative | Oui | Non | Freemium |
| ArtScan | Tableaux | Mondiale (sur photo) | Élevée | Oui | Non | Freemium / abonnement |
| Magnus | Art contemporain (prix) | Marché de l'art | Moyenne | Non | Non | Freemium |

**Lecture stratégique.** Deux axes structurent ce marché : la **couverture** (œuvres en musée → monuments en extérieur) et la **profondeur de l'IA conversationnelle** (fiche/audio figé → assistant ouvert). Quand on place les acteurs sur ces deux axes, le coin « monuments en extérieur + IA conversationnelle » reste **vide**.

- Les généralistes (Google, Apple) sont puissants mais superficiels et sans vrai dialogue.
- Whatizis est excellent sur les monuments mais repose sur de l'audio pré-enregistré, pas un assistant ouvert.
- Les apps à chat IA riche (Chance AI, ArtScan) sont cantonnées aux œuvres de musée.

---

## 4. Positionnement recommandé

**Proposition de valeur :** *« Pointez n'importe quel monument et discutez avec lui comme avec un guide privé. »*

Le positionnement défendable n'est pas d'affronter Google Lens frontalement (perdu d'avance), mais d'occuper le coin vide : **l'assistant de visite conversationnel pour les monuments et sites en extérieur.**

Différenciation face à chaque type de concurrent :

- **vs Google Lens / Apple** : la profondeur et le dialogue continu qu'ils n'offrent pas.
- **vs Whatizis** : une IA qui répond à *toutes* les questions, au lieu de 2-3 pistes audio figées.
- **vs Smartify / Chance AI / ArtScan** : on sort du musée pour couvrir la ville et l'extérieur.

**Stratégie d'entrée :** commencer ultra-concentré. Une seule ville (Paris est idéale), une qualité irréprochable sur quelques centaines de monuments, puis expansion. Ne pas chercher à « couvrir le monde » dès le départ — c'est le terrain de Google.

**Leviers de défense à long terme :**

1. Fiabilité de la reconnaissance en extérieur (fusion vision + GPS + boussole).
2. Personnalisation : l'assistant se souvient des visites et adapte ses réponses.
3. Partenariats locaux (offices de tourisme, guides, mairies) = contenu exclusif et légitimité.

**Modèle économique :** freemium géographique (gratuit pour découvrir, abonnement ou pass par ville pour le contenu enrichi et le chat illimité), complété par des partenariats institutionnels (B2B2C avec les destinations).

---

## 5. Reconnaissance technique : comment ça marche

### 5.1 Les capteurs du téléphone

La force de l'app vient de la **combinaison** des capteurs, pas de la caméra seule. On peut les regrouper par fonction.

- **Voir** — la caméra fournit l'image ; un capteur de profondeur / LiDAR (sur certains appareils) mesure les distances et aide la réalité augmentée.
- **Se localiser** — le GPS/GNSS donne la position (à quelques mètres) ; le Wi-Fi et le Bluetooth affinent la localisation en ville et en intérieur ; le baromètre donne l'altitude approximative.
- **S'orienter** — le magnétomètre (boussole) indique la direction visée ; l'accéléromètre mesure l'inclinaison et la stabilité ; le gyroscope suit les rotations fines en temps réel.
- **Contextualiser** — le capteur de luminosité et l'horloge indiquent le jour/la nuit pour adapter le traitement de l'image.

La **fusion de capteurs** (accéléromètre + gyroscope + magnétomètre = l'IMU) produit une orientation fiable, croisée avec la position. Résultat : avant même d'analyser un pixel, l'app « sait » où elle est et ce qu'elle regarde.

### 5.2 L'entonnoir géographique (l'astuce clé)

On ne compare **pas** la photo à une base mondiale de millions de monuments. À la place :

1. Le GPS + la boussole restreignent la recherche aux monuments situés **autour de l'utilisateur, dans la direction visée**.
2. On passe ainsi de plusieurs millions de candidats à **une trentaine, parfois moins**.
3. La reconnaissance devient à la fois **rapide** (peu de comparaisons) et **fiable** (peu de confusions possibles).

### 5.3 Le modèle de vision et les empreintes

On ne compare jamais des pixels : on transforme chaque image en **empreinte** (un vecteur de quelques centaines de nombres qui résume l'image, indépendamment de l'angle ou de la lumière).

- **Backbone** : un réseau convolutif (EfficientNet, ResNet) ou un Vision Transformer. Pour le téléphone, une version légère (MobileNet, EfficientNet-Lite, ViT distillé).
- **Principe** : dans l'espace des empreintes, les photos d'un même monument se regroupent. La photo de l'utilisateur « tombe » dans le bon groupe → c'est le match.

### 5.4 L'entraînement

- **Approche** : apprentissage métrique (metric learning) plutôt que classification simple — on apprend au modèle à rapprocher les photos d'un même monument et à éloigner les autres. Fonctions de coût à marge type **ArcFace / CosFace**.
- **Avantage** : pour ajouter un monument, il suffit de calculer son empreinte et de l'ajouter à l'index — **aucun réentraînement**.
- **Vérification fine** : des points d'intérêt locaux (type DELG, SuperPoint) confirment les détails géométriques pour départager des bâtiments qui se ressemblent.
- **Données** : jeux publics géolocalisés (Google Landmarks Dataset ~5 M images / ~200 k lieux), images géotaguées de Wikimedia Commons, et collecte ciblée par monument (angles, heures, saisons). Forte augmentation de données.
- **Optimisation** : distillation du gros modèle vers une version compacte pour le téléphone.

### 5.5 Précision et limites

Grâce à l'entonnoir géographique, le modèle ne distingue qu'une trentaine de candidats, pas 200 000 — une tâche bien plus facile, donc une **précision réelle élevée** sur les monuments présents en base.

Limites identifiées (à gérer explicitement) :

- monument caché, en travaux ou sous échafaudage,
- angle inhabituel, nuit sans éclairage,
- bâtiments quasi identiques côte à côte,
- monument absent de la base.

**Règle d'or :** toujours afficher un **score de confiance** et savoir dire « je ne suis pas certain » plutôt que d'inventer. Un mauvais résultat affiché avec assurance détruit la confiance plus sûrement qu'un doute honnête.

**Amélioration continue :** journaliser les cas à faible confiance et les retours utilisateurs, puis enrichir la base et réentraîner périodiquement.

---

## 6. Architecture technique complète

Principe : couper le travail en deux. Le **client** (téléphone) gère ce qui doit être instantané et fonctionner hors-ligne ; le **serveur** (cloud) gère ce qui est trop lourd ou doit rester centralisé.

### 6.1 Côté téléphone (client)

- **Caméra + capteurs** : point d'entrée (image, GPS, boussole).
- **Modèle embarqué** : transforme la photo en empreinte, directement sur l'appareil. Instantané, gratuit (pas d'appel serveur), privé (la photo ne part pas). Formats : TensorFlow Lite (Android), Core ML (iOS).
- **Cache local** : index des empreintes + fiches d'une ville téléchargée → permet le scan **hors-ligne**.
- **Interface + chat** : viseur, fiche, zone de discussion.

### 6.2 Côté serveur (cloud)

- **API (passerelle)** : reçoit les requêtes et les distribue. Node.js, Python/FastAPI, etc.
- **Base vectorielle** : trouve l'empreinte la plus proche (recherche approximative du plus proche voisin, ANN). Outils : Qdrant, Pinecone, Weaviate, FAISS.
- **Base de connaissances** : contenu lisible (histoire, dates, infos pratiques). PostgreSQL convient.
- **Service IA (LLM + RAG)** : le chat. On récupère d'abord les faits pertinents, puis on les fournit au grand modèle de langage pour qu'il réponde **à partir de ces données** (RAG = retrieval-augmented generation), ce qui limite les inventions.

### 6.3 Comment les deux moitiés collaborent

- **Cas fréquent** (monument connu, ville téléchargée) : tout se passe sur le téléphone → ultra-rapide.
- **Le serveur n'est sollicité que** dans deux cas :
  1. monument absent du cache local → on envoie l'**empreinte** (pas la photo) à la base vectorielle ;
  2. l'utilisateur **discute** avec l'assistant → appel au service IA.

### 6.4 Mode hors-ligne

Ce n'est pas un mode séparé : c'est simplement le cas où tout le nécessaire est déjà dans le cache local. La reconnaissance et la fiche fonctionnent sans réseau ; le **chat IA**, lui, nécessite une connexion (un gros modèle ne tient pas dans un téléphone).

---

## 7. Stack technique concrète (proposition)

| Couche | Choix recommandé | Alternatives |
|---|---|---|
| App mobile | Flutter ou React Native | Natif Kotlin / Swift (perf caméra) |
| Modèle embarqué | TensorFlow Lite (Android), Core ML (iOS) | ONNX Runtime Mobile |
| Backbone vision | EfficientNet-Lite / MobileNetV3 | ViT distillé |
| Entraînement | PyTorch + tête ArcFace | TensorFlow |
| API serveur | Python (FastAPI) | Node.js (NestJS) |
| Base vectorielle | Qdrant (auto-hébergé) | Pinecone / Weaviate / FAISS |
| Base de connaissances | PostgreSQL | + PostGIS pour le géospatial |
| Service IA / chat | API d'un LLM (ex. Claude) + RAG | Modèle auto-hébergé |
| Stockage médias | Stockage objet + CDN | — |
| Données monuments | OpenStreetMap (positions), Wikidata (faits), Wikimedia (images) | Contenu propriétaire |

---

## 8. Schéma de base de données (esquisse)

Tables principales pour démarrer :

- **monuments** : `id`, `nom`, `ville`, `latitude`, `longitude`, `type` (édifice, statue, fontaine…), `date_construction`, `architecte`, `description`, `infos_pratiques`.
- **embeddings** : `id`, `monument_id` (→ monuments), `vecteur`, `source_image`, `conditions` (jour/nuit, angle). *Stocké dans la base vectorielle ; la clé `monument_id` fait le lien avec PostgreSQL.*
- **medias** : `id`, `monument_id`, `type` (photo, audio), `langue`, `url`.
- **villes** : `id`, `nom`, `pays`, `bbox` (zone géographique), `taille_index` (pour le téléchargement hors-ligne).
- **utilisateurs** : `id`, `langue`, `abonnement`, `date_creation`.
- **carnet** : `id`, `utilisateur_id`, `monument_id`, `date_scan`, `score_confiance`.
- **conversations** : `id`, `utilisateur_id`, `monument_id`, `messages`, `date`.

Relations clés : un `monument` possède plusieurs `embeddings` et plusieurs `medias` ; une `ville` regroupe des `monuments` (via la zone géographique) ; un `utilisateur` possède un `carnet` et des `conversations`.

---

## 9. Coûts

Quatre postes principaux :

1. **Hébergement serveur + API** — coût fixe modéré, croît avec le trafic.
2. **Base vectorielle** — peu cher en auto-hébergé (FAISS/Qdrant), facturé en service géré (Pinecone).
3. **Appels au LLM (chat)** — souvent le poste le plus **variable**, facturé à peu près par message. D'où l'intérêt de ne déclencher l'IA que lors d'un vrai dialogue.
4. **Stockage + diffusion des médias** (CDN).

À l'inverse, la reconnaissance de base coûte **presque rien** côté serveur, car elle tourne sur le téléphone.

**Règle d'or des coûts :** pousser le maximum de travail sur le téléphone (reconnaissance, cache) et ne solliciter le serveur — surtout l'IA — que lorsque c'est indispensable.

---

## 10. Plan de développement par étapes

### Étape 0 — Préparation (données)
Constituer la base d'une première ville : positions (OpenStreetMap), faits (Wikidata), images (Wikimedia + collecte). Calculer les empreintes et bâtir l'index.

### Étape 1 — MVP (preuve de concept)
- Une ville (Paris), quelques centaines de monuments.
- Reconnaissance avec entonnoir géographique + modèle embarqué.
- Fiche d'information statique.
- Pas encore de chat IA, pas encore de hors-ligne.
- **Objectif :** valider que la reconnaissance marche en conditions réelles.

### Étape 2 — V1 (le différenciateur)
- Ajout de l'**assistant IA conversationnel** (RAG).
- Mode **hors-ligne** (cache local par ville).
- Carnet de voyage, traduction.
- **Objectif :** livrer la proposition de valeur unique.

### Étape 3 — V2 (passage à l'échelle)
- Nouvelles villes, audioguide, personnalisation.
- Partenariats avec offices de tourisme.
- Repli sur modèle généraliste / multimodal pour les monuments hors base.
- **Objectif :** croissance et défensibilité.

---

## 11. Risques et points d'attention

- **Reconnaissance fine** en extérieur (occlusion, travaux, look-alikes) — gérer avec le score de confiance et la vérification géométrique.
- **Qualité GPS** en ville (canyons urbains) — compenser avec Wi-Fi/Bluetooth.
- **Coût du chat IA** à l'échelle — limiter aux dialogues réels, mettre en cache les réponses fréquentes.
- **Qualité du contenu** — un guide médiocre tue l'expérience ; soigner les fiches (partenariats avec guides-conférenciers).
- **Confiance utilisateur** — ne jamais affirmer avec assurance un résultat incertain.

---

## 12. Prochaines étapes possibles

- Cahier des charges détaillé pour développeurs.
- Maquettes d'écrans (UI/UX) complètes.
- Chiffrage détaillé des coûts selon un volume d'utilisateurs cible.
- Plan de collecte et de structuration des données pour la première ville.
- Stratégie de lancement et de partenariats sur Paris.

---

*Document de travail — à affiner selon les priorités et les ressources du projet.*

---

## Documents du projet Cicero

Ce document fait partie d'un ensemble cohérent :

- **Document de conception** — `cicero-conception.md`
- **Cahier des charges développeurs** — `cicero-cahier-des-charges-dev.md`
- **Backlog produit** — `cicero-backlog.md`
- **Charte opérationnelle des agents IA** — `cicero-charte-agents.md`
