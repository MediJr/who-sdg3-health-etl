# Procès-verbal de recette

> 🎭 **Scénario fictif** : voir le [brief client](../mission/2026-10-22-01-brief-client.md).

| | |
|---|---|
| **Référence** | IBS-2026-001 · Livrable L7 |
| **Version recettée** | 1.0.0 |
| **Date de recette** | 2026-10-22 |
| **Client** | Initiative Baobab Santé, représentée par Dr Mariam Koné |
| **Prestataire** | Data engineer indépendant |

---

## 1. Conditions de la recette

- **Environnement neuf :** copie des seuls fichiers publiables du dépôt (45 fichiers : ni données, ni environnement virtuel, ni fichier `.env`).
- **Configuration :** `.env` recréé à partir de `.env.example`, avec un mot de passe aléatoire.
- **Base :** conteneur PostgreSQL **vierge** (nouveau volume Docker), démarré avec `docker compose up -d`.
- **Exécution :** `python -m src.pipeline`, avec une extraction réelle depuis l'API de l'OMS, puis une relance à l'identique et `pytest`.

## 2. Résultats par critère (cahier des charges, section 10)

| # | Critère | Méthode | Résultat | Statut |
|---|---|---|---|---|
| **C1** | Exécution de bout en bout en une commande, base comprise | Environnement neuf | Installation en 57 s. Base prête en 8 s. Pipeline complet en **2 min 43 s** (extraction réelle comprise), code de retour 0. | ✅ Conforme |
| **C2** | Relance sans doublon ni modification | Deuxième exécution sur le même lot | **0 insérée, 0 mise à jour, 129 368 inchangées** | ✅ Conforme |
| **C3** | Clé métier couvrant toutes les dimensions | Contrainte `UNIQUE NULLS NOT DISTINCT`, requête de contrôle, test d'intégration | 0 doublon. Le test `test_contrainte_unicite_empeche_un_doublon` passe. | ✅ Conforme |
| **C4** | Lignes invalides en quarantaine, jamais perdues | Invariant `extraites = chargées + quarantaine`, tests unitaires des 9 règles | 129 368 = 129 368 + 0. Les 9 règles sont testées avec des données volontairement fausses. | ✅ Conforme |
| **C5** | Aucun secret dans le dépôt | Recherche dans les fichiers publiables | `.env` exclu par `.gitignore`. Aucun mot de passe dans les 45 fichiers publiables. | ✅ Conforme |
| **C6** | Suite de tests intégralement verte | `pytest` | **22 / 22** (17 unitaires, 5 d'intégration sur une base dédiée) | ✅ Conforme |
| **C7** | Une requête et une réponse par question | Relecture du rapport | Q1 : 1 requête, Q2 : 2, Q3 : 2, Q4 : 1, plus la couverture des données. Une section par question dans le [rapport](Rapport_OMS_ODD3_FR.pdf). | ✅ Conforme |

## 3. Observations

| # | Observation | Traitement |
|---|---|---|
| O1 | Le lot de recette, extrait plus tard dans la soirée, contient exactement le même nombre d'observations (129 368) que le lot de production. | Aucun. Cela confirme que l'extraction est stable. |
| O2 | Les noms de pays sont en anglais (l'OMS ne publie pas de libellés français). | Limite documentée dans le rapport. |

## 4. Décision

- [x] **Recette prononcée sans réserve.**
- [ ] Recette refusée

| | Client | Prestataire |
|---|---|---|
| **Nom** | Dr Mariam Koné | Data engineer |
| **Date** | 2026-10-22 | 2026-10-22 |
| **Mention** | Bon pour réception | Livraison conforme au cahier des charges IBS-2026-001 |
