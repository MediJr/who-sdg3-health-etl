# ADR 001 : PostgreSQL conteneurisé avec Docker Compose

- **Date :** 2026-10-22
- **Statut :** Acceptée

## Contexte

- L'équipe de suivi-évaluation du client doit interroger la base **en SQL, à plusieurs** (cahier des charges, section 3).
- Le projet 0 utilisait DuckDB, une base dans un fichier, pensée pour un seul utilisateur et pour l'analyse.
- La base doit pouvoir être recréée à l'identique sur n'importe quel poste.

## Décision

- **PostgreSQL 17** comme base de données, exécutée dans un **conteneur Docker** décrit par `docker-compose.yml`.
- Port exposé **uniquement sur la machine locale** (`127.0.0.1`), et port **5433** côté hôte pour éviter un conflit
  avec un PostgreSQL déjà installé.
- Identifiants lus dans un fichier **`.env`** exclu de Git. Un modèle sans secret, `.env.example`, est versionné.
- Un **volume Docker** conserve les données quand le conteneur s'arrête.
- Un **healthcheck** (`pg_isready`) indique quand la base accepte réellement les connexions.

## Alternatives écartées

| Option | Raison du rejet |
|---|---|
| DuckDB (projet 0) | Pas d'accès concurrent de plusieurs utilisateurs |
| PostgreSQL installé directement sur Windows | Installation manuelle, versions différentes selon les postes, difficile à recréer |
| Base cloud (Supabase, RDS…) | Coût et dépendance externe injustifiés à ce stade (au programme du projet 4) |

## Conséquences

- ✅ `docker compose up -d` suffit pour obtenir la même base partout
- ✅ Aucun secret dans le code ni dans le dépôt
- ✅ PostgreSQL apporte l'**UPSERT** natif et l'unicité **`NULLS NOT DISTINCT`** (version 15 et plus), utilisés par le pipeline
- ⚠️ Docker Desktop doit être installé et démarré sur le poste
