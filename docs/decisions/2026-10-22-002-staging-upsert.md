# ADR 002 : Chargement par staging et UPSERT, avec une clé métier complète

- **Date :** 2026-10-22
- **Statut :** Acceptée

## Contexte

- Le client veut **toujours la dernière valeur publiée** par l'OMS, mais aussi **savoir quand une valeur a changé**.
- Le projet 0 utilisait un **rechargement complet** (*full refresh*) : simple, mais sans mémoire.
- L'erreur passée du client venait d'un **mélange de catégories** : la même valeur pays-année existe par sexe, par âge
  et par quintile de richesse (8 lignes pour le Sénégal en 2020).

## Décisions

### 1. Une clé métier qui couvre tout le grain
`UNIQUE NULLS NOT DISTINCT (indicateur, type de lieu, lieu, année, sexe, tranche d'âge, quintile de richesse)`.
- `NULLS NOT DISTINCT` : deux `NULL` sont considérés égaux. Sans cela, PostgreSQL accepterait une infinité de lignes
  « sans ventilation » pour la même clé, car par défaut `NULL ≠ NULL`.
- La contrainte est en base, en plus des contrôles Python : c'est la **défense en profondeur**.

### 2. Staging, puis UPSERT
1. Le lot est copié en masse (`COPY`) dans `staging.observation`, une table vidée à chaque exécution.
2. Une seule requête `INSERT … ON CONFLICT … DO UPDATE` fusionne le staging dans `core.fact_observation`.
3. La clause `WHERE … IS DISTINCT FROM …` ne met à jour **que** les valeurs réellement révisées.
4. `RETURNING (xmax = 0)` distingue les lignes insérées des lignes mises à jour.

### 3. Tout dans une transaction, avec un journal des exécutions
- Fusion, quarantaine et compteurs sont validés ensemble (`COMMIT`), ou pas du tout (`ROLLBACK`).
- Le journal `ops.pipeline_run` est validé **à part**, au démarrage : une exécution en échec reste tracée.

## Conséquences

- ✅ Relancer sans changement côté OMS donne « 0 insérée, 0 mise à jour » : l'idempotence est **mesurable**
- ✅ `last_changed_at` et `last_run_id` disent quand et par quelle exécution chaque valeur a changé
- ✅ `COPY` charge environ 130 000 lignes en quelques secondes
- ⚠️ Une observation **supprimée** par l'OMS reste en base : la suppression n'est pas gérée (limite documentée)
- ⚠️ Seule la dernière valeur est conservée, pas l'historique complet des révisions (historisation prévue au projet 2)
