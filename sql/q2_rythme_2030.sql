-- Q2 · À leur rythme actuel, quels pays atteindront les cibles de mortalité d'ici 2030 ?
--
-- Méthode du taux annuel moyen de réduction (ARR, Annual Rate of Reduction), utilisée par le
-- groupe interagences des Nations unies pour l'estimation de la mortalité de l'enfant (UN IGME) :
--   ARR observé = ln(valeur 2015 / dernière valeur) / (dernière année - 2015)
--   Projection 2030 = dernière valeur × exp(-ARR × (2030 - dernière année))
--   ARR requis = ln(dernière valeur / cible) / (2030 - dernière année)
-- Hypothèse : le rythme observé depuis 2015 se maintient jusqu'en 2030.
WITH serie AS (
    SELECT * FROM core.v_national
    WHERE location_type = 'COUNTRY' AND who_region = 'AFR'
      AND role = 'resultat' AND value > 0
),
bornes AS (
    SELECT
        s.indicator_code, s.name_fr, s.target_2030, s.location_code, s.location_name,
        max(s.value) FILTER (WHERE s.year = 2015) AS valeur_2015,
        max(s.year)                               AS derniere_annee
    FROM serie AS s
    GROUP BY s.indicator_code, s.name_fr, s.target_2030, s.location_code, s.location_name
),
calcul AS (
    SELECT
        b.*,
        s.value AS derniere_valeur,
        ln(b.valeur_2015 / s.value) / NULLIF(b.derniere_annee - 2015, 0) AS arr
    FROM bornes AS b
    JOIN serie AS s
      ON s.indicator_code = b.indicator_code AND s.location_code = b.location_code AND s.year = b.derniere_annee
    WHERE b.valeur_2015 IS NOT NULL
)
SELECT
    indicator_code                                                         AS indicateur,
    name_fr                                                                AS libelle,
    location_code                                                          AS pays_code,
    location_name                                                          AS pays,
    round(valeur_2015, 1)                                                  AS valeur_2015,
    derniere_annee,
    round(derniere_valeur, 1)                                              AS derniere_valeur,
    target_2030                                                            AS cible_2030,
    round(100 * arr, 2)                                                    AS arr_observe_pct,
    round(100 * ln(derniere_valeur / target_2030) / (2030 - derniere_annee), 2) AS arr_requis_pct,
    round(derniere_valeur * exp(-arr * (2030 - derniere_annee)), 1)        AS projection_2030,
    CASE
        WHEN derniere_valeur <= target_2030                                       THEN '1. Cible déjà atteinte'
        WHEN derniere_valeur * exp(-arr * (2030 - derniere_annee)) <= target_2030 THEN '2. En bonne voie'
        WHEN arr > 0                                                              THEN '3. Progrès insuffisants'
        ELSE                                                                           '4. Stagnation ou recul'
    END                                                                    AS statut
FROM calcul
ORDER BY indicateur, statut, pays;
