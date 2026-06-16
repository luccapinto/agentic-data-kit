# Agent Flow

How a request moves through the kit.

```text
User request
   │
   ▼
Route to a specialist  ──►  pick the agent whose domain fits (announce it briefly)
   │                         cross-domain? split across agents, then merge results
   ▼
Load skills on demand  ──►  read a SKILL.md only when the task needs it
   │
   ▼
Execute  ──────────────►  build / edit pipelines, models, DAX, TMDL, PBIR, docs
   │
   ▼
Validate  ──────────────►  Power BI: /validate-pbi (real BPA via Tabular Editor 2)
   │
   ▼
Deliver  ──────────────►  present changes + reasoning, in the user's language
```

## Routing cheatsheet

| Request is about… | Agent |
|---|---|
| Ingestion, pipelines, Spark, orchestration | `data-engineer` |
| dbt, star schemas, warehouse modeling | `analytics-engineer` |
| Metrics, dashboards, analysis, ML, statistics, A/B tests, semantic review | `data-scientist` |
| Power BI models (TMDL) or reports (PBIR) | `powerbi-developer` |
| Presentations, decks, pitches, readouts, business plans, brand/`DESIGN.md` | `presentation-designer` |

> Quality, privacy, contracts, and masking are **cross-cutting rules** (in `rules.md`), applied
> by every agent — not a routing target.

## Principles

- **Less is more** — lean instructions keep the model focused; we don't restate what it knows.
- **Clarify only when genuinely blocked** — otherwise state assumptions and proceed.
- **Check downstream impact** before changing schemas, contracts, or shared models.

**Agents:** 5 · **Skills:** 8 · **Workflows:** 3
