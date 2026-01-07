# ADR-002: Extraction Granularity

## Status

Accepted

## Context

We need to decide on the optimal ingestion unit for this pipeline. Engineering constraints like rate limits, ease of backfills, isolation of
errors and identifying missing data come into play. Options include ingesting data by team-season, by league-season or by match.

## Decision

We will ingest data by league-season.
We will not ingest data by team-season or by match as this will result in a much greater number of requests.

## Consequences

### Positive

- Number of requests needed to obtain data is low.
- Backfilling data for previous seasons will be easier and have clearer requirements for success.

### Negative / Trade-offs

- Isolating errors will be harder.
- More stringent checks will be needed to identify missing data.

### Follow-ups / Next steps

- Next we will need to decide on a raw table structure to store data for each match.

### Personal learnings

- Have to consider the cost of ingestion and the ability to verify the data, e.g. here each previous season should have exactly 380 games
- It's important to design a system around failure - think about the unit of ingestion in terms of how easy it is to monitor and fix failure
- What is the cost of retrying a failed ingestion?
