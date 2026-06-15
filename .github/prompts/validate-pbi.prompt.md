---
description: Run a full quality check on a PBIP project (BPA via Tabular Editor 2
  + structural review).
name: validate-pbi
---

**Context:** ${selection}

# Workflow: /validate-pbi

**Usage:** `/validate-pbi [path/to/project.pbip]`

Answers "is my model healthy?" by running the quality checks on a PBIP semantic model. If no
path is given, use the project in the current folder; if there are several, ask which one.

## Steps

1. **Locate the project.** Use `pbi-semantic-layer-tmdl` to confirm a valid PBIP project.
   If none is found, report it and stop.
2. **Run the BPA.** Use `pbi-quality-rules` to run the Best Practice Analyzer (Tabular Editor 2
   CLI, or the TMDL-parsing fallback). Recommend the user close Desktop first so disk is current.
   Record every `error` and `warning`.
3. **Structural review.**
   - **Doc coverage:** tables/measures with a `description` vs. total.
   - **Relationships:** flag island tables (no relationships), bidirectional filters, and
     many-to-many joins.
4. **Report** — a short Markdown summary:

```markdown
# Validation Report — <Project>
**Date:** <today> | **Source:** TMDL files

## Summary
| Category | Errors | Warnings |
|----------|--------|----------|
| Naming   | 0 | 3 |
| DAX      | 1 | 2 |
| Model    | 0 | 1 |
| Docs     | 0 | 8 |

## Errors (fix before publishing)
- [DAX_EMPTY_EXPRESSION] Measure "Turnover %" — empty expression

## Doc coverage
- Tables: 5/7 described (71%) · Measures: 12/20 described (60%)
```

5. **Offer fixes.** Auto-offer to fix all **errors**; ask whether to address **warnings** and
   missing descriptions.
