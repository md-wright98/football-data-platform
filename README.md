# Football Data Analytics Platform

An end-to-end data engineering pipeline that extracts football match metrics (xG, results) from Understat, processes them in BiqQuery using dbt, and generates live league standings.

<img width="1417" height="292" alt="image" src="https://github.com/user-attachments/assets/0e97bc1c-4e4c-4970-a1e9-fee808b10aa7" />

## Architecture

- **Ingestion:** Python, using the UnderstatAPI to access match data.
- **Warehouse:** Google BigQuery
- **Transformation:** dbt for SQL modelling and data quality testing
- **Quality Assurance:** Automated schema and data tests using dbt_utils

## Data Pipeline Layers

- **Raw:** JSON payloads stored in BigQuery with timestamps and run IDs.
- **Staging:** Type-casted, flattened and de-duplicated match data using SQL window functions.
- **Core Marts:** Star Schema fact and dimension tables containing information on teams and matches.
- **Analytics Marts:** Data analytics outputs built on top of Core Marts.

## Key Engineering Features

- **Idempotency:** The pipeline handles multiple runs without duplicating data in the analytics layer.
- **Schema Enforcement:** Strict casting of JSON strings to `INT64` and `FLOAT64` data types for reliable downstream testing.
- **Automated Testing:** Implementation of `unique`, `not_null`, `relationship` and `accepted_range` tests to ensure data integrity.

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
