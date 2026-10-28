---
# DESIGN.md — visual identity for AI agents (Google Labs spec, Apache-2.0).
# Place this file in your PROJECT ROOT. Tokens below are NORMATIVE; the prose explains intent.
# Token references use braces, e.g. {colors.primary}. Replace every value with your brand's.
version: alpha
name: Acme Analytics
description: Brand tokens for Acme's data presentations, docs, and dashboards.

colors:
  primary:    "#1A1C1E"
  secondary:  "#6C7278"
  accent:     "#2563EB"
  background: "#FFFFFF"
  surface:    "#F5F6F8"
  text:       "#1A1C1E"
  muted:      "#6C7278"
  success:    "#15803D"
  warning:    "#B45309"
  danger:     "#B91C1C"

typography:
  h1:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
  h2:
    fontFamily: Public Sans
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: system-ui
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: system-ui
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4

spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px

rounded:
  sm: 4px
  md: 8px
  lg: 16px

shadows:
  sm: "0 1px 2px rgba(0,0,0,0.06)"
  md: "0 4px 12px rgba(0,0,0,0.10)"

components:
  button:
    background: "{colors.accent}"
    color: "{colors.background}"
    radius: "{rounded.md}"
  card:
    background: "{colors.surface}"
    radius: "{rounded.lg}"
    shadow: "{shadows.sm}"
---

# Overview

**Acme Analytics** presents data with a calm, trustworthy, modern voice. Generous whitespace,
one accent color used sparingly, and clear typographic hierarchy. Charts and numbers are the
hero — chrome stays quiet.

# Colors

`primary` for headings and key text; `accent` ({colors.accent}) only for emphasis and one CTA
per view. `muted` for sources/captions. Semantic colors (`success`/`warning`/`danger`) only for
status — never decoration.

# Typography

Headings in **Public Sans**; body in the system stack for speed and legibility. Follow the type
scale ({typography.h1} → {typography.caption}); don't introduce intermediate sizes.

# Layout & Spacing

Use the spacing scale ({spacing.xs}–{spacing.xl}) — no arbitrary margins. Default page rhythm is
`lg`. Keep one idea per section; let content breathe.

# Elevation & Depth

Two shadow levels only: `sm` for resting cards, `md` for overlays/popovers. Avoid heavy drop
shadows; prefer flat surfaces separated by `surface` vs `background`.

# Shapes

Rounded corners from the `rounded` scale. Cards use `lg`; buttons/inputs use `md`. No sharp 0px
corners except full-bleed media.

# Components

- **Button** — accent background, background-color text, `md` radius. One primary per view.
- **Card** — `surface` background, `lg` radius, `sm` shadow, `md` inner padding.
- **Table** — caption-size source line beneath; right-align numerics.

# Do's and Don'ts

- ✅ Lead slides/sections with the insight; keep the accent rare.
- ✅ Label every chart with source, grain, date range, filters.
- ❌ Don't add off-palette colors or extra fonts.
- ❌ Don't use semantic colors decoratively.
- ❌ Don't stretch logos or place text on low-contrast backgrounds.
