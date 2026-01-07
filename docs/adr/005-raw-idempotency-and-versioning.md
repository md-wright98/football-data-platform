# ADR-005: Raw Layer Idempotency and Versioning Strategy

## Status

Accepted

## Context

In order to store versioning history in the raw layer and ensure that mutliple operations do not create uncontrolled duplication or cause
breakages, we need a strategy to version records and control the creation of updated versions.

## Decision

Records will be versioned using an extracted_at and ingested_at field, as well as a run_id to break ties.
The latest record is the one with the most recent extracted_at timestamp. run_id will be used to break ties.
The canonical JSON payload of each match will be hashed, and this hash will determine if a new version is needed.
A new version of a match record will only be created when the hash of the new record is different to the latest stored data.

## Consequences

### Positive

- Having both an indicator of source time and system time prevents us from ordering versions incorrectly due to delayed ingestions or bugs
- A hash makes it easy to determine if a payload differs from the most recent one we have stored without complex key-wise comparison logic

### Negative / Trade-offs

- A hash will will treat all changes equally, meaning any small change to the data will create a new record
- A hash will require additional overhead to implement

### Follow-ups / Next steps

- Next we will need to define clearly what qualifies a record as the "latest" version
- We will need to decide on a retention strategy to make sure we do not store an uncontrolled number of duplicates for any one match.
