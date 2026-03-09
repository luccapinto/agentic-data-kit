---
description: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
---

# Multi-Agent Orchestration

You are now in **ORCHESTRATION MODE**. Your task: coordinate specialized agents to solve this complex problem.

## Task to Orchestrate
$ARGUMENTS

---

## 🔴 CRITICAL: Minimum Agent Requirement

> ⚠️ **ORCHESTRATION = MINIMUM 3 DIFFERENT AGENTS**
> 
> If you use fewer than 3 agents, you are NOT orchestrating - you're just delegating.
> 
> **Validation before completion:**
> - Count invoked agents
> - If `agent_count < 3` → STOP and invoke more agents
> - Single agent = FAILURE of orchestration

### Agent Selection Matrix

| Task Type | Recommended Agents (in order) |
| :--- | :--- |
| **Data Pipeline** | data-engineer, analytics-engineer, data-governance |
| **Semantic Model & BI** | business-analyst, analytics-engineer, data-governance |
| **Advanced Analytics / ML** | data-scientist, data-engineer, business-analyst |
| **Governance & Security** | data-governance, data-engineer |
| **Full Data Stack** | project-planner, data-engineer, analytics-engineer, business-analyst |
| **Debug** | debugger, explorer-agent, test-engineer |
| **Security** | security-auditor, penetration-tester, devops-engineer |

---

## Pre-Flight: Mode Check

| Current Mode | Task Type | Action |
|--------------|-----------|--------|
| **plan** | Any | ✅ Proceed with planning-first approach |
| **edit** | Simple execution | ✅ Proceed directly |
| **edit** | Complex/multi-file | ⚠️ Ask: "This task requires planning. Switch to plan mode?" |
| **ask** | Any | ⚠️ Ask: "Ready to orchestrate. Switch to edit or plan mode?" |

---

## 🔴 STRICT 2-PHASE ORCHESTRATION

### PHASE 1: PLANNING (Sequential - NO parallel agents)

| Step | Agent | Action |
|-------------|--------|
| 1 | `project-planner` | Create docs/PLAN.md |
| 2 | (optional) `explorer-agent` | Codebase discovery if needed |

> 🔴 **NO OTHER AGENTS during planning!** Only project-planner and explorer-agent.

### ⏸️ CHECKPOINT: User Approval

```
After PLAN.md is complete, ASK:

"✅ Plan created: docs/PLAN.md

Do you approve? (Y/N)
- Y: Start implementation
- N: I'll revise the plan"
```

> 🔴 **DO NOT proceed to Phase 2 without explicit user approval!**

### PHASE 2: IMPLEMENTATION (Parallel agents after approval)

| Parallel Group | Agents |
|----------------|--------|
| Foundation | **Example:** "Build a pipeline to ingest and model sales data."
- Lead: `data-engineer`
- Core: `analytics-engineer`, `business-analyst` |
| Polish | `test-engineer`, `devops-engineer` |

> ✅ After user approval, invoke multiple agents in PARALLEL.

## Available Agents (17 total)

| Agent | Domain | Use When |
| :--- | :--- | :--- |
| `project-planner` | Planning | Task breakdown, PLAN.md |
| `explorer-agent` | Discovery | Codebase mapping |
| `data-engineer` | Pipelines | Databricks, PySpark, ingestion |
| `analytics-engineer` | Modeling | dbt, SQL, dimensional modeling |
| `business-analyst` | BI/Metrics | Power BI, DAX, business context |
| `data-scientist` | Analytics | Python, ML, statistical models |
| `data-governance` | Security | Privacy, PII, compliance, lineage |
| `security-auditor` | Security | Vulnerabilities, Auth |
| `penetration-tester` | Security | Active testing |
| `test-engineer` | Testing | Unit, E2E, Coverage |
| `devops-engineer` | Ops | CI/CD, Docker, Deploy |
| `documentation-writer` | Docs | README, API docs |
| `debugger` | Debug | Error analysis |
| `orchestrator` | Meta | Coordination |

---

## Orchestration Protocol

### Step 1: Analyze Task Domains
Identify ALL domains this task touches:
□ Ingestion/ETL → data-engineer
□ Data Modeling → analytics-engineer
□ Reporting/BI  → business-analyst
□ Stats/ML      → data-scientist
□ Security/PII  → data-governance
□ Testing      → test-engineer
□ DevOps       → devops-engineer
□ Planning     → project-planner
```

### Step 2: Phase Detection

| If Plan Exists | Action |
|----------------|--------|
| NO `docs/PLAN.md` | → Go to PHASE 1 (planning only) |
| YES `docs/PLAN.md` + user approved | → Go to PHASE 2 (implementation) |

### Step 3: Execute Based on Phase

**PHASE 1 (Planning):**
```
Use the project-planner agent to create PLAN.md
→ STOP after plan is created
→ ASK user for approval
```

**PHASE 2 (Implementation - after approval):**
```
Invoke agents in PARALLEL:
Use the data-engineer agent to [ingestion task]
Use the analytics-engineer agent to [modeling task]
Use the test-engineer agent to [testing task]
```

**🔴 CRITICAL: Context Passing (MANDATORY)**

When invoking ANY subagent, you MUST include:

1. **Original User Request:** Full text of what user asked
2. **Decisions Made:** All user answers to Socratic questions
3. **Previous Agent Work:** Summary of what previous agents did
4. **Current Plan State:** If plan files exist in workspace, include them

**Example with FULL context:**
```
Use the project-planner agent to create PLAN.md:

**CONTEXT:**
- User Request: "Pipeline de ponta a ponta para dados de ERP"
- Decisions: Tech=Databricks, Arquitetura=Medallion, Visualização=Power BI
- Previous Work: Orchestrator asked 6 questions, user chose all options
- Current Plan: erp-pipeline-plan.md exists in workspace with initial structure

**TASK:** Create detailed PLAN.md based on ABOVE decisions. Do NOT infer from folder name.
```

> ⚠️ **VIOLATION:** Invoking subagent without full context = subagent will make wrong assumptions!


### Step 4: Verification (MANDATORY)
The LAST agent must run appropriate verification scripts:
```bash
python .agent/skills/vulnerability-scanner/scripts/security_scan.py .
python .agent/skills/lint-and-validate/scripts/lint_runner.py .
```

### Step 5: Synthesize Results
Combine all agent outputs into unified report.

---

## Output Format

```markdown
## 🎼 Orchestration Report

### Task
[Original task summary]

### Mode
[Current Antigravity Agent mode: plan/edit/ask]

### Agents Invoked (MINIMUM 3)
| # | Agent | Focus Area | Status |
|---|-------|------------|--------|
| 1 | project-planner | Task breakdown | ✅ |
| 2 | data-engineer | Pipeline de ingestão | ✅ |
| 3 | test-engineer | Verification scripts | ✅ |

### Verification Scripts Executed
- [x] security_scan.py → Pass/Fail
- [x] lint_runner.py → Pass/Fail

### Key Findings
1. **[Agent 1]**: Finding
2. **[Agent 2]**: Finding
3. **[Agent 3]**: Finding

### Deliverables
- [ ] PLAN.md created
- [ ] Code implemented
- [ ] Tests passing
- [ ] Scripts verified

### Summary
[One paragraph synthesis of all agent work]
```

---

## 🔴 EXIT GATE

Before completing orchestration, verify:

1. ✅ **Agent Count:** `invoked_agents >= 3`
2. ✅ **Scripts Executed:** At least `security_scan.py` ran
3. ✅ **Report Generated:** Orchestration Report with all agents listed

> **If any check fails → DO NOT mark orchestration complete. Invoke more agents or run scripts.**

---

**Begin orchestration now. Select 3+ agents, execute sequentially, run verification scripts, synthesize results.**
