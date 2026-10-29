# Template: Architecture Decision Record (ADR)

Use for significant choices (e.g. Airflow → Dagster, Delta vs. Iceberg, Databricks → dbt+Snowflake).

```markdown
# ADR-001: [Title]

## Status
Proposed / Accepted / Rejected / Deprecated

## Context
Why are we deciding this now? (e.g. Databricks costs too high for simple transforms.)

## Decision
What we chose. (e.g. dbt Core on Snowflake for the transform layer.)

## Consequences
- **Positive:** lower compute cost, analysts can write SQL.
- **Negative:** complex ML transforms are harder to keep inline with ELT.
```
