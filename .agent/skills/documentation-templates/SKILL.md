---
name: documentation-templates
description: Documentation templates and structure guidelines for Data Engineering. Runbooks, Semantic Layers, Data Dictionaries, and AI-friendly documentation.
allowed-tools: Read, Glob, Grep
---

# Documentation Templates (Data Engineering)

> Templates and structure guidelines for common Data Team documentation types.

---

## 1. Pipeline Runbook Template

Every critical pipeline must have a runbook for when it fails at 3 AM.

### Essential Sections

| Section | Purpose |
|---------|---------|
| **Description** | What business process relies on this data? |
| **SLAs** | When must this pipeline be finished by? |
| **Upstream Dependencies** | What sources feed this? (APIs, Databases, etc.) |
| **Downstream Consumers** | Who is impacted if this fails? (e.g., Finance Dashboard) |
| **Common Failures & Fixes** | How to troubleshoot known issues. |
| **Escalation Contacts** | Who to call if the on-call engineer can't fix it. |

### Runbook Template

```markdown
# Pipeline: [Pipeline Name]

**Business Criticality:** High | Medium | Low  
**SLA:** Must complete by 08:00 AM EST  
**Schedule:** Daily at 02:00 AM EST

## Description
Extracts daily sales from Stripe, transforms currency, and loads to the `fct_sales` table.

## Dependencies
- Upstream: Stripe API (Sales), Exchange Rate API
- Downstream: Power BI Sales Executive Dashboard

## Common Failures
1. **API Rate Limit Exceeded (Stripe)**
   - *Symptom:* HTTP 429 errors in logs.
   - *Fix:* Pipeline has auto-retries. If it completely fails, manually clear the task in Airflow and re-trigger after 15 mins.
2. **Missing Exchange Rates**
   - *Symptom:* `null_value` test fails in dbt.
   - *Fix:* Check if the Exchange Rate API changed its payload format.

## Escalation
- Primary: @DataEngineerName
- Secondary: @DataLeadName
```

---

## 2. Table / Model Documentation (Data Dictionary)

Use this format primarily inside `schema.yml` files (dbt) or specific Markdown registry files.

### Template

```markdown
# Table: [schema_name].[table_name]

**Description:** Contains one row per completed order. Contains net amounts and applied discounts.

**Grain:** 1 Row = 1 Order Item

### Columns

| Column Name | Type | Description | PII / Sensitive |
|-------------|------|-------------|-----------------|
| `order_id` | STRING | Primary Key. | No |
| `customer_id` | STRING | Foreign Key to `dim_customer`. | No |
| `net_amount` | FLOAT | Amount paid after taxes and discounts. | No |
| `customer_email` | STRING | Email of the purchaser. | **YES (Masked to PBI)** |

### Tests Applied
- `order_id`: unique, not_null
- `customer_id`: relationships to `dim_customer`
```

---

## 3. Semantic Layer (Metric Definition)

When defining a metric for Business Analysts, use a clear framework.

### Template

```markdown
# Metric: Monthly Active Users (MAU)

**Definition:** The number of unique authenticated users who have logged into the platform at least once trailing 30 days.

**Calculation (Pseudo-SQL):**
`COUNT(DISTINCT user_id) WHERE login_date >= CURRENT_DATE - 30`

**Grain/Dimensions Available:**
- Country
- Device Type
- Subscription Tier

**Source Table:** `gold.fct_user_logins`

**Owner:** Product Analytics Team
```

---

## 4. Architecture Decision Record (ADR)

Use this when making big architectural choices (e.g., moving from Airflow to Dagster, or choosing Delta over Iceberg).

```markdown
# ADR-001: [Title]

## Status
Proposed / Accepted / Rejected / Deprecated

## Context
Why are we making this decision? (e.g., Databricks costs are too high for simple transformations).

## Decision
What did we decide? (e.g., We will use dbt Core on Snowflake for the transform layer).

## Consequences
- **Positive:** Lower compute costs, easier for analysts to write SQL.
- **Negative:** Harder to write complex Machine Learning transformations seamlessly in line with ETL.
```

---

## 5. SQL Commenting Guidelines

| ✅ DO Comment | ❌ Don't Comment |
|-----------|-----------------|
| Complex regex logic (`regexp_replace(..., '(?i)foo', 'bar')`) | Basic SELECT statements |
| Why a specific filter exists (`-- Exclude test accounts created before 2021`) | `LEFT JOIN` mechanics |
| Workarounds for upstream bugs (`-- Coalesce null because source system drops 0s`) | Standard math (`-- Add a and b`) |

---

> **Remember:** Data Documentation rots quickly. Put it as close to the code/schema as possible (e.g., YAML files) rather than isolated Wikis.
