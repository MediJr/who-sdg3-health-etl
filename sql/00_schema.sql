-- =============================================================================
--  Schéma de la base OMS / ODD 3 (PostgreSQL 17)
--  Script IDEMPOTENT : il peut être exécuté à chaque lancement du pipeline sans rien casser
--  (« IF NOT EXISTS » partout). Contrairement au projet 0, on ne recrée PAS les tables :
--  les données sont conservées d'une exécution à l'autre et mises à jour par UPSERT.
--
--  Trois schémas, trois rôles :
--    staging : zone de transit, vidée à chaque exécution (données du lot en cours)
--    core    : données de référence, propres et historisées (ce qu'interroge le client)
--    ops     : métadonnées d'exploitation (journal des exécutions, quarantaine)
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS ops;

-- -----------------------------------------------------------------------------
--  ops : exploitation
-- -----------------------------------------------------------------------------

-- Une ligne par exécution du pipeline : quand, combien, avec quel résultat.
CREATE TABLE IF NOT EXISTS ops.pipeline_run (
    run_id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    raw_batch         TEXT        NOT NULL,           -- dossier du lot brut (AAAA-MM-JJ)
    started_at        TIMESTAMPTZ NOT NULL,
    finished_at       TIMESTAMPTZ,
    status            TEXT        NOT NULL CHECK (status IN ('running', 'success', 'failed')),
    rows_extracted    INTEGER,
    rows_inserted     INTEGER,
    rows_updated      INTEGER,
    rows_unchanged    INTEGER,
    rows_quarantined  INTEGER
);

-- Lignes refusées par les contrôles de qualité : jamais perdues, toujours expliquées.
CREATE TABLE IF NOT EXISTS ops.quarantine (
    quarantine_id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id          BIGINT      NOT NULL REFERENCES ops.pipeline_run (run_id),
    indicator_code  TEXT,
    reason          TEXT        NOT NULL,
    raw_record      JSONB       NOT NULL,             -- la ligne telle que reçue de l'OMS
    quarantined_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -----------------------------------------------------------------------------
--  core : dimensions
-- -----------------------------------------------------------------------------

-- Indicateurs suivis, avec leur cible ODD (référentiel défini dans src/config.py).
CREATE TABLE IF NOT EXISTS core.dim_indicator (
    indicator_code    TEXT PRIMARY KEY,               -- ex. MDG_0000000007
    name_en           TEXT NOT NULL,                  -- libellé officiel de l'OMS
    name_fr           TEXT NOT NULL,
    unit              TEXT NOT NULL,
    role              TEXT NOT NULL CHECK (role IN ('resultat', 'moyen', 'contexte')),
    target_2030       NUMERIC,                        -- NULL si l'indicateur n'a pas de cible chiffrée
    target_direction  TEXT CHECK (target_direction IN ('max', 'min')),  -- 'max' : la valeur doit rester SOUS la cible
    target_source     TEXT
);

-- Lieux : pays, régions OMS, monde, groupes de revenu… Un même code peut exister
-- dans deux typologies : la clé est donc le couple (type, code).
CREATE TABLE IF NOT EXISTS core.dim_location (
    location_type  TEXT NOT NULL,                     -- COUNTRY, REGION, GLOBAL, WORLDBANKINCOMEGROUP…
    location_code  TEXT NOT NULL,                     -- ex. SEN, AFR, GLOBAL
    name           TEXT,
    who_region     TEXT,                              -- région OMS du pays (AFR, EUR…), NULL sinon
    PRIMARY KEY (location_type, location_code)
);

-- Valeurs des dimensions de ventilation : sexe, tranche d'âge, quintile de richesse.
CREATE TABLE IF NOT EXISTS core.dim_breakdown (
    breakdown_code  TEXT PRIMARY KEY,                 -- ex. SEX_FMLE, WEALTHQUINTILE_WQ1
    breakdown_type  TEXT NOT NULL,                    -- SEX, AGEGROUP, WEALTHQUINTILE
    label           TEXT
);

-- -----------------------------------------------------------------------------
--  core : faits
-- -----------------------------------------------------------------------------

-- Une observation = la valeur d'un indicateur, pour un lieu, une année et une ventilation.
-- GRAIN : indicateur × lieu × année × sexe × âge × quintile de richesse.
CREATE TABLE IF NOT EXISTS core.fact_observation (
    observation_id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,   -- clé technique
    indicator_code   TEXT    NOT NULL REFERENCES core.dim_indicator (indicator_code),
    location_type    TEXT    NOT NULL,
    location_code    TEXT    NOT NULL,
    year             INTEGER NOT NULL CHECK (year BETWEEN 1900 AND 2100),
    sex              TEXT    REFERENCES core.dim_breakdown (breakdown_code),   -- NULL = sans ventilation
    age_group        TEXT    REFERENCES core.dim_breakdown (breakdown_code),
    wealth_quintile  TEXT    REFERENCES core.dim_breakdown (breakdown_code),
    value            NUMERIC NOT NULL,
    value_low        NUMERIC,                         -- borne basse de l'intervalle d'incertitude
    value_high       NUMERIC,                         -- borne haute
    who_updated_at   TIMESTAMPTZ,                     -- date de dernière mise à jour par l'OMS
    first_loaded_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_changed_at  TIMESTAMPTZ NOT NULL DEFAULT now(),  -- dernière modification détectée par le pipeline
    last_run_id      BIGINT REFERENCES ops.pipeline_run (run_id),
    FOREIGN KEY (location_type, location_code) REFERENCES core.dim_location (location_type, location_code),
    CHECK (value_low IS NULL OR value_high IS NULL OR value_low <= value_high),
    -- CLÉ MÉTIER : toutes les dimensions du grain. NULLS NOT DISTINCT (PostgreSQL 15+) :
    -- deux NULL sont considérés égaux, sinon « sans ventilation » pourrait être dupliqué à l'infini.
    CONSTRAINT uq_observation_business_key UNIQUE NULLS NOT DISTINCT
        (indicator_code, location_type, location_code, year, sex, age_group, wealth_quintile)
);

-- Index pour les requêtes d'analyse (filtres par indicateur, lieu et année).
CREATE INDEX IF NOT EXISTS ix_observation_indicator_location
    ON core.fact_observation (indicator_code, location_type, location_code, year);

-- -----------------------------------------------------------------------------
--  staging : zone de transit
-- -----------------------------------------------------------------------------

-- UNLOGGED : plus rapide, car PostgreSQL ne journalise pas ces écritures.
-- Acceptable ici : la table est vidée et rechargée à chaque exécution.
CREATE UNLOGGED TABLE IF NOT EXISTS staging.observation (
    indicator_code   TEXT,
    location_type    TEXT,
    location_code    TEXT,
    year             INTEGER,
    sex              TEXT,
    age_group        TEXT,
    wealth_quintile  TEXT,
    value            NUMERIC,
    value_low        NUMERIC,
    value_high       NUMERIC,
    who_updated_at   TIMESTAMPTZ
);
