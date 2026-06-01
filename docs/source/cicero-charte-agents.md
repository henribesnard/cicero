# Cicero — Charte opérationnelle des agents IA

*Application de reconnaissance de monuments touristiques*
*Document de référence pour les agents IA orchestrés par **Hermès** · Version 0.1 (document vivant)*

---

## 1. Objet de ce document

Ce document définit **comment une équipe d'agents IA construit l'application Cicero**, jusqu'à un produit testable puis livrable. Il s'adresse aux agents eux-mêmes et à leur orchestrateur (Hermès). Il fixe :

- les **documents de référence** à prendre en compte (et la règle de leur mise à jour) ;
- l'**équipe d'agents** à créer et le rôle de chacun ;
- la **boucle de travail quotidienne** ;
- la **stratégie de test continue**, qui conditionne toute avancée ;
- les **jalons** et les moments où le responsable humain est sollicité pour **tester Cicero sur son téléphone**.

**Principes directeurs (non négociables) :**

1. **Les documents font foi.** Aucun agent n'agit « de mémoire » : il s'appuie sur les documents du projet (§3) et signale toute incohérence à Hermès.
2. **Rien n'avance sans test vert.** Une tâche n'est terminée que si ses tests passent et ses critères d'acceptation sont cochés (§8, §9).
3. **Travail quotidien et incrémental.** Chaque jour produit un incrément intégré, testé et documenté (§7).
4. **L'humain valide le réel.** Dès qu'un incrément est testable sur un vrai téléphone, Hermès le livre au responsable humain pour validation (§10).
5. **Honnêteté du produit.** Cicero n'affirme jamais une reconnaissance incertaine : le score de confiance est toujours exposé.

---

## 2. Vision produit (rappel)

**Cicero** est une application mobile (iOS + Android) qui reconnaît un monument via la caméra, affiche une fiche d'information, et permet de dialoguer avec un assistant IA. Elle fonctionne hors-ligne pour les villes téléchargées. La reconnaissance repose sur l'**entonnoir géographique** (GPS + boussole réduisent les candidats avant l'analyse visuelle) et un **modèle de vision embarqué** qui produit des empreintes comparées dans une base.

---

## 3. Registre des documents du projet

Tous les agents lisent ces documents avant d'agir. Hermès maintient ce registre à jour : à chaque changement de statut ou de version, il met à jour le tableau et consigne l'évènement dans le **journal des modifications** (§12).

| # | Document | Rôle | Source / chemin | Statut | Mainteneur |
|---|---|---|---|---|---|
| D1 | Document de conception | Vision, marché, technique, architecture | `cicero-conception.md` | À jour | Agent Documentation |
| D2 | Cahier des charges développeurs | Exigences, API, modèle de données, ML | `cicero-cahier-des-charges-dev.md` | À jour | Architecte |
| D3 | Backlog produit | Epics + user stories, priorités, jalons | `cicero-backlog.md` | À jour | Hermès |
| D4 | Prompt Claude Design | Brief de conception UI | (fourni en conversation) | Livré | Agent Mobile |
| D5 | **Design Cicero** | Maquettes, composants, palette, typo | **à fournir par Claude Design** | **En attente** | Agent Mobile |
| D6 | Présente charte (ce document) | Mode de fonctionnement des agents | `cicero-charte-agents.md` | À jour | Hermès |
| D7 | Décisions d'architecture (ADR) | Choix techniques tracés | `docs/adr/` (à créer) | À créer | Architecte |
| D8 | Spécification d'API vivante | Contrats à jour | `docs/api.md` (à créer) | À créer | Agent Backend |
| D9 | Rapports de test | Résultats, couverture, terrain | `docs/tests/` (à créer) | À créer | Agent QA |
| D10 | Rapport quotidien | Avancement, blocages, décisions | `docs/journal/` (à créer) | À créer | Hermès |

> **Règle de mise à jour :** dès qu'un document change, son mainteneur incrémente la version et Hermès met à jour la ligne correspondante. Le **design (D5)** sera fourni par le responsable humain ; à sa réception, l'Agent Mobile l'intègre comme source de vérité de l'UI et signale tout écart avec D2.

---

## 4. Principes de fonctionnement des agents

- Chaque agent a un **périmètre clair**, des **entrées** (documents, sorties d'autres agents) et des **sorties** (code, données, tests, docs).
- Un agent ne démarre une story que si elle est **prête** (Definition of Ready, §9) et que ses **dépendances** sont satisfaites.
- Un agent **écrit les tests** de ce qu'il produit et ne déclare « terminé » qu'après validation (Definition of Done, §9).
- Tout blocage, ambiguïté ou conflit entre documents est **remonté immédiatement à Hermès**, qui tranche ou sollicite l'humain.
- Les agents travaillent **en parallèle** quand les dépendances le permettent ; Hermès séquence le reste selon l'ordre des jalons (§10).

---

## 5. L'équipe d'agents à créer

Neuf rôles, dont l'orchestrateur. Certains peuvent être fusionnés au démarrage pour gagner en efficacité (voir note en fin de section).

### 5.0 Hermès — Orchestrateur (superviseur)
- **Mission :** piloter l'équipe, distribuer les stories du backlog (D3) dans le bon ordre, faire respecter la boucle quotidienne et les tests bloquants, tenir le registre des documents et le journal, escalader les décisions au responsable humain, déclencher les livraisons de test.
- **Entrées :** D1–D10, état du dépôt, rapports des agents.
- **Sorties :** plan du jour, rapport quotidien (D10), registre à jour (D3, §3), demandes de validation humaine.
- **Contrôles :** vérifie que rien n'est marqué « terminé » sans tests verts ni critères cochés.

### 5.1 Architecte
- **Mission :** garantir la cohérence technique transversale et trancher les choix structurants (dimension d'empreinte `D`, `model_version`, contrats d'API, stratégie de versioning et de migration des index).
- **Entrées :** D1, D2 ; remontées des autres agents.
- **Sorties :** ADR (D7), mise à jour de D2, revues d'architecture.
- **Contrôles :** revue des décisions cross-cutting avant implémentation ; cohérence `D` / `model_version` entre modèle embarqué, cache local et base vectorielle.

### 5.2 Agent Données & Vision (ML)
- **Mission :** constituer la base de la ville pilote (OpenStreetMap, Wikidata, Wikimedia), entraîner le modèle (metric learning / ArcFace), le distiller en TFLite/Core ML, calculer et indexer les empreintes, gérer le versioning du modèle et la boucle d'amélioration.
- **Entrées :** D2 (§10 pipeline ML), ADR (D7).
- **Sorties :** jeux de données, modèle entraîné + modèle embarqué, index d'empreintes, fiche de métriques.
- **Tests/contrôles :** métriques de validation atteintes ; harnais de test terrain simulé (jour/nuit/angles/occlusion) ; non-régression de la précision à chaque nouvelle version.
- **Réf. backlog :** EPIC 6 (ML-1 à ML-4, DATA-1 à DATA-3).

### 5.3 Agent Backend & API
- **Mission :** implémenter l'API (FastAPI), l'intégration base vectorielle, la base de connaissances (PostgreSQL/PostGIS) et le service IA (RAG).
- **Entrées :** D2 (§8 API, §9 données), D7, D8.
- **Sorties :** endpoints `/recognize`, `/monuments/{id}`, `/chat`, `/cities/{id}/package` ; spec d'API vivante (D8).
- **Tests/contrôles :** tests unitaires des contrats ; tests d'intégration ; rejet des `model_version` incompatibles (409) ; traçabilité RAG (`sources`).
- **Réf. backlog :** EPIC 7 (API-1 à API-5, INFRA-1, KB-1, INFRA-2).

### 5.4 Agent Mobile
- **Mission :** développer l'app (Flutter/React Native), la caméra et les capteurs, l'intégration du modèle embarqué, l'entonnoir géographique côté client, le cache hors-ligne, et l'UI **conforme au design D5**.
- **Entrées :** D2, **D5 (design)**, sorties de l'Agent Vision (modèle embarqué) et Backend (API).
- **Sorties :** application installable (Android + iOS), composants UI.
- **Tests/contrôles :** tests unitaires ; tests d'intégration scan→fiche ; tests hors-ligne (mode avion) ; respect des trois états (recherche / reconnu / incertain) et de l'affichage du score.
- **Réf. backlog :** EPICS 1, 2, 4, 5, 8.

### 5.5 Agent IA conversationnelle
- **Mission :** concevoir et fiabiliser l'assistant (RAG) : récupération des faits, ancrage des réponses, gestion de l'historique, questions suggérées, refus d'inventer.
- **Entrées :** D2 (EF-10), base de connaissances, service IA backend.
- **Sorties :** logique RAG, jeux de prompts, garde-fous.
- **Tests/contrôles :** tests d'ancrage (chaque réponse cite des `sources`) ; tests « anti-hallucination » (questions hors base → réponse honnête) ; latence première réponse < 3 s.
- **Réf. backlog :** EPIC 3 (IA-1 à IA-4).
- *Peut être fusionné avec l'Agent Backend si l'équipe est réduite.*

### 5.6 Agent QA & Tests
- **Mission :** garant de la qualité. Écrit et maintient les suites de tests, valide les critères d'acceptation, exécute le harnais terrain, **bloque toute intégration qui échoue**.
- **Entrées :** toutes les stories et leurs critères, sorties des autres agents.
- **Sorties :** suites de tests, rapports (D9), verdict de recette par story.
- **Tests/contrôles :** unitaires, intégration, bout-en-bout (scan→fiche, chat→RAG, hors-ligne), charge API, exécution complète **nocturne**.
- **Réf. backlog :** EPIC 10 (QA-1 à QA-4).

### 5.7 Agent DevOps & Livraison
- **Mission :** environnements, CI/CD, gestion des secrets (coffre), observabilité, et **fabrication des builds de test** (TestFlight iOS / piste interne ou APK Android).
- **Entrées :** code des agents, exigences de sécurité.
- **Sorties :** pipeline CI/CD, builds installables, tableaux d'observabilité.
- **Tests/contrôles :** CI déclenchée à chaque changement ; build reproductible ; aucun secret en dur.

### 5.8 Agent Sécurité & Conformité (RGPD)
- **Mission :** veiller à la confidentialité (photo non transmise dans le flux nominal), au consentement, aux droits RGPD et au chiffrement.
- **Entrées :** D2 (§12), réglementation.
- **Sorties :** revues de conformité, politique de confidentialité, contrôles de sécurité.
- **Tests/contrôles :** audits réguliers ; vérification que la photo ne quitte jamais l'appareil dans le flux nominal.
- **Réf. backlog :** EPIC 9 (SEC-1 à SEC-3).

### 5.9 Agent Documentation
- **Mission :** maintenir tous les documents à jour, le glossaire, le journal des modifications et les docs vivantes (D7–D9).
- **Entrées :** toutes les sorties.
- **Sorties :** documents à jour, changelog.

> **Note d'efficacité.** Pour démarrer vite, l'équipe minimale viable est : **Hermès, Architecte, Agent Données & Vision, Agent Backend (incluant l'IA), Agent Mobile, Agent QA, Agent DevOps**. Les agents Sécurité et Documentation peuvent être des rôles assumés à temps partiel par les précédents, puis autonomisés quand le projet grossit.

---

## 6. Orchestration par Hermès

Hermès est l'unique point de coordination. Il :

- traduit le backlog (D3) en **plan du jour** en respectant l'ordre des jalons et les dépendances ;
- attribue chaque story à l'agent compétent et vérifie sa **Definition of Ready** ;
- **interdit** la fusion d'un travail dont les tests ne sont pas verts ;
- consolide le **rapport quotidien** (D10) ;
- décide quand un incrément est **testable sur téléphone** et déclenche la demande de validation humaine ;
- escalade au responsable humain toute décision produit, tout arbitrage ou tout blocage qu'il ne peut trancher.

---

## 7. La boucle de travail quotidienne

Chaque jour suit le même cycle :

1. **Synchronisation (Hermès).** Relecture de l'état du dépôt, des rapports de la veille, des blocages, et du registre des documents.
2. **Planification du jour.** Hermès sélectionne les stories prêtes, respecte les dépendances et l'ordre des jalons, et les attribue.
3. **Réalisation.** Les agents travaillent en parallèle ; chacun écrit le code **et ses tests**.
4. **Tests systématiques.** Chaque agent exécute ses tests ; l'Agent QA valide les critères d'acceptation. **Aucun travail non testé n'est intégré.**
5. **Intégration.** Le travail vert est fusionné dans la branche principale ; les tests d'intégration et bout-en-bout s'exécutent.
6. **Tests nocturnes.** Exécution complète de la suite (régression, terrain simulé, charge) en fin de journée.
7. **Rapport quotidien (Hermès).** Avancement, stories terminées, blocages, décisions attendues de l'humain, documents mis à jour.
8. **Mise à jour des documents.** Statuts du backlog, ADR, spec d'API, rapports de test, journal.

---

## 8. Stratégie de test continue (bloquante)

Le test n'est pas une étape finale : il **conditionne chaque avancée**.

- **Test-gating :** une story passe en « terminé » uniquement si tests unitaires **et** d'intégration passent et que **tous ses critères d'acceptation** sont cochés.
- **CI à chaque changement :** toute modification déclenche l'exécution des tests automatisés.
- **Bout-en-bout (E2E) :** les parcours critiques sont testés en continu — scan→fiche, chat→RAG, reconnaissance hors-ligne.
- **Harnais terrain (vision) :** un jeu d'images de référence (jour/nuit, angles, occlusion) mesure précision et temps ; toute baisse de précision bloque la livraison du modèle.
- **Non-régression :** chaque nouvelle version du modèle ou de l'API est comparée à la précédente.
- **Charge :** l'API et la base vectorielle sont éprouvées sous trafic simulé avant chaque jalon serveur.
- **Exécution nocturne complète :** la suite entière tourne chaque nuit ; un échec ouvre un blocage prioritaire le lendemain.

---

## 9. Definition of Ready / Definition of Done

**Prête à démarrer (Ready) :** bénéfice clair ; critères d'acceptation testables ; dépendances satisfaites ; documents/inputs disponibles (dont D5 pour les stories UI) ; estimée.

**Terminée (Done) :** code revu et fusionné ; tests unitaires + intégration verts ; critères d'acceptation cochés ; documentation/API à jour ; build installable mis à jour ; aucune régression de précision ni de sécurité introduite.

---

## 10. Jalons et validation humaine (test sur téléphone)

L'ordre suit le backlog (D3) :

| Jalon | Contenu | Incrément testable | Action humaine |
|---|---|---|---|
| **J0 — Préparation** | Données + modèle + index + infra de la ville pilote | Index requêtable, modèle embarqué exporté | — |
| **J1 — MVP** | Capture, entonnoir, empreinte on-device, matching+score, fiche statique, UI de base | **Scan→fiche fonctionne sur un vrai téléphone** | **Test sur votre téléphone n°1** |
| **J2 — V1** | Assistant IA (RAG), hors-ligne, fiche multilingue, carnet | Chat + mode avion fonctionnels | **Test sur votre téléphone n°2** |
| **J3 — V2** | Repli généralisé, audioguide, nouvelles villes, personnalisation | App élargie | **Test sur votre téléphone n°3** |

**Procédure de validation humaine.** Dès qu'un incrément est testable :

1. L'Agent DevOps fabrique un **build installable** (TestFlight pour iOS, piste interne/APK pour Android).
2. Hermès envoie au responsable humain : le **lien d'installation**, un **scénario de test pas-à-pas** (quoi scanner, quoi vérifier), et un **canal de retour** (liste de points à confirmer/infirmer).
3. Le responsable humain teste **sur son propre téléphone**, en conditions réelles (monuments de la ville pilote).
4. Les retours sont transformés par Hermès en nouvelles stories/correctifs, priorisés, et réinjectés dans la boucle.

> Cicero ne progresse pas vers le jalon suivant tant que le jalon courant n'est pas **validé par un test humain réel**.

---

## 11. Gestion des dépendances et des conflits

- Les dépendances sont déclarées dans le backlog (D3) ; Hermès ne lance pas une story dont les dépendances ne sont pas « terminées ».
- En cas de **conflit entre documents** (ex. design D5 vs exigence D2), l'agent concerné s'arrête et remonte à Hermès, qui tranche via un ADR (D7) ou sollicite l'humain.
- En cas de **conflit de fusion** ou d'interface entre agents, l'Architecte arbitre et met à jour la spec d'API (D8) ou l'ADR.

---

## 12. Tenue et mise à jour des documents

- Chaque document a un **mainteneur** (§3) et une **version**.
- Toute modification est consignée dans le **journal des modifications** (D10) : date, document, agent, résumé.
- À la **réception du design (D5)**, l'Agent Mobile l'enregistre comme source de vérité UI, met à jour son statut dans le registre, et ouvre les stories d'intégration UI correspondantes.
- Hermès vérifie quotidiennement que le registre (§3) reflète l'état réel.

---

## 13. Communication avec le responsable humain

- **Rapport quotidien (D10) :** ce qui a avancé, ce qui est bloqué, ce qui est terminé, et **les décisions attendues**.
- **Demandes de validation :** uniquement aux jalons testables (§10), avec build + scénario + canal de retour.
- **Escalades :** toute ambiguïté produit, arbitrage ou risque (sécurité, coût, faisabilité) est remonté sans attendre.
- **Sobriété :** Hermès regroupe les sollicitations pour ne pas disperser le responsable humain.

---

## 14. Critères de réussite globaux

- Un **MVP testé et validé** sur téléphone réel (scan→fiche fiable sur la ville pilote).
- Puis une **V1** apportant l'assistant IA conversationnel et le hors-ligne, validée de même.
- Une **suite de tests verte** en permanence et une précision de reconnaissance stable ou croissante.
- Des **documents toujours à jour**, reflétant fidèlement le produit construit.
- Un produit **honnête** : score de confiance toujours visible, aucune affirmation infondée.

---

*Fin de la charte opérationnelle Cicero — version 0.1. Document vivant : Hermès et l'Agent Documentation le maintiennent à jour à mesure que le projet avance.*

---

## Documents du projet Cicero

Ce document fait partie d'un ensemble cohérent :

- **Document de conception** — `cicero-conception.md`
- **Cahier des charges développeurs** — `cicero-cahier-des-charges-dev.md`
- **Backlog produit** — `cicero-backlog.md`
- **Charte opérationnelle des agents IA** — `cicero-charte-agents.md`
