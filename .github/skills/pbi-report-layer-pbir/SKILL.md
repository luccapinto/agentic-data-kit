---
name: pbi-report-layer-pbir
description: Edit the Power BI report layer as code — pages, visuals, bookmarks, and themes — by writing PBIR JSON files in a PBIP project (offline, Desktop closed).
---

# Skill: pbi-report-layer-pbir

The report layer (`.Report/`) is **PBIR** — report metadata decomposed into per-page and
per-visual JSON files, each with a public JSON schema. PBIR is becoming the default report
format (rolling out across Service and Desktop through 2026), and it is explicitly designed to
be edited by tools other than Power BI.

## Hard precondition
**Power BI Desktop must be CLOSED** while editing these `.json` files — live edits corrupt or
get overwritten by autosave.

## `.Report` structure (PBIR)
```
<Project>.Report/
  definition.pbir                        ← pointer (model binding)
  definition/
    report.json                          ← master metadata incl. themeCollection
    pages/
      <pageId>/
        page.json                        ← canvas size, background, displayName
        visuals/<visualId>/visual.json   ← one visual per file
  StaticResources/
    RegisteredResources/<id>/<id>.json   ← custom themes (create new themes here)
    SharedResources/BaseThemes/          ← Microsoft base themes — NEVER edit
```

## Navigating
- **Pages:** scan `definition/pages/`; read each `page.json` `displayName` (the user-facing name).
- **Visuals:** files sit under GUID folders. To find "the bar chart", grep `visual.json` for
  `"visualType": "barChart"`.

## Visual anatomy (`visual.json`)
```json
{
  "name": "<new GUID if creating>",
  "position": { "x": 10, "y": 20, "width": 400, "height": 300, "tabOrder": 1 },
  "visual": {
    "visualType": "barChart",
    "query": { "queryState": { "Category": { "projections": [] }, "Y": { "projections": [] } } }
  }
}
```
Positioning is a pixel grid (x=0, y=0 top-left). Generate fresh GUIDs for any new component
(`[System.Guid]::NewGuid()` on Windows, or any UUID generator).

## Themes
1. Create the theme JSON under `StaticResources/RegisteredResources/<guid>/<guid>.json`.
2. Register that `<guid>` in `report.json`'s `themeCollection`.
3. Define ≥ 8 `dataColors`. To standardize fonts globally, use the wildcard `visualStyles`:
   ```json
   "visualStyles": { "*": { "*": { "fontSize": [{ "value": 11 }], "fontFamily": [{ "value": "Segoe UI" }] } } }
   ```

## Cautions
- The visual schema evolves with Desktop releases; old keys may be ignored on newer versions.
- Validate JSON against the PBIR schema where possible. Always have the user commit (`git add`)
  before large UI refactors and test by opening the file in Desktop.
