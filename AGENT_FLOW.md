# 🔄 Agent Flow Architecture

> **Agentic Data Kit** - Comprehensive AI Agent Workflow Documentation

---

## 📊 Overview Flow Diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REQUEST CLASSIFICATION                        │
│  • Analyze intent (build pipeline, debug DAX, deploy models)   │
│  • Identify domain (data engineering, BI, ML, governance)      │
│  • Detect complexity (simple, medium, complex)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
    ┌───────────────────┐      ┌──────────────────┐
    │ WORKFLOW COMMAND  │      │  DIRECT AGENT    │
    │  (Slash Command)  │      │  ASSIGNMENT      │
    └─────────┬─────────┘      └────────┬─────────┘
              │                         │
              ▼                         ▼
    ┌───────────────────┐      ┌──────────────────┐
    │ /plan             │      │ Agent Selection  │
    │ /validate-pbi     │      │ Based on Domain  │
    │ /document-dash... │      │                  │
    │                   │      │ • data-engineer  │
    │                   │      │ • analytics-*    │
    │                   │      │ • powerbi-*      │
    │                   │      │ • data-analyst   │
    │                   │      │ • data-governance│
    └─────────┬─────────┘      └────────┬─────────┘
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
         ┌─────────────────────────────────────┐
         │       AGENT INITIALIZATION          │
         │  • Load agent persona/role          │
         │  • Load required skills             │
         │  • Set behavioral mode              │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │      SKILL LOADING PROTOCOL         │
         │                                      │
         │  1. Read SKILL.md metadata          │
         │  2. Load references/ (if needed)    │
         │  3. Execute scripts/ (if needed)    │
         │  4. Apply rules and patterns        │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │         TASK EXECUTION              │
         │                                      │
         │  • Analyze pipelines/semantic models│
         │  • Apply best data practices        │
         │  • Generate/modify ETL/Views/DAX    │
         │  • Run validations                  │
         │  • Execute queries/tests            │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │      VALIDATION LAYER               │
         │                                      │
         │  Quick Check (checklist.py):        │
         │  • Code Linting (Ruff/SQLFluff)     │
         │  • Schema Validation                │
         │  • Data Contracts Validator         │
         │                                      │
         │  Full Check (verify_all.py):        │
         │  • All above                        │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │         RESULT DELIVERY             │
         │  • Present changes to user          │
         │  • Provide explanations             │
         └─────────────────────────────────────┘
```

---

## 🎯 Detailed Agent Workflow

### 1️⃣ **Request Entry Points**

#### Socratic Gate Protocol

Before implementation, verify:
- **New Feature** → ASK 3 strategic questions
- **Vague request** → Ask Purpose, Users, Scope
- **Direct Proceed** → Validate assumptions and ask 1 edge-case question.

### 2️⃣ **Agent Selection Matrix**

Before ANY data engineering/BI work:

| Step | Check                        | Action                                   |
| ---- | ---------------------------- | ---------------------------------------- |
| 1    | Identify correct agent       | Analyze request domain                   |
| 2    | Read agent's .md file        | Open `.agent/agents/{agent}.md`          |
| 3    | Announce agent               | `🤖 Applying knowledge of @[agent]...`   |
| 4    | Load skills from frontmatter | Check `skills:` field                    |

### 3️⃣ **Skill Loading Protocol**

1. Match request to Skill (e.g. "Create DAX" → `pbi-tmdl-authoring`)
2. Load Skill Metadata (`SKILL.md`)
3. Execute validation scripts if requested.
4. Apply structured knowledge to the task.

### 4️⃣ **Validation & Quality Gates**

```text
During Development (Quick Checks):
┌──────────────────────────────────────────┐
│ python .agent/scripts/checklist.py .     │
├──────────────────────────────────────────┤
│ ✓ Code Quality (Ruff, Sqlfluff)          │
│ ✓ Schema Validation                      │
│ ✓ Data Contracts                         │
└──────────────────────────────────────────┘

Pre-Deployment (Full Verification):
┌──────────────────────────────────────────────────────┐
│ python .agent/scripts/verify_all.py .                │
├──────────────────────────────────────────────────────┤
│ ✓ All Quick Checks                                   │
│ ✓ Additional Rules                                   │
└──────────────────────────────────────────────────────┘
```

---

## 📈 Statistics & Metrics

| Metric | Value |
| --- | --- |
| Total Agents | 9 |
| Total Skills | 10 |
| Total Workflows | 3 |
| Master Scripts | 5 |

**Last Updated**: April 2026
**Version**: 3.0.0 (Agentic Lean Edition)
