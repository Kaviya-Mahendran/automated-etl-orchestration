import schedule
import time
import logging
from pathlib import Path

from scripts.pipeline import run_pipeline


def setup_logging():
    """
    Configure scheduler-level logging.
    Keeps scheduling logs separate from pipeline execution logs.
    """
    logs_path = Path("logs/scheduler.log")
    logs_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(logs_path),
            logging.StreamHandler(),
        ],
    )


def start_scheduler():
    """
    Starts the ETL scheduler.

    The pipeline is executed on a fixed schedule to simulate
    production-style automated ETL orchestration.
    """

    setup_logging()
    logging.info("ETL scheduler started")

    # -------------------------------
    # Schedule definition
    # -------------------------------
    # Example: daily run at 02:00 UTC
    schedule.every().day.at("02:00").do(run_pipeline)

    logging.info("Pipeline scheduled to run daily at 02:00 UTC")

    # -------------------------------
    # Scheduler loop
    # -------------------------------
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            logging.exception("Scheduler encountered an error")
            time.sleep(60)


if __name__ == "__main__":
    start_scheduler()
