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

## Deterministic hook — measure metadata (optional, Claude Code)
For an *always-on* guardrail (not dependent on the model remembering), `scripts/` ships a
deterministic check that flags any **measure** missing `Description`, `DisplayFolder`, or
`FormatString` — the same enforcement as data-goblin's hooks.

```bash
# Manual / CI — pass files or the .SemanticModel folder:
python .claude/skills/pbi-quality-rules/scripts/check_tmdl_metadata.py "Sales.SemanticModel"
```

- `scripts/hooks-config.yaml` toggles it: `enabled`, `mode` (`warn` reports only / `block`
  stops the save), and per-field requirements. Default is **warn**.
- **Wire it as a Claude Code hook** so it fires automatically on every TMDL save: the kit's
  `scripts/sync_agents.py` writes a `PostToolUse` entry into `.claude/settings.json` that runs
  this script on `Edit`/`Write` to `*.tmdl`. In `block` mode a non-zero exit stops the tool and
  feeds the missing-metadata list back to the model.
- Hooks are Claude-Code-specific; on other tools run the script in CI or on demand — the rule
  itself stays portable.

This complements the BPA: the hook is a fast pre-flight on save; the BPA is the full audit.

## Agent flow
1. Run after large model edits / refactors, or on demand.
2. Show errors first; for each `error`, offer an immediate fix. For `warning`, suggest but
   don't force. Group by category so the report is scannable.
