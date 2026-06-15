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
├── agents/      # 6 specialist personas
├── skills/      # 7 on-demand knowledge modules
├── workflows/   # 3 slash commands
├── rules/       # global rules (rules.md)
└── scripts/     # optional validation helpers
```

## Agents (5)

| Agent | Focus | Skills |
|---|---|---|
| `data-engineer` | ETL, pipelines, Medallion | — |
| `analytics-engineer` | dbt, dimensional modeling | data-quality-testing |
| `data-scientist` | Analysis, metrics, dashboards, ML, statistics, A/B testing | data-quality-testing |
| `data-governance` | Quality, contracts, LGPD/GDPR | data-quality-testing |
| `powerbi-developer` | Power BI as code (TMDL + PBIR) | pbi-semantic-layer-tmdl, pbi-report-layer-pbir, pbi-quality-rules, pbi-dashboard-documentation |

## Skills (7)

Skills self-activate by their `description` — no agent required. They load on demand.

| Skill | Description |
|---|---|
| `creating-agents-and-skills` | Governance gate for adding agents/skills/workflows + multi-folder sync |
| `data-quality-testing` | dbt tests, Great Expectations, contracts, WAP |
| `documentation-templates` | Runbooks, data dictionaries, ADRs |
| `pbi-semantic-layer-tmdl` | Author TMDL semantic models |
| `pbi-report-layer-pbir` | Edit PBIR reports, visuals, themes |
| `pbi-quality-rules` | Real BPA via free Tabular Editor 2 CLI |
| `pbi-dashboard-documentation` | Generate Markdown catalogs from PBIP |

## Workflows (3)

`/plan` · `/validate-pbi` · `/document-dashboard`

## Design principles

- **Less is more.** Capture domain-specific context only; never restate what the model knows.
- **Progressive disclosure.** Skills load when relevant, not upfront.
- **No ambiguous routing.** Each agent owns a distinct domain; no overlapping responsibilities.
