"""Tests d'intégration du chargement : ils utilisent une VRAIE base PostgreSQL.

Une base de test dédiée (« <POSTGRES_DB>_test ») est créée puis recréée à chaque session :
les tests ne touchent jamais aux données réelles. Ils sont ignorés si PostgreSQL ne répond pas.
Lancement seul :  pytest -m integration
"""

import psycopg
import pytest

from src import config, load as load_module

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def test_database():
    try:
        settings = config.database_settings()
        admin = psycopg.connect(**{**settings, "dbname": "postgres", "connect_timeout": 3}, autocommit=True)
    except (psycopg.OperationalError, RuntimeError) as error:
        pytest.skip(f"PostgreSQL indisponible ({error}) : lancez « docker compose up -d »")
    name = f"{settings['dbname']}_test"
    admin.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')
    admin.execute(f'CREATE DATABASE "{name}"')
    yield {**settings, "dbname": name}
    admin.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')
    admin.close()


@pytest.fixture
def fresh_database(test_database, monkeypatch):
    """Base vide avant chaque test, et pipeline redirigé vers elle."""
    with psycopg.connect(**test_database, autocommit=True) as connection:
        connection.execute("DROP SCHEMA IF EXISTS core, staging, ops CASCADE")
    monkeypatch.setattr(load_module, "connect", lambda: psycopg.connect(**test_database))
    return test_database


def test_premier_chargement_insere_tout(fresh_database, transform_result):
    counts = load_module.load(transform_result, raw_batch="test")
    assert (counts["inserted"], counts["updated"], counts["unchanged"]) == (8, 0, 0)


def test_relance_idempotente_aucune_modification(fresh_database, transform_result):
    """Critère C2 : relancer sans changement côté OMS ne crée ni ne modifie aucune ligne."""
    load_module.load(transform_result, raw_batch="test")
    counts = load_module.load(transform_result, raw_batch="test")
    assert (counts["inserted"], counts["updated"], counts["unchanged"]) == (0, 0, 8)
    with psycopg.connect(**fresh_database) as connection:
        assert connection.execute("SELECT count(*) FROM core.fact_observation").fetchone()[0] == 8


def test_revision_par_l_oms_detectee_et_appliquee(fresh_database, transform_result):
    load_module.load(transform_result, raw_batch="test")
    transform_result.observations.loc[0, "value"] = 42.0
    counts = load_module.load(transform_result, raw_batch="test")
    assert (counts["inserted"], counts["updated"], counts["unchanged"]) == (0, 1, 7)


def test_quarantaine_conservee_en_base(fresh_database, transform_result):
    transform_result.quarantine.append({"indicator_code": "MDG_0000000007", "reason": "test",
                                        "raw_record": {"NumericValue": None}})
    load_module.load(transform_result, raw_batch="test")
    with psycopg.connect(**fresh_database) as connection:
        reason, raw = connection.execute("SELECT reason, raw_record FROM ops.quarantine").fetchone()
    assert reason == "test" and raw == {"NumericValue": None}


def test_contrainte_unicite_empeche_un_doublon(fresh_database, transform_result):
    """Même si le code Python laissait passer un doublon, la base le refuserait (défense en profondeur)."""
    load_module.load(transform_result, raw_batch="test")
    with psycopg.connect(**fresh_database) as connection:
        with pytest.raises(psycopg.errors.UniqueViolation):
            connection.execute("""
                INSERT INTO core.fact_observation (indicator_code, location_type, location_code, year,
                                                   sex, age_group, wealth_quintile, value)
                SELECT indicator_code, location_type, location_code, year, sex, age_group, wealth_quintile, value
                FROM core.fact_observation LIMIT 1
            """)
