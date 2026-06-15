---
description: Auto-generate complete Markdown documentation for a PBIP project.
name: document-dashboard
---

**Context:** ${selection}

# Workflow: /document-dashboard

**Usage:** `/document-dashboard [path/to/project.pbip] [--output path/to/doc.md]`

Builds a data catalog for a Power BI model by parsing the semantic model and report, removing
the need to hand-maintain dashboard documentation. Default output: `DASHBOARD_DOC.md` at the
project root.

## Steps

1. **Inventory.** Use `pbi-semantic-layer-tmdl` to confirm the PBIP project and count tables,
   measures, relationships, pages, and visuals.
2. **Parse both layers.**
   - **Semantic model (`.tmdl`):** names, data types, `description`, DAX `expressions`, and
     relationships from `relationships.tmdl`.
   - **Report (`.json`):** scan `pages/*/visuals/*/visual.json` for visual type, title, and the
     fields/measures used (`projections`).
3. **Generate.** Use the `pbi-dashboard-documentation` skill to compile a Markdown doc with at
   least: overview, data dictionary, measure inventory (with DAX blocks), visual→measure→column
   map per page, and a relationships table.
4. **Deliver.** Save `DASHBOARD_DOC.md`, then report its location and the documentation coverage
   (% of tables and measures with descriptions). If coverage < 80%, suggest running
   `/validate-pbi` or offer to fill the gaps via TMDL.
