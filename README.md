# Agentic Data Kit

> **Drop one folder. Get a team of AI specialists.**

Stop explaining the same things to your AI over and over. The Agentic Data Kit is a curated library of **14 dedicated AI agents**, **23 specialized skills**, and **6 automated workflows** — all pre-configured for Data Engineering, Analytics, and Business Intelligence.

Copy the `.agent/` folder into your repository. That's it. Your AI assistant now knows how to build Databricks pipelines, edit Power BI reports from scratch, design star schemas, write DAX measures, run data quality checks, and much more — without you having to teach it anything.

---

## 🧠 Why This Exists

In the AI era, your role has shifted. You **delegate**, **orchestrate**, and **validate** — the agents do the heavy lifting. But generic AI assistants don't know *your* stack, *your* standards, or *your* architecture.

This kit solves that. It's **pre-built intellectual property** for data teams:

- **Agents already know their job.** A `data-engineer` agent thinks in Medallion Architecture and Delta Lake. A `powerbi-developer` agent edits TMDL files and builds semantic models. They don't need to be told how — they already know.
- **Skills package the hard knowledge.** Instead of pasting documentation into a chat window, skills like `databricks-patterns`, `tmdl-modeling`, and `pbip-report-hacking` give the AI deep, structured expertise on specific tools.
- **Self-validating code.** The kit goes beyond "generate and hope." Built-in validation scripts automatically check architecture compliance, DAX best practices, schema integrity, and idempotency — so the AI also handles the validation step that used to be yours.

---

## 🎯 What's Inside

### Agents — Your Dedicated Specialists

| Agent | What It Does |
|---|---|
| `data-engineer` | Builds ETL pipelines, Databricks notebooks, Delta Lake tables |
| `analytics-engineer` | Designs star schemas, writes dbt models, creates semantic layers |
| `powerbi-developer` | Edits Power BI reports, writes DAX, builds TMDL models |
| `business-analyst` | Gathers requirements, defines metrics, designs dashboards |
| `data-scientist` | Builds ML pipelines, analyzes data with Python & PySpark |
| `data-governance` | Enforces data quality, contracts, and compliance |
| `database-architect` | Designs database schemas, indexing strategies, and data models |
| `data-analyst` | Explores data, creates visualizations, answers business questions |
| `orchestrator` | Coordinates multiple agents for complex, multi-domain tasks |
| `project-planner` | Breaks down projects into phases with structured plans |
| `debugger` | Systematic root-cause analysis with evidence-based fixes |
| `documentation-writer` | Produces data dictionaries, runbooks, and technical docs |
| `explorer-agent` | Navigates and maps unfamiliar codebases |
| `agent-creator` | Builds new agents and skills for the kit itself |

### Skills — Deep, Pre-Packaged Expertise

| Skill | Domain |
|---|---|
| `databricks-patterns` | PySpark, Delta Lake, Unity Catalog best practices |
| `tmdl-modeling` | Tabular Model Definition Language for Power BI |
| `pbip-report-hacking` | Programmatic editing of `.pbip` report files |
| `powerbi-semantic-mcp` | Power BI semantic model via MCP & REST API |
| `database-design` | Star schemas, indexing, normalization patterns |
| `clean-code` | Idempotency, WAP pattern, testing pyramid |
| `data-quality-testing` | Data contracts, Great Expectations, dbt tests |
| `architecture` | Medallion Architecture, Data Mesh, dimensional modeling |
| `python-data` | Pandas, Polars, NumPy engineering patterns |
| `plan-writing` | Structured task planning with dependencies |
| ... and 13 more | Brainstorming, debugging, deployment, code review, etc. |

### Workflows — One-Command Automation

| Command | What Happens |
|---|---|
| `/plan` | AI creates a phased project plan before writing any code |
| `/debug` | Systematic 4-phase debugging with root cause analysis |
| `/brainstorm` | Socratic questioning to explore options before committing |
| `/orchestrate` | Multi-agent coordination for complex tasks |
| `/test` | Generates and runs tests following the testing pyramid |
| `/status` | Shows project progress and task tracking |

---

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/luccapinto/agentic-data-kit.git
```

### 2. Drop

Copy the `.agent/` folder into your project repository.

### 3. Work

Start asking your AI to build things. The agents are already loaded and ready.

```
You: "Build an ETL pipeline for customer data using Medallion Architecture"
AI:  🤖 Applying @data-engineer... [builds complete Bronze → Silver → Gold pipeline]

You: "Create a star schema for the sales domain"
AI:  🤖 Applying @analytics-engineer... [designs fact and dimension tables]

You: "Edit the Power BI report to add a new revenue measure"
AI:  🤖 Applying @powerbi-developer... [writes DAX, updates TMDL]
```

---

## 🔄 Multi-Platform Support

The kit natively works with **Antigravity** (autonomous agents). If you also use **GitHub Copilot** or **Claude Code**, a sync script compiles the `.agent/` source into their formats:

```bash
python scripts/sync_agents.py
```

This generates `.github/` and `.claude/` folders automatically. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 🤝 Contributing

Want to add a new agent or skill? Read the [CONTRIBUTING.md](CONTRIBUTING.md) guide. The golden rule: **never edit `.github/` or `.claude/` directly** — always work inside `.agent/`.

## 🙏 Acknowledgments

This project was heavily inspired by the pioneering work of [vudovn/antigravity-kit](https://github.com/vudovn/antigravity-kit) in the software engineering space. We've adapted and expanded upon those foundational concepts to create a dedicated solution for Data Engineering and Analytics teams. 

## 📄 License

MIT © Lucca Pinto
