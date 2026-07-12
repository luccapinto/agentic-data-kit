---
name: plan
description: Draft an implementation plan for a data task — a plan file only, no code.
---

# Workflow: /plan

**Usage:** `/plan <what you want to build>`

Produce a written plan before any implementation. This command writes a plan file and stops —
it does not write code.

## Steps

1. **Understand.** Read the relevant parts of the repo. If a key requirement is genuinely
   ambiguous, ask; otherwise state your assumptions.
2. **Route.** Identify which agent(s) own each part of the work (e.g. `data-engineer` for the
   pipeline, `analytics-engineer` for the model, `powerbi-developer` for the dashboard).
3. **Write the plan** to `docs/PLAN-<slug>.md`, where `<slug>` is 2–3 hyphenated keywords from
   the request. Include:
   - **Goal & scope** (and explicit non-goals).
   - **Task breakdown** with the responsible agent per task.
   - **Dependencies & risks.**
   - **Verification checklist** (how we'll know it works).
4. **Report** the exact file path created and suggest reviewing it before implementing.
