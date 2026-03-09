---
description: Test generation and test running command. Creates and executes tests
  for code.
name: test
---

**Contexto:** {{selection}}

# /test - Test Generation and Execution

$ARGUMENTS

---

## Purpose

This command generates tests, runs existing tests, or checks test coverage.

---

## Sub-commands

```
/test                - Run all tests
/test [file/feature] - Generate tests for specific target
/test coverage       - Show test coverage report
/test watch          - Run tests in watch mode
```

---

## Behavior

### Generate Tests

When asked to test a file or feature:

1. **Analyze the data model / pipeline**
   - Identify transformations and business logic
   - Find edge cases (nulls, duplicates, anomalies)
   - Detect upstream dependencies

2. **Generate test cases**
   - Data quality tests (unique, not null, accepted values)
   - Business logic validation
   - Edge cases (schema drift, malformed data)

3. **Write tests**
   - Use the project's data testing framework (`dbt test`, `pytest`, `Great Expectations`)
   - Follow existing patterns
   - Create mock DataFrames or fixtures if testing PySpark logic

---

## Output Format

### For Test Generation

```markdown
## 🧪 Tests: [Target]

### Test Plan
| Test Case | Type | Coverage |
|-----------|------|----------|
| Should have unique IDs | Data Quality | Unique constraint |
| Should reject null values | Data Quality | Not null constraint |
| Should calculate gross margin correctly | Logic | Business rule |

### Generated Tests

`models/staging/schema.yml`

```yaml
version: 2
models:
  - name: stg_sales
    columns:
      - name: sale_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['completed', 'pending', 'cancelled']
```

---

Run with: `dbt test --select stg_sales`
```

### For Test Execution

```
🧪 Running tests...

✅ stg_customers (5 passed)
✅ stg_products (8 passed)
❌ fct_sales (2 passed, 1 failed)

Failed:
  ✗ dbt_utils.accepted_range_fct_sales_discount
    Expected: discount <= 1.0
    Received: discount > 1.0 in 3 rows

Total: 15 tests (14 passed, 1 failed)
```

---

## Examples

```
/test dbt_model_sales
/test validação de nulls na camada bronze
/test measure de YTD no power bi
/test coverage dbt --state target
```

---

## Test Patterns

### PySpark Unit Test Structure

```python
import pytest
from pyspark.sql import Row
from src.transformations import calculate_gross_margin

def test_calculate_gross_margin(spark):
    # Arrange
    data = [
        Row(revenue=100.0, cost=60.0),
        Row(revenue=200.0, cost=180.0)
    ]
    df = spark.createDataFrame(data)
    
    # Act
    result_df = calculate_gross_margin(df)
    results = result_df.collect()
    
    # Assert
    assert results[0].gross_margin == 40.0
    assert results[1].gross_margin == 20.0
```

---

## Key Principles

- **Test data quality over unit logic** (for pipelines)
- **Use standard transformations** to isolate logic for PySpark testing
- **Document assumptions** as data tests (unique, not_null, relationship)
- **Catch errors early** in the Bronze layer
