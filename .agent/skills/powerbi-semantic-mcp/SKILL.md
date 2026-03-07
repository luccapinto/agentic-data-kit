---
name: powerbi-semantic-mcp
description: Technical expertise in documenting, exploring, and modifying Power BI Semantic Models and tabular data using MCPs and APIs.
---

# Power BI Semantic Model Operations

This skill guides the usage of Model Context Protocols (MCPs) and external scripting tools to interact directly with Power BI Semantic Models (Tabular Object Model - TOM).

## 🧠 Core Principles

1. **Semantic Layer is King**: The Semantic Model is the single version of truth. Logic belongs here, not in the visual layer.
2. **DAX Formatting Matters**: `CALCULATE` statements must be formatted beautifully. If you can't read it top-down, it's a structural liability.
3. **Automate the Tedious**: Generating descriptions for 100 columns manually is torture. Use MCPs and AI to enforce widespread metadata perfection.

---

## 🛠️ MCP Integration Strategies

When editing or documenting semantic models using an MCP (like Tabular Editor CLI, Power BI REST API, or a custom Python MCP):

### 1. Documenting Measures & Columns
* **Extraction**: Query the model metadata to list all items missing descriptions.
* **Generation**: Use business context to write clear definitions (e.g., "Total count of active users within the trailing 30 days").
* **Push**: Apply translations/descriptions back to the semantic model via the MCP.

### 2. Best Practice Auditing
You must routinely leverage MCP endpoints to flag:
- Bidirectional relationships.
- Implicit measures (columns simply dragged into visuals rather than explicitly defined with DAX).
- Tables lacking a proper relationship to `DimDate`.

### 3. DAX Optimization Refactoring
When pulling DAX measures through an MCP for review:
* Break complex `IF` statements into nicely formatted `VAR` and `RETURN` blocks.
* Replace inefficient iteration functions (e.g., `FILTER`) with simple boolean arguments in `CALCULATE` when context permits.

---

## ❌ Common Pitfalls to Avoid

* **Don't touch visuals with MCPs**: MCPs are fantastic for the *Tabular Model* layer (Metadata, DAX, RLS). Altering `.pbix` visual layout binaries is unsupported and highly dangerous.
* **Don't ignore Row-Level Security (RLS)**: If you implement new dimensions via scripting, ensure the RLS filters are mapped, tested, and documented.
* **Never commit direct API changes without version control**: Always pull the `Model.bim` or `TMDL` (Tabular Model Definition Language) representation to Azure DevOps before pushing major modifications.
