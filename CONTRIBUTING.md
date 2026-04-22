# Contributing to the Agentic Data Kit

> This kit is designed to work out of the box. But if you want to extend it, here's how.

---

## 🚨 The Golden Rule

**NEVER manually edit `.github/` or `.claude/` folders.**

These are auto-generated outputs. Any changes you make there **will be overwritten** the next time the sync script runs.

**The only place to create or modify agents, skills, and workflows is inside `.agent/`.**

---

## How to Add Something New

### 1. Create

Add your file inside the appropriate `.agent/` subfolder:

- **New agent?** → `.agent/agents/your-agent.md`
- **New skill?** → `.agent/skills/your-skill/SKILL.md`
- **New workflow?** → `.agent/workflows/your-workflow.md`
- **Global rule change?** → `.agent/rules/rules.md`

### 2. Sync

Compile your changes to GitHub Copilot and Claude Code formats:

```bash
python scripts/sync_agents.py
```

### 3. Use

Your new agent appears in Copilot's `@` mentions and Claude's CLI. No extra configuration.

---

## Folder Structure

```
.agent/                     ← SOURCE OF TRUTH (edit here)
├── agents/                 ← AI specialist personas
│   ├── data-engineer.md
│   ├── powerbi-developer.md
│   └── ...
├── skills/                 ← Deep knowledge modules
│   ├── data-quality-testing/
│   ├── pbi-tmdl-authoring/
│   └── ...
├── workflows/              ← Slash command procedures
│   ├── plan.md
│   ├── validate-pbi.md
│   └── ...
└── rules/                  ← Universal directives
    └── rules.md

.github/                    ← AUTO-GENERATED (do not edit)
.claude/                    ← AUTO-GENERATED (do not edit)
```

---

## Conventions

- **Agents** use YAML frontmatter with `name`, `description`, and `skills` fields.
- **Skills** live in their own folder and must include a `SKILL.md` index file.
- **Workflows** use YAML frontmatter with a `description` field.
- Write all code comments and variable names in **English**, regardless of the prose language.
