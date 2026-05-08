# ADR-008: landing table

## Status

Superseded by ADR-009

## Context

Need to find a way to create accurate ingested_at timestamps for data and to merge updated records into the raw table without
truncating the entire table.

## Decision

When initially loaded to BigQuery data will be loaded into a landing table named understat_matches_landing.
From here data will be merged into the raw table using match_id as the identifier.
The ingested_at timestamp will be created when data is moved from the landing table to the raw table.
If a match_id does not exist in raw, a new record will be created.
If the match_id does exist in raw, but the payload_hash matches in both tables, the ingested_at and extracted_at timestamps will be updated.
If the match_id does exist in raw but the payload_hash does not match, the ingested_at, extracted_at, payload and payload_hash will be updated.

## Consequences

### Positive

- Allows implementation of a more accurate ingested_at timestamp.
- Allows raw table to be a single source of truth for the latest, most up to date match data.

### Negative / Trade-offs

- Adds an additional layer to warehouse architecture.
