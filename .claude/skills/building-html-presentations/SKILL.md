---
name: building-html-presentations
description: Use when the user wants to build a presentation, deck, slides, pitch, readout, or interactive report from data work — exploratory analysis, dashboards, business plans, proposals. Covers three as-code formats (reveal.js deck, interactive one-page site, Markdown→PDF via Marp), how to choose between them, and ready-to-edit starters. Default engine is reveal.js.
---

# Skill: building-html-presentations

Build presentations **as code** so they are versionable, diffable, and reproducible. This skill
covers when to use each format and gives starters you copy and fill with real content. Pair it
with `applying-visual-identity` to make the output on-brand.

## Pick the format first

| Output | Use when | Engine | Export |
|---|---|---|---|
| **Slide deck** | Live readout / meeting; linear narrative, fixed canvas | **reveal.js** (default) | HTML, PDF (`?print-pdf`) |
| **Flexible / scrollable deck** | Slides that hold more than one screen and need in-slide scroll + buttons to switch visuals | custom vanilla JS (`flex-deck.html`) | HTML |
| **Interactive site** | Self-serve exploration; one long scrolling page with anchors | single static HTML page (`interactive-site.html`) | HTML |
| **Designed report PDF** | Polished consulting-style document (action titles, exhibits) | HTML print template (`report-pdf.html`) | PDF (print) |
| **Quick handout PDF/PPTX** | Plain Markdown deliverable, no custom design | **Marp** (Markdown → PDF/PPTX) | PDF, PPTX |

Default to **reveal.js**: most mature, pure HTML/CSS (easy theming from `DESIGN.md`), and it
exports to PDF — so one source covers deck + site + print. Reach for **Marp** only when the
deliverable is fundamentally a document (Markdown-only, clean PDF/PPTX, no interactivity).
**Slidev** is a fine choice for fully technical audiences already on Node/Vue — mention it,
don't default to it.

## Workflow
1. **Audience & format.** Exec → fewer slides, takeaway titles, no code. Technical → allow
   detail/appendix. Choose deck vs site vs PDF (table above) and say which.
2. **Outline before slides.** Agree the storyline (5–9 beats) before writing HTML. Lead with
   the conclusion (BLUF), then evidence, then "so what / next".
3. **Apply the brand.** If a `DESIGN.md` exists, load `applying-visual-identity` and map its
   tokens to CSS variables (see that skill). Otherwise use the neutral defaults in the starter.
4. **Build from a starter** (`templates/`), drop in real numbers and charts, keep it
   **self-contained** (works offline; pin CDN versions or vendor the files).
5. **Export** if needed (see the export note below).

## Exporting (incl. PowerPoint)
- **reveal.js → PDF:** open the deck with `?print-pdf` appended, then print → Save as PDF. This is
  the clean, high-fidelity export.
- **reveal.js → PPTX:** there is **no native, editable** path. If a `.pptx` file is required, use
  **Marp** (`marp deck.md --pptx`) — but note each slide becomes an **image** (not editable text).
  A PDF→PPTX converter is equally image-based. For truly editable native PPTX, generate it
  separately (e.g. `python-pptx`); tell the user it's a different workflow, not an HTML export.
- **Marp → PDF / PPTX:** `marp deck.md --pdf` or `--pptx`.
- **Interactive site:** ship the HTML file itself (or host it); it isn't meant for PDF/PPTX.

## Starters (in `templates/`)
- `reveal-deck.html` — a sophisticated, single-file **data-dashboard deck system** (dark theme,
  brand tokens in `:root` mapped from `DESIGN.md`). Ships reusable layout primitives:
  - **Cover** with KPI grid + stat chips + CTA bar; **section dividers**.
  - **2×2 dashboard panels** mixing charts and narrative with colored keyword highlights.
  - **Ranking bars** (CSS, value + ±pp delta, semantic colors); **heatmap matrix** with a
    score-band color scale and metric **toggle pills**; **quote cards** with category tags.
  - **Custom chrome**: zero-padded `01 / 07` counter, top progress bar, section tag, and a
    dots + prev/next nav wired to the reveal.js API.
  - **Charts**: pure-CSS bars for rankings + **ECharts** (pinned) for line/combo charts.
  Copy it, swap the tokens, replace the demo content. Reach for the panel/bar/heatmap classes
  rather than hand-rolling layout each time.
- `flex-deck.html` — a **flexible, scrollable deck** (no framework, no fixed aspect ratio): each
  slide is a full-width sub-page that can be **taller than the screen and scrolls vertically**,
  while ← → moves between slides. Includes **dynamic toggle buttons** that swap the visual in place
  (chart series, and chart ↔ table). Use when a deck slide carries dashboard-density content.
- `interactive-site.html` — a single-file **scrolling report site** (not slides): sticky nav with
  active-link highlight, reading-progress bar, hero + KPI band, scroll-reveal sections, a sticky
  data table, and ECharts (line + donut). Same tokens as the deck. Use for self-serve exploration.
- `report-pdf.html` — a **consulting-style report** (McKinsey/Deloitte feel) built for PDF export:
  print-first A4, light theme, page header/footer chrome, **full-sentence action titles**, numbered
  **Exhibits** with source lines, an executive summary with numbered key findings + a takeaways box.
  Export via Chrome Print → Save as PDF (A4, margins none, background graphics on).
- `marp-deck.md` — Markdown deck for a quick, plain PDF/PPTX deliverable (no custom design).
- `data-story-outline.md` — fill-in narrative skeleton for analyses, EDA, and business plans.

All HTML starters use a generic **sales review** as demo content — replace it with your own.

## Charts & data
- Embed charts as inline SVG or a small JS lib (e.g. Chart.js / ECharts via pinned CDN). Prefer
  static SVG for PDF targets.
- Every data slide states **source, grain, date range, filters**. Never invent numbers — mark
  unknowns `TODO`.

## Rules
- One idea per slide; the title is the **insight**, not the field name.
- Keep it self-contained and offline-capable; pin versions, don't rely on live network at present time.
- Accessibility: real text (not images of text), sufficient contrast, logical heading order.
