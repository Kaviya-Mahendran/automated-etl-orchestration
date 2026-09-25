# Automated ETL Orchestration Pipeline

> A lightweight Python ETL system demonstrating ingestion, validation, transformation, scheduling, logging and run-level observability.

## Why this project matters

Manual data movement is easy to start and difficult to maintain. This project demonstrates how a small analytics workflow can become a repeatable system with explicit validation, logging and operational metadata.

## Architecture

```text
Source
  ↓
Schema Validation
  ↓
Extract
  ↓
Transform
  ↓
Quality Checks
  ↓
Load
  ↓
Run Metadata + Logs
```

## Pipeline responsibilities

### Extract
- Read source data
- Validate expected schema
- Fail early when required fields are missing

### Transform
- Standardise categories
- Parse dates
- Enforce numeric types
- Derive analytics-ready fields
- Remove unnecessary sensitive fields

### Load
- Write structured outputs
- Track row counts
- Control overwrite behaviour

### Observability
- Stage-level logging
- Scheduler logging
- Explicit error propagation
- Run metadata including status, row counts and duration

## Run locally

```bash
pip install -r requirements.txt
python scripts/pipeline.py
python scheduler/schedule.py
```

## Production extensions

- Retries with backoff
- Incremental processing
- Idempotent loads
- Backfills
- Schema versioning
- Automated data-quality tests
- Docker packaging
- Airflow/Prefect migration
- Cloud warehouse integration

**Focus:** Python · ETL · data quality · orchestration · logging · analytics engineering