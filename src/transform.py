"""Étape T : des réponses brutes de l'OMS à des tables propres, contrôlées et au bon grain.

Deux idées centrales :
1. Les ventilations (sexe, âge, richesse) sont rangées selon leur TYPE déclaré (Dim1Type…),
   jamais selon leur position : l'OMS peut placer le sexe en Dim1 pour un indicateur et en Dim2 pour un autre.
2. Toute ligne qui échoue à un contrôle de qualité part en QUARANTAINE avec son motif.
   Elle n'est ni chargée, ni perdue en silence.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from src import config
from src.extract import read_raw

logger = logging.getLogger(__name__)

BUSINESS_KEY = ["indicator_code", "location_type", "location_code", "year", "sex", "age_group", "wealth_quintile"]
BREAKDOWN_COLUMNS = {"SEX": "sex", "AGEGROUP": "age_group", "WEALTHQUINTILE": "wealth_quintile"}


@dataclass
class TransformResult:
    indicators: pd.DataFrame
    locations: pd.DataFrame
    breakdowns: pd.DataFrame
    observations: pd.DataFrame
    quarantine: list[dict] = field(default_factory=list)
    rows_extracted: int = 0


# --- Dimensions --------------------------------------------------------------

def build_indicators(metadata: list[dict]) -> pd.DataFrame:
    """Référentiel des indicateurs : config.py (cible, rôle) + libellé officiel de l'OMS."""
    official = {record["IndicatorCode"]: record["IndicatorName"] for record in metadata}
    return pd.DataFrame([{
        "indicator_code": indicator.code,
        "name_en": official.get(indicator.code, indicator.code),
        "name_fr": indicator.name_fr,
        "unit": indicator.unit,
        "role": indicator.role,
        "target_2030": indicator.target_2030,
        "target_direction": indicator.target_direction,
        "target_source": indicator.target_source,
    } for indicator in config.INDICATORS])


def build_locations(dimension_files: dict[str, list[dict]]) -> pd.DataFrame:
    rows = []
    for location_type in config.LOCATION_TYPES:
        for record in dimension_files.get(location_type, []):
            rows.append({
                "location_type": location_type,
                "location_code": record["Code"],
                "name": record.get("Title"),
                # Seuls les pays ont une région OMS de rattachement.
                "who_region": record.get("ParentCode") if record.get("ParentDimension") == "REGION" else None,
            })
    locations = pd.DataFrame(rows, columns=["location_type", "location_code", "name", "who_region"])
    return locations.drop_duplicates(["location_type", "location_code"])


def build_breakdowns(dimension_files: dict[str, list[dict]]) -> pd.DataFrame:
    rows = [{"breakdown_code": record["Code"], "breakdown_type": breakdown_type, "label": record.get("Title")}
            for breakdown_type in config.BREAKDOWN_TYPES
            for record in dimension_files.get(breakdown_type, [])]
    breakdowns = pd.DataFrame(rows, columns=["breakdown_code", "breakdown_type", "label"])
    return breakdowns.drop_duplicates("breakdown_code")


# --- Observations ------------------------------------------------------------

def flatten_observation(record: dict) -> dict:
    """Aplatit une ligne OData de l'OMS. Les ventilations sont rangées selon leur type déclaré."""
    row = {
        "indicator_code": record.get("IndicatorCode"),
        "location_type": record.get("SpatialDimType"),
        "location_code": record.get("SpatialDim"),
        "year": record.get("TimeDim"),
        "sex": None, "age_group": None, "wealth_quintile": None,
        "value": record.get("NumericValue"),
        "value_low": record.get("Low"),
        "value_high": record.get("High"),
        "who_updated_at": record.get("Date"),
        "unknown_breakdown": None,
    }
    for position in ("Dim1", "Dim2", "Dim3"):
        breakdown_type = record.get(f"{position}Type")
        if breakdown_type is None:
            continue
        column = BREAKDOWN_COLUMNS.get(breakdown_type)
        if column is None:
            row["unknown_breakdown"] = breakdown_type     # type de ventilation imprévu : à mettre en quarantaine
        else:
            row[column] = record.get(position)
    return row


def quality_reasons(row: pd.Series, known_locations: set, known_breakdowns: set) -> list[str]:
    """Contrôles de qualité d'une observation. Une liste vide signifie « valide »."""
    reasons = []
    indicator = config.INDICATORS_BY_CODE.get(row["indicator_code"])
    if indicator is None:
        return ["indicateur hors référentiel"]
    # isinstance plutôt qu'un simple « if » : dans une colonne pandas mixte, None devient NaN,
    # et NaN est « vrai » en Python. Bug réel détecté par les tests (journal du 2026-10-22).
    if isinstance(row["unknown_breakdown"], str):
        reasons.append(f"type de ventilation inconnu : {row['unknown_breakdown']}")
    if pd.isna(row["value"]):
        reasons.append("valeur absente ou non numérique")
    elif not indicator.plausible_min <= row["value"] <= indicator.plausible_max:
        reasons.append(f"valeur hors bornes de vraisemblance [{indicator.plausible_min}, {indicator.plausible_max}]")
    if not pd.isna(row["value"]) and (
        (not pd.isna(row["value_low"]) and row["value_low"] > row["value"])
        or (not pd.isna(row["value_high"]) and row["value"] > row["value_high"])
    ):
        reasons.append("intervalle d'incertitude incohérent")
    if pd.isna(row["year"]) or not 1900 <= row["year"] <= 2100:
        reasons.append("année invalide")
    if (row["location_type"], row["location_code"]) not in known_locations:
        reasons.append("lieu absent du référentiel")
    for column in BREAKDOWN_COLUMNS.values():
        if row[column] is not None and not pd.isna(row[column]) and row[column] not in known_breakdowns:
            reasons.append(f"ventilation absente du référentiel : {row[column]}")
    return reasons


def validate_observations(records: list[dict], locations: pd.DataFrame,
                          breakdowns: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    """Sépare les observations valides des observations à mettre en quarantaine."""
    frame = pd.DataFrame([flatten_observation(record) for record in records])
    if frame.empty:
        return frame, []
    known_locations = set(zip(locations.location_type, locations.location_code))
    known_breakdowns = set(breakdowns.breakdown_code)

    reasons = frame.apply(quality_reasons, axis=1, args=(known_locations, known_breakdowns))

    # Doublons sur la clé métier : on garde la première occurrence, les suivantes vont en quarantaine.
    duplicated = frame.duplicated(BUSINESS_KEY, keep="first")
    reasons = [r + (["doublon de clé métier"] if dup else []) for r, dup in zip(reasons, duplicated)]

    quarantine = [{"indicator_code": records[i].get("IndicatorCode"), "reason": " ; ".join(r), "raw_record": records[i]}
                  for i, r in enumerate(reasons) if r]
    valid = frame[[not r for r in reasons]].drop(columns="unknown_breakdown")
    valid = valid.astype({"year": "int64"})
    valid["who_updated_at"] = pd.to_datetime(valid["who_updated_at"], utc=True, errors="coerce", format="ISO8601")
    return valid.reset_index(drop=True), quarantine


def transform(run_dir: Path) -> TransformResult:
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    files = {entry["file"]: read_raw(run_dir / entry["file"])["value"] for entry in manifest["files"]}

    dimension_files = {name.split("/")[1].removesuffix(".json.gz"): values
                       for name, values in files.items() if name.startswith("dimensions/")}
    indicators = build_indicators(files["metadata/indicators.json.gz"])
    locations = build_locations(dimension_files)
    breakdowns = build_breakdowns(dimension_files)

    records = [record for name, values in files.items() if name.startswith("indicators/") for record in values]
    observations, quarantine = validate_observations(records, locations, breakdowns)

    logger.info("Observations : %d extraites, %d valides, %d en quarantaine",
                len(records), len(observations), len(quarantine))
    logger.info("Référentiels : %d indicateurs, %d lieux, %d ventilations",
                len(indicators), len(locations), len(breakdowns))
    return TransformResult(indicators, locations, breakdowns, observations, quarantine, len(records))
