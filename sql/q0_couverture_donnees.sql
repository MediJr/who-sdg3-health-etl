-- Q0 · Couverture des données dans la région africaine de l'OMS
-- Avant toute analyse : de combien de pays dispose-t-on, et à quel point les données sont-elles récentes ?
WITH pays_afr AS (
    SELECT location_code FROM core.dim_location
    WHERE location_type = 'COUNTRY' AND who_region = 'AFR'
)
SELECT
    i.indicator_code                                                   AS indicateur,
    i.name_fr                                                          AS libelle,
    (SELECT count(*) FROM pays_afr)                                    AS pays_region,
    count(l.location_code)                                             AS pays_avec_donnees,
    min(l.year)                                                        AS derniere_annee_min,
    percentile_disc(0.5) WITHIN GROUP (ORDER BY l.year)                AS derniere_annee_mediane,
    max(l.year)                                                        AS derniere_annee_max,
    count(*) FILTER (WHERE l.year >= 2020)                             AS pays_donnee_depuis_2020
FROM core.dim_indicator AS i
LEFT JOIN core.v_latest AS l
       ON l.indicator_code = i.indicator_code
      AND l.location_type = 'COUNTRY'
      AND l.location_code IN (SELECT location_code FROM pays_afr)
GROUP BY i.indicator_code, i.name_fr
ORDER BY i.role DESC, i.indicator_code;
