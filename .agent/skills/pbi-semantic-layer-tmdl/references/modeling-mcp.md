# Power BI Modeling MCP — setup and use

Microsoft now calls it the **Power BI Authoring MCP server**; the package and server id are still
`powerbi-modeling-mcp`. Sources:
- Microsoft Learn — [Power BI Authoring MCP server](https://learn.microsoft.com/en-us/power-bi/developer/mcp/power-bi-authoring-mcp)
- [microsoft/powerbi-modeling-mcp](https://github.com/microsoft/powerbi-modeling-mcp) (README, TROUBLESHOOTING)
- [microsoft/skills-for-fabric › powerbi-authoring](https://github.com/microsoft/skills-for-fabric/tree/main/plugins/powerbi-authoring)
  (skill `semantic-model-authoring`, bundles the same server)

## Local vs hosted
Working against a model **open in Power BI Desktop** (or PBIP files on disk) needs the **local**
server: it runs on the same Windows machine and talks to Desktop's local Analysis Services
instance over XMLA. The hosted endpoint only reaches Fabric workspaces. Register one of the two,
not both — duplicate tool sets confuse the agent. The local server does not run on macOS.

## Register the local server
Command in every client: `npx -y @microsoft/powerbi-modeling-mcp@latest --start`
(Node 18+; or install the VS Code extension `analysis-services.powerbi-modeling-mcp`).

| Client | File | Shape |
|---|---|---|
| Claude Code | `.mcp.json` (project) | `{"mcpServers": {"powerbi-modeling-mcp": {"type": "stdio", "command": "npx", "args": ["-y", "@microsoft/powerbi-modeling-mcp@latest", "--start"]}}}` |
| GitHub Copilot (VS Code) | `.vscode/mcp.json` | `{"servers": {"powerbi-modeling-mcp": {"type": "stdio", "command": "npx", "args": ["-y", "@microsoft/powerbi-modeling-mcp@latest", "--start"]}}}` |
| OpenCode | `opencode.json` | `{"mcp": {"powerbi-modeling-mcp": {"type": "local", "command": ["npx", "-y", "@microsoft/powerbi-modeling-mcp@latest", "--start"]}}}` |
| Cursor | `.cursor/mcp.json` | same shape as Claude Code (`mcpServers`) |

Useful flags: `--readonly` (inspection only — good for reviews), `--readwrite` (default; asks for
confirmation before the first write per database).

## Connect and work
- Desktop: `Connect to '<file name>' in Power BI Desktop` (tool `ConnectToPowerBIDesktop`; the
  PBIP must be open in Desktop).
- PBIP on disk without Desktop: `Open semantic model from PBIP folder '<path>\<Name>.SemanticModel\definition'`
  (changes stay in the session until exported back to TMDL).
- First call after connecting: a read (`List the tables and measures`) to confirm the target.

Tool groups you will use most: `measure_operations`, `column_operations`, `table_operations`,
`relationship_operations`, `dax_query_operations` (run/validate DAX, max 100,000 rows),
`transaction_operations` (begin/commit/rollback a batch), `calculation_group_operations`,
`security_role_operations`, `object_translation_operations`, `database_operations`
(import/export TMDL). Ask the agent "what can the Power BI Authoring MCP do" to list the current set.

## Rules of thumb
- Prefer one transaction per logical change; roll back on a failed step instead of leaving
  half-applied edits.
- Verify every new or changed measure with a DAX query before calling it done.
- Changes are live in Desktop but not on disk until the user saves (Ctrl+S); a PBIP under git
  makes every MCP change a reviewable diff.
- The MCP edits the model only — never report pages (use `pbi-report-layer-pbir`).
- Model metadata and query results go to the LLM provider of the client. Do not query
  sensitive columns just to "look at the data".

## Troubleshooting
| Symptom | Check |
|---|---|
| Server missing from the tool list | Client in agent mode? Server registered and started? Copilot Business/Enterprise: "MCP servers in Copilot" policy enabled by an admin. |
| "No Power BI Desktop instance found" | The PBIP/PBIX is open in Desktop and the name matches the file name you gave. |
| Reads work, writes fail | `--readonly` set, or (Fabric) only Build permission / XMLA read-only. |
| Edits vanish after reopening the file | The user closed Desktop without saving. |
| TMDL on disk does not show the change | Not saved yet — Desktop writes TMDL on save. |
