import logging
import time
from pathlib import Path
from datetime import datetime
import json

from extract import extract_raw_data
from transform import transform_raw_data
from load import load_transformed_data


def run_pipeline() -> None:
    """
    Orchestrates the full ETL pipeline:
    Extract → Transform → Load

    This function is designed to be scheduled and run unattended.
    """

    start_time = time.time()
    run_timestamp = datetime.utcnow().isoformat()

    # -------------------------------
    # Paths
    # -------------------------------
    RAW_DATA_PATH = Path("data/raw/sample_raw_data.csv")
    CLEANED_DATA_PATH = Path("data/cleaned/cleaned_data.csv")
    TRANSFORMED_DATA_PATH = Path("data/transformed/analytics_ready_data.csv")
    LOGS_PATH = Path("logs/pipeline.log")
    METADATA_PATH = Path("outputs/run_metadata.json")

    # -------------------------------
    # Logging configuration
    # -------------------------------
    LOGS_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOGS_PATH),
            logging.StreamHandler(),
        ],
    )

    logging.info("ETL pipeline started")

    metadata = {
        "run_timestamp": run_timestamp,
        "status": "started",
    }

    try:
        # -------------------------------
        # Extract
        # -------------------------------
        raw_df = extract_raw_data(RAW_DATA_PATH)
        metadata["rows_raw"] = len(raw_df)

        # -------------------------------
        # Transform
        # -------------------------------
        transformed_df = transform_raw_data(raw_df)
        metadata["rows_transformed"] = len(transformed_df)

        # -------------------------------
        # Load
        # -------------------------------
        load_transformed_data(
            df=transformed_df,
            cleaned_path=CLEANED_DATA_PATH,
            transformed_path=TRANSFORMED_DATA_PATH,
            overwrite=True,
        )

        metadata["status"] = "success"
        logging.info("ETL pipeline completed successfully")

    except Exception as e:
        metadata["status"] = "failed"
        metadata["error"] = str(e)
        logging.exception("ETL pipeline failed")
        raise

    finally:
        duration = round(time.time() - start_time, 2)
        metadata["duration_seconds"] = duration

        METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(METADATA_PATH, "w") as f:
            json.dump(metadata, f, indent=2)

        logging.info(f"Run metadata written to {METADATA_PATH}")
        logging.info(f"Pipeline duration: {duration} seconds")


if __name__ == "__main__":
    run_pipeline()
