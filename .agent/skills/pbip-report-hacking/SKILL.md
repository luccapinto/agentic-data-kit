---
name: pbip-report-hacking
description: Techniques and rules for programmatically modifying Power BI report files (.pbir, report.json) within a PBIP project. Covers PBIR format, theme manipulation, custom visual injection, and layout automation.
---

# PBIP Report Hacking

This skill focuses on manipulating the **visual layer** of a Power BI `.pbip` project by directly editing the underlying JSON files in the PBIR format.

> **Official Docs:** [PBIP Report folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report) | [JSON Schemas](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition)

## ⚠️ High-Risk Activity Warning

Editing PBIR files directly bypasses the Power BI Desktop validation layer. An invalid JSON property or missing key can **block the report from opening**.

**Rule #1: Always have a clean git state (commit your work) before editing any PBIR file.**

---

## 🏗️ PBIR Folder Structure

The PBIR format stores each page, visual, and bookmark as individual JSON files:

```
{ProjectName}.Report/
├── definition.pbir               # Core settings + semantic model reference
├── .pbi/
│   └── localSettings.json        # LOCAL ONLY — add to .gitignore
├── CustomVisuals/                # Private .pbiviz custom visual files
├── RegisteredResources/          # Custom themes (.json), images, and resource files
│   └── {ThemeName}.json          # ← EDIT THIS to change the report theme
└── definition/
    ├── report.json               # Report-level config (theme, canvas settings, filters)
    ├── reportExtensions.json     # Report extensions (e.g., Copilot annotations)
    ├── version.json              # PBIR format version
    ├── bookmarks/
    │   ├── bookmarks.json        # Bookmark ordering metadata
    │   └── {bookmarkName}.bookmark.json  # Individual bookmark state
    └── pages/
        ├── pages.json            # Page ordering metadata
        └── {pageName}/
            ├── page.json         # Page layout, filters, background
            └── visuals/
                └── {visualName}/
                    ├── visual.json       # Visual definition, config, data bindings
                    └── mobile.json      # Mobile layout override (optional)
```

> ⚠️ **Naming convention:** Page/visual/bookmark folder names must consist **only** of word characters (letters, digits, underscores) or hyphens. Invalid names are silently ignored by Power BI Desktop.

---

## 🧠 Core Concepts

### 1. PBIR vs Legacy `report.json`

| Feature | Legacy (`report.json`) | PBIR (`definition\` folder) |
|---------|------------------------|------------------------------|
| File structure | Single monolithic JSON | One file per object |
| Git diffs | Massive, hard to review | Clean, per-visual diffs |
| External editing | Risky (entire report in one file) | Safer (isolated scope per file) |
| Schema support | No | Yes — IntelliSense in VS Code |

> Check `definition.pbir` to see the report format version. If `"version"` is `"4.0"`, it supports PBIR.

### 2. Finding Object Names

Every page, visual, and bookmark has a unique 20-character name (e.g., `90c2e07d8e84e7d5c026`). To find the name of a specific object:
1. In Power BI Desktop: **File → Options → Report settings → Report objects** → enable "Copy object names when right clicking".
2. Right-click on any page/visual/bookmark → **Copy object name**.
3. Use that name to locate the file in the PBIR folder.

### 3. JSON Schemas (IntelliSense)

Every PBIR JSON file has a `$schema` declaration at the top. Open PBIR files in **VS Code** to get built-in validation and IntelliSense:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.0.0/schema.json",
  ...
}
```

All schemas are public: [github.com/microsoft/json-schemas](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition)

### 4. Annotations (First-Class Citizens)

PBIR supports `annotations` at the **visual**, **page**, and **report** level. Power BI Desktop ignores them, but scripts and external tools can read/write them:

```json
{
  "$schema": "...",
  "themeCollection": { ... },
  "annotations": [
    { "name": "defaultPage", "value": "c2d9b4b1487b2eb30e98" },
    { "name": "generated_by", "value": "agentic-data-kit" }
  ]
}
```

Use annotations to tag AI-generated visuals, store pipeline metadata, or mark audit timestamps.

---

## 🎨 Customization Patterns

### 1. Theme & Color Automation

Themes in PBIR are stored in `RegisteredResources\{ThemeName}.json`. You can edit hex codes, font families, and color palettes programmatically and the changes apply across the entire report:

```json
{
  "name": "CorpTheme",
  "dataColors": ["#1A73E8", "#34A853", "#EA4335", "#FBBC04"],
  "background": "#F8F9FA",
  "foreground": "#202124",
  "textClasses": {
    "title": { "fontFace": "Segoe UI", "fontSize": 16, "fontWeight": "bold" }
  }
}
```

The active theme is referenced in `definition\report.json` under `themeCollection.baseTheme`. Visual-specific theme overrides live in each visual's `visual.json` under the `objects` property.

> ⚠️ **Every resource file in `RegisteredResources\` must already have a corresponding entry in `report.json`** (registered during a previous Power BI Desktop session). You cannot add net-new theme files purely through file system edits.

### 2. Custom Visual Injection (SVG/HTML)

You can build custom visuals without `.pbiviz` files by injecting SVG or HTML strings via DAX measures rendered in Table/Matrix visuals.

**Workflow:**
1. Write a DAX measure that outputs a valid SVG string:
   ```dax
   KPI Sparkline = 
       "<svg width='120' height='30'><rect x='" & [Valor] & "' width='10' height='30' fill='#1A73E8'/></svg>"
   ```
2. In the Semantic Model (TMDL), set the column's `dataCategory` to `ImageUrl`.
3. Place the measure in a Table or Matrix visual — Power BI renders the SVG natively.

### 3. Visual Layout Editing (`visual.json`)

The `visual.json` file controls the visual's position, size, type, and formatting. Key paths:

```json
{
  "$schema": "...",
  "name": "90c2e07d8e84e7d5c026",
  "position": { "x": 0, "y": 0, "z": 0, "width": 600, "height": 400, "tabOrder": 1000 },
  "visual": {
    "visualType": "barChart",
    "query": { ... },
    "objects": {
      "general": [{ "properties": { "outspace": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FF0000'" } } } } } } }]
    }
  }
}
```

> **Safe to edit:** `position` (size/coordinates), `objects` (formatting properties), `visual.title`.
> **Dangerous to edit:** `query` and `dataTransforms` — mismatch with the Semantic Model will break the visual silently.

---

## 🛠️ Execution Protocol

When asked to edit a report visual programmatically:

1. **Identify the Format:** Check if the report uses PBIR (`definition\` folder exists) or legacy `report.json`. Apply different strategies accordingly.
2. **Copy the Object Name:** In Power BI Desktop, right-click the target visual/page → Copy object name. Use it to find the specific file.
3. **Open in VS Code:** Use the `$schema` IntelliSense to understand available properties before editing.
4. **Make Targeted Edits:** Change only `position`, `objects`, or theme files. Avoid touching `query`/`dataTransforms`.
5. **Validate JSON:** Ensure the JSON is strictly valid — no trailing commas, correctly escaped strings. VS Code schema validation will catch most errors.
6. **Test:** Restart Power BI Desktop (or reload the PBIR file) to confirm changes rendered correctly.

---

## ❌ Error Types & Common Pitfalls

### Blocking Errors (prevent report from opening)
- Invalid JSON syntax (trailing commas, unclosed brackets)
- Missing required schema properties
- Invalid property names/types

### Non-Blocking Errors (auto-fixed by Power BI Desktop, with a warning)
- Invalid `activePageName` reference
- Bookmark referencing visuals that no longer exist

### Common Mistakes

| Mistake | Result |
|---------|--------|
| Editing `query`/`dataTransforms` | Visual breaks silently (data binding mismatch) |
| Invalid folder/file name (e.g., spaces) | Page/visual silently ignored by Power BI Desktop |
| Copying a page folder without copying its visuals | Bookmark state for that page is corrupted |
| Copying a page without updating `pageBinding.name` | Error: `"Values for 'pageBinding.name' must be unique"` |
| Adding a new theme file to `RegisteredResources\` without a prior Desktop registration | Theme file ignored — no effect |
| Escaping strings incorrectly inside nested JSON | Blocking JSON parse error |

---

## 📋 Quick Reference

| Task | File to Edit | Safe? |
|------|-------------|-------|
| Change theme colors globally | `RegisteredResources\{Theme}.json` | ✅ Safe |
| Change visual position/size | `definition\pages\{page}\visuals\{visual}\visual.json` → `position` | ✅ Safe |
| Change visual formatting | `visual.json` → `objects` | ✅ Safe |
| Change page background / filter | `definition\pages\{page}\page.json` | ✅ Safe |
| Add report-level annotation | `definition\report.json` → `annotations` | ✅ Safe |
| Change data bindings | `visual.json` → `query`/`dataTransforms` | ⚠️ High risk |
| Add a brand-new theme file | `RegisteredResources\` + `report.json` registration | ⚠️ Must pre-register |
| Rename visual/page folders | File system rename + update references | ⚠️ Must restart Desktop |
