# Template: Pipeline Runbook

Every critical pipeline needs a runbook for when it fails at 3 AM. Essential sections:
Description, SLAs, Upstream dependencies, Downstream consumers, Common failures & fixes,
Escalation contacts.

```markdown
# Pipeline: [Name]

**Business Criticality:** High | Medium | Low
**SLA:** Must complete by 08:00 AM
**Schedule:** Daily at 02:00 AM

## Description
Extracts daily sales from Stripe, converts currency, loads to `fct_sales`.

## Dependencies
- Upstream: Stripe API (Sales), Exchange Rate API
- Downstream: Power BI Sales Executive Dashboard

## Common Failures
1. **API rate limit (Stripe)** — *Symptom:* HTTP 429. *Fix:* auto-retries; if it fully fails,
   clear the task and re-trigger after 15 min.
2. **Missing exchange rates** — *Symptom:* `not_null` test fails. *Fix:* check the rate API payload.

## Escalation
- Primary: @DataEngineer  ·  Secondary: @DataLead
```
