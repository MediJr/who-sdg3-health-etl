"""Point d'entrée : Extract → Transform → Load → Rapport.

Utilisation (la base doit tourner : docker compose up -d) :
    python -m src.pipeline                        # extraction du jour, puis tout le reste
    python -m src.pipeline --run-date 2026-10-22  # rejoue un lot brut existant, sans appeler l'API
    python -m src.pipeline --skip-report          # sans régénérer graphiques et résultats
"""

import argparse
import logging
import sys
import time
from datetime import date

from src import config
from src.extract import extract
from src.load import load
from src.transform import transform

logger = logging.getLogger("pipeline")


def configure_logging() -> None:
    """Journal à la console ET dans un fichier daté (logs/), pour garder une trace des exécutions."""
    config.LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)-13s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(config.LOG_DIR / f"pipeline-{date.today().isoformat()}.log", encoding="utf-8")],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline ETL OMS : indicateurs ODD 3")
    parser.add_argument("--run-date", type=date.fromisoformat, help="rejouer un lot brut existant (AAAA-MM-JJ)")
    parser.add_argument("--skip-report", action="store_true", help="ne pas régénérer graphiques et résultats")
    args = parser.parse_args()
    configure_logging()
    started = time.perf_counter()

    if args.run_date:
        run_dir = config.RAW_DIR / args.run_date.isoformat()
        if not (run_dir / "manifest.json").exists():
            parser.error(f"aucun lot brut complet dans {run_dir}")
        logger.info("Rejeu du lot brut %s (aucun appel à l'API)", run_dir.name)
    else:
        run_dir = extract()

    result = transform(run_dir)
    load(result, raw_batch=run_dir.name)

    if not args.skip_report:
        from src.report import build_report   # import tardif : matplotlib n'est utile qu'ici
        build_report()
    logger.info("Pipeline terminé en %.0f s", time.perf_counter() - started)


if __name__ == "__main__":
    main()
