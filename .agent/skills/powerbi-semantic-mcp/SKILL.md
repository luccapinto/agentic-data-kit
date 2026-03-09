---
name: powerbi-semantic-mcp
description: Technical expertise in documenting, exploring, and modifying Power BI Semantic Models using the official Power BI MCP servers, REST API, and scripting tools.
---

# Power BI Semantic Model Operations via MCP

This skill guides the use of the **Power BI Modeling MCP Server** — Microsoft's official tool for enabling AI agents to build, modify, and manage Power BI semantic models through natural language.

> **Status:** Public Preview. Tools may significantly change before General Availability.
> **GitHub:** [microsoft/powerbi-modeling-mcp](https://github.com/microsoft/powerbi-modeling-mcp) | **Demo:** [End-to-end video](https://aka.ms/power-modeling-mcp-demo)

---

## 🏗️ What is the Power BI Modeling MCP Server?

A **local MCP server** (VS Code extension) that gives AI agents direct access to Power BI's Tabular Object Model (TOM) API. It exposes modeling tools that the AI uses to create, update, and manage semantic model objects in real-time.

**It connects to three target types:**

| Target | Connection prompt |
|--------|-------------------|
| Power BI Desktop | `Connect to '[File Name]' in Power BI Desktop` |
| Fabric Workspace | `Connect to semantic model '[Model Name]' in Fabric Workspace '[Workspace Name]'` |
| PBIP Files | `Open semantic model from PBIP folder '[Path to the definition/ TMDL folder in the PBIP]'` |

> ⚠️ **Scope:** The Modeling MCP can only execute **modeling operations**. It **cannot** modify report pages, visual layout, or diagram layouts. For that, use the `pbip-report-hacking` skill.

---

## 📦 Installation

**Option 1 — VS Code (Recommended):**
1. Install [VS Code](https://code.visualstudio.com/)
2. Install **GitHub Copilot** + **GitHub Copilot Chat** extensions
3. Install the [Power BI Modeling MCP extension](https://aka.ms/powerbi-modeling-mcp-vscode) (`Microsoft.powerbi-modeling-mcp`)
4. Open GitHub Copilot Chat → confirm `powerbi-modeling-mcp` appears in the MCP tools (hammer icon)

**Option 2 — Manual (any MCP client):**
Download the `.vsix` from the Marketplace, rename to `.zip`, unzip, run `\extension\server\powerbi-modeling-mcp.exe`:
```json
{
  "servers": {
    "powerbi-modeling-mcp": {
      "type": "stdio",
      "command": "C:\\MCPServers\\PowerBIModelingMCP\\extension\\server\\powerbi-modeling-mcp.exe",
      "args": ["--start"],
      "env": {}
    }
  }
}
```

**Settings flags:**
| Flag | Description |
|------|-------------|
| `--readwrite` | Default — allows model edits |
| `--readonly` | Restricts to read + DAX queries only |
| `--skipconfirmation` | Skips the Elicitation approval prompts |
| `PBI_MODELING_MCP_ACCESS_TOKEN` | Env var for token auth in CI/CD scenarios |

> Search `@ext:Microsoft.powerbi-modeling-mcp` in VS Code User Settings to configure.

---

## 🧠 Core Principles

1. **Semantic Layer is King.** Logic belongs in the Semantic Model, not in the report layer.
2. **Bulk Operations are the killer use-case.** Hours of renaming, refactoring, or documenting become seconds.
3. **Use deep-reasoning models.** For best results, use **GPT-4o** or **Claude Sonnet**. Model quality directly impacts output quality.
4. **Always back up first.** AI may produce unexpected changes. Commit a clean git state before any MCP session.

---

## 💡 What Can It Do?

- **Build & Modify:** Tables, columns, measures, hierarchies, relationships — all via natural language
- **Bulk Operations (at scale):** Rename patterns, refactor DAX, bulk descriptions, translations — with transaction support and error handling
- **Best Practice Evaluation:** Audit the model for anti-patterns and apply fixes
- **DAX Query & Validate:** Execute DAX against the model, benchmark measures, test calculations
- **Agentic TMDL Workflows:** Autonomously plan, create, and execute complex modeling tasks on PBIP project files

---

## 🚀 Official Example Prompts (from GitHub README)

```
Analyze my model's naming conventions and suggest renames to ensure consistency.
```
```
Add descriptions to all measures, columns, and tables to clearly explain their 
purpose and the logic behind the DAX code in simple, understandable terms.
```
```
Generate a French translation for my model including tables, columns and measures.
```
```
Refactor measures 'Sales Amount 12M Avg' and 'Sales Amount 6M Avg' into a 
calculation group and include new variants: 24M and 3M.
```
```
Analyze the Power Query code for all tables, identify the data source configuration, 
and create semantic model parameters to enable easy switching of the data source location.
```
```
Connect to semantic model 'V1' and 'V2'. Benchmark the following DAX query against 
both models. [DAX Query]
```
```
Generate a Markdown file documenting this Semantic Model: use a Mermaid diagram for 
relationships, document each measure with DAX and business-friendly descriptions, 
document RLS filters, and document data sources via Power Query analysis.
```

> 💡 These are starting points. With the right prompt and context, virtually any modeling task can be automated.

---

## ⚙️ Built-in MCP Prompts (`/` commands in VS Code)

| Prompt | Description |
|--------|-------------|
| `/dax_query_instructions_and_examples` | Step-by-step DAX query guidance with examples |
| `/powerbi_project_instructions` | Instructions for working with PBIP project files |

> Some prompts attach resources that provide critical context to the LLM. Run them at session start.

---

## 🔐 Confirmation & Data Privacy

### Elicitation Protocol (Confirmation Prompts)
The MCP follows the [Elicitation MCP protocol](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation) — it asks for user approval:
- **Before the first modification** to a semantic model
- **Before the first DAX query** executed against a model

Use `--skipconfirmation` to disable this in automated/trusted environments.

### Data Privacy
- The MCP runs **locally** and connects using **your existing credentials** — it does not bypass Power BI security.
- However, **model metadata, schemas, and query results** retrieved by the MCP are sent to the MCP client (VS Code) and then forwarded to the **configured LLM provider** as context.
- ⚠️ Exercise caution when sharing chat sessions. Sensitive metadata (column names, business logic in DAX) may appear in LLM logs.
- Governance focus: your organization's **AI data-handling policy** and the **LLM provider's terms of service**.

---

## ❌ Critical Pitfalls

| Pitfall | Risk |
|---------|------|
| No git backup before session | AI changes cannot be natively undone |
| Using it to modify visual layer | Not supported — use `pbip-report-hacking` skill instead |
| Applying bulk renames without testing | May break visual bindings in PBIR files (not MCP's scope to fix) |
| Ignoring RLS when adding dimensions | New tables may not inherit existing RLS filters |
| Sharing chat sessions without review | Sensitive model metadata may be exposed in LLM logs |
| Using a weak LLM model | Quality of output degrades significantly — use GPT-4o or Claude Sonnet |

---

## 🔗 Alternative Tools (When MCP is Not Available)

| Tool | Use Case |
|------|----------|
| **Tabular Editor 3** | Advanced DAX, Best Practice Analyzer, C# scripting |
| **Power BI REST API** | CI/CD: refresh, clone reports, deploy models |
| **Fabric Notebooks + `semantic-link`** | Python-based automated testing, scaling across workspaces |
| **ALM Toolkit** | Compare and merge semantic models, deploy schema-only changes |
| **TMDL (direct file editing)** | Version-controlled model changes via `.tmdl` files in PBIP |

> Use the **`tmdl-modeling`** skill when editing the Semantic Model via TMDL files.
> Use the **`pbip-report-hacking`** skill when editing the visual/report layer (PBIR files).
