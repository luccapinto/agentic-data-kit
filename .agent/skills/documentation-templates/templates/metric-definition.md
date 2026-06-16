# Template: Metric Definition

Define metrics unambiguously so analysts and dashboards agree on the number.

```markdown
# Metric: Monthly Active Users (MAU)

**Definition:** Unique authenticated users who logged in at least once in the trailing 30 days.
**Calculation (pseudo-SQL):** `COUNT(DISTINCT user_id) WHERE login_date >= CURRENT_DATE - 30`
**Grain / dimensions:** Country, Device Type, Subscription Tier
**Source table:** `gold.fct_user_logins`
**Polarity:** UP is good
**Owner:** Product Analytics
```
