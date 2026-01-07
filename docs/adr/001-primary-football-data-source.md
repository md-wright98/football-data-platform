# ADR-001: Primary Football Data Source

## Status

Accepted

## Context

We need a source of Premier League football data. Since the budget for the project is £0, paid options cannot be considered. The source must
provide league-wide data coverage, be easy to access in JSON format, and include data for the current Premier League season. Free data source
options include FBref, Understat and StatsBomb.

## Decision

We will use Understat as the primary source of data for this project.
We will not use FBref (requires scraping) or StatsBomb (no data for current season).

## Consequences

### Positive

- Data is easily available as JSON payloads.
- Data is granular enough to get team-level data on every Premier League match.
- Also contains more granular data on other leagues, event-level data and player-level data for future expansions.

### Negative / Trade-offs

- Limited defensive metrics compared to other providers.
- Unofficial source; availability and schema stability are not guaranteed.

### Follow-ups / Next steps

- Next need to decide on a strategy for ingesting the data and the ingestion granularity
- Also need to decide on a warehouse technology for storing the data
- This decision may be revisited if FBref makes their data available through an API or if StatsBomb starts including current season data.

### Personal Learnings

- The choice of source affects everything downstream
- There are important engineering considerations here: the scope of the source, the accessibility of the data, any biases in the data
