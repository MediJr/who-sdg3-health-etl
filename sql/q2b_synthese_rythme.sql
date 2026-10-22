-- Q2b · Synthèse : nombre de pays par statut de trajectoire, pour chaque indicateur de mortalité.
-- Reprend exactement les calculs de q2_rythme_2030.sql (même méthode ARR, même hypothèse).
WITH serie AS (
    SELECT * FROM core.v_national
    WHERE location_type = 'COUNTRY' AND who_region = 'AFR' AND role = 'resultat' AND value > 0
),
bornes AS (
    SELECT indicator_code, name_fr, target_2030, location_code,
           max(value) FILTER (WHERE year = 2015) AS valeur_2015, max(year) AS derniere_annee
    FROM serie GROUP BY indicator_code, name_fr, target_2030, location_code
),
calcul AS (
    SELECT b.*, s.value AS derniere_valeur,
           ln(b.valeur_2015 / s.value) / NULLIF(b.derniere_annee - 2015, 0) AS arr
    FROM bornes b
    JOIN serie s ON s.indicator_code = b.indicator_code AND s.location_code = b.location_code AND s.year = b.derniere_annee
    WHERE b.valeur_2015 IS NOT NULL
)
SELECT
    indicator_code AS indicateur,
    name_fr        AS libelle,
    count(*)       AS pays,
    count(*) FILTER (WHERE derniere_valeur <= target_2030)                                         AS deja_atteinte,
    count(*) FILTER (WHERE derniere_valeur > target_2030
                       AND derniere_valeur * exp(-arr * (2030 - derniere_annee)) <= target_2030)    AS en_bonne_voie,
    count(*) FILTER (WHERE derniere_valeur > target_2030 AND arr > 0
                       AND derniere_valeur * exp(-arr * (2030 - derniere_annee)) > target_2030)     AS progres_insuffisants,
    count(*) FILTER (WHERE derniere_valeur > target_2030 AND arr <= 0)                             AS stagnation_ou_recul,
    round(100 * percentile_cont(0.5) WITHIN GROUP (ORDER BY arr)::numeric, 2)                     AS arr_median_pct
FROM calcul
GROUP BY indicator_code, name_fr
ORDER BY indicator_code;
