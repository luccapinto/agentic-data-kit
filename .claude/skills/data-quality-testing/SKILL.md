---
name: data-quality-testing
description: Principles and frameworks for data quality, testing models with dbt, Great Expectations, Data Contracts, and Write-Audit-Publish (WAP).
allowed-tools: Read, Write, Glob, Grep
---

# Data Quality & Testing Patterns

> In Software Engineering, you mock data to test logic. 
> In Data Engineering, you test logic by validating the data itself.

---

## 1. The Core Paradigm Shift

- **Unit Testing (Limited Value):** Mocking a DataFrame to test a PySpark function is useful but often doesn't catch the real issues (bad source data).
- **Data Testing (High Value):** Testing the actual output data against expectations. "Is this column ever null?", "Are there duplicate Primary Keys?", "Did sales drop 50% overnight?"

---

## 2. WAP Pattern (Write-Audit-Publish)

The gold standard for safe data pipelines.

1. **Write:** A pipeline runs and writes data to a staging table, shadow schema, or specific branch (e.g., Iceberg/Nessie logic).
2. **Audit:** Data Quality tests are run against this staging area.
3. **Publish:**
   - If tests **PASS**: The staging data is merged/swapped into the production tables.
   - If tests **FAIL**: The pipeline alerts the team, and production data remains unchanged.

---

## 3. dbt Testing Principles

dbt (Data Build Tool) is the industry standard for testing SQL transformations.

### Base Tests (Mandatory on every modeled table)
- `unique`: Ensure your primary key actually is unique.
- `not_null`: Ensure critical columns (PKs, amounts, dates) are never null.

### Referential Tests
- `relationships`: Ensure a foreign key in a Fact table actually exists in the associated Dimension table. Avoids silent data drops when joining.

### Accepted Values 
- `accepted_values`: Ensure categorical columns only contain expected data (e.g., `status` must be one of `['active', 'pending', 'deleted']`).

---

## 4. Anomaly Detection / Observability

For issues that aren't strictly "failures" but are highly suspicious.

- **Freshness:** "This table hasn't received new rows in 26 hours."
- **Volume Anomalies:** "We usually process 1M rows a day. Today we processed 10,000."
- **Distribution Anomalies:** "The percentage of NULLs in the `discount` column spiked from 5% to 80%."

**Tools:** dbt source freshness, Monte Carlo, elementary data.

---

## 5. Data Contracts

A Data Contract is an agreement between the **Data Producers** (Software Engineers) and the **Data Consumers** (Data Engineers/Analysts).

- **Concept:** Software Engineers cannot change the schema of a source database table or an emitted JSON event without warning the Data Team.
- **Enforcement:** Enforced at the CI/CD level in the software application repository using JSON Schema, Protobuf, or tools like Datafold.

---

## 6. PySpark / Python Dataframe Testing

When writing custom transformations in Python (Pandas/Polars/PySpark).

### Best Practices
- **Use Synthetic Data:** Create minimal DataFrames with edge cases explicitly designed to test your transformation logic.
- **Test the "Why", not the "How":** Assert that the output DataFrame has the correct transformed columns, not that `df.groupby()` was called.
- **Tools:** `pytest` + `chispa` (for PySpark DataFrame equality assertions).

```python
# ✅ Good PySpark Test Example using chispa
def test_calculate_taxes():
    input_df = spark.createDataFrame([("A", 100), ("B", 200)], ["id", "amount"])
    expected_df = spark.createDataFrame([("A", 100, 10), ("B", 200, 20)], ["id", "amount", "tax"])
    
    actual_df = calculate_taxes(input_df)
    assert_df_equality(actual_df, expected_df)
```

---

## 7. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Write 100% Mock Unit Tests | Focus on Data Quality tests (dbt/Great Expectations) |
| Allow silent failures (NULLs propagating) | Fail the pipeline loudly with WAP |
| Merge code without any `yaml` tests | Require `unique` and `not_null` on all models |
| Alert on every minor data anomaly | Alert only on SLA breaches or critical data loss |

---

> **Remember:** A data pipeline without tests is a random number generator.
