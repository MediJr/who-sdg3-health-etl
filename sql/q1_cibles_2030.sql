-- Q1 · Où en sont les pays de la région africaine par rapport aux cibles de 2030 ?
-- Pour chaque indicateur à cible : dernière valeur de chaque pays, comparée à la cible,
-- puis médiane régionale et valeur mondiale de référence.
WITH derniere AS (
    SELECT * FROM core.v_latest
    WHERE location_type = 'COUNTRY' AND who_region = 'AFR' AND target_2030 IS NOT NULL
),
mondial AS (
    SELECT indicator_code, year AS annee_mondiale, value AS valeur_mondiale
    FROM core.v_latest WHERE location_type = 'GLOBAL'
)
SELECT
    d.indicator_code                                                   AS indicateur,
    d.name_fr                                                          AS libelle,
    d.target_2030                                                      AS cible_2030,
    count(*)                                                           AS pays,
    count(*) FILTER (WHERE (d.target_direction = 'max' AND d.value <= d.target_2030)
                        OR (d.target_direction = 'min' AND d.value >= d.target_2030)) AS pays_cible_atteinte,
    round(100.0 * count(*) FILTER (WHERE (d.target_direction = 'max' AND d.value <= d.target_2030)
                        OR (d.target_direction = 'min' AND d.value >= d.target_2030)) / count(*), 0) AS pct_cible_atteinte,
    round(percentile_cont(0.5) WITHIN GROUP (ORDER BY d.value)::numeric, 1) AS mediane_afrique,
    round(m.valeur_mondiale, 1)                                        AS valeur_mondiale,
    m.annee_mondiale
FROM derniere AS d
LEFT JOIN mondial AS m USING (indicator_code)
GROUP BY d.indicator_code, d.name_fr, d.target_2030, m.valeur_mondiale, m.annee_mondiale
ORDER BY d.indicator_code;
