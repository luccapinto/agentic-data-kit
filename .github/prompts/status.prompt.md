---
description: Display agent and project status. Progress tracking and status board.
name: status
---

**Contexto:** {{selection}}

# /status - Show Status

$ARGUMENTS

---

## Task

Show current project and agent status.

### What It Shows

1. **Project Info**
   - Project name and path
   - Tech stack
   - Current features

2. **Feature Status**
| Feature | Status | Notes |
|---------|--------|-------|
| Azure DevOps Pipeline | 🟢 Done | Deployed perfectly |
| Databricks Ingestion | 🟡 85% | Needs incremental loading fix |
| dbt Core Models | 🔴 Blocked | Waiting for API keys |
| Power BI Dashboard | ⚪ Pending | Spec ready |

3. **File Statistics**
   - Files created count
   - Files modified count

4. **Preview Status**
   - Is server running
   - URL
   - Health check

---

## Example Output

```
=== Project Status ===

📁 Project: erp-medallion-pipeline
📂 Path: C:/projects/erp-data
🏷️ Type: databricks-dbt-pipeline
📊 Status: active

## Tech Stack Overview
 - Platform: Databricks
 - Visualization: Power BI

✅ Features (5):
   • bronze-ingestion
   • silver-cleansing
   • gold-marts
   • semantic-model-refresh
   • row-level-security

⏳ Pending (2):
   • data-quality-tests
   • data-governance-docs

📄 Files: 73 created, 12 modified

=== Agent Status ===

## Active Agents
1. `data-engineer` (Data ingestion pipeline)
2. `analytics-engineer` (dbt dimensional modeling)
3. `business-analyst` (Power BI semantic models)

=== Preview ===

🌐 URL: https://app.powerbi.com/groups/workspace-id
💚 Health: Refresh Successful
```

---

## Technical

Status uses these scripts:
- `python .agent/scripts/session_manager.py status`
- `python .agent/scripts/auto_preview.py status`
