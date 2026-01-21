import pandas as pd
import logging
from pathlib import Path


REQUIRED_COLUMNS = {
    "record_id",
    "user_id",
    "email",
    "signup_channel",
    "last_activity_date",
    "total_transactions",
    "total_value",
    "status",
    "ingestion_timestamp",
}


def extract_raw_data(raw_data_path: Path) -> pd.DataFrame:
    """
    Extract raw data from source file and perform basic validation.

    This function represents the controlled ingestion layer of the ETL pipeline.
    """

    logging.info("Starting data extraction")

    if not raw_data_path.exists():
        logging.error(f"Raw data file not found: {raw_data_path}")
        raise FileNotFoundError(f"Missing raw data file: {raw_data_path}")

    df = pd.read_csv(raw_data_path)

    logging.info(f"Raw rows extracted: {len(df)}")

    # Schema validation
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        logging.error(f"Missing required columns: {missing_columns}")
        raise ValueError(f"Schema validation failed. Missing columns: {missing_columns}")

    logging.info("Schema validation passed")

    return df
