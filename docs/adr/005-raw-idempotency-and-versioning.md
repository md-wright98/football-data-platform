# ADR-005: Raw Layer Idempotency and Versioning Strategy

## Status

Accepted

## Context

In order to store versioning history in the raw layer and ensure that mutliple operations do not create uncontrolled duplication or cause
breakages, we need a strategy to version records and control the creation of updated versions.

## Decision

We will implement Batch-Level Idempotency using metadata timestamps rather than row-level hashing.

1. Metadata Fields: Every record is enriched with an extracted_at timestamp during ingestion.
2. De-duplication Logic: We will utilize the dbt QUALIFY statement in the staging layer to partition by match_id and select only the record with the most recent extracted_at value.
3. Storage: The raw layer will remain "Append-Only," preserving a full audit trail of how match data changed over time.

## Consequences

### Positive

- The Python ingestion script remains "stateless" and lightweight.
- The de-duplication logic is transparently documented in the dbt SQL code.
- 100% data retention is maintained in the Bronze layer.

### Negative / Trade-offs

- The raw table will contain multiple rows for the same match_id. While storage costs are negligible for this project, a long-term retention policy may eventually be required.

### Follow-ups / Next steps

- Monitor BigQuery storage usage if the number of leagues increases significantly.
- Implement dbt tests to verify that the stg\_ models contain exactly one record per match_id.
