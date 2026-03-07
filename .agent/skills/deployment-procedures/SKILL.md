---
name: deployment-procedures
description: Production deployment principles for Data Engineering. Safe deployment workflows for dbt, Airflow, and BI Dashboards. Includes rollback strategies and Slim CI verification.
allowed-tools: Read, Glob, Grep, Bash
---

# Deployment Procedures (Data Engineering)

> Deployment principles and decision-making for safe production releases in Analytics and Data Engineering.
> **Deploying pipeline code determines the STATE of data.**

---

## 1. Platform Selection

### Each Ecosystem Has Different Procedures

| Ecosystem | Deployment Method | Key Concept |
|----------|------------------|-------------|
| **dbt (Transformations)** | dbt Cloud CI/CD or GitHub Actions | **Slim CI:** Only build/test models modified in the PR and their downstream dependents. |
| **Airflow / Dagster (Orchestration)** | CI/CD Git Sync or Docker Image built | Ensure DAGs parse correctly without executing tasks during CI. |
| **Databricks** | Asset Bundles (DABs) or Terraform | Code is deployed side-by-side with Job definitions. |
| **Power BI / BI Tools** | ALM Tools / Deployment Pipelines | Move from Dev Workspace -> Test Workspace -> Prod Workspace. |

---

## 2. Pre-Deployment Principles (Data Quality)

### The 4 Verification Categories

| Category | What to Check |
|----------|--------------|
| **Code Quality** | SQLFluff passes, Python linters pass (Ruff). |
| **State Impact** | `dbt build` succeeds in an isolated schema using **Slim CI**. |
| **Data Contracts** | `unique` and `not_null` schema tests pass on the newly built models. |
| **BI Impact** | No columns used by downstream reports were renamed or deleted. |

### Pre-Deployment Checklist

- [ ] Slim CI pipeline is green.
- [ ] Code reviewed and approved (Query costs checked).
- [ ] Backfill strategy is defined (if changing historical logic, how far back do we process?).
- [ ] Schema changes (added/removed columns) communicated to BI/Data Science teams.
- [ ] Rollback plan documented (Can we revert the code? Do we need to restore data?).

---

## 3. Deployment Workflow Principles

### The 5-Phase Process

```text
1. PREPARE
   └── Verify CI, check downstream BI impacts.

2. SNAPSHOT (If Destructive)
   └── If dropping tables or massive updates, ensure Time Travel (Delta/Snowflake) is active or explicitly backup.

3. DEPLOY CODE
   └── Merge to main. CI syncs DAGs or dbt definitions to production.

4. TRIGGER/WAIT
   └── Let the next scheduled run execute OR manually trigger the modified DAGs.

5. VERIFY DATA
   └── Check row counts, run data quality sensors, verify BI dashboard renders.
```

---

## 4. Post-Deployment Verification

### What to Verify

| Check | Why |
|-------|-----|
| **Pipeline Status** | Did the Airflow DAG or Databricks Job turn green? |
| **Data Recency** | Is `MAX(date)` correct in the target tables? |
| **Data Volume** | Did row counts unexpectedly drop or explode (fan-out)? |
| **Consumers** | Does the Executive Dashboard load without breaking? |

---

## 5. Rollback Principles (Code vs Data)

### The Hard Truth in Data Engineering
In Software Engineering, reverting code often fixes the app instantly. **In Data Engineering, reverting code does NOT revert data.** 

If bad data was processed and merged into production:
1. Revert the code (Git Revert).
2. Fix the data (Run a backfill or use Time Travel to restore the previous table state).

### Rollback Strategy by Platform

| Platform | Rollback Method |
|----------|----------------|
| **dbt/Snowflake/Databricks** | Revert PR -> Use `RESTORE TABLE` or `CLONE` from Time Travel. |
| **Airflow** | Revert PR -> Clear task instances and run again with fixed code. |
| **Power BI** | Deploy backward using Deployment Pipeline, or restore the `.pbix` backup. |

---

## 6. Advanced Deployments (WAP Pattern)

### Write-Audit-Publish (WAP)
Instead of Blue-Green deployments used in web apps, Data Teams use WAP.

1. **Write:** Pipeline runs and writes data to a hidden staging or branching area (e.g., Iceberg branches or Snowflake zero-copy clones).
2. **Audit:** Data quality tests run against this staging area.
3. **Publish:** If tests pass, the staging area is cleanly swapped/published to production (e.g., View swap or Branch merge). If tests fail, production is untouched.

---

## 7. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Run `dbt build` on all models | Use `state:modified+` (Slim CI) |
| Test changes in the `PROD` schema | Test in a dedicated `PR_123` schema |
| Rename columns without warning | Alias columns as a deprecation phase first |
| Deploy massive backfills on Friday | Deploy early in the week with monitoring |
| Force push to production Databricks | Use Databricks Asset Bundles |
