# 🔄 Agent Flow Architecture

> **Agentic Data Kit** - Comprehensive AI Agent Workflow Documentation

---

## 📊 Overview Flow Diagram

```
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
    │ /brainstorm       │      │ Agent Selection  │
    │ /debug            │      │ Based on Domain  │
    │ /orchestrate      │      │                  │
    │ /plan             │      │ • data-engineer  │
    │ /status           │      │ • analytics-*    │
    │ /test             │      │ • powerbi-*      │
    │                   │      │ • database-*     │
    │                   │      │ • business-*     │
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
         │  • Security scan                    │
         │  • Python/SQL Linter                │
         │  • Medallion architecture drift     │
         │  • Idempotency Check                │
         │                                      │
         │  Full Check (verify_all.py):        │
         │  • All above + Databricks Lint      │
         │  • Great Expectations / Data Tests  │
         │  • Power BI Layout Sanity           │
         │  • DAX Best Practices Auditor       │
         │  • TMDL Syntax Check                │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │         RESULT DELIVERY             │
         │  • Present changes to user          │
         │  • Provide pipeline explanations    │
         │  • Suggest next deployment steps    │
         └─────────────────────────────────────┘
```

---

## 🎯 Detailed Agent Workflow

### 1️⃣ **Request Entry Points**

```
User Input Types:
┌─────────────────────────────────────────────────────────────┐
│ A. Natural Language Request                                 │
│    "Build a Databricks silver pipeline for sales"           │
│                                                              │
│ B. Slash Command                                            │
│    "/plan migrate on-prem SQL to Delta Lake"                │
│                                                              │
│ C. Domain-Specific Request                                  │
│    "Optimize DAX Measure" → powerbi-developer               │
│    "Check PII exposure" → data-governance                   │
│    "Add tests for dbt schema" → analytics-engineer          │
└─────────────────────────────────────────────────────────────┘
```

#### Socratic Gate Protocol

Before implementation, verify:

- **New Feature** → ASK 3 strategic questions
- **Bug Fix** → Confirm understanding + ask impact
- **Vague request** → Ask Purpose, Users, Scope

### 2️⃣ **Agent Selection Matrix**

#### Agent Routing Checklist (Mandatory)

Before ANY data engineering/BI work:

| Step | Check                        | If Unchecked                             |
| ---- | ---------------------------- | ---------------------------------------- |
| 1    | Identify correct agent       | → Analyze request domain                 |
| 2    | Read agent's .md file        | → Open `.agent/agents/{agent}.md`        |
| 3    | Announce agent               | → `🤖 Applying knowledge of @[agent]...` |
| 4    | Load skills from frontmatter | → Check `skills:` field                  |

```
Request Domain → Agent Mapping:

┌──────────────────────┬─────────────────────┬──────────────────────────┐
│ Domain               │ Primary Agent       │ Skills Loaded            │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Spark/Pipelines      │ data-engineer       │ databricks-patterns      │
│                      │                     │ architecture             │
│                      │                     │ clean-code               │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ dbt/Dimensional      │ analytics-engineer  │ tmdl-modeling            │
│                      │                     │ database-design          │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Power BI Models/DAX  │ powerbi-developer   │ powerbi-semantic-mcp     │
│                      │                     │ pbip-report-hacking      │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Business/Requirements│ business-analyst    │ data-documentation       │
│                      │                     │ plan-writing             │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Data Quality/Gov     │ data-governance     │ data-quality-testing     │
│                      │                     │ data-documentation       │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ ML/Statistics        │ data-scientist      │ python-data              │
│                      │                     │ databricks-patterns      │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Schema Opt.          │ database-architect  │ database-design          │
│                      │                     │ architecture             │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Planning/Task Board  │ project-planner     │ brainstorming            │
│                      │                     │ plan-writing             │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Multi-Agent Tasks    │ orchestrator        │ parallel-agents          │
│                      │                     │ behavioral-modes         │
└──────────────────────┴─────────────────────┴──────────────────────────┘
```

### 3️⃣ **Skill Loading Protocol**

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILL LOADING FLOW                        │
└─────────────────────────────────────────────────────────────┘

Step 1: Match Request to Skill
┌──────────────────────────────────────────┐
│ User: "I need to tune this PySpark code" │
│   ↓                                       │
│ Keyword Match: "PySpark" → databricks-patterns│
└──────────────────────────────────────────┘
                    ↓
Step 2: Load Skill Metadata
┌──────────────────────────────────────────┐
│ Read: .agent/skills/databricks-patterns/ │
│       └── SKILL.md (main instructions)   │
└──────────────────────────────────────────┘
                    ↓
Step 3: Execute Scripts (if needed)
┌──────────────────────────────────────────┐
│ Run: scripts/dbx_notebook_linter.py      │
│      (validates notebook logic)          │
└──────────────────────────────────────────┘
                    ↓
Step 4: Apply Knowledge
┌──────────────────────────────────────────┐
│ Agent now has:                           │
│ • Delta table optimization               │
│ • Broadcast join strategies              │
│ • Spark session handling                 │
│ • Linter outputs                         │
└──────────────────────────────────────────┘
```

### 4️⃣ **Workflow Command Execution**

```
Slash Command Flow:

/brainstorm
    ↓
    1. Load: brainstorming skill
    2. Apply: Socratic questioning for Data (Volume, Velocity, Variability)
    3. Output: Structured discovery document

/debug
    ↓
    1. Load: systematic-debugging skill
    2. Analyze: Pipeline failure logs, Stack traces
    3. Apply: Root cause analysis
    4. Suggest: Fix with PySpark/SQL code examples
    5. Test: Verify idempotency check and fix works

/test
    ↓
    1. Load: data-quality-testing skill
    2. Detect: Framework (pytest, dbt test, great_expectations)
    3. Generate: Data contracts
    4. Execute: Validate testing scripts
    5. Report: Data validation results

/orchestrate
    ↓
    1. Load: parallel-agents skill
    2. Decompose: Data task into subtasks
    3. Assign: Each subtask to specialist agent
    4. Coordinate: Parallel execution
    5. Merge: Combine pipeline/BI results
    6. Validate: Run verify_all.py logic

/plan
    ↓
    1. Load: plan-writing + architecture skills
    2. Analyze: Business requirements
    3. Break down: Models, pipelines, dashboards
    4. Output: Structured task list with data milestones
```

### 5️⃣ **Multi-Agent Orchestration**

```
Complex Task → /orchestrate → Multiple Specialist Personas

Example: "Build a customer 360 view from raw data to Power BI"

┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR AGENT                       │
│  Decomposes task into sequential workstreams                │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ DATA          │   │ ANALYTICS     │   │ POWER BI      │
│ ENGINEER      │   │ ENGINEER      │   │ DEVELOPER     │
│               │   │               │   │               │
│ Skills:       │   │ Skills:       │   │ Skills:       │
│ • databricks-*│   │ • database-*  │   │ • powerbi-*   │
│ • architecture│   │ • tmdl-*      │   │ • pbip-*      │
│               │   │               │   │               │
│ Builds:       │   │ Builds:       │   │ Builds:       │
│ • Bronze Jobs │   │ • Star Schema │   │ • TMDL Model  │
│ • Silver Cleans │ • dbt Models  │   │ • DAX Measures│
│ • Medallion   │   │ • Fact/Dims   │   │ • PBIR Report │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └─────────────────┬─┴───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │      DATA COHERENCE                 │
        │  • AI maintains model parity        │
        │  • Ensures dimensional mapping      │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │    VALIDATION (All Agents)          │
        │  • data-gov → Docs & Contracts      │
        │  • test-eng → Pipeline Tests        │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │    DEPLOYMENT                       │
        │  • devops-engineer → Databricks/PBI │
        └─────────────────────────────────────┘
```

### 6️⃣ **Validation & Quality Gates**

```
┌─────────────────────────────────────────────────────────────┐
│                 VALIDATION PIPELINE                          │
└─────────────────────────────────────────────────────────────┘

During Development (Quick Checks):
┌──────────────────────────────────────────┐
│ python .agent/scripts/checklist.py .     │
├──────────────────────────────────────────┤
│ ✓ Security Scan (vulnerabilities)        │
│ ✓ Code Quality (Ruff, Sqlfluff)          │
│ ✓ Medallion Architecture Check           │
│ ✓ Idempotency Checker                    │
└──────────────────────────────────────────┘
        Time: ~10 seconds

Pre-Deployment (Full Verification):
┌──────────────────────────────────────────────────────┐
│ python .agent/scripts/verify_all.py .                │
├──────────────────────────────────────────────────────┤
│ ✓ All Quick Checks                                   │
│ ✓ Data Contracts Validator                           │
│ ✓ Star Schema Auditor                                │
│ ✓ Pandas/Polars Perf Check                           │
│ ✓ PBIP Layout & TMDL Syntax Checks                   │
│ ✓ DAX Best Practices Auditor                         │
│ ✓ Databricks Notebook Linter                         │
└──────────────────────────────────────────────────────┘
        Time: ~1 minute
```

---

## 🧩 Skill-to-Script Mapping

```
Skills with Automated Scripts:

┌─────────────────────────┬──────────────────────────────────────────┐
│ Skill                   │ Script                                   │
├─────────────────────────┼──────────────────────────────────────────┤
│ architecture            │ scripts/medallion_drift_checker.py       │
│ database-design         │ scripts/star_schema_auditor.py           │
│ data-quality-testing    │ scripts/data_contracts_validator.py      │
│ tmdl-modeling           │ scripts/tmdl_syntax_lint.py              │
│ pbip-report-hacking     │ scripts/pbir_layout_sanity_check.py      │
│ powerbi-semantic-mcp    │ scripts/dax_best_practices_auditor.py    │
│ clean-code              │ scripts/idempotency_checker.py           │
│ data-documentation      │ scripts/docs_completeness_auditor.py     │
│ plan-writing            │ scripts/checklist_format_verifier.py     │
│ databricks-patterns     │ scripts/dbx_notebook_linter.py           │
│ python-data             │ scripts/pandas_polars_analyzer.py        │
│ lint-and-validate       │ scripts/lint_runner.py, sql_lint.py      │
│ vulnerability-scanner   │ scripts/security_scan.py                 │
└─────────────────────────┴──────────────────────────────────────────┘
```

---

## 🔄 Complete Request Lifecycle Example

```
User Request: "Migrate our daily sales pipeline from stored procs to Databricks Medallion"

1. REQUEST CLASSIFICATION
   ├─ Type: Pipeline implementation
   ├─ Domain: Data Engineering + Architecture
   ├─ Complexity: High
   └─ Suggested: /plan then /orchestrate

2. WORKFLOW SELECTION
   └─ User chooses: /orchestrate (multi-agent approach)

3. ORCHESTRATOR DECOMPOSITION
   ├─ Data Eng 1: Bronze ingestion (Auto Loader)
   ├─ Data Eng 2: Silver transformation (MERGE/Idempotent updates)
   ├─ Analytics Eng: Gold dimensional aggregation
   └─ QA/Gov: Build data contracts and test suite

4. AGENT ASSIGNMENT
   ├─ data-engineer
   │   └─ Skills: databricks-patterns, architecture
   ├─ analytics-engineer
   │   └─ Skills: database-design
   └─ data-governance
       └─ Skills: data-quality-testing, data-documentation

5. SEQUENTIAL MULTI-DOMAIN EXECUTION
   Note: AI writes processing scripts, orchestrates DAGs, and builds
   governance artifacts cohesively.

   ├─ Ingestion Builds:
   │   └─ src/jobs/bronze_load.py (PySpark)
   ├─ Transform Builds:
   │   ├─ src/jobs/silver_cleanse.py
   │   └─ src/models/gold_sales_fact.py
   └─ Testing Builds:
       ├─ tests/test_silver.py (pytest)
       └─ dbt/models/schema.yml (data contracts)

6. CODE INTEGRATION
   └─ AI ensures data moves accurately between layers
       ├─ Resolves references and schema evolution
       └─ Connects silver keys to gold dimensional mappings

7. VALIDATION
   ├─ checklist.py
   │   ✓ Security: No plaintext tokens
   │   ✓ Lint: Code complies with PEP8 and Ruff
   │   ✓ Medallion: Gold isn't querying Bronze directly
   └─ verify_all.py
       ✓ Databricks patterns: No collect() on 1B rows
       ✓ Contracts: Null/Unique checks exist on SKs

8. RESULT DELIVERY
   └─ User receives:
       ├─ Complete Spark Job definitions
       ├─ DLT (Delta Live Tables) or task orchestrations
       ├─ Testing suite results
       └─ Validated Databricks scripts
```

---

## 📈 Statistics & Metrics

```
┌──────────────────────────────────────────────────────────┐
│                    SYSTEM CAPABILITIES                    │
├──────────────────────────────────────────────────────────┤
│ Total Agents:              14                            │
│ Total Skills:              23                            │
│ Total Workflows:           6                             │
│ Master Scripts:            2 (checklist, verify_all)     │
│ Skill-Level Scripts:       ~15                           │
│ Coverage:                  Data Engineering, BI, DS      │
│                                                          │
│ Supported Frameworks:                                    │
│ ├─ Engineering: PySpark, Databricks, SQL, dbt          │
│ ├─ Storage: Delta Lake, Parquet, Snowflake             │
│ ├─ BI/Dashboards: Power BI DAX, TMDL, PBIP              │
│ ├─ Data Science: Pandas, Polars, Scikit-learn           │
│ ├─ Testing: pytest, Great Expectations, dbt tests      │
│ └─ DevOps: Azure DevOps, GitHub Actions                 │
└──────────────────────────────────────────────────────────┘
```

---

## 🔗 Quick Reference Links

- **Architecture**: `.agent/ARCHITECTURE.md`
- **Agents**: `.agent/agents/`
- **Skills**: `.agent/skills/`
- **Workflows**: `.agent/workflows/`
- **Scripts**: `.agent/scripts/`

---

**Last Updated**: 2026-03-07
**Version**: 2.5.0 (Data Framework Edition)
