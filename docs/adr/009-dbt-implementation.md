# ADR-000: <Short decision title>

## Status

Accepted

## Context

As the project transitioned from a script-based MVP to a production-grade ELT pipeline, the previous method of managing transformations (via procedural Python or complex SQL MERGE statements in ADR-007) became a bottleneck. We required a solution that provided:

- Data Lineage: Visibility into how raw JSON becomes analytics-ready tables.
- Testing: Automated validation of unique keys, null values, and relationship integrity.
- Modularity: A way to separate "Staging" (cleaning) from "Marts" (business logic).

## Decision

We will implement dbt (data build tool) as the primary transformation engine.

- Medallion Architecture: We will organize data into Bronze (Raw Append-only), Silver (Staged/Deduplicated), and Gold (Marts/Aggregated) layers.
- Virtual De-duplication: Instead of physical MERGE operations, we will use dbt stg\_ models with QUALIFY row_number() to select the latest records dynamically.
- Schema Testing: Every source and model will have a .yml file defining at least unique and not_null tests.

## Consequences

### Positive

- Declarative Logic: We describe what the data should look like, and dbt handles the how (DDL/DML).
- Reduced Ingestion Complexity: The Python "Extract & Load" phase is now purely responsible for moving data, making it less prone to failure.
- Improved Trust: Automated tests catch data issues (like missing matches or duplicate IDs) before they reach the final dashboard.

### Negative / Trade-offs

- Tooling Overhead: Adds a dependency on dbt-core and requires managing a separate execution step in the pipeline.
- Compute Cost: Virtual de-duplication (scanning the raw table and filtering) uses more BigQuery "slots" than a simple table read, though this is negligible at the current scale.
