---
name: python-data
description: Development principles specifically tailored for Data Scientists and Data Engineers using Pandas, Polars, and NumPy.
---

# Python Data Engineering & Analysis

Python is the backbone of modern data work. However, writing "data scripts" is very different from writing standard application software.

## 🧠 Core Principles

1. **Vectorization Over Iteration**: If you find yourself writing a `for` loop to iterate over millions of rows, you have already failed. Use Pandas vectorization or Polars expressions.
2. **Type Casting Saves Gigabytes**: Using `int8` instead of the default `int64` drops memory consumption by 8x. Be aggressive with `category` and downcasting.
3. **Environment Determinism**: "It works on my machine" is solved by `requirements.txt`, `Poetry`, or `conda`. Pin your `pandas` versions.

---

## 📋 Tool Selection

| Library | When to Use It | When to Avoid It |
|---------|----------------|------------------|
| **Pandas** | Small to Medium data (< 5GB). Rapid prototyping. Existing extensive codebase. | When memory pressure is tight. In distributed clusters. |
| **Polars** | High-performance requirements. Complex string parsing. Tight memory budget. | When you require highly niche machine learning integrations that strictly expect `pandas.DataFrame`. |
| **PySpark**| True Big Data (50GB+). Distributed cluster executions. | Single machine execution (overhead of local JVM initialization isn't worth it). |

---

## 🛠️ Pandas/Polars Performance Rules

### 1. Vectorize, Don't Apply
Avoid `.apply(lambda x: ...)` in Pandas at all costs. It essentially runs a hidden Python `for` loop. Write mathematical column vector operations: `df['A'] = df['B'] * df['C']`.

### 2. Functional Chaining
Write clean, readable transformations using `.pipe()` in Pandas or lazy chains in Polars:

```python
# Polars example
(
    df.lazy()
    .filter(pl.col('status') == 'active')
    .with_columns(
        (pl.col('revenue') * 0.2).alias('tax')
    )
    .collect()
)
```

### 3. Explaining Memory Leaks
Dataframes retain memory. If you must process massive files sequentially in Pandas, read them in chunks `pd.read_csv(..., chunksize=100000)` or invoke Garbage Collection `import gc; gc.collect()` after dropping large dataframe references.

---

## ❌ Anti-Patterns

* **Setting with Copy Warning Ignore**: Supressing standard warnings in Pandas when trying to modify a slice of a DataFrame (`df[df['A'] > 5]['B'] = 10`). Fix the code, don't suppress the warning.
* **The "To CSV" Crutch**: Writing intermediate processed data to `output_temp.csv` instead of a highly compressed, typed format like `.parquet`.
* **String Comparisons for Dates**: Never leave a date column as an `object` (string). Always parse it into a `datetime64[ns]` immediately upon ingestion so that native date lookups work perfectly.
