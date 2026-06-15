---
name: pbi-semantic-layer-tmdl
description: Edit the Power BI semantic model as code by authoring TMDL files in a PBIP project (offline, Desktop closed). Covers structure, syntax, and post-edit verification.
---

# Skill: pbi-semantic-layer-tmdl

Author and edit the semantic model (tables, columns, measures, relationships, RLS) by writing
**TMDL** files directly. TMDL is the GA, human-readable text format for tabular models — great
diffs, one file per table, fully scriptable.

## Hard precondition
**Power BI Desktop must be CLOSED** before saving. Desktop keeps the model in memory and
overwrites disk on save, so editing live corrupts files or loses work.

## `.SemanticModel` structure
```
<Project>.SemanticModel/
  definition.pbism          ← pointer (do not hand-edit)
  definition/
    model.tmdl              ← model-level definition, lists tables
    database.tmdl           ← compatibility level / annotations
    tables/<Table>.tmdl     ← ONE table per file (golden rule)
    relationships.tmdl      ← all relationships
    expressions.tmdl        ← shared M expressions / parameters
    cultures/               ← translations
    roles.tmdl              ← RLS
  .pbi/                     ← local cache/settings — NEVER edit (localSettings.json, cache.abf)
```
Edit `.tmdl` files only. One table per file — never define every table inside `model.tmdl`.

## TMDL syntax reference
```tmdl
table 'Sales'
    description: "Primary sales fact."

    measure 'Total Sales' = SUM(Sales[Amount])
        formatString: "#,##0.00"
        displayFolder: "Financials"
        description: "Sum of sales amount."

    column 'Amount'
        dataType: decimal
        sourceColumn: BaseAmount
```
```tmdl
relationship Sales_Date
    fromColumn: Sales.DateId
    toColumn: Date.DateId
    fromCardinality: many
    toCardinality: one
```

**Serialization rules:** keep functional properties (`dataType`, `sourceColumn`) before
cosmetic ones; match the file's existing indentation; for multi-line DAX, break with `\` at the
end of the line.

## Tooling
- **Tabular Editor 2 (free)** can open the `.SemanticModel` folder, validate, batch-edit, and
  re-serialize clean TMDL. Use it to sanity-check non-trivial edits.
- **Optional:** Microsoft's `powerbi-modeling-mcp` (preview) edits the same PBIP/TMDL files and
  is handy for bulk operations. File editing remains the default, accessible path.

## Post-edit verification
1. Ask the user to open the `.pbip` in Desktop and wait for the field list to populate.
2. **View → Diagnostics** — report any error/warning shown.
3. For each new/changed measure, drop it on a **Card** and confirm the value (no red error icon).
4. On error: re-read the edited TMDL, find the syntax/reference issue, propose the fix.
5. Run the `pbi-quality-rules` skill (BPA) after significant changes.
