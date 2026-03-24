# ADR-007: Versioning Strategy Change

## Status

Accepted

## Context

During building, I had to think about how to implement versioning and retention. In the context of football data, I no longer
believe it makes sense to retain historical versions of match data, since we can only work with the latest version anyway.

## Decision

The raw layer of the warehouse will no longer store 5 versions of each match record.
Instead the raw layer will now only contain a single row for each match_id with the latest match data.

## Consequences

### Positive

- Pipeline is more lightweight without implementing versioning.
- Retention strategy is now more reflective of the context of the data domain.

### Negative / Trade-offs

- Will no longer retain data lineage to be able to track changes.
