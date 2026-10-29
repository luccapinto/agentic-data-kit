---
name: plan
description: Draft an implementation plan for a data task — a plan file only, no code.
---

**Context:** ${selection}

# Workflow: /plan

**Usage:** `/plan <what you want to build>`

Produce a written plan before any implementation. This command writes a plan file and stops —
it does not write code.

## Steps

1. **Understand.** Read the relevant parts of the repo. If a key requirement is genuinely
   ambiguous, ask; otherwise state your assumptions.
2. **Map to skills and scripts.** For each part of the work, name the skills it will load and
   the validation scripts it will run (e.g. `pbi-semantic-layer-tmdl` + `run_bpa.py` for a model
   change, `pbi-report-layer-pbir` + `validate_pbir.py` for a report change,
   `dbt-modeling-conventions` for dbt models).
3. **Write the plan** to `docs/PLAN-<slug>.md`, where `<slug>` is 2–3 hyphenated keywords from
   the request. Include:
   - **Goal & scope** (and explicit non-goals).
   - **Task breakdown** with the skills/scripts each task uses.
   - **Dependencies & risks.** For Power BI work, state whether Desktop will be open (Modeling
     MCP + Desktop Bridge) or closed (edit on disk).
   - **Verification checklist** (how we'll know it works — scripts to run, and the independent
     visual review for report changes).
4. **Report** the exact file path created and suggest reviewing it before implementing.
