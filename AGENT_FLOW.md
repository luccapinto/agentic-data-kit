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
Validate (optional)  ──►  .agent/scripts/checklist.py  ·  Power BI: /validate-pbi (BPA)
   │
   ▼
Deliver  ──────────────►  present changes + reasoning, in the user's language
```

## Routing cheatsheet

| Request is about… | Agent |
|---|---|
| Ingestion, pipelines, Spark, orchestration | `data-engineer` |
| dbt, star schemas, warehouse modeling | `analytics-engineer` |
| Metrics, dashboards, ad-hoc analysis, semantic review | `data-analyst` |
| ML, forecasting, A/B tests, statistics | `data-scientist` |
| Quality, contracts, privacy, masking | `data-governance` |
| Power BI models (TMDL) or reports (PBIR) | `powerbi-developer` |

## Principles

- **Less is more** — lean instructions keep the model focused; we don't restate what it knows.
- **Clarify only when genuinely blocked** — otherwise state assumptions and proceed.
- **Check downstream impact** before changing schemas, contracts, or shared models.

**Agents:** 6 · **Skills:** 6 · **Workflows:** 3
