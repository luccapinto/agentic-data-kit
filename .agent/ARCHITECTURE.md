# Antigravity Kit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit for Data Teams

---

## 📋 Overview

Antigravity Kit is a modular system consisting of:

- **9 Specialist Agents** - Role-based AI personas
- **10 Skills** - Domain-specific knowledge modules
- **3 Workflows** - Slash command procedures

---

## 🏗️ Directory Structure

```plaintext
.agent/
├── ARCHITECTURE.md          # This file
├── agents/                  # 9 Specialist Agents
├── skills/                  # 10 Skills
├── workflows/               # 3 Slash Commands
├── rules/                   # Global Rules
└── scripts/                 # Master Validation Scripts
```

---

## 🤖 Agents (9)

Specialist AI personas for different Data domains.

| Agent                       | Focus                      | Skills Used                                              |
| --------------------------- | -------------------------- | -------------------------------------------------------- |
| `data-engineer`             | ETL, pipelines, infra      | -                                                        |
| `analytics-engineer`        | dbt, dimensional modeling  | data-quality-testing                                     |
| `data-analyst`              | Dashboards, SQL, metrics   | data-quality-testing                                     |
| `data-scientist`            | ML, statistics, models     | -                                                        |
| `data-governance`           | Quality, LGPD, contracts   | data-quality-testing                                     |
| `powerbi-developer`         | PBI Orchestrator           | pbi-live-connection, pbi-pbip-structure, pbi-quality-rules, pbi-tmdl-authoring, pbi-dax-testing |
| `powerbi-report-designer`   | PBI Visual Layer           | pbi-theme-design, pbi-pbir-visual-authoring              |
| `documentation-writer`      | Manuals, docs              | documentation-templates, pbi-dashboard-documentation     |
| `agent-creator`             | Creates new agents/skills  | -                                                        |

---

## 🧩 Skills (10)

Modular knowledge domains that agents can load on-demand based on task context.

### Documentation & Quality

| Skill                     | Description                                                           |
| ------------------------- | --------------------------------------------------------------------- |
| `documentation-templates` | Doc formats and templates                                             |
| `data-quality-testing`    | dbt tests, Great Expectations, Data Contracts                         |

### Power BI

| Skill                         | Description                                                           |
| ----------------------------- | --------------------------------------------------------------------- |
| `pbi-live-connection`         | TOM and ADOMD connection directly to local MSMDSRV                    |
| `pbi-pbip-structure`          | Spatial navigation for Power BI projects                              |
| `pbi-quality-rules`           | Execution of BPA-like rules via PowerShell                            |
| `pbi-tmdl-authoring`          | Writing TMDL files                                                    |
| `pbi-dax-testing`             | Querying model via ADOMD to test DAX                                  |
| `pbi-theme-design`            | Report Themes JSON                                                    |
| `pbi-pbir-visual-authoring`   | Directly creating pages and visuals                                   |
| `pbi-dashboard-documentation` | Automatic documentation generation                                    |

---

## 🔄 Workflows (3)

Slash command procedures. Invoke with `/command`.

| Command                | Description                               |
| ---------------------- | ----------------------------------------- |
| `/plan`                | Project Breakdown and task scoping        |
| `/validate-pbi`        | Validates Power BI Model                  |
| `/document-dashboard`  | Automatically documents a Power BI Report |

---

## 🛠️ Scripts (5)

Master validation scripts that orchestrate validation for CI/CD or local checks.

### Master Scripts

| Script                 | Purpose                                 | When to Use              |
| ---------------------- | --------------------------------------- | ------------------------ |
| `checklist.py`         | Priority-based validation (Core checks) | Development, pre-commit  |
| `verify_all.py`        | Comprehensive verification (All checks) | Pre-deployment, releases |
| `lint_runner.py`       | SQLFluff and Ruff execution             | Checkstyle               |
| `schema_validator.py`  | Validates database modeling rules       | Commit                   |
| `data_contracts...py`  | Validates Data Contracts (YAML)         | Commit                   |

### Usage

```bash
# Quick validation before commit
python .agent/scripts/checklist.py .

# Full verification across all Data CI/CD checks
python .agent/scripts/verify_all.py .
```

---

## 📊 Statistics

| Metric              | Value                         |
| ------------------- | ----------------------------- |
| **Total Agents**    | 9                             |
| **Total Skills**    | 10                            |
| **Total Workflows** | 3                             |
| **Total Scripts**   | 5                             |
| **Coverage**        | ~100% Data Engineering & BI   |
