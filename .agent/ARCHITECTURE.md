# Antigravity Kit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit for Data Teams

---

## 📋 Overview

Antigravity Kit is a modular system consisting of:

- **17 Specialist Agents** - Role-based AI personas
- **27 Skills** - Domain-specific knowledge modules
- **6 Workflows** - Slash command procedures

---

## 🏗️ Directory Structure

```plaintext
.agent/
├── ARCHITECTURE.md          # This file
├── agents/                  # 17 Specialist Agents
├── skills/                  # 27 Skills
├── workflows/               # 6 Slash Commands
├── rules/                   # Global Rules
└── scripts/                 # Master Validation Scripts
```

---

## 🤖 Agents (17)

Specialist AI personas for different domains.

| Agent                    | Focus                      | Skills Used                                              |
| ------------------------ | -------------------------- | -------------------------------------------------------- |
| `orchestrator`           | Multi-agent coordination   | parallel-agents, behavioral-modes                        |
| `project-planner`        | Discovery, task planning   | brainstorming, plan-writing, architecture                |
| `database-architect`     | Schema, SQL                | database-design                                          |
| `devops-engineer`        | CI/CD                      | deployment-procedures, azure-devops-workflow             |
| `debugger`               | Root cause analysis        | systematic-debugging                                     |
| `documentation-writer`   | Manuals, docs              | documentation-templates                                  |
| `product-manager`        | Requirements, user stories | plan-writing, brainstorming                              |
| `product-owner`          | Strategy, backlog, MVP     | plan-writing, brainstorming                              |
| `code-archaeologist`     | Legacy code, refactoring   | clean-code, code-review-checklist                        |
| `explorer-agent`         | Codebase analysis          | -                                                        |
| `data-engineer`          | ETL, pipelines, infra      | clean-code, databricks-patterns, database-design         |
| `analytics-engineer`     | dbt, dimensional modeling  | clean-code, database-design, azure-devops-workflow       |
| `data-analyst`           | Dashboards, SQL, insights  | clean-code, python-data, database-design                 |
| `data-scientist`         | ML, statistics, models     | clean-code, python-data, databricks-patterns             |
| `data-governance`        | Quality, LGPD, contracts   | data-documentation, database-design                      |
| `business-analyst`       | Power BI, Reqs, Metrics    | clean-code, powerbi-semantic-mcp, data-documentation     |
| `agent-creator`          | Creates new agents         | plan-writing                                             |

---

## 🧩 Skills (27)

Modular knowledge domains that agents can load on-demand based on task context.

### Data Engineering & Analytics

| Skill                   | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `databricks-patterns`   | Delta Lake, Unity Catalog, PySpark optimization                       |
| `powerbi-semantic-mcp`  | Tabular Editor, REST API, Documentation, DAX Checkers                 |
| `python-data`           | Pandas, Polars, memory management                                     |
| `data-documentation`    | dbt YML, lineage, metric definitions                                  |

### Database

| Skill             | Description                 |
| ----------------- | --------------------------- |
| `database-design` | Schema design, optimization |

### Architecture & Planning

| Skill           | Description                |
| --------------- | -------------------------- |
| `architecture`  | System design patterns     |
| `plan-writing`  | Task planning, breakdown   |
| `brainstorming` | Socratic questioning       |

### Cloud & Infrastructure

| Skill                   | Description               |
| ----------------------- | ------------------------- |
| `deployment-procedures` | CI/CD, deploy workflows   |
| `server-management`     | Infrastructure management |

### Testing & Quality

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `testing-patterns`      | PyTest, Great Expectations|
| `tdd-workflow`          | Test-driven development  |
| `code-review-checklist` | Code review standards    |
| `lint-and-validate`     | SQLFluff, Ruff, Flake8   |

### Security

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `vulnerability-scanner` | Security auditing, OWASP |
| `red-team-tactics`      | Offensive security       |

### Shell/CLI

| Skill                | Description               |
| -------------------- | ------------------------- |
| `bash-linux`         | Linux commands, scripting |
| `powershell-windows` | Windows PowerShell        |

### Other

| Skill                     | Description               |
| ------------------------- | ------------------------- |
| `clean-code`              | Coding standards (Global) |
| `behavioral-modes`        | Agent personas            |
| `parallel-agents`         | Multi-agent patterns      |
| `mcp-builder`             | Model Context Protocol    |
| `documentation-templates` | Doc formats               |
| `performance-profiling`   | Heavy Query Profiling     |
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
- SQL Lint & Python Lint
- Data Documentation Check
- Data Pipeline Test Runner (PyTest)
- Heavy Query Profiler

**verify_all.py** (Full Suite):
- Everything in checklist.py PLUS:
- Secrets & Credential Scan
- Dependency Vulnerability
- Data Privacy (PII) Check
- Power BI DAX Format Check
- Data Expectations (Great Expectations, Data Quality)

---

## 📊 Statistics

| Metric              | Value                         |
| ------------------- | ----------------------------- |
| **Total Agents**    | 17                            |
| **Total Skills**    | 27                            |
| **Total Workflows** | 6                             |
| **Total Scripts**   | 2 (master) + skill-level      |
| **Coverage**        | ~100% Data Engineering & BI   |

---

## 🔗 Quick Reference

| Need     | Agent                 | Skills                                |
| -------- | --------------------- | ------------------------------------- |
| Pipeline | `data-engineer`       | databricks-patterns, database-design  |
| Semantic | `business-analyst`    | powerbi-semantic-mcp, data-documentation |
| Models   | `analytics-engineer`  | database-design, azure-devops-workflow |
| ML / AI  | `data-scientist`      | python-data, databricks-patterns      |
| SQL Arch | `database-architect`  | database-design                       |
| DevOps   | `devops-engineer`     | deployment-procedures, azure-devops-workflow |
| Debug    | `debugger`            | systematic-debugging                  |
| Plan     | `project-planner`     | brainstorming, plan-writing           |
