# ADR-006: Raw Layer Version Retention Strategy

## Status

Accepted

## Context

The raw layer of the warehouse will store multiple versions of records for matches, each with different data. We will need a strategy to
determine how many versions of each match we will store to prevent uncontrolled duplication.

## Decision

Versions are ordered by extracted_at, tie-broekn by run_id.
The raw layer will store the 5 most recent versions of the match data.
Versions older than this will be deleted from the raw layer as part of ingestion cleanup.

## Consequences

### Positive

- Preserves data lineage and revision history without unnecessary bloating.

### Negative / Trade-offs

- The current hash strategy will detect any small change in the data and create a new record, so we may get through versions quickly.
