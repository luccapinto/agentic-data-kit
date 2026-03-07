---
name: pbip-report-hacking
description: Techniques and rules for programmatically modifying Power BI report files (.pbir, report.json) within a PBIP project. Covers theme manipulation, custom visual injection, and layout automation.
---

# PBIP Report Hacking

This skill focuses on manipulating the visual layer of a Power BI project (`.pbip`) by directly editing the underlying JSON/PBIR files.

## ⚠️ High-Risk Activity Warning

Editing `report.json` or `.pbir` files directly bypasses the Power BI Desktop validation layer. A single missing comma or bracket will corrupt the report and prevent it from opening. 

**Rule #1: Always ensure you have a clean git state before hacking the report layer.**

## 🧠 Core Hacking Concepts

### 1. The PBIR Structure
The new PBIR (Power BI Report) format uses individual JSON files for each page, visual, and bookmark. Unlike the legacy `report.json` (which was a monolithic file), PBIR is modular and much safer to version control and edit.

- `\Report\pages\` -> Contains folders for each page.
- `\Report\pages\{page_id}\visuals\` -> Contains individual `.json` files for each visual.
- `\Report\bookmarks\` -> Contains bookmark states.

### 2. Custom Visual Injection (SVG/HTML)
You can build highly custom visuals (sparklines, dynamic indicators, HTML tables) without custom visual files (`.pbiviz`) by injecting SVG or HTML directly into DAX measures and rendering them in native Table or Matrix visuals.

**Workflow:**
1.  Write a DAX measure that outputs a valid SVG string (e.g., `"<svg width='100' height='20'><rect width='" & [Value] & "' height='20' fill='red'/></svg>"`).
2.  Ensure the column/measure data category is set to 'Image URL' in the semantic model (TMDL).
3.  Place the measure in a Table or Matrix visual.

### 3. Theme & Color Automation
Themes are defined in `\Report\StaticResources\SharedResources\BaseThemes\`.
- You can programmatically update the hex codes in the `theme.json` file to instantly roll out a rebranding across the entire report.
- Visual-specific formatting (e.g., overriding the theme color for a specific bar chart) is found within the visual's JSON file under the `objects` property.

## 🛠️ Execution Protocol

When asked to "hack" or edit a report visual programmatically:

1.  **Locate the Target:** If using the PBIR format, navigate to `\Report\pages\` and find the correct page and visual JSON file. If using the legacy `.pbip` format, carefully parse `report.json`.
2.  **Understand the Schema:** Power BI JSON schemas are deeply nested. Look for paths like `sections -> visualContainers -> config -> singleVisual -> objects`.
3.  **Make the Edit:** Apply the necessary JSON changes (e.g., changing a hex color, altering coordinates, or modifying a property).
4.  **Validate:** Ensure the resulting JSON is strictly valid. No trailing commas, correct quote escaping.
5.  **Test:** The user will need to open the `.pbip` file in Power BI Desktop to confirm the changes rendered correctly and didn't corrupt the file.

## ❌ Pitfalls to Avoid

-   **Modifying Data Bindings:** Be extremely careful when editing the `dataTransforms` or `query` sections of a visual's JSON. A mismatch between the visual's query and the Semantic Model will break the visual. Usually, it's safer to let Power BI Desktop handle data binding and only hack the formatting/properties.
-   **Invalid Escaping:** When injecting JSON strings within JSON strings (often seen in the `config` property), be meticulous with your string escaping (`\"`).
-   **Legacy vs. PBIR:** Always verify if the project is using the legacy `report.json` or the new `PBIR` format before attempting edits. The directory structure and file contents are completely different.
