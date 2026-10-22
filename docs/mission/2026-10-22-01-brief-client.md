# 01 · Brief client : demande initiale

> 🎭 **Scénario fictif.** L'ONG *Initiative Baobab Santé* et ses interlocuteurs sont inventés pour les besoins du portfolio.
> Les données analysées sont réelles : elles proviennent de l'**Observatoire mondial de la santé de l'OMS**
> (*Global Health Observatory*, GHO). Ce projet n'est ni commandé, ni validé, ni affilié à l'Organisation mondiale de la santé.

| | |
|---|---|
| **Date de réception** | 2026-10-22 |
| **Canal** | Email |
| **Client** | Initiative Baobab Santé, ONG de santé maternelle et infantile (siège à Dakar, 9 pays d'intervention) |
| **Interlocutrice** | Dr Mariam Koné, directrice des programmes |
| **Objet** | « Suivre l'ODD 3 en Afrique avec les données de l'OMS » |

---

## Message reçu

> Bonjour,
>
> Notre ONG finance des programmes de santé maternelle et infantile en Afrique. Chaque année, notre conseil
> d'administration nous demande où en sont les pays par rapport aux **Objectifs de développement durable (ODD 3)**
> et où concentrer nos financements.
>
> Aujourd'hui, notre équipe de suivi-évaluation télécharge les tableaux de l'OMS **à la main**, les copie dans Excel,
> et les chiffres ne concordent jamais d'une année sur l'autre. L'an dernier, nous avons même présenté un indicateur
> faux au conseil, parce qu'un tableau mélangeait plusieurs catégories sans que nous le voyions.
>
> Nous voudrions une **base de données fiable et à jour**, alimentée automatiquement depuis l'OMS, et une première analyse
> de la situation dans la région africaine.
>
> Cordialement,
> Dr Mariam Koné, Initiative Baobab Santé

---

## 🔍 Première analyse (interne, avant la réunion de cadrage)

**Ce que le client exprime :** un suivi des ODD 3 en Afrique.

**Ce dont le client a besoin :** avant tout, un **système de données fiable**. L'analyse vient en second.
Son vrai problème est un problème d'**ingénierie des données** :
1. **Processus manuel** (téléchargement, copier-coller) : il n'est ni reproductible ni traçable.
2. **Incohérences d'une année sur l'autre** : les données de l'OMS sont révisées, et personne ne garde l'historique.
3. **Erreur de grain** (« un tableau mélangeait plusieurs catégories ») : c'est exactement le piège de l'API de l'OMS,
   où une même valeur pays-année peut exister par sexe, par tranche d'âge et par quintile de richesse.

**Points à clarifier en cadrage :**
- Quels indicateurs suivre exactement ? Quelles cibles ODD ?
- Quel périmètre géographique : 9 pays d'intervention, ou toute la région africaine de l'OMS ?
- Qui utilisera la base, et avec quels outils ?
- À quelle fréquence faut-il la mettre à jour ?
- Comment traiter les révisions de données par l'OMS ?

➡️ Suite : [02 · Compte rendu de la réunion de cadrage](2026-10-22-02-compte-rendu-cadrage.md)
