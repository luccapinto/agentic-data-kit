# Desktop Bridge — setup, commands, errors

Sources (read these when something here looks outdated):
- Microsoft Learn — [What is the Power BI Desktop Bridge?](https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-desktop-bridge-overview)
- Microsoft Learn — [Power BI Report skill](https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-report-skill-overview)
- [microsoft/skills-for-fabric › powerbi-authoring](https://github.com/microsoft/skills-for-fabric/tree/main/plugins/powerbi-authoring)
  (skill `powerbi-report-cli`, MIT) — the official agent guidance this kit follows.
- npm: [`@microsoft/powerbi-report-authoring-cli`](https://www.npmjs.com/package/@microsoft/powerbi-report-authoring-cli)
  (`powerbi-report-author`), [`@microsoft/powerbi-desktop-bridge-cli`](https://www.npmjs.com/package/@microsoft/powerbi-desktop-bridge-cli)
  (`powerbi-desktop`). Both MIT, Node 20+.

## What it is
A local JSON-RPC 2.0 server inside each running Power BI Desktop window, reachable only on the
same Windows machine through the named pipe `pbi-desktop-bridge-<processId>`. One operation runs
at a time per window; a second request while one is running fails — wait and retry, never run
two Desktop commands in parallel.

Methods (discover the current list with `bridge.manifest`):
| Method | Used for |
|---|---|
| `bridge.manifest` | Supported methods and their schemas for this Desktop build |
| `application.state.get/v1` | `currentFilePath`, `hasUnsavedChanges` |
| `report.snapshot.capture/v1` | PNG of one page (`pageId`, `scale` 1–3) |
| `file.reload/v1` | Reload the open PBIP from disk; `reloadModelDefinition` true/false |

## Setup (once per machine)
1. Power BI Desktop for Windows, recent enough to show **File > Options and settings > Options >
   Security > Desktop Bridge**. Keep *Enable external tool access to Power BI Desktop through
   secure local APIs* checked (default on). Admins can force it with the registry value
   `HKLM\SOFTWARE\Policies\Microsoft\Power BI Desktop\DesktopNamedPipeBridge` (`1` on, `0` off).
2. Node.js 20+, then `npm i -g @microsoft/powerbi-report-authoring-cli`.
3. Check: `powerbi-report-author doctor` and `powerbi-report-author preview --list-hosts`
   (the `desktop` host must say `available: true` while a PBIP is open).
4. The report must be a **PBIP saved in PBIR format** (not a `.pbix`, not PBIR-Legacy).

## Commands
Use `powerbi-report-author preview` for every Desktop operation; it finds the Desktop window
that has `<folder>` open, so there is no PID to pass. `<folder>` = the project folder or `.pbip`.

| Intent | Command |
|---|---|
| Status (save gate) | `powerbi-report-author preview "<folder>" --host desktop --status` |
| Open / attach | `powerbi-report-author preview "<folder>" --host desktop` |
| Reload report | `powerbi-report-author preview "<folder>" --host desktop --reload` |
| Reload report + on-disk model | `powerbi-report-author preview "<folder>" --host desktop --reload-with-model` |
| Screenshot one page | `powerbi-report-author preview "<folder>" --host desktop --screenshot "<shots>\<page>.png" --page "<pageId or display name>"` |
| Screenshot all pages | `powerbi-report-author preview "<folder>" --host desktop --screenshot "<shots>" --all-pages` |
| Validate files | `powerbi-report-author validate "<folder>"` (`--no-schema` offline) |

Optional `--scale 1..3` on screenshots. Every command prints a JSON envelope:
`{"data": {...}}` on success, `{"error": {"code": ..., "message": ..., "correction"?: {...}}}` on
failure. If an error carries a `correction` object, retry once changing only that value;
otherwise report the error and stop — do not improvise another command.

The bridge CLI underneath (`powerbi-desktop status | manifest | open | reload | screenshot |
screenshot-all`) is useful for manual troubleshooting by the user (e.g. `powerbi-desktop status`
lists every open window and its unsaved state). Agents stay on `powerbi-report-author`.

### Status before open/reload — never before a screenshot
```json
{"data":{"state":"ready","reports":[{"folder":"C:\\work\\Sales","hostInstanceId":"12345"}],
 "details":{"hasUnsavedChanges":false}}}
```
| `details.hasUnsavedChanges` | Action |
|---|---|
| `false` | Reload / open is allowed. |
| `true` | Stop. Ask the user to save (Ctrl+S) — or to discard — in Desktop, then check again. |
| missing, `null`, or the call failed | Treat as unsafe. Stop and report. |
| error `HOST_UNAVAILABLE` (no window has the report) | Open/attach is allowed; reload is not. |

## Errors you will meet
| Code / symptom | Meaning | What to do |
|---|---|---|
| `UNSUPPORTED_OS` in `--list-hosts` | Not on Windows | Use the Desktop-closed path; `validate` still works. |
| `HOST_UNAVAILABLE` — "Several Power BI Desktop instances have this report open" | Same report in 2+ windows (`details.candidatePids`) | Ask the user to close the extras. Never close Desktop yourself. |
| `HOST_UNAVAILABLE` — no instance | Desktop closed or setting off | Ask the user to open the `.pbip`; check the Security setting. |
| `RENDER_FAILED` with "unknown page id" | Page exists on disk but not in the open window | Status → reload → capture that page again. |
| `PAGE_NOT_FOUND` | The page is not in the definition at all | Fix `pages.json` / the page id. Reload will not help. |
| `status: "partial"` + non-zero exit | Some pages captured, some failed | Keep the PNGs you got; report which pages failed and why. |
| JSON-RPC `-32601 MethodNotFound` (bridge CLI) | Desktop build lacks that method | Update Desktop; check `powerbi-desktop manifest`. |
| "operation in progress" | Another bridge call is running | Wait, then retry once. |
| Theme change invisible after reload | Desktop cached the theme by file name | Rename the theme file + both refs in `report.json`, validate, reload. |
| Change invisible after reload, no error | Edited a file Desktop does not read (e.g. outside `definition/`) or the wrong report folder | `preview-visuals <folder>` to confirm paths; check `--status` `folder`. |
