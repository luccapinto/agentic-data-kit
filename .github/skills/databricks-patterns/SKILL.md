---
name: databricks-patterns
description: Engineering best practices for PySpark, Delta Lake, Unity Catalog, and Databricks notebooks.
---

# Databricks Engineering Patterns

This skill focuses on building scalable, idempotent, and highly performant data pipelines on the Databricks platform.

## 🧠 Core Principles

1. **Think in Partitions**: Distributed data means partitions. Shuffling is the enemy of speed.
2. **ACID is Your Friend**: Rely on Delta Lake capabilities (`MERGE`, Time Travel, Z-Ordering) natively instead of reinventing the wheel.
3. **Notebooks are Not Codebases**: Notebooks are great for exploration, but production code belongs in modular, testable Python packages or modularized orchestrations (Databricks Workflows/DABs).

---

## 📋 The Medallion Architecture

All data pipelines must rigidly enforce the separation of concerns:

| Layer | Purpose | Rules |
|-------|---------|-------|
| **Bronze (Raw)** | History and ingestion. | Append-only. No schema enforcement. Store as raw JSON/Parquet/Delta. |
| **Silver (Cleansed)**| Joined, filtered, and cleansed data. | Enforce schema. Handle deduplication. `MERGE INTO` standard. |
| **Gold (Curated)** | Business-level aggregations. | Ready for BI/ML consumption. Highly aggregated. |

---

## 🛠️ Performance & PySpark Optimization

* **Avoid UDFs (User Defined Functions)**: Python UDFs trigger massive serialization overhead between the JVM and Python. Use built-in `pyspark.sql.functions` whenever structurally possible.
* **Broadcast Joins**: If joining a massive table with a tiny lookup table (< 10GB usually), force a `broadcast()` join to avoid expensive networking shuffles.
* **Predicate Pushdown**: Always filter data *before* a join or aggregation to minimize the payload early.
* **Optimize & Vacuum**: Schedule regular `OPTIMIZE` (to compact small parquets into larger files) and `VACUUM` (to clear old transaction history) on high-churn Delta tables.

---

## ❌ Anti-Patterns

* **`collect()` Abuse**: Calling `.collect()` or `.toPandas()` on a billion-row DataFrame will instantly crash the driver node memory.
* **Hardcoded Paths**: Never hardcode `dbfs:/mnt/...` paths. Use environment variables, Databricks Secrets, or Unity Catalog volumes.
* **Ignoring Unity Catalog Grants**: Failing to specify explicit `GRANT` statements when creating Gold tables, accidentally exposing PII data across the workspace.
