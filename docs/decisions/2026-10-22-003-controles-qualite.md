# ADR 003 : Contrôles de qualité, quarantaine et calibrage des seuils

- **Date :** 2026-10-22
- **Statut :** Acceptée

## Contexte

Le client présente ces chiffres à son conseil d'administration : une valeur aberrante chargée en silence est inacceptable.
Mais rejeter une valeur **vraie** au motif qu'elle est extrême fausserait tout autant l'analyse.

## Décisions

### 1. Huit contrôles avant chargement
Indicateur connu · valeur numérique présente · valeur dans les bornes de vraisemblance · intervalle d'incertitude cohérent ·
année valide · lieu connu · ventilation connue · type de ventilation connu. Une neuvième règle écarte les doublons de clé métier.

### 2. La quarantaine plutôt que la suppression
Une ligne invalide est enregistrée dans `ops.quarantine` **telle que reçue** (JSON) avec son motif.
Invariant contrôlé à chaque exécution : `lignes extraites = lignes chargées + lignes en quarantaine`.

### 3. Des bornes LOGIQUES, pas intuitives

Lors du premier passage sur les données réelles, des seuils « intuitifs » ont mis **25 lignes en quarantaine** :

| Seuil initial | Lignes écartées | Ce qu'étaient ces valeurs |
|---|---|---|
| Mortalité des moins de 5 ans ≤ 500 ‰ | 18 | Cambodge 1975-1978 (Khmers rouges), Soudan du Sud 1988, Irak 1942-1944, Centrafrique 2009 (quintiles pauvres) |
| Mortalité maternelle ≤ 5 000 / 100 000 | 7 | Rwanda 1994 (génocide), Soudan du Sud 1987-1998 (guerre civile) |

Ces valeurs sont **réelles** : ce sont les traces chiffrées de crises humanitaires majeures. Les seuils ont donc été remplacés par
des **limites logiques** :

| Indicateur | Nouvelle borne | Justification |
|---|---|---|
| Mortalité des moins de 5 ans, néonatale | 1 000 ‰ | Un taux pour 1 000 naissances ne peut pas dépasser 1 000 |
| Mortalité maternelle | 20 000 / 100 000 | Plus du double du maximum historique observé (8 045, Soudan du Sud 1987) |
| Pourcentages | 100 % | Limite mathématique |

## Conséquences

- ✅ Les valeurs extrêmes mais réelles sont conservées, et les erreurs grossières restent bloquées
- ✅ Résultat sur le lot du 2026-10-22 : **129 368 lignes valides, 0 en quarantaine**
- 📚 **Leçon :** une règle de qualité se calibre avec la connaissance du domaine. La quarantaine a joué son rôle :
  elle a isolé ces valeurs pour qu'un humain les examine, au lieu de les supprimer ou de les charger sans examen.
