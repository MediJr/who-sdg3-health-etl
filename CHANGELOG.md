# Changelog

Toutes les évolutions notables du projet sont consignées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/). Le projet suit le [versionnage sémantique](https://semver.org/lang/fr/).

## [1.0.0] - 2026-10-22

Première version livrée au client.

### Ajouté
- Dossier de mission : brief client, compte rendu de cadrage, cahier des charges
- Base PostgreSQL 17 conteneurisée (Docker Compose), identifiants dans `.env` (modèle `.env.example`)
- Schéma en trois couches (`staging`, `core`, `ops`), clé métier `UNIQUE NULLS NOT DISTINCT`, vues d'analyse
- Pipeline en une commande (`python -m src.pipeline`) :
  - **Extract** : 9 indicateurs de l'OMS, réessais `urllib3.Retry`, pagination OData, couche brute gzip, manifeste SHA-256
  - **Transform** : ventilations rangées par type, 9 règles de qualité, quarantaine
  - **Load** : `COPY` vers staging, UPSERT avec compteurs insérées / mises à jour / inchangées, journal des exécutions
- 22 tests `pytest` (17 unitaires, 5 d'intégration sur une base dédiée)
- 8 requêtes SQL d'analyse et de recette, 5 graphiques en français et en anglais
- Rapports d'ingénierie des données en LaTeX, en français et en anglais (21 pages chacun)
- Dictionnaire de données, 3 ADR, journal de bord, PV de recette

### Corrigé (pendant le développement)
- Quarantaine générale causée par `None` devenu `NaN` dans une colonne pandas mixte (détecté par les tests)
- Seuils de vraisemblance trop stricts, qui rejetaient des valeurs historiques réelles (ADR 003)
- Connexion de 130 s : `localhost` résolu en IPv6. Hôte `127.0.0.1` et délai de connexion de 10 s ajoutés.
- Description des données par quintile de richesse : estimations annuelles, et non enquêtes ponctuelles
