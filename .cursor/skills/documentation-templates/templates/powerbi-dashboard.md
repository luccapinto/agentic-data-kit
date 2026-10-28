# Template: Power BI Dashboard Catalog

Generate a `DASHBOARD_DOC.md` for a PBIP project by parsing its files — a living catalog of the
model and report. Driven by the `/document-dashboard` workflow.

## Parsing
- **TMDL** (`tables/*.tmdl`, `relationships.tmdl`): indented text — extract names, data types,
  `description`, DAX `expressions`, and relationships via block parsing (regex / line logic).
- **PBIR** (`pages/*/visuals/*/visual.json`): plain JSON — iterate `projections` for fields/values.
- Objects without a `description` show `[no description]`; custom visuals without a title are
  identified by GUID. Skip schema mismatches gracefully.

## Output structure (`DASHBOARD_DOC.md`)

**1. Overview** — title, generation date, and counts (tables, measures, pages, visuals).

**2. Data dictionary** — per `tables/<Table>.tmdl`:
```markdown
## Table: <Name>
> <description>

| Column | Type | Hidden | Description |
|--------|------|--------|-------------|
| Id | int64 | Yes | Primary key |
```

**3. Measure inventory** — per table, with the DAX in a fenced ```dax block:
```markdown
### [Measure] <Name>
**Folder:** <displayFolder> | **Format:** <formatString>
**Description:** <description or "[no description]">
```

**4. Visual → measure/column map** — per page, from `visual.json` `projections`:
```markdown
## Page: <displayName>
### Visual: <title> (<visualType>)
- **X:** Table[Column]   - **Y:** [Measure]
```

**5. Relationships** — from `relationships.tmdl`: a table of From, To, Cardinality, Direction.
