# Football Data Analytics Platform

An end-to-end data engineering pipeline that extracts football match metrics (xG, results) from Understat, processes them in BiqQuery using dbt, and generates live league standings.

<img width="1067" height="112" alt="Screenshot 2026-05-08 at 12 13 36" src="https://github.com/user-attachments/assets/8aebc282-bbd4-496f-ae5e-a795f4c44848" />

## Architecture

- **Ingestion:** Python, using the UnderstatAPI to access match data.
- **Warehouse:** Google BigQuery
- **Transformation:** dbt for SQL modelling and data quality testing
- **Quality Assurance:** Automated schema and data tests using dbt_utils

## Data Pipeline Layers

- **Raw:** JSON payloads stored in BigQuery with timestamps and run IDs.
- **Staging:** Type-casted, flattened and de-duplicated match data using SQL window functions.
- **Marts:** Aggregated fact tables showing real-time league standings and performance metrics.

## Key Engineering Features

- **Idempotency:** The pipeline handles multiple runs without duplicating data in the analytics layer.
- **Schema Enforcement:** Strict casting of JSON strings to `INT64` and `FLOAT64` data types for reliable downstream testing.
- **Automated Testing:** Implementation of `unique`, `not_null` and `accepted_range` tests to ensure data integrity.

## Tech Stack

- **Language:** Python 3.12.0
- **Database:** Google BigQuery
- **Transformation:** dbt Core
- **Environment:** Virtualenv
- **Version Control:** Git

## Future Roadmap

- **Orchestration:** Implement Prefect Cloud for automated weekly runs
- **Containerisation:** Dockerize the ingestion script for cloud deployment
- **Visualization**: Connect a Looker Studio or Evidence.dev dashboard for the marts layer.
