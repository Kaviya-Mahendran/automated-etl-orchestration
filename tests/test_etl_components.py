import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from extract import extract_raw_data
from load import load_transformed_data
from transform import transform_raw_data


def sample_dataframe():
    return pd.DataFrame(
        {
            "record_id": [1, 2],
            "user_id": ["u1", "u2"],
            "email": ["a@example.com", "b@example.com"],
            "signup_channel": [" Web ", "Email"],
            "last_activity_date": ["2026-01-01", "2026-08-01"],
            "total_transactions": ["2", "bad"],
            "total_value": ["100.5", "bad"],
            "status": [" Active ", "Inactive"],
            "ingestion_timestamp": ["2026-09-01", "2026-09-01"],
        }
    )


def test_transform_standardises_and_drops_email():
    result = transform_raw_data(sample_dataframe())
    assert "email" not in result.columns
    assert result.loc[0, "signup_channel"] == "web"
    assert result.loc[0, "status"] == "active"
    assert result.loc[1, "total_transactions"] == 0
    assert "days_since_last_activity" in result.columns
    assert "engagement_band" in result.columns


def test_extract_rejects_missing_schema(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"record_id": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Schema validation failed"):
        extract_raw_data(path)


def test_load_rejects_empty_dataframe(tmp_path):
    with pytest.raises(ValueError, match="Cannot load empty dataframe"):
        load_transformed_data(
            pd.DataFrame(),
            tmp_path / "clean.csv",
            tmp_path / "transformed.csv",
        )
