# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [5.0.0] - 2026-10-28

Power BI becomes the flagship, developed with Power BI Desktop open.

### Breaking

- **The 5 agents are removed:** `data-engineer`, `analytics-engineer`, `data-scientist`,
  `powerbi-developer` and `presentation-designer`. An agent now exists only if it imposes
  something the model cannot impose on itself (restricted tools, independent review, a different
  model, or an automatic trigger). Domain knowledge lives in skills; generic knowledge was dropped.
- **No more agent routing or handoffs.** Skills self-activate; the always-on rules no longer
  tell the assistant to route to a specialist.
- **Desktop-open is the default Power BI workflow** (Modeling MCP for the model, Desktop Bridge for
  the report). The previous "Desktop must be closed" flow remains documented as an alternative.
- Counts are now **1 agent · 9 skills · 3 workflows · 5 targets**.

### Added

- `pbi-visual-reviewer` agent (tools: Read, Grep, Glob): independent review of report
  screenshots against the spec and the PBIR folder, with PASS/FAIL per page and per visual.
- `dbt-modeling-conventions` skill (the org conventions of the removed analytics-engineer agent).
- Validation scripts (Python 3.9+, stdlib only; `--format text|json`; exit 0/1/2):
  `run_bpa.py`, `bpa_fallback.py` and `validate_pbir.py`.
- References: `pbi-report-layer-pbir/references/desktop-bridge.md` and
  `pbi-semantic-layer-tmdl/references/modeling-mcp.md`.
- `cursor` install target, now including `.cursor/skills`.
- `python3 scripts/sync_agents.py --check` plus the CI workflow `sync-check.yml`; `npm prepack`
  runs the sync before publishing.
- `npm test` with Python `unittest` and a fixture PBIP at `tests/fixtures/SalesSample/`.
- `THIRD_PARTY_NOTICES.md`.
- This changelog.

### Changed

- `pbi-semantic-layer-tmdl`, `pbi-report-layer-pbir` and `pbi-quality-rules` rewritten around the
  Desktop-open loop and the scripts above.
- `rules.md` no longer contains agent routing.
- Workflows updated: `/plan` lists skills and scripts per task instead of agents;
  `/validate-pbi` runs the scripts.
- `building-html-presentations` absorbs the data-storytelling rules of the removed
  presentation-designer agent; `creating-agents-and-skills` now enforces the agent-survival rule.
- Copilot agents get `tools` mapped from Claude names (Read→read, Grep/Glob→search,
  Edit/Write→edit, Bash→execute); OpenCode agents get a `permission` block.
- The sync script is written in English.
- README, ARCHITECTURE, AGENT_FLOW and CONTRIBUTING rewritten for v5.
- Package `files` whitelist: only what `init` installs is published (no tests, CI files or
  cover image).
- `init --target copilot` installs only the kit's entries in `.github/` (agents, skills, prompts,
  `copilot-instructions.md`) and no longer refuses to run because a `.github/` folder exists.
- `init --target antigravity` also installs `scripts/sync_agents.py`.
- The CLI banner counts agents/skills/workflows from the package instead of hard-coding them.

### Fixed

- `init --target opencode` now installs the root `AGENTS.md`; it previously looked for a removed
  `.opencode/AGENTS.md`.
- `init --target copilot` copied the whole `.github/` folder, which would have included the
  kit's own CI workflow.

Earlier versions are in the git history.
