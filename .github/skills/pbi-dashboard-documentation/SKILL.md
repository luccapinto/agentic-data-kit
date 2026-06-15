---
name: pbi-dashboard-documentation
description: Generate structured Markdown documentation of a Power BI dashboard by reading TMDL and PBIR files (data dictionary, measure inventory, visual-to-measure map, relationships).
---

# Skill: pbi-dashboard-documentation

Generate a `DASHBOARD_DOC.md` for a PBIP project by parsing its files — a living catalog of
the model and report. Used by the `/document-dashboard` workflow.

## Document structure

**1. Overview** — title, generation date, and counts (tables, measures, pages, visuals).

**2. Data dictionary** — for each `tables/<Table>.tmdl`:
```markdown
## Table: <Name>
> <description from the `description` property>

| Column | Type | Hidden | Description |
|--------|------|--------|-------------|
| Id | int64 | Yes | Primary key |
```

**3. Measure inventory** — per table:
```markdown
### [Measure] <Name>
**Folder:** <displayFolder> | **Format:** <formatString>
**Description:** <description or "[no description]">
```
Followed by the DAX expression in a ```dax fenced block.

**4. Visual → measure/column map** — from `pages/*/visuals/*/visual.json`, read `projections`:
```markdown
## Page: <displayName>
### Visual: <title> (<visualType>)
- **X:** Table[Column]   - **Y:** [Measure]
```

**5. Relationships** — from `relationships.tmdl`: a table of From, To, Cardinality, Direction.

## Parsing notes
- **TMDL:** indented text — extract via block parsing (regex / line logic).
- **PBIR:** plain JSON — load and iterate `projections` for fields/values.
- Objects without a `description` show `[no description]`; suggest filling them via TMDL.
- Third-party/custom visuals without a title are identified by GUID; skip schema mismatches gracefully.
