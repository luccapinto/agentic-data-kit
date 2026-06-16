<div align="center">

# 📊 Agentic Data Kit

### Drop one folder. Get a team of AI data specialists.

**Lean, opinionated AI agents · skills · workflows for data teams —
one source of truth, every assistant.**

[![License: MIT](https://img.shields.io/badge/License-MIT-2563EB.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-4.1.0-1E7A4D.svg)
![Platforms](https://img.shields.io/badge/Claude%20Code%20·%20Copilot%20·%20OpenCode%20·%20Cursor-1B2733.svg)
![PRs welcome](https://img.shields.io/badge/PRs-welcome-9A6B12.svg)
![Philosophy](https://img.shields.io/badge/philosophy-less%20is%20more-6A7787.svg)

```bash
npx @luccapinto/agentic-data-kit@latest init
```

**5 agents · 8 skills · 3 workflows · 4 platforms**

</div>

---

## Contents

- [🧠 Why this exists](#-why-this-exists)
- [🚀 Quick start](#-quick-start)
- [🎯 What's inside](#-whats-inside)
- [🤖 Agents](#-agents)
- [🧩 Skills](#-skills)
- [📈 Power BI — as code, not clicks](#-power-bi--as-code-not-clicks)
- [🎨 Presentations — as code](#-presentations--as-code)
- [🔄 How it works (multi-platform)](#-how-it-works-multi-platform)
- [🧭 Design philosophy](#-design-philosophy)
- [🤝 Contributing & license](#-contributing--license)

---

## 🧠 Why this exists

Generic LLMs don't know *your* stack, *your* standards, or *your* architecture — but they
already know how to write clean code. So this kit follows one rule:

> **Capture only the domain-specific context that matters, and nothing the model already does well.**

Lean instructions keep the model's attention on what's important — which is exactly what makes
agents reliable. The result is a curated library for **Data Engineering, Analytics, BI, and data
storytelling** that drops into your assistant and just works: build pipelines, design star schemas,
edit Power BI as code, run quality checks, document models, and turn analyses into on-brand
presentations — without re-explaining the basics.

---

## 🚀 Quick start

```bash
npx @luccapinto/agentic-data-kit@latest init
```

Pick your AI assistant in the prompt and the kit installs itself. Then just ask:

```text
You: "Build an ETL pipeline for customer data using Medallion Architecture"
AI:  Applying @data-engineer → Bronze → Silver → Gold pipeline

You: "Add a revenue measure to the Power BI model"
AI:  Applying @powerbi-developer → writes DAX, edits TMDL, runs the BPA

You: "Turn this analysis into a McKinsey-style PDF"
AI:  Applying @presentation-designer → builds the report, exports to PDF
```

> 🌍 Instructions are written in English for portability; the assistant replies in **your**
> language automatically.

---

## 🎯 What's inside

| | Count | What it is |
|---|:---:|---|
| 🤖 **Agents** | **5** | Role-based specialists with isolated context and clear domains |
| 🧩 **Skills** | **8** | On-demand knowledge modules that self-activate by description |
| 🔄 **Workflows** | **3** | Slash-command procedures (`/plan`, `/validate-pbi`, `/document-dashboard`) |
| 🖥️ **Platforms** | **4** | Claude Code · GitHub Copilot · OpenCode · Cursor (from one source) |

---

## 🤖 Agents

Focused specialists — each owns a distinct domain, so routing is never ambiguous.

| Agent | What it does |
|---|---|
| `data-engineer` | ETL/ELT pipelines, Medallion architecture, idempotency, Write-Audit-Publish |
| `analytics-engineer` | Star schemas, dbt models, warehouse architecture & performance |
| `data-scientist` | Analysis, metrics, dashboards & semantic review — through to ML, statistics, forecasting, A/B testing |
| `powerbi-developer` | Power BI as code — TMDL semantic model **and** PBIR reports, validated with Tabular Editor 2 |
| `presentation-designer` | Analyses → presentations as code — decks, interactive sites, consulting PDFs, **editable PPTX** — on-brand via `DESIGN.md` |

> 🛡️ **Governance is cross-cutting, not a role.** PII masking, Write-Audit-Publish, contracts, and
> downstream-impact checks live in the always-on workspace rules and apply to every agent.

---

## 🧩 Skills

Skills **activate themselves** from their description (progressive disclosure) — no agent required,
no need to name them. Ask *"document this"* and the docs skill fires on its own.

| Skill | Use it for |
|---|---|
| `pbi-semantic-layer-tmdl` | Author Power BI semantic models in TMDL |
| `pbi-report-layer-pbir` | Edit Power BI reports as code (pages, visuals, themes) |
| `pbi-quality-rules` | Real Best Practice Analyzer via the **free** Tabular Editor 2 |
| `building-html-presentations` | Decks, scrollable decks, interactive sites & consulting PDFs + an 18-chart cookbook |
| `generating-pptx` | **Native, editable PowerPoint** via python-pptx (real charts, not images) |
| `applying-visual-identity` | Apply a company brand from a `DESIGN.md` (Google Labs spec) |
| `documentation-templates` | Runbooks, data dictionaries, metric defs, ADRs, Power BI catalog |
| `creating-agents-and-skills` | Governance gate — add an agent/skill only when it helps, and keep every tool folder in sync |

---

## 📈 Power BI — as code, not clicks

The `powerbi-developer` agent edits **PBIP** projects directly on disk:

- 🧱 **TMDL** for the semantic model (tables, measures, relationships, RLS)
- 📊 **PBIR** for reports (pages, visuals, themes, bookmarks)
- ✅ Validated with the **free Tabular Editor 2** Best Practice Analyzer — no paid tooling, no Fabric required

Microsoft's official `powerbi-modeling-mcp` (preview) is supported as an optional path for bulk
refactors, but **file editing is the default**.

---

## 🎨 Presentations — as code

The `presentation-designer` agent turns analyses, EDAs, and business plans into polished, on-brand
deliverables — and reads your brand from a `DESIGN.md` so everything stays consistent.

| Starter | Output |
|---|---|
| `reveal-deck.html` | Dashboard-style slide deck (reveal.js) → HTML + PDF |
| `flex-deck.html` | Flexible **scrollable** deck with dynamic visual toggles |
| `interactive-site.html` | Self-serve scrolling report site |
| `report-pdf.html` | **McKinsey/Deloitte-style** PDF (action titles, exhibits, callouts) |
| `marp-deck.md` | Quick Markdown → PDF/PPTX |
| `charts-reference.html` | **Chart cookbook** — 18 ready-to-copy chart patterns |

Plus **`generating-pptx`** for native, **editable PowerPoint** (real text & charts, not images) via
`python-pptx`.

---

## 🔄 How it works (multi-platform)

`.agent/` is the **single source of truth**. One sync script compiles it for every assistant in
that tool's native format — write once, run everywhere.

```bash
python scripts/sync_agents.py
```

| Target | Output |
|---|---|
| Antigravity | `.agent/` (native source) |
| Claude Code | `.claude/` + `CLAUDE.md` |
| GitHub Copilot | `.github/` + `copilot-instructions.md` |
| OpenCode | `.opencode/` + `AGENTS.md` |
| Cursor / others | root `AGENTS.md` |

```text
.agent/                ← edit here (source of truth)
├── agents/            # 5 specialist personas
├── skills/            # 8 on-demand knowledge modules
├── workflows/         # 3 slash commands
└── rules/             # global rules (rules.md)

.claude/  .github/  .opencode/  AGENTS.md   ← auto-generated (do not edit)
```

---

## 🧭 Design philosophy

- **Less is more.** Extra agents and verbose instructions cost the model attention and blur routing.
  We capture domain-specific context only — never restate what the model already knows.
- **Progressive disclosure.** Skills load when relevant, not upfront.
- **No ambiguous routing.** Each agent owns a distinct domain.
- **Idempotent & safe by default.** Write-Audit-Publish, mask PII at Silver, check downstream impact.
- **Self-orchestrating.** Agents route, skills self-activate, governance is always on.

---

## 🤝 Contributing & license

Want to extend it? See **[CONTRIBUTING.md](CONTRIBUTING.md)** — especially the *"should this agent
exist?"* gates. The `creating-agents-and-skills` skill walks you through deciding, authoring, and
syncing a new capability across every platform.

**MIT** © [Lucca Pinto](https://github.com/luccapinto)

<div align="center"><sub>Built for data teams who'd rather ship than re-explain the basics.</sub></div>
