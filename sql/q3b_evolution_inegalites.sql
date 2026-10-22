-- Q3b · L'écart de mortalité entre les plus pauvres et les plus riches se réduit-il ?
-- Ratio médian Q1 / Q5 (pays de la région africaine) en 1990, 2000, 2015 et 2024.
WITH paires AS (
    SELECT o.location_code, o.year,
           max(o.value) FILTER (WHERE o.wealth_quintile = 'WEALTHQUINTILE_WQ1') AS plus_pauvres,
           max(o.value) FILTER (WHERE o.wealth_quintile = 'WEALTHQUINTILE_WQ5') AS plus_riches
    FROM core.fact_observation AS o
    JOIN core.dim_location AS l USING (location_type, location_code)
    WHERE o.indicator_code = 'MDG_0000000007' AND o.location_type = 'COUNTRY' AND l.who_region = 'AFR'
      AND o.sex = 'SEX_BTSX' AND o.year IN (1990, 2000, 2015, 2024)
    GROUP BY o.location_code, o.year
)
SELECT
    year                                                                             AS annee,
    count(*)                                                                         AS pays,
    round(percentile_cont(0.5) WITHIN GROUP (ORDER BY plus_pauvres)::numeric, 1)     AS mortalite_mediane_q1,
    round(percentile_cont(0.5) WITHIN GROUP (ORDER BY plus_riches)::numeric, 1)      AS mortalite_mediane_q5,
    round(percentile_cont(0.5) WITHIN GROUP (ORDER BY plus_pauvres - plus_riches)::numeric, 1) AS ecart_absolu_median,
    round(percentile_cont(0.5) WITHIN GROUP (ORDER BY plus_pauvres / plus_riches)::numeric, 2) AS ratio_median
FROM paires
WHERE plus_pauvres IS NOT NULL AND plus_riches > 0
GROUP BY year
ORDER BY year;
