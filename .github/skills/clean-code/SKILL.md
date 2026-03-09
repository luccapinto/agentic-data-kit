---
name: clean-code
description: Pragmatic coding standards for Data Engineering - concise, declarative, idempotency-focused, formatting SQL with CTEs, and DRY aggregations.
allowed-tools: Read, Write, Edit
version: 2.0
priority: CRITICAL
---

# Clean Code - Pragmatic Data Engineering Standards

> **CRITICAL SKILL** - Be **declarative, idempotent, and highly readable**.

---

## Core Principles

| Principle | Rule |
|-----------|------|
| **Declarative > Imperative** | Describe *what* you want (SQL), not *how* to get it (loops). |
| **Idempotency** | Pipelines MUST yield the exact same result if run twice. |
| **DRY Aggregations** | Don't Repeat Yourself - reuse base staging models/CTEs instead of recalculating metrics. |
| **Immutability** | Data in lower zones (Bronze/Silver) should never be mutated. Append-only. |
| **Readability First** | Storage is cheap, CPU is cheap, human reading time is expensive. |

---

## SQL & Pipeline Rules

| Element | Convention |
|---------|------------|
| **CTEs (WITH clause)** | NEVER use nested sub-queries (`SELECT * FROM (SELECT...)`). Always use linear CTEs. |
| **Naming CTEs** | Name them by what they do: `stg_customers`, `calc_monthly_revenue`. |
| **Table Naming** | Prefix by layer/domain: `dim_customer`, `fct_sales`, `stg_stripe_payments`. |
| **Formatting** | Left-align SQL keywords. Commas at the end of the line. |
| **Aliases** | Use meaningful aliases (`AS total_sales`). Never use vague aliases like `a`, `b`, `c`. |

> **Rule:** If you need a comment to explain a SQL transformation, rename your CTE or split it into two.

---

## Data Pipeline Logic

| Rule | Description |
|------|-------------|
| **Small Models** | Break down 1000-line SQL scripts into smaller, modular dbt models. |
| **One Grain per Model** | A model/table should represent exactly one grain (e.g., one row = one order). |
| **Filter Early** | Apply `WHERE` clauses as early as possible in the pipeline to reduce processed data. |
| **Explicit Types** | Always cast explicitly (`CAST(id AS STRING)`), do not rely on implicit conversions. |
| **No Silent Drops** | Use `LEFT JOIN` by default unless an `INNER JOIN` is strictly intended as a filter. |

---

## Anti-Patterns (DON'T)

| ❌ Pattern | ✅ Fix |
|-----------|-------|
| Nested Subqueries | Linear `WITH` (CTEs) |
| Hardcoded Dates/IDs | Parameterized variables (Jinja/Airflow params) |
| `SELECT *` in production | Explicitly select columns: `SELECT id, name` |
| Updating historical rows | Append new records (Type 2 SCD) |
| Complex Python Pandas Loops | Vectorized operations (Polars/PySpark) or SQL |

---

## 🔴 Before Editing ANY Pipeline (THINK FIRST!)

**Before changing a schema or pipeline, ask yourself:**

| Question | Why |
|----------|-----|
| **Downstream Impact** | Are BI dashboards or ML models using this column? |
| **Data Volume** | Will this `JOIN` explode a 1 Billion row table? |
| **Backfill Reality** | If I change this logic, do we need to recalculate the last 5 years of data? |
| **Cost** | Is this query doing a full table scan on BigQuery/Snowflake? |

**Quick Check:**
```
Pipeline to edit: stg_sales.sql
└── Who consumes this? → fct_monthly_sales.sql, dim_store.sql
└── Do they need changes too? → Check column dependencies
```

> 🔴 **Rule:** Edit the model + all dependent downstream models in the SAME task.

---

## Summary

| Do | Don't |
|----|-------|
| Write declarative SQL | Write stateful processing loops |
| Use CTEs heavily | Use nested sub-queries |
| Use clear column names | Use abbreviations (e.g., `amt` -> `amount`) |
| Filter data early | Join large tables before filtering |

> **Remember: The user wants reliable, idempotent pipelines, not clever code golf.**
