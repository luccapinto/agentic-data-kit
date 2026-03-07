---
name: lint-and-validate
description: Automatic quality control, linting, and static analysis procedures for Data Engineering. Use after every code modification to ensure syntax correctness, SQL standards, and pipeline integrity. Keywords: lint, format, check, validate, sqlfluff, dbt, ruff.
allowed-tools: Read, Glob, Grep, Bash
---

# Lint and Validate Skill (Data Focus)

> **MANDATORY:** Run appropriate validation tools after EVERY code change. Do not finish a task until the code is error-free.

### Procedures by Ecosystem

#### SQL / Data Warehousing
1. **SQL Lint/Format (SQLFluff):** `sqlfluff lint "path"` or `sqlfluff fix "path"`
2. **dbt Compliance (Project Evaluator):** `dbt build --select package:dbt_project_evaluator`
3. **dbt Compilation:** `dbt compile --select "path"` to ensure models render correctly without syntax errors.

#### Python (Data Pipelines / Airflow / Databricks)
1. **Linter & Formatter (Ruff):** `ruff check "path" --fix` and `ruff format "path"`
2. **Security (Bandit):** `bandit -r "path" -ll`
3. **Types (MyPy):** `mypy "path"` (especially for custom Airflow operators and complex transformations)

## The Quality Loop
1. **Write/Edit Code** (SQL models, Python DAGs, Transformations)
2. **Run Validate:** e.g., `sqlfluff fix path/to/model.sql` or `ruff check path/`
3. **Analyze Report:** Check the specific errors. 
4. **Fix & Repeat:** Submitting models with compilation failures or severe linting violations is NOT allowed.

## Error Handling
- If `sqlfluff` fails: Fix the SQL style (e.g., trailing commas, capitalization, alias naming) immediately.
- If `dbt compile` fails: Fix Jinja compilation, missing refs, or syntax issues.
- If no tool is configured: Check the project root for `.sqlfluff`, `dbt_project.yml`, `pyproject.toml` and suggest creating one.

---
**Strict Rule:** No code should be committed or reported as "done" without passing these structural and compilation checks.

---

## Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/lint_runner.py` | Unified lint check (SQL/Python) | `python scripts/lint_runner.py <project_path>` |
| `scripts/schema_validator.py` | Validates YAML schemas/contracts | `python scripts/schema_validator.py <project_path>` |

