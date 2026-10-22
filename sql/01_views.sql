-- =============================================================================
--  Vues d'analyse (recréées à chaque exécution du pipeline)
--  Elles encapsulent les règles de grain : un analyste du client n'a plus à se demander
--  quelles lignes correspondent à la « valeur nationale ».
-- =============================================================================

-- Valeur nationale totale : les deux sexes, sans ventilation par richesse.
-- C'est exactement le filtre qui manquait au tableau Excel du client l'an dernier.
CREATE OR REPLACE VIEW core.v_national AS
SELECT
    o.indicator_code,
    i.name_fr,
    i.role,
    i.target_2030,
    i.target_direction,
    o.location_type,
    o.location_code,
    l.name        AS location_name,
    l.who_region,
    o.year,
    o.value,
    o.value_low,
    o.value_high
FROM core.fact_observation AS o
JOIN core.dim_indicator AS i USING (indicator_code)
JOIN core.dim_location  AS l USING (location_type, location_code)
WHERE (o.sex IS NULL OR o.sex = 'SEX_BTSX')
  AND (o.wealth_quintile IS NULL OR o.wealth_quintile = 'WEALTHQUINTILE_TOTL');

-- Dernière valeur disponible par indicateur et par lieu.
CREATE OR REPLACE VIEW core.v_latest AS
SELECT DISTINCT ON (indicator_code, location_type, location_code) *
FROM core.v_national
ORDER BY indicator_code, location_type, location_code, year DESC;
