-- Q3 · Écart de mortalité des moins de 5 ans entre les ménages les plus pauvres (Q1) et les plus riches (Q5)
-- Estimations annuelles modélisées publiées par l'OMS (1990-2024, 106 pays dans le monde).
-- On retient, pour chaque pays, la dernière année où les deux quintiles existent.
WITH quintiles AS (
    SELECT o.location_code, l.name AS pays, o.year, o.wealth_quintile, o.value
    FROM core.fact_observation AS o
    JOIN core.dim_location AS l USING (location_type, location_code)
    WHERE o.indicator_code = 'MDG_0000000007'
      AND o.location_type = 'COUNTRY' AND l.who_region = 'AFR'
      AND o.sex = 'SEX_BTSX'
      AND o.wealth_quintile IN ('WEALTHQUINTILE_WQ1', 'WEALTHQUINTILE_WQ5')
),
paires AS (
    SELECT location_code, pays, year,
           max(value) FILTER (WHERE wealth_quintile = 'WEALTHQUINTILE_WQ1') AS plus_pauvres,
           max(value) FILTER (WHERE wealth_quintile = 'WEALTHQUINTILE_WQ5') AS plus_riches
    FROM quintiles
    GROUP BY location_code, pays, year
    HAVING count(DISTINCT wealth_quintile) = 2
)
SELECT DISTINCT ON (location_code)
    location_code                               AS pays_code,
    pays,
    year                                        AS annee_enquete,
    round(plus_pauvres, 1)                      AS mortalite_q1_plus_pauvres,
    round(plus_riches, 1)                       AS mortalite_q5_plus_riches,
    round(plus_pauvres - plus_riches, 1)        AS ecart_absolu,
    round(plus_pauvres / NULLIF(plus_riches, 0), 2) AS ratio_pauvres_riches
FROM paires
ORDER BY location_code, year DESC;
