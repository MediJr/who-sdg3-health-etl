"""Paramètres du pipeline : périmètre (cahier des charges), connexion et comportement réseau.

Les secrets (identifiants PostgreSQL) ne sont PAS ici : ils sont lus dans le fichier .env,
exclu de Git. Ce fichier-ci peut donc être publié sans risque.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
LOG_DIR = PROJECT_DIR / "logs"
SQL_DIR = PROJECT_DIR / "sql"

load_dotenv(PROJECT_DIR / ".env")

# --- API de l'OMS (Global Health Observatory, protocole OData) -------------
GHO_BASE_URL = "https://ghoapi.azureedge.net/api"
REQUEST_TIMEOUT_SECONDS = 120     # certains indicateurs pèsent plusieurs dizaines de Mo
MAX_RETRIES = 4
BACKOFF_FACTOR = 2                # attentes entre réessais : 2 s, 4 s, 8 s, 16 s
USER_AGENT = "portfolio-etl-oms-odd3/1.0 (projet pedagogique, usage non commercial)"

# Typologies de lieux et de ventilations dont on télécharge les libellés.
LOCATION_TYPES = ["COUNTRY", "REGION", "GLOBAL", "WORLDBANKINCOMEGROUP",
                  "UNSDGREGION", "UNICEFREGION", "MGHEREG"]
BREAKDOWN_TYPES = ["SEX", "AGEGROUP", "WEALTHQUINTILE"]

# --- Périmètre d'analyse -----------------------------------------------------
FOCUS_REGION = "AFR"              # région africaine de l'OMS
BASELINE_YEAR = 2015              # adoption des ODD : point de départ du calcul de rythme (Q2)
TARGET_YEAR = 2030


@dataclass(frozen=True)
class Indicator:
    code: str
    name_fr: str
    unit: str
    role: str                     # 'resultat', 'moyen' ou 'contexte'
    # Bornes de vraisemblance des contrôles de qualité : des limites LOGIQUES (un taux pour 1 000 naissances
    # ne dépasse pas 1 000, un pourcentage pas 100), et non des seuils « intuitifs ». Voir l'ADR 003.
    plausible_min: float
    plausible_max: float
    target_2030: float | None = None
    target_direction: str | None = None   # 'max' : la valeur doit passer SOUS la cible
    target_source: str | None = None


# Référentiel des indicateurs (cahier des charges, section 3).
INDICATORS = [
    Indicator("MDG_0000000026", "Taux de mortalité maternelle", "pour 100 000 naissances vivantes",
              "resultat", 0, 20000, 70, "max", "ODD 3.1.1"),
    Indicator("MDG_0000000007", "Mortalité des moins de 5 ans", "pour 1 000 naissances vivantes",
              "resultat", 0, 1000, 25, "max", "ODD 3.2.1"),
    Indicator("WHOSIS_000003", "Mortalité néonatale", "pour 1 000 naissances vivantes",
              "resultat", 0, 1000, 12, "max", "ODD 3.2.2"),
    Indicator("WHOSIS_000001", "Espérance de vie à la naissance", "années", "contexte", 20, 100),
    Indicator("WHOSIS_000002", "Espérance de vie en bonne santé", "années", "contexte", 15, 100),
    Indicator("WHS4_100", "Couverture vaccinale DTP3 (enfants d'un an)", "%", "moyen", 0, 100,
              90, "min", "Programme pour la vaccination à l'horizon 2030"),
    Indicator("MDG_0000000025", "Accouchements assistés par du personnel qualifié", "%", "moyen", 0, 100),
    Indicator("HWF_0001", "Médecins", "pour 10 000 habitants", "moyen", 0, 200),
    Indicator("GHED_CHE_pc_US_SHA2011", "Dépenses courantes de santé par habitant", "USD", "moyen", 0, 20000),
]
INDICATORS_BY_CODE = {indicator.code: indicator for indicator in INDICATORS}


def database_settings() -> dict:
    """Paramètres de connexion PostgreSQL, lus dans l'environnement (fichier .env)."""
    missing = [name for name in ("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB") if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"Variables manquantes dans .env : {', '.join(missing)} (voir .env.example)")
    return {
        # 127.0.0.1 plutôt que « localhost » : sous Windows, localhost est d'abord résolu en IPv6 (::1),
        # où Docker n'écoute pas ; la connexion attendait alors 130 s avant de basculer en IPv4.
        "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "port": int(os.getenv("POSTGRES_PORT", "5433")),
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "dbname": os.environ["POSTGRES_DB"],
        "connect_timeout": 10,   # échouer vite et clairement si la base ne répond pas
    }
