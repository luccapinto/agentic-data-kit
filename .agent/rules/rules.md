---
trigger: always_on
---

# Agentic Data Kit — Operating Rules

Global behavior for AI assistants working in this repository. Keep it short on purpose:
every token here competes for the model's attention, so this file holds only high-signal,
data-specific rules — not things a capable model already does well.

## Language

- Write all code, identifiers, and artifacts in English.
- **Respond to the user in the language they write in** (Portuguese in, Portuguese out).

## How to work

1. **Route to a specialist.** Pick the agent whose domain fits the request and briefly say
   which one you're applying (e.g. "Applying @data-engineer"). For cross-domain requests,
   split the work across agents and merge the results.
2. **Skills activate themselves.** Every skill declares when it applies in its `description`.
   When a request matches it — "document this", "edit this Power BI model" — load that
   `SKILL.md` on demand, **with or without an agent involved**. Skills do not require an owning
   agent; the `skills:` field on an agent is only a hint. Don't preload every file in a folder.
3. **Creating or changing an agent/skill/workflow?** Load the `creating-agents-and-skills`
   skill first — it decides whether to build an agent, a skill, or nothing, and keeps every
   installed tool folder (`.agent`, `.claude`, `.github`, `.opencode`) in sync.
4. **Clarify only when genuinely blocked.** If the request is ambiguous enough that you'd
   likely build the wrong thing, ask. Otherwise state your assumptions and proceed.

## Data engineering principles (always apply)

- **Idempotency:** Pipelines must be safely re-runnable. Prefer `MERGE`/`OVERWRITE` over
  blind `INSERT`. Re-running a window yields the same result.
- **Write-Audit-Publish:** Write to staging → run quality checks → publish only if they pass.
- **Check downstream impact** before changing any schema, contract, or shared model.
- **Never hardcode secrets or PII.** Use secret managers; mask PII at the Silver layer.

## Data debugging quick reference

| Symptom | Likely cause | First check |
|---|---|---|
| Silent row drops | Schema/type mismatch or silent cast | DDL and explicit `CAST` |
| Duplicates in Gold | Non-idempotent Silver | `MERGE` keys / upsert logic |
| Slow dashboard | High-cardinality join in DAX | Pre-aggregate upstream |
| Pipeline OOM | Partition skew | Partition keys / data skew |
| PII in BI | Masking missed Bronze→Silver | PII masking policies |
