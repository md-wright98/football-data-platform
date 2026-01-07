# ADR-003: Data Warehouse Choice

## Status

Accepted

## Context

We need to decide on a data warehouse. The data warehouse needs to have a free tier to fit within constraints. The options under consideration
are BigQuery and Snowflake.

## Decision

We will use BigQuery Sandbox for this project.
We will not use Snowflake for this project, as the scale of the project is likely to exceed what is allowed by Snowflake's free tier.

## Consequences

### Positive

- BigQuery Sanbox is a free tool.
-

### Negative / Trade-offs

- What gets harder / worse?
- What risks does this introduce?

### Follow-ups / Next steps

- We may revisit this choice if the scale of the project in the future exceeds the limits of BigQuery Sandbox.

### Personal Learnings

- Different warehouses have different constraints
- The majority of warehouse cost comes from scanning and querying, not storing data
