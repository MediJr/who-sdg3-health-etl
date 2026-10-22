# 02 · Compte rendu de la réunion de cadrage

> 🎭 **Scénario fictif** : voir le [brief client](2026-10-22-01-brief-client.md).

| | |
|---|---|
| **Date** | 2026-10-22 |
| **Format** | Visioconférence, 1 h |
| **Participants** | Dr Mariam Koné (directrice des programmes) · Yann Diallo (responsable suivi-évaluation) · Data engineer (prestataire) |
| **Objectif** | Préciser les indicateurs, le périmètre, les utilisateurs et les exigences de fiabilité |

---

## 1. Questions posées et réponses du client

| # | Question du prestataire | Réponse du client |
|---|---|---|
| 1 | Quels indicateurs suivez-vous ? | Ceux des cibles **ODD 3.1 et 3.2** : mortalité maternelle, néonatale et des moins de 5 ans. Plus des indicateurs de « moyens » : vaccination, accouchements assistés, médecins, dépenses de santé. Et l'espérance de vie pour le contexte. |
| 2 | Quel périmètre géographique ? | Toute la **région africaine de l'OMS** : notre conseil veut voir nos 9 pays dans leur contexte régional. Le chiffre mondial sert de référence. |
| 3 | Qui utilisera la base ? | Yann et son équipe, en **SQL** et dans Excel. Ils doivent pouvoir s'y connecter directement. |
| 4 | À quelle fréquence ? | Au moins une fois par trimestre, et après chaque grande publication de l'OMS. |
| 5 | Que faire quand l'OMS révise une valeur ? | Toujours utiliser la **dernière** valeur publiée, mais savoir **quand** elle a changé. |
| 6 | Avez-vous besoin des données par sexe, âge, richesse ? | Oui, surtout la **richesse** : nos programmes ciblent les ménages pauvres. |
| 7 | Quelles marges d'incertitude affichez-vous ? | Aucune pour l'instant, mais l'OMS les publie et le conseil devrait les voir. |
| 8 | Quel format de livrable ? | La base, un rapport lisible par le conseil et une documentation pour que notre équipe soit autonome. |

---

## 2. Questions business retenues

| # | Question | Décision éclairée |
|---|---|---|
| **Q1** | Où en sont les pays de la région africaine par rapport aux **cibles ODD 3 de 2030** ? | Diagnostic annuel présenté au conseil |
| **Q2** | **À leur rythme actuel**, quels pays atteindront ces cibles d'ici 2030 ? | Priorisation des pays à financer |
| **Q3** | Quel est l'**écart de mortalité infantile** entre les ménages les plus pauvres et les plus riches ? | Ciblage des programmes vers les ménages pauvres |
| **Q4** | Les **moyens du système de santé** (vaccination, personnel, dépenses) vont-ils de pair avec de meilleurs résultats ? | Choix des leviers d'action |

## 3. Exigences techniques retenues

| Exigence | Raison |
|---|---|
| Base **PostgreSQL**, accessible en SQL à l'équipe du client | Plusieurs utilisateurs simultanés, outil standard |
| Mise à jour **relançable à tout moment**, sans doublons | Usage trimestriel, aucune manipulation manuelle |
| **Mise à jour des valeurs révisées** par l'OMS, avec la date de révision | Exigence n°5 du client |
| **Grain explicite** (indicateur × pays × année × sexe × âge × richesse) | Éviter l'erreur de l'an dernier |
| **Contrôles de qualité** avant chargement, avec mise à l'écart des lignes invalides | Fiabilité des chiffres présentés au conseil |
| **Mots de passe hors du code** | Sécurité de la base |
| **Tests automatisés** | Permettre à l'équipe de faire évoluer le code sans tout casser |

## 4. Points de vigilance signalés au client

- ⚠️ **Les données de l'OMS sont des estimations**, souvent modélisées, avec des intervalles d'incertitude.
- ⚠️ **Les dernières années disponibles varient** selon les indicateurs (2023 à 2025) et selon les pays.
- ⚠️ **Les données par richesse proviennent d'enquêtes** ponctuelles : elles ne sont pas disponibles chaque année.
- ⚠️ **Corrélation n'est pas causalité** : Q4 montrera des liens, pas des effets.

## 5. Actions

| Action | Responsable | Échéance |
|---|---|---|
| Rédiger et envoyer le cahier des charges | Prestataire | 2026-10-22 |
| Valider le cahier des charges | Dr Mariam Koné | À réception |

➡️ Suite : [03 · Cahier des charges](2026-10-22-03-cahier-des-charges.md)
