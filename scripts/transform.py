import pandas as pd
import logging
from datetime import datetime


def transform_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform raw extracted data into an analytics-ready dataset.

    This step applies deterministic transformations and data quality rules
    suitable for downstream analytics and modelling.
    """

    logging.info("Starting data transformation")

    transformed_df = df.copy()

    # -------------------------------
    # Standardise categorical values
    # -------------------------------
    transformed_df["signup_channel"] = (
        transformed_df["signup_channel"]
        .str.strip()
        .str.lower()
    )

    transformed_df["status"] = (
        transformed_df["status"]
        .str.strip()
        .str.lower()
    )

    # -------------------------------
    # Parse and validate dates
    # -------------------------------
    transformed_df["last_activity_date"] = pd.to_datetime(
        transformed_df["last_activity_date"],
        errors="coerce"
    )

    transformed_df["ingestion_timestamp"] = pd.to_datetime(
        transformed_df["ingestion_timestamp"],
        errors="coerce"
    )

    # -------------------------------
    # Handle numeric fields
    # -------------------------------
    transformed_df["total_transactions"] = pd.to_numeric(
        transformed_df["total_transactions"],
        errors="coerce"
    ).fillna(0).astype(int)

    transformed_df["total_value"] = pd.to_numeric(
        transformed_df["total_value"],
        errors="coerce"
    ).fillna(0.0)

    # -------------------------------
    # Derive behavioural features
    # -------------------------------
    today = pd.Timestamp(datetime.utcnow().date())

    transformed_df["days_since_last_activity"] = (
        today - transformed_df["last_activity_date"]
    ).dt.days

    transformed_df["days_since_last_activity"] = (
        transformed_df["days_since_last_activity"]
        .fillna(9999)
        .astype(int)
    )

    transformed_df["engagement_band"] = pd.cut(
        transformed_df["days_since_last_activity"],
        bins=[-1, 30, 90, 365, 99999],
        labels=["recent", "warm", "cold", "inactive"]
    )

    transformed_df["value_band"] = pd.cut(
        transformed_df["total_value"],
        bins=[-1, 0, 100, 300, 1000, float("inf")],
        labels=["none", "low", "medium", "high", "very_high"]
    )

    # -------------------------------
    # Drop fields not required downstream
    # -------------------------------
    transformed_df = transformed_df.drop(
        columns=["email"]
    )

    logging.info(
        f"Transformation completed. Output rows: {len(transformed_df)}"
    )

    return transformed_df
