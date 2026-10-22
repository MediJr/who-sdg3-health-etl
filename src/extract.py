"""Étape E : extraction des données brutes depuis l'API de l'OMS (Global Health Observatory).

Nouveautés par rapport au projet 0 :
- les réessais sont confiés à urllib3 (`Retry`), qui gère l'attente croissante et l'en-tête
  « Retry-After » envoyé par le serveur ;
- les réponses brutes sont compressées (gzip) : environ 10 fois moins de place sur le disque ;
- le manifeste contient une empreinte SHA-256 de chaque fichier, pour prouver son intégrité.

Exécution seule :  python -m src.extract
"""

import gzip
import hashlib
import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src import config

logger = logging.getLogger(__name__)


def build_session() -> requests.Session:
    """Session HTTP avec réessais automatiques sur les erreurs temporaires."""
    retry = Retry(
        total=config.MAX_RETRIES,
        backoff_factor=config.BACKOFF_FACTOR,           # 2 s, 4 s, 8 s, 16 s
        status_forcelist=(429, 500, 502, 503, 504),     # erreurs temporaires uniquement (jamais 404)
        allowed_methods=("GET",),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers.update({"User-Agent": config.USER_AGENT, "Accept": "application/json"})
    return session


def _write_atomic(path: Path, payload: dict) -> None:
    """Écrit un JSON compressé de façon atomique (fichier temporaire, puis renommage)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with gzip.open(temporary, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False)
    temporary.replace(path)


def read_raw(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch_odata(session: requests.Session, url: str, params: dict | None = None) -> dict:
    """Récupère une ressource OData complète, en suivant la pagination si l'API en utilise une."""
    records: list[dict] = []
    next_url, next_params = url, params
    while next_url:
        response = session.get(next_url, params=next_params, timeout=config.REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
        if "value" not in payload:
            # Échec explicite si la structure de la réponse change : mieux vaut planter qu'ingérer n'importe quoi.
            raise ValueError(f"Réponse inattendue de {next_url} : clé « value » absente")
        records.extend(payload["value"])
        next_url, next_params = payload.get("@odata.nextLink"), None
    return {"source_url": url, "params": params, "record_count": len(records), "value": records}


def _fetch_to_raw(session, run_dir: Path, relative: str, url: str, params: dict | None = None) -> dict:
    """Télécharge une ressource dans la couche brute, sauf si elle y est déjà (reprise après incident)."""
    path = run_dir / relative
    if not path.exists():
        payload = fetch_odata(session, url, params)
        payload["fetched_at"] = datetime.now(timezone.utc).isoformat()
        _write_atomic(path, payload)
        logger.info("%-45s %7d lignes", relative, payload["record_count"])
    payload = read_raw(path)
    return {"file": relative, "records": payload["record_count"], "sha256": _sha256(path)}


def extract(run_date: date | None = None) -> Path:
    """Extrait indicateurs, métadonnées et libellés de dimensions. Renvoie le dossier du lot brut."""
    run_date = run_date or date.today()
    run_dir = config.RAW_DIR / run_date.isoformat()
    session = build_session()
    logger.info("Extraction vers %s", run_dir)
    files = []

    # 1. Les observations de chaque indicateur.
    for indicator in config.INDICATORS:
        files.append(_fetch_to_raw(session, run_dir, f"indicators/{indicator.code}.json.gz",
                                   f"{config.GHO_BASE_URL}/{indicator.code}"))

    # 2. Les métadonnées des indicateurs (libellé officiel de l'OMS).
    codes = " or ".join(f"IndicatorCode eq '{indicator.code}'" for indicator in config.INDICATORS)
    files.append(_fetch_to_raw(session, run_dir, "metadata/indicators.json.gz",
                               f"{config.GHO_BASE_URL}/Indicator", {"$filter": codes}))

    # 3. Les libellés des lieux et des ventilations.
    for dimension in config.LOCATION_TYPES + config.BREAKDOWN_TYPES:
        files.append(_fetch_to_raw(session, run_dir, f"dimensions/{dimension}.json.gz",
                                   f"{config.GHO_BASE_URL}/DIMENSION/{dimension}/DimensionValues"))

    manifest = {
        "run_date": run_date.isoformat(),
        "source": config.GHO_BASE_URL,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logger.info("Extraction terminée : %d fichiers, %d lignes d'observations", len(files),
                sum(f["records"] for f in files if f["file"].startswith("indicators/")))
    return run_dir


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")
    extract()
