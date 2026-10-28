# Architecture

A lean kit for Power BI development with Desktop open: on-demand **skills**, validation
**scripts**, one independent **agent**, and **workflows** — with `.agent/` as the single source
of truth.

## Source of truth & sync

Edit only `.agent/`. `scripts/sync_agents.py` compiles it to every assistant:

```
.agent/        →  .claude/ (+ CLAUDE.md, commands/)                   Claude Code
               →  .github/ (agents, skills, prompts, copilot-instructions.md)   GitHub Copilot
               →  .opencode/ (agents mode: subagent, skills, commands)          OpenCode
               →  .cursor/ (rules/*.mdc, commands/, skills/)                    Cursor
               →  AGENTS.md (root)                                    OpenCode, OpenAI Codex, cross-tool
```

`python3 scripts/sync_agents.py --check` exits 1 if a generated folder is stale; CI
(`.github/workflows/sync-check.yml`) runs it and `npm prepack` regenerates before publishing.

```
.agent/
├── agents/      # 1 independent reviewer (pbi-visual-reviewer)
├── skills/      # 9 on-demand knowledge modules (+ scripts/, references/)
├── workflows/   # 3 slash commands
└── rules/       # always-on rules (rules.md)
```

Targets of `npx @luccapinto/agentic-data-kit init --target <t>`: `antigravity` → `.agent/`,
`copilot` → `.github/`, `claude` → `.claude/`, `opencode` → `.opencode/` + root `AGENTS.md`,
`cursor` → `.cursor/` (rules, commands, skills). The generated folders ship in the package
because `init` installs one folder per tool.

## Agent (1) — the survival rule

An agent exists only if it imposes something the model cannot impose on itself:

1. **Restricted tools** in the frontmatter.
2. **Independent review** — fresh context, no access to the author's reasoning.
3. **A different model.**
4. **An automatic trigger.**

Domain knowledge becomes a skill, or is dropped if the model already knows it.

| Agent | Why it survives | Tools |
|---|---|---|
| `pbi-visual-reviewer` | Independent review (2) with restricted tools (1): judges screenshots + spec + PBIR against a fixed checklist; PASS/FAIL per page and per visual | Read, Grep, Glob |

No handoffs between agents. Where subagents are unavailable (Cursor, Antigravity), the review
runs in a fresh chat given only the screenshots, the spec and the PBIR folder.

## Skills (9)

Skills self-activate by their `description`. They load on demand.

| Skill | Description |
|---|---|
| `pbi-semantic-layer-tmdl` | TMDL semantic models; live changes via the Power BI Modeling MCP (`references/modeling-mcp.md`) |
| `pbi-report-layer-pbir` | PBIR reports, visuals, themes; Desktop Bridge loop (`references/desktop-bridge.md`); `scripts/validate_pbir.py` |
| `pbi-quality-rules` | BPA via Tabular Editor 2 CLI with Python fallback; `scripts/run_bpa.py`, `scripts/bpa_fallback.py` |
| `dbt-modeling-conventions` | dbt CTE structure, `stg_`/`dim_`/`fct_`/`mart_` naming, keys, tests |
| `documentation-templates` | Runbooks, data dictionaries, metric defs, ADRs, Power BI catalog (templates in separate files) |
| `applying-visual-identity` | Apply a brand from `DESIGN.md` (Google Labs spec) to any output |
| `building-html-presentations` | Decks / flex-deck / sites / consulting PDF as code + chart cookbook (reveal.js default) |
| `generating-pptx` | Native, editable PowerPoint via python-pptx (real charts/text, not images) |
| `creating-agents-and-skills` | Decide agent vs skill vs nothing; author lean; keep every tool folder in sync |

## Workflows (3)

`/plan` · `/validate-pbi` · `/document-dashboard`

## Validation is scripts, not agents

| Script | Behavior |
|---|---|
| `pbi-quality-rules/scripts/run_bpa.py <model>` | Real BPA (`TabularEditor.exe <model> -A bpa-rules.json -V`); falls back to `bpa_fallback.py` if TE2 is missing |
| `pbi-quality-rules/scripts/bpa_fallback.py <model>` | The 10 rules of `bpa-rules.json` re-implemented in Python over TMDL (less exact) |
| `pbi-report-layer-pbir/scripts/validate_pbir.py <path>` | `powerbi-report-author validate` when installed; otherwise a structural PBIR check |

All: `--format text|json`; exit 0 = no errors, 1 = errors found, 2 = usage/tool failure.
Python 3.9+, stdlib only. Tests: `npm test` (fixture PBIP at `tests/fixtures/SalesSample/`).

## Design principles

- **Less is more.** Capture domain-specific context only; never restate what the model knows.
- **Progressive disclosure.** Skills load when relevant, not upfront.
- **Default to a skill.** Agents are the exception and must pass the survival rule.
- **Verify with tools, not opinion.** Scripts and an independent reviewer gate delivery.
