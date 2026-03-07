---
name: data-documentation
description: Documentation templates and rules for data dictionaries, lineage, metric definitions, and semantic models.
---

# Data Documentation Standards

Data is useless without context. The documentation layer is the bridge between raw tables and business value. Every data artifact must be self-explanatory to an analyst or business user reading it 6 months later.

## 🧠 Core Principles

1. **Definitions Live Close to Code**: A word document on SharePoint dies in a week. Table descriptions, DDL comments, and Power BI semantic properties live forever.
2. **Clarity over Jargon**: The definition of "Active User" must completely encapsulate edge cases without relying on acronyms.
3. **Data Lineage is Mandatory**: Every Gold table must explicitly define its Bronze/Silver upstream dependencies.

---

## 📋 The Metric/Column Definition Template

Whenever documenting a column name, DAX measure, or dashboard metric, enforce this structure:

### `Metric Name` (e.g., `30-Day Churn Rate`)
* **Description**: A plain-English summary. (e.g., "The percentage of users who canceled their active subscription within the trailing 30 calendar days").
* **Mathematical Formula**: The exact calculation logic. `(Canceled Subscriptions / Active Subscriptions at Start of Period) * 100`
* **Exclusions/Filters**: What data is omitted? (e.g., "Excludes enterprise accounts; Excludes internal employees").
* **Owner/Steward**: Who makes the final call if this metric definition requires a change?

---

## 🛠️ Table DDL Documentation

When a Data Engineer creates a table (in Databricks/Snowflake/dbt):

```sql
CREATE TABLE gold.dim_customer (
    customer_id STRING COMMENT 'Unique alphanumeric identifier matching the global Salesforce CRM system.',
    signup_date DATE COMMENT 'The UTC date when the user first successfully completed checkout.',
    is_active BOOLEAN COMMENT 'TRUE if the user has an active billing plan as of the last pipeline run.'
) COMMENT 'Dimensional table containing a unified, deduplicated list of all purchasing customers. Refreshed daily at 02:00 UTC.';
```

### dbt `schema.yml` Standards
In dbt environments, every table pushed to the warehouse must have a minimal `.yml` file accompanying it describing every single column and executing `not_null` and `unique` generic tests on the Primary Key.

---

## ❌ Anti-Patterns

* **The Tautological Definition**: Defining `Customer_ID` as "The ID of the Customer." Explain *which* system generates it and its format.
* **Ghost Dependencies**: A dashboard driven by an undocumented, manually uploaded Excel spreadsheet that sits on someone's desktop.
* **"Will Document Later"**: Code pushed to production without dbt YAML definitions, or DAX measures submitted without the description attribute filled out in the semantic model. Later means never.
