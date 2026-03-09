---
name: code-review-checklist
description: Code review guidelines for Data Engineering covering query cost, performance, data quality, and idempotency.
allowed-tools: Read, Glob, Grep
---

# Code Review Checklist (Data Engineering)

## Quick Review Checklist

### 📉 Performance & Cost (CRITICAL)
- [ ] No `SELECT *` in production (all fields explicitly declared)
- [ ] No unnecessary Full Table Scans (are partitions/clustered keys being used in the `WHERE` clause?)
- [ ] Is there a massive `CROSS JOIN` or exploding `JOIN` without strict filters?
- [ ] Are incremental loads preferred over full refreshes for large tables?

### 🛡️ Data Quality & Correctness
- [ ] Are we handling `NULL` values safely in `COALESCE` or aggregations?
- [ ] Does the `JOIN` logic accidentally create duplicate rows (fan-out)?
- [ ] Is the grain of the table explicitly clear and documented?
- [ ] Are surrogate keys generated deterministically (e.g., `md5()`)?

### 🏗️ Pipeline & Orchestration
- [ ] Is the pipeline/DAG **idempotent**? (If I run it twice, is the data duplicated?)
- [ ] Are dependencies explicitly declared? (e.g., using `ref()` in dbt, or Task Groups in Airflow)
- [ ] Are sensors or upstream checks in place before processing begins?
- [ ] Are there proper retry mechanisms for transient failures (like API Rate Limits)?

### 🧪 Contracts & Testing
- [ ] Are Primary Keys tested for uniqueness (`unique` test in dbt)?
- [ ] Are crucial columns tested for `not_null`?
- [ ] Do we have accepted value tests for categorical columns?
- [ ] Is there a data quality alert/notification step on failure?

## Anti-Patterns to Flag (SQL / Python Data)

```sql
-- ❌ Inefficient JOINs and Filters
SELECT a.*, b.* 
FROM sales a 
LEFT JOIN customers b ON a.cust_id = b.cust_id
WHERE b.is_active = true -- Turns LEFT JOIN into INNER JOIN, breaks logic

-- ✅ Filter safely before or inside JOIN
SELECT a.id, b.name 
FROM sales a 
LEFT JOIN customers b ON a.cust_id = b.cust_id AND b.is_active = true

-- ❌ Deeply nested subqueries
SELECT x FROM (SELECT y FROM (SELECT z FROM table))

-- ✅ Linear CTEs
WITH step_one AS (SELECT z FROM table),
     step_two AS (SELECT y FROM step_one)
SELECT x FROM step_two;
```

```python
# ❌ Processing in memory with Pandas instead of Spark/SQL for large datasets
df = pd.read_sql("SELECT * FROM huge_table")
df['new'] = df['a'] + df['b']

# ✅ Pushdown compute to Warehouse or use Distributed Processing (PySpark)
df = spark.sql("SELECT a, b, a+b as new FROM huge_table")
```

## Review Comments Guide

```
// Blocking issues use 🔴
🔴 BLOCKING: This JOIN will cause a massive Cartesian product (fan-out) without a secondary key.

// Cost/Performance issues use 💰
💰 COST WARNING: You are doing a full table scan on a 50TB table. Please filter by `partition_date`.

// Important suggestions use 🟡
🟡 SUGGESTION: Consider moving this complex regex into a Python UDF for better readability.

// Minor nits use 🟢
🟢 NIT: Please use `snake_case` for the new column `CustomerID` -> `customer_id`.
```
