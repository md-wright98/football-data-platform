# ADR-004: Raw Layer Contract

## Status

Accepted

## Context

We need to determine what the exact purpose of the raw layer is and what it will store in our warehouse.

## Decision

The raw layer will store match data as recieved from the source with no modification or interpretation. Each row in the table will
represent a single football match. The raw layer will be append-only, and store multiple versions of the data for the same match over
time if the data changes.
The raw layer will not apply any business logic or transformation to the data.

## Consequences

### Positive

- Provides a source of truth by storing data as provided by the source and keeping historical versions for lineage.
- Does not require transformation or deduplication logic.

### Negative / Trade-offs

- Will not store information on status or failed runs, as these will be stored in logs and orchestration metadata.
- Will require explicit duplicate retention protocols to prevent table from becoming bloated while preserving lineage.

### Follow-ups / Next steps

- Next need to define a startegy to ensure idempotency
- Need a versioning and retention policy
- Need to define what constitutes a successful ingestion of data
- Need to define the raw table schema and required fields

### Personal Learnings

- What exactly the raw layer should and should not store must be clearly defined
- One of the most important considerations is what a single row represents
- Applying logic at the raw layer should be kept to a minimum
