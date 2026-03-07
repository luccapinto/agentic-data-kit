# Antigravity Kit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit for Data Teams

---

## 📋 Overview

Antigravity Kit is a modular system consisting of:

- **14 Specialist Agents** - Role-based AI personas
- **23 Skills** - Domain-specific knowledge modules
- **6 Workflows** - Slash command procedures

---

## 🏗️ Directory Structure

```plaintext
.agent/
├── ARCHITECTURE.md          # This file
├── agents/                  # 14 Specialist Agents
├── skills/                  # 23 Skills
├── workflows/               # 6 Slash Commands
├── rules/                   # Global Rules
└── scripts/                 # Master Validation Scripts
```

---

## 🤖 Agents (14)

Specialist AI personas for different Data domains.

| Agent                    | Focus                      | Skills Used                                              |
| ------------------------ | -------------------------- | -------------------------------------------------------- |
| `orchestrator`           | Multi-agent coordination   | parallel-agents, behavioral-modes                        |
| `project-planner`        | Discovery, task planning   | brainstorming, plan-writing, architecture                |
| `database-architect`     | Schema, SQL                | database-design                                          |
| `debugger`               | Root cause analysis        | systematic-debugging                                     |
| `documentation-writer`   | Manuals, docs              | documentation-templates                                  |
| `explorer-agent`         | Codebase analysis          | -                                                        |
| `data-engineer`          | ETL, pipelines, infra      | clean-code, databricks-patterns, database-design         |
| `analytics-engineer`     | dbt, dimensional modeling  | clean-code, database-design, tmdl-modeling               |
| `data-analyst`           | Dashboards, SQL, insights  | clean-code, python-data, database-design                 |
| `data-scientist`         | ML, statistics, models     | clean-code, python-data, databricks-patterns             |
| `data-governance`        | Quality, LGPD, contracts   | data-documentation, database-design                      |
| `business-analyst`       | Power BI, Reqs, Metrics    | clean-code, powerbi-semantic-mcp, data-documentation     |
| `powerbi-developer`      | Power BI Models & Reports  | powerbi-semantic-mcp, pbip-report-hacking, tmdl-modeling |
| `agent-creator`          | Creates new agents         | plan-writing                                             |

---

## 🧩 Skills (23)

Modular knowledge domains that agents can load on-demand based on task context.

### Data Engineering & Analytics

| Skill                   | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `databricks-patterns`   | Delta Lake, Unity Catalog, PySpark optimization                       |
| `python-data`           | Pandas, Polars, memory management                                     |
| `data-documentation`    | dbt YML, lineage, metric definitions                                  |

### Business Intelligence & Reporting

| Skill                   | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `powerbi-semantic-mcp`  | Tabular Editor, REST API, Documentation, DAX Checkers                 |
| `pbip-report-hacking`   | Programmatic extraction/manipulation of .pbip files                   |
| `tmdl-modeling`         | Tabular Model Definition Language structural best practices           |

### Database

| Skill             | Description                 |
| ----------------- | --------------------------- |
| `database-design` | Schema design, optimization |

### Testing & Quality

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `data-quality-testing`  | dbt tests, Great Expectations, Data Contracts |
| `code-review-checklist` | Code review standards    |
| `lint-and-validate`     | SQLFluff, Ruff, Flake8   |

### Architecture & Planning

| Skill           | Description                |
| --------------- | -------------------------- |
| `architecture`  | System design patterns     |
| `plan-writing`  | Task planning, breakdown   |
| `brainstorming` | Socratic questioning       |
| `deployment-procedures` | CI/CD, deploy workflows  |

### Shell/CLI

| Skill                | Description               |
| -------------------- | ------------------------- |
| `bash-linux`         | Linux commands, scripting |
| `powershell-windows` | Windows PowerShell        |

### Core & Meta

| Skill                     | Description               |
| ------------------------- | ------------------------- |
| `clean-code`              | Coding standards (Global) |
| `behavioral-modes`        | Agent personas            |
| `parallel-agents`         | Multi-agent patterns      |
| `mcp-builder`             | Model Context Protocol    |
| `documentation-templates` | Doc formats               |
| `systematic-debugging`    | Troubleshooting           |
| `intelligent-routing`     | Routing definitions       |

---

## 🔄 Workflows (6)

Slash command procedures. Invoke with `/command`.

| Command          | Description              |
| ---------------- | ------------------------ |
| `/brainstorm`    | Socratic discovery       |
| `/debug`         | Debug issues             |
| `/orchestrate`   | Multi-agent coordination |
| `/plan`          | Task breakdown           |
| `/status`        | Check project status     |
| `/test`          | Run tests                |

---

## 🎯 Skill Loading Protocol

```plaintext
User Request → Skill Description Match → Load SKILL.md
                                            ↓
                                    Read references/
                                            ↓
                                    Read scripts/
```

### Skill Structure

```plaintext
skill-name/
├── SKILL.md           # (Required) Metadata & instructions
├── scripts/           # (Optional) Python/Bash scripts
├── references/        # (Optional) Templates, docs
└── assets/            # (Optional) Images, logos
```

---

## 🛠️ Scripts (2)

Master validation scripts that orchestrate skill-level scripts for Data Pipelines.

### Master Scripts

| Script             | Purpose                                 | When to Use              |
| ------------------ | --------------------------------------- | ------------------------ |
| `checklist.py`     | Priority-based validation (Core checks) | Development, pre-commit  |
| `verify_all.py`    | Comprehensive verification (All checks) | Pre-deployment, releases |

### Usage

```bash
# Quick validation before commit
python .agent/scripts/checklist.py .

# Full verification across all Data CI/CD checks
python .agent/scripts/verify_all.py .
```

### What They Check

**checklist.py** (Core Data Checks):
- Security (vulnerabilities, credentials)
- SQL Linter & Python Linter
- Medallion Architecture Check

**verify_all.py** (Full Suite):
- Everything in checklist.py PLUS:
- Power BI DAX Best Practices
- Star Schema Conventions Check
- Data Quality Tests (Data Contracts)
- PBIP, TMDL Layout Sanity Check
- Idempotency Checks

---

## 📊 Statistics

| Metric              | Value                         |
| ------------------- | ----------------------------- |
| **Total Agents**    | 14                            |
| **Total Skills**    | 23                            |
| **Total Workflows** | 6                             |
| **Total Scripts**   | 2 (master) + skill-level      |
| **Coverage**        | ~100% Data Engineering & BI   |

---

## 🔗 Quick Reference

| Need     | Agent                 | Skills                                |
| -------- | --------------------- | ------------------------------------- |
| Pipeline | `data-engineer`       | databricks-patterns, database-design  |
| Power BI | `powerbi-developer`   | powerbi-semantic-mcp, pbip-report-hacking|
| Models   | `analytics-engineer`  | database-design, tmdl-modeling        |
| ML / AI  | `data-scientist`      | python-data, databricks-patterns      |
| SQL Arch | `database-architect`  | database-design                       |
| Debug    | `debugger`            | systematic-debugging                  |
| Plan     | `project-planner`     | brainstorming, plan-writing           |

