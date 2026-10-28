---
name: validate-pbi
description: Run a full quality check on a PBIP project (BPA via Tabular Editor 2
  or the Python fallback, PBIR validation, structural review).
---

**Context:** ${selection}

# Workflow: /validate-pbi

**Usage:** `/validate-pbi [path/to/project.pbip]`

Answers "is my Power BI project healthy?". If no path is given, use the project in the current
folder; if there are several, ask which one.

## Steps

1. **Locate the project** (`.pbip` + `<Name>.SemanticModel/` + `<Name>.Report/`). If none is
   found, report it and stop.
2. **Make disk current.** If Power BI Desktop has the project open, ask the user to save
   (Ctrl+S). Desktop does not need to be closed — the checks read the files Desktop saved.
3. **Model — BPA** (`pbi-quality-rules`):
   `python3 <pbi-quality-rules>/scripts/run_bpa.py <project> --format json`.
   Record every `error` and `warning` and which engine ran (Tabular Editor 2 or Python fallback).
4. **Report — PBIR** (`pbi-report-layer-pbir`):
   `python3 <pbi-report-layer-pbir>/scripts/validate_pbir.py <project> --format json`.
   Record errors and warnings and whether `powerbi-report-author` or the structural fallback ran.
5. **Structural review** of the TMDL:
   - **Doc coverage:** tables/measures with a `///` description vs. total.
   - **Relationships:** island tables, bidirectional filters, many-to-many joins.
6. **Report** — a short Markdown summary:

```markdown
# Validation Report — <Project>
**Date:** <today> | **BPA engine:** Tabular Editor 2 | **PBIR check:** powerbi-report-author

## Summary
| Area | Errors | Warnings |
|------|--------|----------|
| Model — DAX | 1 | 1 |
| Model — Naming | 0 | 2 |
| Model — Docs | 0 | 2 |
| Report (PBIR) | 0 | 0 |

## Errors (fix before publishing)
- [DAX_EMPTY_EXPRESSION] Measure 'Sales'[Forecast] — empty expression

## Doc coverage
- Tables: 3/4 described (75%) · Measures: 3/4 described (75%)
```

7. **Offer fixes.** Offer to fix every **error** (model fixes through the Modeling MCP when
   Desktop is open, otherwise in TMDL); ask before addressing warnings and missing descriptions.
