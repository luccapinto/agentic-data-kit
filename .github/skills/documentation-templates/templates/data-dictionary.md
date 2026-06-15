# Template: Table / Model Data Dictionary

Prefer placing this inside the model's `schema.yml` (dbt) or a Markdown registry next to the code.

```markdown
# Table: [schema].[table]

**Description:** One row per completed order, with net amounts and applied discounts.
**Grain:** 1 row = 1 order item

### Columns
| Column | Type | Description | PII / Sensitive |
|--------|------|-------------|-----------------|
| `order_id` | STRING | Primary key. | No |
| `customer_id` | STRING | FK to `dim_customer`. | No |
| `net_amount` | FLOAT | Paid after taxes and discounts. | No |
| `customer_email` | STRING | Purchaser email. | **YES (masked to BI)** |

### Tests
- `order_id`: unique, not_null
- `customer_id`: relationships to `dim_customer`
```
