# Agent Flow

How a request moves through the kit.

```text
User request
   │
   ▼
Skills self-activate  ──►  a SKILL.md loads only when its description matches the task
   │
   ▼
Execute  ───────────────►  Power BI loop with Desktop open:
   │                         model/measures → Modeling MCP (live) → user saves in Desktop
   │                         visuals → edit PBIR → validate_pbir.py → preview --reload
   │                         → --screenshot --all-pages
   │                       other work: dbt models, docs, decks, PPTX
   ▼
Validate (scripts)  ────►  run_bpa.py (BPA, TE2 or Python fallback) · validate_pbir.py
   │
   ▼
Independent review  ────►  pbi-visual-reviewer: fresh context, screenshots + spec + PBIR only,
   │                       PASS/FAIL per page and per visual; FAIL → back to Execute
   ▼
Deliver  ───────────────►  present changes + reasoning, in the user's language
```

Before `--reload`, confirm Desktop has no unsaved changes
(`powerbi-report-author preview <folder> --host desktop --status` → `details.hasUnsavedChanges`
is `false`): reload discards them, and it only covers the report — model changes go through the
Modeling MCP. Without Desktop Bridge (older Desktop, CI), use the Desktop-closed path: edit
TMDL/PBIR on disk, validate with the scripts, reopen Desktop.

Where subagents are unavailable (Cursor, Antigravity), run the review in a fresh chat given only
the screenshots, the spec and the PBIR folder.

## Principles

- **Less is more** — lean instructions keep the model focused; we don't restate what it knows.
- **Clarify only when genuinely blocked** — otherwise state assumptions and proceed.
- **Check downstream impact** before changing schemas, contracts, or shared models.
- **Never self-review** — validation is scripts; visual review is an independent agent.

**Agents:** 1 · **Skills:** 9 · **Workflows:** 3
