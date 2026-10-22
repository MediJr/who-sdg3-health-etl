-- Q4 · Les moyens du système de santé vont-ils de pair avec une mortalité des moins de 5 ans plus faible ?
-- Pour chaque pays de la région africaine : dernière valeur (depuis 2015) de chaque indicateur de moyens,
-- comparée à la dernière mortalité des moins de 5 ans. Corrélation de rang (Spearman) : robuste aux valeurs extrêmes.
-- Rappel : une corrélation décrit un lien, elle ne prouve pas une cause.
WITH derniere AS (
    SELECT * FROM core.v_latest
    WHERE location_type = 'COUNTRY' AND who_region = 'AFR' AND year >= 2015
),
mortalite AS (
    SELECT location_code, value AS u5mr FROM derniere WHERE indicator_code = 'MDG_0000000007'
),
paires AS (
    SELECT d.indicator_code, d.name_fr, d.value AS moyen, m.u5mr
    FROM derniere AS d
    JOIN mortalite AS m USING (location_code)
    WHERE d.role = 'moyen'
),
rangs AS (
    SELECT indicator_code, name_fr, moyen, u5mr,
           rank() OVER (PARTITION BY indicator_code ORDER BY moyen) AS rang_moyen,
           rank() OVER (PARTITION BY indicator_code ORDER BY u5mr)  AS rang_u5mr
    FROM paires
)
SELECT
    indicator_code                                         AS indicateur,
    name_fr                                                AS moyen,
    count(*)                                               AS pays,
    round(corr(rang_moyen, rang_u5mr)::numeric, 2)         AS correlation_spearman,
    round(corr(moyen, u5mr)::numeric, 2)                   AS correlation_pearson
FROM rangs
GROUP BY indicator_code, name_fr
ORDER BY correlation_spearman;
