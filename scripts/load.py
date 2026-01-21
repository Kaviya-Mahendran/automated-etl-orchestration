import pandas as pd
import logging
from pathlib import Path


def load_transformed_data(
    df: pd.DataFrame,
    cleaned_path: Path,
    transformed_path: Path,
    overwrite: bool = True,
) -> None:
    """
    Load cleaned and transformed datasets to disk.

    This function represents the final stage of the ETL pipeline and ensures
    analytics-ready outputs are written in a controlled and auditable way.
    """

    logging.info("Starting load step")

    # -------------------------------
    # Validate dataframe
    # -------------------------------
    if df.empty:
        logging.error("Transformed dataframe is empty. Aborting load.")
        raise ValueError("Cannot load empty dataframe")

    row_count = len(df)
    logging.info(f"Rows to load: {row_count}")

    # -------------------------------
    # Ensure output directories exist
    # -------------------------------
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    transformed_path.parent.mkdir(parents=True, exist_ok=True)

    # -------------------------------
    # Write cleaned dataset
    # -------------------------------
    if cleaned_path.exists() and not overwrite:
        logging.error("Cleaned data already exists and overwrite is False")
        raise FileExistsError("Cleaned output already exists")

    df.to_csv(cleaned_path, index=False)
    logging.info(f"Cleaned data written to {cleaned_path}")

    # -------------------------------
    # Write transformed dataset
    # -------------------------------
    if transformed_path.exists() and not overwrite:
        logging.error("Transformed data already exists and overwrite is False")
        raise FileExistsError("Transformed output already exists")

    df.to_csv(transformed_path, index=False)
    logging.info(f"Transformed data written to {transformed_path}")

    logging.info("Load step completed successfully")
