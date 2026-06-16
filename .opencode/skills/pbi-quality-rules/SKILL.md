---
name: pbi-quality-rules
description: Validate a Power BI semantic model with the real Best Practice Analyzer (BPA) via the free Tabular Editor 2 CLI, using a shareable BPA rules file.
---

# Skill: pbi-quality-rules

Run the **Best Practice Analyzer (BPA)** — the industry-standard model linter — against a PBIP
semantic model. This skill uses the *real* BPA engine from **Tabular Editor 2 (free, open
source)** instead of a homegrown checker, so results match what Power BI developers expect and
the rules are portable.

## Rule set
`bpa-rules.json` (next to this file) holds the team's BPA rules in Tabular Editor's native
format (`ID`, `Name`, `Category`, `Severity`, `Scope`, `Expression` in Dynamic LINQ over the
TOM). Severity: `3` = error, `2` = warning, `1` = info. Edit this file to add or tune rules;
it loads directly into Tabular Editor's BPA UI too.

## Primary path — Tabular Editor 2 CLI (recommended)
Requires Tabular Editor 2 (free). Desktop should be closed so disk reflects the latest state.

```bash
# Windows (TabularEditor.exe on PATH). Point at the .SemanticModel folder (TMDL) or model.bim.
TabularEditor.exe "Sales.SemanticModel" -A ".agent/skills/pbi-quality-rules/bpa-rules.json" -V
```

- `-A <rulesfile>` runs the BPA with the given rules; `-V` writes violations to the console
  (and sets a non-zero exit code on error-severity hits — useful in CI).
- The cross-platform `te` CLI (preview) accepts the same rules file if installed instead.

Parse the console output, then present **errors and warnings only** (omit info unless asked).

## Fallback — no Tabular Editor installed
The kit stays usable without the tool. Parse the TMDL files directly and evaluate the same
rules by hand: for each rule, read its `Scope` and `Expression` from `bpa-rules.json` and apply
the equivalent check to the parsed objects (measures, tables, columns, relationships). This is
less robust than the real BPA — say so, and recommend installing Tabular Editor 2 for accuracy.

## Agent flow
1. Run after large model edits / refactors, or on demand.
2. Show errors first; for each `error`, offer an immediate fix. For `warning`, suggest but
   don't force. Group by category so the report is scannable.
