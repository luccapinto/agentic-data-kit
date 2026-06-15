<p align="center">
  <h1 align="center">Agentic Data Kit</h1>
  <p align="center">
    <strong>Drop one folder. Get a team of AI Data Specialists.</strong>
  </p>
</p>

---

## 🧠 Why This Exists

Generic LLMs don't know *your* stack, *your* standards, or *your* architecture — but they
already know how to write clean code. So this kit follows one rule: **capture only the
domain-specific context that matters, and nothing the model already does well.** Lean
instructions keep the model's attention on what's important, which is exactly what makes agents
reliable.

The **Agentic Data Kit** is a curated library of **6 focused AI agents**, **6 on-demand skills**,
and **3 workflows** for Data Engineering, Analytics, and Business Intelligence. Drop it in, and
your assistant can build pipelines, design star schemas, edit Power BI as code, run quality
checks, and document models — without you re-explaining the basics.

## 🚀 Quick Start

```bash
npx @luccapinto/agentic-data-kit@latest init
```

Pick your AI assistant and the kit is installed. Then just ask:

```text
You: "Build an ETL pipeline for customer data using Medallion Architecture"
AI:  Applying @data-engineer → Bronze → Silver → Gold pipeline

You: "Add a revenue measure to the Power BI model"
AI:  Applying @powerbi-developer → writes DAX, edits TMDL, runs the BPA
```

> Instructions are written in English for portability; the assistant replies in **your**
> language automatically.

---

## 🎯 What's Inside

### 🤖 Agents — Focused Specialists

| Agent | What it does |
|---|---|
| `data-engineer` | ETL/ELT pipelines, Medallion architecture, idempotency, WAP |
| `analytics-engineer` | Star schemas, dbt models, warehouse architecture & performance |
| `data-analyst` | Metrics, dashboard ideation, semantic-model review (also business analysis) |
| `data-scientist` | ML, statistics, forecasting, A/B testing |
| `data-governance` | Data quality, contracts, PII masking, LGPD/GDPR |
| `powerbi-developer` | Power BI as code — TMDL semantic model **and** PBIR reports, validated with Tabular Editor 2 |

### 🧩 Skills — Deep, On-Demand Expertise

Loaded only when relevant (progressive disclosure), so they cost almost nothing until used:

- **Power BI:** `pbi-semantic-layer-tmdl`, `pbi-report-layer-pbir`, `pbi-quality-rules` (real
  Best Practice Analyzer via the free Tabular Editor 2), `pbi-dashboard-documentation`
- **Quality & docs:** `data-quality-testing`, `documentation-templates`

### 🔄 Workflows

`/plan` (scope a task) · `/validate-pbi` (model health check via BPA) ·
`/document-dashboard` (auto-generate a data catalog)

---

## 🛠️ Power BI: as code, not clicks

The Power BI agent edits **PBIP** projects directly — **TMDL** for the semantic model and
**PBIR** for reports — and validates with the **free Tabular Editor 2** Best Practice Analyzer.
No paid tooling, no Fabric required. Microsoft's official `powerbi-modeling-mcp` (preview) is
supported as an optional path for bulk refactors, but file editing is the default.

---

## 🔄 Multi-Platform Support

`.agent/` is the single source of truth. A sync script compiles it for every assistant:

```bash
python scripts/sync_agents.py
```

| Target | Output |
|---|---|
| Antigravity | `.agent/` (native) |
| Claude Code | `.claude/` + `CLAUDE.md` |
| GitHub Copilot | `.github/` + `copilot-instructions.md` |
| OpenCode | `.opencode/` + `AGENTS.md` |
| Cursor / others | root `AGENTS.md` |

---

## 🤝 Contributing & License

Want to extend it? See [CONTRIBUTING.md](CONTRIBUTING.md) — especially the "should this agent
exist?" gates.

MIT © Lucca Pinto
