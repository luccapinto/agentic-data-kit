# Architecture

A modular kit for data teams: role-based **agents**, on-demand **skills**, and **workflows**,
with `.agent/` as the single source of truth.

## Source of truth & sync

Edit only `.agent/`. `scripts/sync_agents.py` compiles it to every assistant:

```
.agent/        →  .claude/ (+ CLAUDE.md)        Claude Code
               →  .github/ (+ copilot-instructions.md)   GitHub Copilot
               →  .opencode/ (+ AGENTS.md)       OpenCode
               →  AGENTS.md (root)               Cursor / cross-tool standard
```

```
.agent/
├── agents/      # 5 specialist personas
├── skills/      # 7 on-demand knowledge modules
├── workflows/   # 3 slash commands
└── rules/       # global rules (rules.md)
```

## Agents (5)

| Agent | Focus | Skills |
|---|---|---|
| `data-engineer` | ETL, pipelines, Medallion | — |
| `analytics-engineer` | dbt, dimensional modeling | — |
| `data-scientist` | Analysis, metrics, dashboards, ML, statistics, A/B testing | — |
| `powerbi-developer` | Power BI as code (TMDL + PBIR) | pbi-semantic-layer-tmdl, pbi-report-layer-pbir, pbi-quality-rules, documentation-templates |
| `presentation-designer` | Presentations as code (decks, sites, PDF) + brand | building-html-presentations, applying-visual-identity |

Governance is cross-cutting, not a role — PII masking, WAP, contracts, and downstream-impact
checks live in `rules/rules.md` and apply to every agent.

## Skills (7)

Skills self-activate by their `description` — no agent required. They load on demand.

| Skill | Description |
|---|---|
| `creating-agents-and-skills` | Governance gate for adding agents/skills/workflows + multi-folder sync |
| `documentation-templates` | Runbooks, data dictionaries, metric defs, ADRs, Power BI catalog (templates in separate files) |
| `pbi-semantic-layer-tmdl` | Author TMDL semantic models |
| `pbi-report-layer-pbir` | Edit PBIR reports, visuals, themes |
| `pbi-quality-rules` | Real BPA via free Tabular Editor 2 CLI |
| `building-html-presentations` | Build decks / interactive sites / PDFs as code (reveal.js default) |
| `applying-visual-identity` | Apply a brand from `DESIGN.md` (Google Labs spec) to any output |

## Workflows (3)

`/plan` · `/validate-pbi` · `/document-dashboard`

## Design principles

- **Less is more.** Capture domain-specific context only; never restate what the model knows.
- **Progressive disclosure.** Skills load when relevant, not upfront.
- **No ambiguous routing.** Each agent owns a distinct domain; no overlapping responsibilities.
