# ADR-006: Raw Layer Version Retention Strategy

## Status

Accepted

## Context

The raw layer is designed as an append-only layer, storing every version of match data received from the source. We originally considered a "Rolling 5-version" limit to prevent table bloat.

## Decision

We will move to a Permanent Retention strategy for the raw layer.

- No Deletion: No records will be deleted from the raw layer during normal operations.
- Partitioning: If data volume grows, we will implement BigQuery Ingestion-time Partitioning to optimize query costs rather than deleting history.

## Consequences

### Positive

- Perfect Lineage: We never lose data. If the source provider (Understat) changes a historical value, we can track exactly when that change happened.
- Simplified Ingestion: The Python script only needs WRITE_APPEND permissions, not DELETE permissions.

### Negative / Trade-offs

- The raw table size will grow linearly over time. While not an issue now, a long-term archival strategy (e.g., moving data older than 2 years to Coldline Storage) may be considered in the future.
