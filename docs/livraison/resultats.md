# Résultats des requêtes SQL

> Fichier **généré automatiquement** par `python -m src.report` (lot brut du 2026-10-22).
> Ne pas modifier à la main : relancer le pipeline pour le régénérer.

## `controle_recette.sql`

| controle | resultat | detail |
|---|---|---|
| C2 · dernière exécution sans insertion ni mise à jour (relance à l'identique) | OK | run 3 : 0 insérées, 0 mises à jour, 129368 inchangées |
| C3 · aucun doublon sur la clé métier complète | OK | 0 doublon(s) |
| C4 · toute ligne extraite est soit chargée, soit en quarantaine | OK | 129368 extraites = 129368 chargées + 0 en quarantaine |
| Volumétrie · observations en base | INFO | 129368 |
| Volumétrie · exécutions réussies | INFO | 3 |

## `q0_couverture_donnees.sql`

| indicateur | libelle | pays_region | pays_avec_donnees | derniere_annee_min | derniere_annee_mediane | derniere_annee_max | pays_donnee_depuis_2020 |
|---|---|---|---|---|---|---|---|
| MDG_0000000007 | Mortalité des moins de 5 ans | 50 | 47 | 2024 | 2024 | 2024 | 47 |
| MDG_0000000026 | Taux de mortalité maternelle | 50 | 47 | 2023 | 2023 | 2023 | 47 |
| WHOSIS_000003 | Mortalité néonatale | 50 | 47 | 2024 | 2024 | 2024 | 47 |
| GHED_CHE_pc_US_SHA2011 | Dépenses courantes de santé par habitant | 50 | 47 | 2023 | 2023 | 2023 | 47 |
| HWF_0001 | Médecins | 50 | 47 | 2022 | 2024 | 2024 | 47 |
| MDG_0000000025 | Accouchements assistés par du personnel qualifié | 50 | 47 | 2010 | 2021 | 2024 | 32 |
| WHS4_100 | Couverture vaccinale DTP3 (enfants d'un an) | 50 | 47 | 2025 | 2025 | 2025 | 47 |
| WHOSIS_000001 | Espérance de vie à la naissance | 50 | 47 | 2023 | 2023 | 2023 | 47 |
| WHOSIS_000002 | Espérance de vie en bonne santé | 50 | 47 | 2023 | 2023 | 2023 | 47 |

## `q1_cibles_2030.sql`

| indicateur | libelle | cible_2030 | pays | pays_cible_atteinte | pct_cible_atteinte | mediane_afrique | valeur_mondiale | annee_mondiale |
|---|---|---|---|---|---|---|---|---|
| MDG_0000000007 | Mortalité des moins de 5 ans | 25 | 47 | 5 | 11 | 48.7 | 37.4 | 2024 |
| MDG_0000000026 | Taux de mortalité maternelle | 70 | 47 | 4 | 9 | 258.2 | 197.3 | 2023 |
| WHOSIS_000003 | Mortalité néonatale | 12 | 47 | 4 | 9 | 23.0 | 17.2 | 2024 |
| WHS4_100 | Couverture vaccinale DTP3 (enfants d'un an) | 90 | 47 | 16 | 34 | 84.0 | 85.0 | 2025 |

## `q2_rythme_2030.sql`

| indicateur | libelle | pays_code | pays | valeur_2015 | derniere_annee | derniere_valeur | cible_2030 | arr_observe_pct | arr_requis_pct | projection_2030 | statut |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MDG_0000000007 | Mortalité des moins de 5 ans | DZA | Algeria | 24.9 | 2024 | 21.6 | 25 | 1.56 | -2.41 | 19.7 | 1. Cible déjà atteinte |
| MDG_0000000007 | Mortalité des moins de 5 ans | CPV | Cabo Verde | 19.2 | 2024 | 11.1 | 25 | 6.02 | -13.47 | 7.8 | 1. Cible déjà atteinte |
| MDG_0000000007 | Mortalité des moins de 5 ans | MUS | Mauritius | 14.5 | 2024 | 15.4 | 25 | -0.62 | -8.11 | 15.9 | 1. Cible déjà atteinte |
| MDG_0000000007 | Mortalité des moins de 5 ans | STP | Sao Tome and Principe | 23.3 | 2024 | 13.6 | 25 | 6.04 | -10.20 | 9.4 | 1. Cible déjà atteinte |
| MDG_0000000007 | Mortalité des moins de 5 ans | SYC | Seychelles | 14.6 | 2024 | 14.0 | 25 | 0.47 | -9.71 | 13.6 | 1. Cible déjà atteinte |
| MDG_0000000007 | Mortalité des moins de 5 ans | AGO | Angola | 61.8 | 2024 | 49.0 | 25 | 2.57 | 11.22 | 42.0 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | BEN | Benin | 96.1 | 2024 | 74.7 | 25 | 2.80 | 18.25 | 63.2 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | BWA | Botswana | 46.7 | 2024 | 33.3 | 25 | 3.76 | 4.78 | 26.6 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | BFA | Burkina Faso | 100.8 | 2024 | 74.9 | 25 | 3.30 | 18.29 | 61.5 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | BDI | Burundi | 66.9 | 2024 | 47.1 | 25 | 3.92 | 10.54 | 37.2 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | CMR | Cameroon | 88.5 | 2024 | 64.8 | 25 | 3.46 | 15.88 | 52.7 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | CAF | Central African Republic | 113.7 | 2024 | 89.7 | 25 | 2.63 | 21.30 | 76.6 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | TCD | Chad | 128.7 | 2024 | 97.3 | 25 | 3.11 | 22.64 | 80.7 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | COM | Comoros | 48.9 | 2024 | 39.0 | 25 | 2.52 | 7.40 | 33.5 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | COG | Congo | 52.7 | 2024 | 39.1 | 25 | 3.31 | 7.46 | 32.1 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | CIV | Cote d'Ivoire | 85.5 | 2024 | 64.5 | 25 | 3.13 | 15.79 | 53.4 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | COD | Democratic Republic of the Congo | 91.9 | 2024 | 89.7 | 25 | 0.27 | 21.29 | 88.2 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | GNQ | Equatorial Guinea | 92.1 | 2024 | 68.0 | 25 | 3.38 | 16.67 | 55.5 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | ERI | Eritrea | 46.4 | 2024 | 34.3 | 25 | 3.35 | 5.27 | 28.0 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | SWZ | Eswatini | 57.5 | 2024 | 45.1 | 25 | 2.70 | 9.84 | 38.4 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | ETH | Ethiopia | 64.4 | 2024 | 44.5 | 25 | 4.11 | 9.61 | 34.8 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | GAB | Gabon | 44.4 | 2024 | 32.6 | 25 | 3.42 | 4.44 | 26.6 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | GMB | Gambia | 58.9 | 2024 | 42.4 | 25 | 3.66 | 8.81 | 34.0 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | GHA | Ghana | 52.5 | 2024 | 35.9 | 25 | 4.24 | 6.02 | 27.8 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | GIN | Guinea | 113.7 | 2024 | 92.1 | 25 | 2.34 | 21.74 | 80.1 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | GNB | Guinea-Bissau | 91.6 | 2024 | 67.3 | 25 | 3.42 | 16.51 | 54.8 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | KEN | Kenya | 46.8 | 2024 | 38.8 | 25 | 2.07 | 7.35 | 34.3 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | LSO | Lesotho | 75.1 | 2024 | 60.0 | 25 | 2.50 | 14.58 | 51.6 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | LBR | Liberia | 93.2 | 2024 | 86.4 | 25 | 0.84 | 20.67 | 82.1 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | MDG | Madagascar | 65.3 | 2024 | 62.4 | 25 | 0.50 | 15.25 | 60.6 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | MWI | Malawi | 57.4 | 2024 | 48.8 | 25 | 1.81 | 11.14 | 43.8 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | MLI | Mali | 109.7 | 2024 | 73.0 | 25 | 4.53 | 17.86 | 55.6 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | MRT | Mauritania | 49.1 | 2024 | 36.9 | 25 | 3.18 | 6.49 | 30.5 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | MOZ | Mozambique | 75.8 | 2024 | 59.4 | 25 | 2.71 | 14.43 | 50.5 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | NAM | Namibia | 51.8 | 2024 | 39.5 | 25 | 3.03 | 7.61 | 32.9 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | NER | Niger | 125.4 | 2024 | 110.7 | 25 | 1.38 | 24.80 | 101.9 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | NGA | Nigeria | 117.8 | 2024 | 115.6 | 25 | 0.21 | 25.53 | 114.2 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | RWA | Rwanda | 47.3 | 2024 | 37.7 | 25 | 2.51 | 6.86 | 32.5 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | SEN | Senegal | 52.2 | 2024 | 36.5 | 25 | 3.97 | 6.32 | 28.8 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | SLE | Sierra Leone | 136.8 | 2024 | 90.5 | 25 | 4.59 | 21.44 | 68.7 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | ZAF | South Africa | 38.2 | 2024 | 35.1 | 25 | 0.95 | 5.64 | 33.1 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | SSD | South Sudan | 240.8 | 2024 | 96.7 | 25 | 10.14 | 22.55 | 52.6 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | TGO | Togo | 75.2 | 2024 | 56.1 | 25 | 3.25 | 13.48 | 46.2 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | UGA | Uganda | 57.9 | 2024 | 48.7 | 25 | 1.92 | 11.12 | 43.4 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | TZA | United Republic of Tanzania | 54.3 | 2024 | 37.0 | 25 | 4.26 | 6.53 | 28.7 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | ZMB | Zambia | 60.2 | 2024 | 48.4 | 25 | 2.42 | 11.00 | 41.8 | 3. Progrès insuffisants |
| MDG_0000000007 | Mortalité des moins de 5 ans | ZWE | Zimbabwe | 59.2 | 2024 | 64.7 | 25 | -0.97 | 15.84 | 68.6 | 4. Stagnation ou recul |
| MDG_0000000026 | Taux de mortalité maternelle | DZA | Algeria | 79.5 | 2023 | 62.5 | 70 | 3.01 | -1.62 | 50.6 | 1. Cible déjà atteinte |
| MDG_0000000026 | Taux de mortalité maternelle | CPV | Cabo Verde | 46.4 | 2023 | 40.0 | 70 | 1.84 | -7.98 | 35.2 | 1. Cible déjà atteinte |
| MDG_0000000026 | Taux de mortalité maternelle | MUS | Mauritius | 61.5 | 2023 | 65.9 | 70 | -0.87 | -0.86 | 70.0 | 1. Cible déjà atteinte |
| MDG_0000000026 | Taux de mortalité maternelle | SYC | Seychelles | 46.5 | 2023 | 41.9 | 70 | 1.30 | -7.33 | 38.2 | 1. Cible déjà atteinte |
| MDG_0000000026 | Taux de mortalité maternelle | SWZ | Eswatini | 283.0 | 2023 | 117.9 | 70 | 10.94 | 7.45 | 54.8 | 2. En bonne voie |
| MDG_0000000026 | Taux de mortalité maternelle | MOZ | Mozambique | 182.5 | 2023 | 82.2 | 70 | 9.96 | 2.30 | 40.9 | 2. En bonne voie |
| MDG_0000000026 | Taux de mortalité maternelle | NAM | Namibia | 306.6 | 2023 | 138.9 | 70 | 9.90 | 9.78 | 69.4 | 2. En bonne voie |
| MDG_0000000026 | Taux de mortalité maternelle | STP | Sao Tome and Principe | 127.8 | 2023 | 75.4 | 70 | 6.60 | 1.05 | 47.5 | 2. En bonne voie |
| MDG_0000000026 | Taux de mortalité maternelle | ZMB | Zambia | 154.4 | 2023 | 85.5 | 70 | 7.40 | 2.85 | 50.9 | 2. En bonne voie |
| MDG_0000000026 | Taux de mortalité maternelle | AGO | Angola | 249.4 | 2023 | 183.2 | 70 | 3.85 | 13.74 | 139.9 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | BEN | Benin | 606.4 | 2023 | 518.2 | 70 | 1.96 | 28.60 | 451.7 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | BFA | Burkina Faso | 327.8 | 2023 | 241.8 | 70 | 3.81 | 17.71 | 185.2 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | BDI | Burundi | 525.2 | 2023 | 392.0 | 70 | 3.66 | 24.61 | 303.4 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | CMR | Cameroon | 417.3 | 2023 | 258.2 | 70 | 6.00 | 18.65 | 169.7 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | CAF | Central African Republic | 980.5 | 2023 | 691.7 | 70 | 4.36 | 32.72 | 509.8 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | TCD | Chad | 1176.0 | 2023 | 747.5 | 70 | 5.66 | 33.83 | 502.9 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | COM | Comoros | 236.6 | 2023 | 178.9 | 70 | 3.50 | 13.40 | 140.1 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | COG | Congo | 284.1 | 2023 | 241.1 | 70 | 2.05 | 17.67 | 208.8 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | CIV | Cote d'Ivoire | 505.1 | 2023 | 359.0 | 70 | 4.27 | 23.35 | 266.2 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | COD | Democratic Republic of the Congo | 545.4 | 2023 | 427.0 | 70 | 3.06 | 25.83 | 344.8 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | GNQ | Equatorial Guinea | 222.2 | 2023 | 173.7 | 70 | 3.08 | 12.98 | 140.0 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | ERI | Eritrea | 412.8 | 2023 | 291.4 | 70 | 4.36 | 20.37 | 214.8 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | ETH | Ethiopia | 400.7 | 2023 | 194.9 | 70 | 9.01 | 14.63 | 103.8 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | GAB | Gabon | 239.1 | 2023 | 232.7 | 70 | 0.34 | 17.16 | 227.1 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | GMB | Gambia | 526.7 | 2023 | 354.4 | 70 | 4.95 | 23.17 | 250.5 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | GHA | Ghana | 310.3 | 2023 | 234.3 | 70 | 3.51 | 17.26 | 183.3 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | GIN | Guinea | 641.7 | 2023 | 494.1 | 70 | 3.27 | 27.92 | 393.1 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | GNB | Guinea-Bissau | 631.2 | 2023 | 505.4 | 70 | 2.78 | 28.24 | 416.1 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | KEN | Kenya | 453.4 | 2023 | 378.8 | 70 | 2.25 | 24.12 | 323.7 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | LSO | Lesotho | 593.9 | 2023 | 478.0 | 70 | 2.71 | 27.45 | 395.4 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | LBR | Liberia | 784.2 | 2023 | 627.7 | 70 | 2.78 | 31.34 | 516.6 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | MDG | Madagascar | 473.9 | 2023 | 445.4 | 70 | 0.77 | 26.44 | 421.9 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | MWI | Malawi | 353.8 | 2023 | 225.0 | 70 | 5.66 | 16.68 | 151.3 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | MLI | Mali | 489.7 | 2023 | 367.3 | 70 | 3.59 | 23.68 | 285.6 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | MRT | Mauritania | 469.2 | 2023 | 381.1 | 70 | 2.60 | 24.21 | 317.6 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | NER | Niger | 473.0 | 2023 | 350.3 | 70 | 3.75 | 23.00 | 269.3 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | NGA | Nigeria | 1167.7 | 2023 | 992.8 | 70 | 2.03 | 37.89 | 861.4 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | RWA | Rwanda | 291.6 | 2023 | 229.5 | 70 | 2.99 | 16.96 | 186.1 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | SEN | Senegal | 356.7 | 2023 | 237.4 | 70 | 5.09 | 17.45 | 166.3 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | SLE | Sierra Leone | 730.1 | 2023 | 353.6 | 70 | 9.06 | 23.14 | 187.5 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | ZAF | South Africa | 150.4 | 2023 | 117.6 | 70 | 3.08 | 7.41 | 94.8 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | SSD | South Sudan | 1435.6 | 2023 | 691.8 | 70 | 9.12 | 32.73 | 365.2 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | TGO | Togo | 470.4 | 2023 | 348.9 | 70 | 3.73 | 22.95 | 268.7 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | UGA | Uganda | 299.2 | 2023 | 170.3 | 70 | 7.04 | 12.70 | 104.0 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | TZA | United Republic of Tanzania | 433.2 | 2023 | 275.8 | 70 | 5.64 | 19.59 | 185.8 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | ZWE | Zimbabwe | 427.9 | 2023 | 357.6 | 70 | 2.24 | 23.30 | 305.6 | 3. Progrès insuffisants |
| MDG_0000000026 | Taux de mortalité maternelle | BWA | Botswana | 140.5 | 2023 | 155.1 | 70 | -1.23 | 11.37 | 169.1 | 4. Stagnation ou recul |
| WHOSIS_000003 | Mortalité néonatale | CPV | Cabo Verde | 12.3 | 2024 | 8.0 | 12 | 4.74 | -6.68 | 6.0 | 1. Cible déjà atteinte |
| WHOSIS_000003 | Mortalité néonatale | MUS | Mauritius | 9.1 | 2024 | 9.6 | 12 | -0.63 | -3.73 | 10.0 | 1. Cible déjà atteinte |
| WHOSIS_000003 | Mortalité néonatale | STP | Sao Tome and Principe | 11.0 | 2024 | 6.4 | 12 | 5.97 | -10.47 | 4.5 | 1. Cible déjà atteinte |
| WHOSIS_000003 | Mortalité néonatale | SYC | Seychelles | 8.8 | 2024 | 8.3 | 12 | 0.65 | -6.06 | 8.0 | 1. Cible déjà atteinte |
| WHOSIS_000003 | Mortalité néonatale | DZA | Algeria | 15.2 | 2024 | 15.0 | 12 | 0.16 | 3.68 | 14.8 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | AGO | Angola | 20.9 | 2024 | 18.1 | 12 | 1.59 | 6.87 | 16.5 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | BEN | Benin | 31.4 | 2024 | 27.2 | 12 | 1.62 | 13.63 | 24.7 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | BWA | Botswana | 22.0 | 2024 | 17.6 | 12 | 2.45 | 6.42 | 15.2 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | BFA | Burkina Faso | 28.1 | 2024 | 23.8 | 12 | 1.86 | 11.38 | 21.2 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | BDI | Burundi | 23.5 | 2024 | 19.1 | 12 | 2.31 | 7.72 | 16.6 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | CMR | Cameroon | 29.5 | 2024 | 24.8 | 12 | 1.93 | 12.07 | 22.0 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | CAF | Central African Republic | 33.9 | 2024 | 29.9 | 12 | 1.38 | 15.23 | 27.6 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | TCD | Chad | 35.4 | 2024 | 30.4 | 12 | 1.71 | 15.49 | 27.4 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | COM | Comoros | 26.3 | 2024 | 22.1 | 12 | 1.92 | 10.21 | 19.7 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | COG | Congo | 19.7 | 2024 | 16.5 | 12 | 1.97 | 5.33 | 14.7 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | CIV | Cote d'Ivoire | 32.2 | 2024 | 27.4 | 12 | 1.81 | 13.76 | 24.6 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | COD | Democratic Republic of the Congo | 24.0 | 2024 | 23.6 | 12 | 0.18 | 11.29 | 23.4 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | GNQ | Equatorial Guinea | 31.5 | 2024 | 26.3 | 12 | 2.02 | 13.07 | 23.3 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | ERI | Eritrea | 19.4 | 2024 | 15.6 | 12 | 2.43 | 4.39 | 13.5 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | SWZ | Eswatini | 26.6 | 2024 | 25.0 | 12 | 0.69 | 12.24 | 24.0 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | ETH | Ethiopia | 32.3 | 2024 | 25.2 | 12 | 2.74 | 12.39 | 21.4 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | GAB | Gabon | 21.3 | 2024 | 16.3 | 12 | 2.93 | 5.14 | 13.7 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | GMB | Gambia | 29.0 | 2024 | 23.0 | 12 | 2.59 | 10.81 | 19.6 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | GHA | Ghana | 24.3 | 2024 | 18.1 | 12 | 3.30 | 6.82 | 14.8 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | GIN | Guinea | 33.7 | 2024 | 29.8 | 12 | 1.35 | 15.16 | 27.5 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | GNB | Guinea-Bissau | 39.1 | 2024 | 32.0 | 12 | 2.23 | 16.34 | 28.0 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | KEN | Kenya | 23.2 | 2024 | 20.7 | 12 | 1.29 | 9.09 | 19.2 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | LSO | Lesotho | 34.1 | 2024 | 28.5 | 12 | 2.01 | 14.41 | 25.3 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | LBR | Liberia | 34.0 | 2024 | 32.9 | 12 | 0.35 | 16.83 | 32.2 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | MDG | Madagascar | 23.7 | 2024 | 23.1 | 12 | 0.30 | 10.89 | 22.7 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | MWI | Malawi | 24.0 | 2024 | 23.6 | 12 | 0.21 | 11.28 | 23.3 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | MLI | Mali | 35.4 | 2024 | 28.0 | 12 | 2.60 | 14.12 | 24.0 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | MRT | Mauritania | 25.6 | 2024 | 20.8 | 12 | 2.29 | 9.18 | 18.1 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | MOZ | Mozambique | 26.6 | 2024 | 25.1 | 12 | 0.64 | 12.29 | 24.1 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | NAM | Namibia | 24.6 | 2024 | 21.4 | 12 | 1.57 | 9.62 | 19.5 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | NER | Niger | 34.5 | 2024 | 32.8 | 12 | 0.56 | 16.73 | 31.7 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | RWA | Rwanda | 19.9 | 2024 | 17.4 | 12 | 1.52 | 6.15 | 15.8 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | SEN | Senegal | 25.4 | 2024 | 20.9 | 12 | 2.14 | 9.28 | 18.4 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | SLE | Sierra Leone | 34.0 | 2024 | 28.3 | 12 | 2.05 | 14.28 | 25.0 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | SSD | South Sudan | 41.8 | 2024 | 39.5 | 12 | 0.64 | 19.84 | 38.0 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | TGO | Togo | 26.7 | 2024 | 22.6 | 12 | 1.87 | 10.54 | 20.2 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | UGA | Uganda | 23.3 | 2024 | 21.3 | 12 | 0.98 | 9.59 | 20.1 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | TZA | United Republic of Tanzania | 23.4 | 2024 | 19.9 | 12 | 1.82 | 8.43 | 17.8 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | ZMB | Zambia | 23.4 | 2024 | 21.4 | 12 | 0.97 | 9.67 | 20.2 | 3. Progrès insuffisants |
| WHOSIS_000003 | Mortalité néonatale | NGA | Nigeria | 38.0 | 2024 | 39.0 | 12 | -0.31 | 19.66 | 39.8 | 4. Stagnation ou recul |
| WHOSIS_000003 | Mortalité néonatale | ZAF | South Africa | 11.7 | 2024 | 12.4 | 12 | -0.71 | 0.60 | 13.0 | 4. Stagnation ou recul |
| WHOSIS_000003 | Mortalité néonatale | ZWE | Zimbabwe | 27.3 | 2024 | 33.7 | 12 | -2.33 | 17.20 | 38.7 | 4. Stagnation ou recul |

## `q2b_synthese_rythme.sql`

| indicateur | libelle | pays | deja_atteinte | en_bonne_voie | progres_insuffisants | stagnation_ou_recul | arr_median_pct |
|---|---|---|---|---|---|---|---|
| MDG_0000000007 | Mortalité des moins de 5 ans | 47 | 5 | 0 | 41 | 1 | 3.03 |
| MDG_0000000026 | Taux de mortalité maternelle | 47 | 4 | 5 | 37 | 1 | 3.59 |
| WHOSIS_000003 | Mortalité néonatale | 47 | 4 | 0 | 40 | 3 | 1.71 |

## `q3_inegalites_richesse.sql`

| pays_code | pays | annee_enquete | mortalite_q1_plus_pauvres | mortalite_q5_plus_riches | ecart_absolu | ratio_pauvres_riches |
|---|---|---|---|---|---|---|
| AGO | Angola | 2024 | 58.4 | 35.2 | 23.2 | 1.66 |
| BDI | Burundi | 2024 | 61.5 | 32.4 | 29.2 | 1.90 |
| BEN | Benin | 2024 | 83.5 | 49.3 | 34.2 | 1.69 |
| BFA | Burkina Faso | 2024 | 91.5 | 51.0 | 40.4 | 1.79 |
| CAF | Central African Republic | 2024 | 110.4 | 62.9 | 47.5 | 1.75 |
| CIV | Cote d'Ivoire | 2024 | 82.5 | 43.9 | 38.6 | 1.88 |
| CMR | Cameroon | 2024 | 86.3 | 39.7 | 46.6 | 2.18 |
| COD | Democratic Republic of the Congo | 2024 | 109.5 | 55.8 | 53.7 | 1.96 |
| COG | Congo | 2024 | 48.5 | 28.8 | 19.7 | 1.68 |
| COM | Comoros | 2024 | 50.6 | 27.5 | 23.1 | 1.84 |
| DZA | Algeria | 2024 | 29.1 | 16.1 | 13.0 | 1.81 |
| ERI | Eritrea | 2024 | 37.4 | 22.7 | 14.7 | 1.65 |
| ETH | Ethiopia | 2024 | 51.3 | 35.7 | 15.6 | 1.44 |
| GAB | Gabon | 2024 | 42.4 | 22.7 | 19.7 | 1.87 |
| GHA | Ghana | 2024 | 46.3 | 26.9 | 19.4 | 1.72 |
| GIN | Guinea | 2024 | 118.4 | 56.6 | 61.7 | 2.09 |
| GMB | Gambia | 2024 | 54.9 | 28.0 | 27.0 | 1.96 |
| GNB | Guinea-Bissau | 2024 | 79.3 | 52.5 | 26.8 | 1.51 |
| GNQ | Equatorial Guinea | 2024 | 82.2 | 58.6 | 23.6 | 1.40 |
| KEN | Kenya | 2024 | 46.2 | 30.1 | 16.0 | 1.53 |
| LBR | Liberia | 2024 | 94.6 | 74.9 | 19.7 | 1.26 |
| LSO | Lesotho | 2024 | 68.2 | 46.5 | 21.7 | 1.47 |
| MDG | Madagascar | 2024 | 75.8 | 40.7 | 35.1 | 1.86 |
| MLI | Mali | 2024 | 96.1 | 40.1 | 56.0 | 2.40 |
| MOZ | Mozambique | 2024 | 67.7 | 46.8 | 21.0 | 1.45 |
| MRT | Mauritania | 2024 | 47.4 | 24.6 | 22.8 | 1.93 |
| MWI | Malawi | 2024 | 56.5 | 37.6 | 18.9 | 1.50 |
| NAM | Namibia | 2024 | 49.1 | 26.1 | 23.0 | 1.88 |
| NER | Niger | 2024 | 118.4 | 77.7 | 40.7 | 1.52 |
| NGA | Nigeria | 2024 | 150.7 | 59.5 | 91.2 | 2.53 |
| RWA | Rwanda | 2024 | 47.9 | 27.9 | 19.9 | 1.71 |
| SEN | Senegal | 2024 | 51.2 | 23.0 | 28.1 | 2.22 |
| SLE | Sierra Leone | 2024 | 105.0 | 74.0 | 31.0 | 1.42 |
| SSD | South Sudan | 2024 | 105.0 | 92.0 | 13.0 | 1.14 |
| STP | Sao Tome and Principe | 2024 | 17.5 | 11.4 | 6.1 | 1.53 |
| SWZ | Eswatini | 2024 | 57.0 | 35.4 | 21.6 | 1.61 |
| TCD | Chad | 2024 | 96.0 | 81.5 | 14.5 | 1.18 |
| TGO | Togo | 2024 | 74.3 | 32.5 | 41.8 | 2.29 |
| TZA | United Republic of Tanzania | 2024 | 39.6 | 34.0 | 5.5 | 1.16 |
| UGA | Uganda | 2024 | 60.5 | 34.9 | 25.6 | 1.73 |
| ZAF | South Africa | 2024 | 48.8 | 21.4 | 27.4 | 2.28 |
| ZMB | Zambia | 2024 | 54.6 | 41.2 | 13.4 | 1.33 |
| ZWE | Zimbabwe | 2024 | 75.5 | 48.8 | 26.7 | 1.55 |

## `q3b_evolution_inegalites.sql`

| annee | pays | mortalite_mediane_q1 | mortalite_mediane_q5 | ecart_absolu_median | ratio_median |
|---|---|---|---|---|---|
| 1990 | 43 | 186.6 | 118.8 | 63.3 | 1.56 |
| 2000 | 43 | 159.7 | 94.2 | 50.5 | 1.49 |
| 2015 | 43 | 74.4 | 46.3 | 28.2 | 1.67 |
| 2024 | 43 | 61.5 | 37.6 | 23.2 | 1.71 |

## `q4_moyens_resultats.sql`

| indicateur | moyen | pays | correlation_spearman | correlation_pearson |
|---|---|---|---|---|
| MDG_0000000025 | Accouchements assistés par du personnel qualifié | 45 | -0.75 | -0.69 |
| HWF_0001 | Médecins | 47 | -0.54 | -0.49 |
| WHS4_100 | Couverture vaccinale DTP3 (enfants d'un an) | 47 | -0.49 | -0.47 |
| GHED_CHE_pc_US_SHA2011 | Dépenses courantes de santé par habitant | 47 | -0.48 | -0.51 |
