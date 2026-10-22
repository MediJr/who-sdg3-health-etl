"""Étape L : chargement dans PostgreSQL par « staging + UPSERT ».

Différence majeure avec le projet 0 (rechargement complet) :
- les données sont CONSERVÉES d'une exécution à l'autre ;
- chaque observation est insérée si elle est nouvelle, mise à jour si l'OMS l'a révisée,
  et laissée intacte sinon (UPSERT = INSERT … ON CONFLICT … DO UPDATE) ;
- on sait donc, pour chaque exécution, combien de lignes sont nouvelles, révisées ou inchangées.

Le lot passe d'abord par une table de transit (staging), remplie en masse avec COPY,
puis la fusion vers core se fait en une seule requête SQL, dans une transaction.
"""

import logging
from datetime import datetime, timezone

import pandas as pd
import psycopg
from psycopg.types.json import Jsonb

from src import config
from src.transform import TransformResult

logger = logging.getLogger(__name__)

STAGING_COLUMNS = ["indicator_code", "location_type", "location_code", "year", "sex", "age_group",
                   "wealth_quintile", "value", "value_low", "value_high", "who_updated_at"]

# Fusion staging → core. La clause WHERE de DO UPDATE évite de « toucher » une ligne dont les valeurs
# n'ont pas changé : l'exécution reste idempotente et last_changed_at garde un sens.
# xmax = 0 est une astuce PostgreSQL : vrai pour une ligne insérée, faux pour une ligne mise à jour.
UPSERT_OBSERVATIONS = """
WITH upserted AS (
    INSERT INTO core.fact_observation AS f
        (indicator_code, location_type, location_code, year, sex, age_group, wealth_quintile,
         value, value_low, value_high, who_updated_at, last_run_id)
    SELECT indicator_code, location_type, location_code, year, sex, age_group, wealth_quintile,
           value, value_low, value_high, who_updated_at, %(run_id)s
    FROM staging.observation
    ON CONFLICT ON CONSTRAINT uq_observation_business_key DO UPDATE SET
        value           = EXCLUDED.value,
        value_low       = EXCLUDED.value_low,
        value_high      = EXCLUDED.value_high,
        who_updated_at  = EXCLUDED.who_updated_at,
        last_changed_at = now(),
        last_run_id     = EXCLUDED.last_run_id
    WHERE (f.value, f.value_low, f.value_high)
          IS DISTINCT FROM (EXCLUDED.value, EXCLUDED.value_low, EXCLUDED.value_high)
    RETURNING (xmax = 0) AS inserted
)
SELECT count(*) FILTER (WHERE inserted)     AS inserted,
       count(*) FILTER (WHERE NOT inserted) AS updated
FROM upserted
"""


def connect() -> psycopg.Connection:
    return psycopg.connect(**config.database_settings())


def apply_schema(connection: psycopg.Connection) -> None:
    """Crée schémas, tables et vues s'ils n'existent pas encore (scripts idempotents)."""
    for script in ("00_schema.sql", "01_views.sql"):
        connection.execute((config.SQL_DIR / script).read_text(encoding="utf-8"))
    connection.commit()


def _records(frame: pd.DataFrame) -> list[dict]:
    """Lignes d'un DataFrame en dictionnaires, avec None à la place des NaN (NULL en SQL)."""
    return frame.astype(object).where(pd.notna(frame), None).to_dict("records")


def _upsert_dimensions(cursor: psycopg.Cursor, result: TransformResult) -> None:
    cursor.executemany("""
        INSERT INTO core.dim_indicator (indicator_code, name_en, name_fr, unit, role,
                                        target_2030, target_direction, target_source)
        VALUES (%(indicator_code)s, %(name_en)s, %(name_fr)s, %(unit)s, %(role)s,
                %(target_2030)s, %(target_direction)s, %(target_source)s)
        ON CONFLICT (indicator_code) DO UPDATE SET
            name_en = EXCLUDED.name_en, name_fr = EXCLUDED.name_fr, unit = EXCLUDED.unit, role = EXCLUDED.role,
            target_2030 = EXCLUDED.target_2030, target_direction = EXCLUDED.target_direction,
            target_source = EXCLUDED.target_source
    """, _records(result.indicators))
    cursor.executemany("""
        INSERT INTO core.dim_location (location_type, location_code, name, who_region)
        VALUES (%(location_type)s, %(location_code)s, %(name)s, %(who_region)s)
        ON CONFLICT (location_type, location_code) DO UPDATE SET
            name = EXCLUDED.name, who_region = EXCLUDED.who_region
    """, _records(result.locations))
    cursor.executemany("""
        INSERT INTO core.dim_breakdown (breakdown_code, breakdown_type, label)
        VALUES (%(breakdown_code)s, %(breakdown_type)s, %(label)s)
        ON CONFLICT (breakdown_code) DO UPDATE SET
            breakdown_type = EXCLUDED.breakdown_type, label = EXCLUDED.label
    """, _records(result.breakdowns))


def _copy_to_staging(cursor: psycopg.Cursor, observations: pd.DataFrame) -> None:
    """Remplit la table de transit avec COPY : des dizaines de fois plus rapide que des INSERT."""
    cursor.execute("TRUNCATE staging.observation")
    with cursor.copy(f"COPY staging.observation ({', '.join(STAGING_COLUMNS)}) FROM STDIN") as copy:
        for row in observations[STAGING_COLUMNS].astype(object).where(pd.notna(observations[STAGING_COLUMNS]), None).itertuples(index=False):
            copy.write_row(row)


def load(result: TransformResult, raw_batch: str) -> dict:
    """Charge un lot transformé. Renvoie les compteurs de l'exécution."""
    with connect() as connection:
        apply_schema(connection)

        # Le journal d'exécution est validé à part : un échec reste ainsi tracé.
        run_id = connection.execute(
            "INSERT INTO ops.pipeline_run (raw_batch, started_at, status, rows_extracted) "
            "VALUES (%s, %s, 'running', %s) RETURNING run_id",
            (raw_batch, datetime.now(timezone.utc), result.rows_extracted)).fetchone()[0]
        connection.commit()

        try:
            with connection.transaction(), connection.cursor() as cursor:
                _upsert_dimensions(cursor, result)
                _copy_to_staging(cursor, result.observations)
                inserted, updated = cursor.execute(UPSERT_OBSERVATIONS, {"run_id": run_id}).fetchone()
                cursor.executemany(
                    "INSERT INTO ops.quarantine (run_id, indicator_code, reason, raw_record) VALUES (%s, %s, %s, %s)",
                    [(run_id, q["indicator_code"], q["reason"], Jsonb(q["raw_record"])) for q in result.quarantine])
                counts = {
                    "run_id": run_id,
                    "inserted": inserted,
                    "updated": updated,
                    "unchanged": len(result.observations) - inserted - updated,
                    "quarantined": len(result.quarantine),
                }
                cursor.execute("""
                    UPDATE ops.pipeline_run SET finished_at = now(), status = 'success',
                        rows_inserted = %(inserted)s, rows_updated = %(updated)s,
                        rows_unchanged = %(unchanged)s, rows_quarantined = %(quarantined)s
                    WHERE run_id = %(run_id)s
                """, counts)
        except Exception:
            connection.execute("UPDATE ops.pipeline_run SET finished_at = now(), status = 'failed' WHERE run_id = %s",
                               (run_id,))
            connection.commit()
            raise

    logger.info("Exécution n°%d : %d insérées, %d mises à jour, %d inchangées, %d en quarantaine",
                counts["run_id"], counts["inserted"], counts["updated"], counts["unchanged"], counts["quarantined"])
    return counts
