<p align="center">
  <h1 align="center">Agentic Data Kit</h1>
  <p align="center">
    <strong>Drop one folder. Get a team of AI Data Specialists.</strong>
  </p>
</p>

---

## 🧠 Why This Exists

Stop explaining the same concepts to your AI over and over. Generic LLMs don't know *your* stack, *your* standards, or *your* architecture.

The **Agentic Data Kit** is a curated library of **9 dedicated AI agents**, **7 specialized skills**, and **3 automated workflows** — all pre-configured for Data Engineering, Analytics, and Business Intelligence.

By dropping this kit into your repository, your AI assistant instantly knows how to build robust Data pipelines, edit Power BI reports programmatically, design star schemas, run data quality checks, and much more — without you having to teach it anything.

## 🚀 Quick Start

### 1. Install the Kit

In your terminal, navigate to your project folder and run the interactive CLI:

```bash
npx @luccapinto/agentic-data-kit@latest init
```

*Press `Enter`, choose your AI assistant (Antigravity, Copilot, or Claude), and the `.agent` folder will be dropped into your project.*

### 2. Put Your Team to Work

Start asking your AI to build things. The agents are already loaded and ready.

```text
You: "Build an ETL pipeline for customer data using Medallion Architecture"
AI:  🤖 Applying @data-engineer... [builds complete Bronze → Silver → Gold pipeline]

You: "Create a star schema for the sales domain"
AI:  🤖 Applying @analytics-engineer... [designs fact and dimension tables]

You: "Edit the Power BI report to add a new revenue measure"
AI:  🤖 Applying @powerbi-developer... [writes DAX, updates TMDL]
```

---

## 🎯 What's Inside

### 🤖 Agents — Your Dedicated Specialists

| Agent | What It Does |
|---|---|
| `data-engineer` | Builds ETL pipelines, architectures, and ensures data idempotency |
| `analytics-engineer` | Designs star schemas, builds dimensional models and transformations |
| `data-analyst` | Explores data, defines rigorous metrics, and ideates dashboards |
| `data-scientist` | Builds ML pipelines, runs statistical models and A/B tests |
| `data-governance` | Enforces data quality, contracts, PII masking, and LGPD/GDPR compliance |
| `powerbi-developer` | Master orchestrator for Power BI models, DAX, and TMDL manipulation |
| `powerbi-report-designer`| Designs Power BI themes and manipulates visuals via PBIR |
| `documentation-writer` | Produces data dictionaries, runbooks, and standardized technical docs |
| `agent-creator` | The architect gatekeeper that builds new agents and skills safely |

### 🧩 Skills — Deep, Pre-Packaged Expertise

Instead of pasting documentation into a chat window, skills give the AI deep, structured expertise on specific tools and frameworks:
- **Power BI Mastery:** `pbi-live-automation`, `pbi-semantic-layer-tmdl`, `pbi-report-layer-pbir`, `pbi-quality-rules`, `pbi-dashboard-documentation`
- **Quality & Docs:** `data-quality-testing`, `documentation-templates`

### 🔄 Workflows & Scripts

Built-in automation and CI/CD ready validation scripts:
- **Commands:** `/plan` (Project scoping), `/validate-pbi` (Power BI Model validation), `/document-dashboard` (Auto-documentation)
- **Validation:** `checklist.py` (Pre-commit checks), `verify_all.py` (Full CI/CD verification)

---

## 🔄 Multi-Platform Support

The kit natively works with **Antigravity** (autonomous agents) via the `.agent` folder. If you also use **GitHub Copilot** or **Claude Code**, a sync script compiles the source into their formats:

```bash
python scripts/sync_agents.py
```

---

## 🤝 Contributing & License

Want to add a new agent or skill? Read the [CONTRIBUTING.md](CONTRIBUTING.md) guide. 

MIT © Lucca Pinto
