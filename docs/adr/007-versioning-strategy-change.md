# ADR-007: Versioning Strategy Change

## Status

Accepted

## Context

Initial designs (ADR-005/006) proposed a complex physical retention and hashing strategy to manage historical versions. During implementation, it became clear that the primary requirement is always the "latest" state of a match, and managing physical deletions adds unnecessary risk.

## Decision

We will shift from Physical Version Management (deleting rows) to Virtual Version Management (filtering rows).

- Raw Layer : Remains Append-Only. We will store every ingestion burst as-is.
- Staging Layer: This layer is now responsible for versioning logic. It will use a QUALIFY window function to present only the latest version of a match to the rest of the business.
- Retention: We will no longer manually prune old records in the Python script.

## Consequences

### Positive

- Stateless Ingestion: The Python script is simpler and more robust.
- Auditability: We retain the ability to "Time Travel" through the data if needed, but the analytics layer stays clean and performant.

### Negative / Trade-offs

- The raw table in BigQuery acts as a "log" rather than a clean table. This is solved by directing all downstream users to the `stg_` models instead of the raw tables.
