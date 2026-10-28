#!/usr/bin/env python3
"""Validate a PBIR report: Microsoft's `powerbi-report-author validate` when installed,
otherwise a structural check written in Python.

Usage:
  python3 validate_pbir.py <path> [--structural-only] [--offline] [--format text|json]

<path>: a .pbip file, a <Name>.Report folder, a folder containing definition/, or a project
folder with exactly one *.Report.

The CLI (`npm i -g @microsoft/powerbi-report-authoring-cli`) is found through
$PBIR_AUTHOR_CLI or `powerbi-report-author` on PATH. It validates every file against the
published PBIR JSON schemas plus visual roles/types, so it is the authoritative check.
--offline passes --no-schema to it (no download of remote schemas).

The structural fallback checks what breaks Desktop most often: JSON that does not parse,
PBIR-Legacy layout, a broken semantic-model binding, pages.json out of sync with the page
folders, page/visual `name` != folder, visuals without position/visualType, visuals outside
the page canvas, and theme/resource files that are registered but missing. It does NOT know
the schemas or visual roles — say so when reporting.

Exit codes: 0 = no errors, 1 = errors found, 2 = usage error / the CLI could not run.
Python 3.9+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

CLI_NAME = "powerbi-report-author"
CLI_TIMEOUT_SECONDS = 300


class UsageError(Exception):
    pass


# ---------------------------------------------------------------------------
# Locate the .Report folder
# ---------------------------------------------------------------------------
def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def resolve_report(path: Path) -> Path:
    path = Path(path)
    if not path.exists():
        raise UsageError(f"path does not exist: {path}")
    if path.is_file():
        if path.suffix.lower() != ".pbip":
            raise UsageError(f"unsupported file: {path.name} (use a .pbip or a .Report folder)")
        try:
            artifacts = _read_json(path).get("artifacts", [])
        except ValueError as exc:
            raise UsageError(f"{path.name} is not valid JSON: {exc}") from exc
        for artifact in artifacts:
            report = artifact.get("report", {}).get("path")
            if report and (path.parent / report).is_dir():
                return (path.parent / report).resolve()
        sibling = path.with_name(path.stem + ".Report")
        if sibling.is_dir():
            return sibling.resolve()
        raise UsageError(f"{path.name} does not point to an existing .Report folder")
    if (path / "definition").is_dir() or (path / "definition.pbir").is_file() or path.suffix == ".Report":
        return path.resolve()
    reports = sorted(p for p in path.glob("*.Report") if p.is_dir())
    if len(reports) == 1:
        return reports[0].resolve()
    if len(reports) > 1:
        raise UsageError(f"several reports in {path}: {', '.join(p.name for p in reports)}; pass one")
    raise UsageError(f"no .Report folder found under {path}")


# ---------------------------------------------------------------------------
# Structural fallback
# ---------------------------------------------------------------------------
class Findings:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        self.items: list = []

    def add(self, severity: str, code: str, message: str, file: Optional[Path] = None, path: str = ""):
        rel = ""
        if file is not None:
            try:
                rel = file.relative_to(self.report_dir).as_posix()
            except ValueError:
                rel = str(file)
        self.items.append({"severity": severity, "code": code, "message": message, "file": rel, "path": path})

    def error(self, *args, **kwargs):
        self.add("error", *args, **kwargs)

    def warning(self, *args, **kwargs):
        self.add("warning", *args, **kwargs)


def _load(findings: Findings, file: Path, required: bool = True):
    if not file.is_file():
        if required:
            findings.error("FILE_MISSING", f"required file is missing: {file.name}", file)
        return None
    try:
        return _read_json(file)
    except ValueError as exc:
        findings.error("JSON_INVALID", f"invalid JSON: {exc}", file)
        return None


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def structural_check(report_dir: Path) -> dict:
    f = Findings(report_dir)
    definition = report_dir / "definition"

    for file in sorted(report_dir.rglob("*.json")):
        if ".pbi" in file.relative_to(report_dir).parts:
            continue
        try:
            _read_json(file)
        except ValueError as exc:
            f.error("JSON_INVALID", f"invalid JSON: {exc}", file)
    invalid = {i["file"] for i in f.items}

    if not definition.is_dir():
        if (report_dir / "report.json").is_file():
            f.error("PBIR_LEGACY_FORMAT", "PBIR-Legacy layout (report.json at the root); save the "
                    "report in PBIR format (Desktop: File > Options > Preview features > PBIR)", report_dir / "report.json")
        else:
            f.error("FILE_MISSING", "definition/ folder is missing", definition)
        return _result(f, "structural")

    pbir = _load(f, report_dir / "definition.pbir")
    if isinstance(pbir, dict):
        ref = pbir.get("datasetReference", {})
        by_path = ref.get("byPath", {}).get("path") if isinstance(ref.get("byPath"), dict) else None
        if by_path:
            target = (report_dir / by_path).resolve()
            if not target.is_dir():
                f.error("MODEL_BINDING_BROKEN", f"datasetReference.byPath points to a missing folder: {by_path}",
                        report_dir / "definition.pbir", "datasetReference.byPath.path")
        elif not ref.get("byConnection"):
            f.error("MODEL_BINDING_MISSING", "datasetReference has neither byPath nor byConnection",
                    report_dir / "definition.pbir", "datasetReference")

    _load(f, definition / "version.json")
    report = _load(f, definition / "report.json")
    if isinstance(report, dict):
        _check_resources(f, report, report_dir)

    pages_dir = definition / "pages"
    pages_meta = _load(f, pages_dir / "pages.json")
    page_folders = sorted(p.name for p in pages_dir.iterdir() if p.is_dir()) if pages_dir.is_dir() else []
    if isinstance(pages_meta, dict):
        order = pages_meta.get("pageOrder", [])
        for page_id in order:
            if page_id not in page_folders:
                f.error("PAGE_MISSING", f"pages.json lists page '{page_id}' but its folder is missing",
                        pages_dir / "pages.json", "pageOrder")
        for page_id in page_folders:
            if page_id not in order:
                f.warning("PAGE_NOT_IN_ORDER", f"page folder '{page_id}' is not listed in pages.json pageOrder",
                          pages_dir / page_id)
        active = pages_meta.get("activePageName")
        if active and active not in order:
            f.error("ACTIVE_PAGE_UNKNOWN", f"activePageName '{active}' is not in pageOrder",
                    pages_dir / "pages.json", "activePageName")

    for page_id in page_folders:
        _check_page(f, pages_dir / page_id, invalid)

    return _result(f, "structural")


def _check_resources(f: Findings, report: dict, report_dir: Path) -> None:
    static = report_dir / "StaticResources"
    for package in report.get("resourcePackages", []) or []:
        folder = static / package.get("name", "")
        for item in package.get("items", []) or []:
            rel = item.get("path")
            if rel and not (folder / rel).is_file():
                f.error("RESOURCE_MISSING", f"resource '{item.get('name')}' registered in report.json is "
                        f"missing on disk: {package.get('name')}/{rel}", report_dir / "definition" / "report.json",
                        "resourcePackages")
    custom = (report.get("themeCollection") or {}).get("customTheme")
    if isinstance(custom, dict) and custom.get("name"):
        registered = {
            item.get("name")
            for package in report.get("resourcePackages", []) or []
            if package.get("type") == custom.get("type", "RegisteredResources")
            for item in package.get("items", []) or []
        }
        if custom["name"] not in registered:
            f.error("THEME_NOT_REGISTERED", f"customTheme '{custom['name']}' has no matching resourcePackages item",
                    report_dir / "definition" / "report.json", "themeCollection.customTheme.name")


def _check_page(f: Findings, page_dir: Path, invalid: set) -> None:
    page_file = page_dir / "page.json"
    page = _load(f, page_file)
    if not isinstance(page, dict):
        return
    if page.get("name") != page_dir.name:
        f.error("NAME_MISMATCH", f"page.json name '{page.get('name')}' != folder '{page_dir.name}'", page_file, "name")
    if not page.get("displayName"):
        f.warning("PAGE_NO_DISPLAY_NAME", "page has no displayName", page_file, "displayName")
    width, height = page.get("width"), page.get("height")
    if not (_is_number(width) and _is_number(height)):
        f.error("PAGE_SIZE_INVALID", "page width/height must be numbers", page_file)
        width = height = None

    visuals_dir = page_dir / "visuals"
    if not visuals_dir.is_dir():
        return
    for visual_dir in sorted(p for p in visuals_dir.iterdir() if p.is_dir()):
        visual_file = visual_dir / "visual.json"
        rel = visual_file.relative_to(f.report_dir).as_posix()
        if rel in invalid:
            continue
        visual = _load(f, visual_file)
        if not isinstance(visual, dict):
            continue
        if visual.get("name") != visual_dir.name:
            f.error("NAME_MISMATCH", f"visual.json name '{visual.get('name')}' != folder '{visual_dir.name}'",
                    visual_file, "name")
        pos = visual.get("position")
        if not isinstance(pos, dict) or not all(_is_number(pos.get(k)) for k in ("x", "y", "width", "height")):
            f.error("POSITION_INVALID", "position needs numeric x, y, width and height", visual_file, "position")
            pos = None
        kind = (visual.get("visual") or {}).get("visualType")
        if not kind and "visualGroup" not in visual:
            f.error("VISUAL_TYPE_MISSING", "visual.visualType is missing (and this is not a visualGroup)",
                    visual_file, "visual.visualType")
        if pos and width is not None and not visual.get("parentGroupName"):
            right, bottom = pos["x"] + pos["width"], pos["y"] + pos["height"]
            if pos["x"] < 0 or pos["y"] < 0 or right > width + 0.5 or bottom > height + 0.5:
                f.warning("OUTSIDE_CANVAS", f"visual extends outside the {width}x{height} page "
                          f"(x={pos['x']}, y={pos['y']}, right={right}, bottom={bottom})", visual_file, "position")


def _result(f: Findings, engine: str) -> dict:
    errors = sum(1 for i in f.items if i["severity"] == "error")
    warnings = sum(1 for i in f.items if i["severity"] == "warning")
    return {
        "engine": engine,
        "report": str(f.report_dir),
        "result": "failed" if errors else ("succeededWithWarnings" if warnings else "succeeded"),
        "errorCount": errors,
        "warningCount": warnings,
        "diagnostics": f.items,
    }


# ---------------------------------------------------------------------------
# powerbi-report-author CLI
# ---------------------------------------------------------------------------
def find_cli(env: Optional[dict] = None) -> Optional[str]:
    env = os.environ if env is None else env
    explicit = env.get("PBIR_AUTHOR_CLI")
    if explicit:
        return explicit if Path(explicit).is_file() else None
    return shutil.which(CLI_NAME)


def build_cli_command(cli: str, report_dir: Path, offline: bool) -> list:
    cmd = [cli, "validate", str(report_dir)]
    if offline:
        cmd.append("--no-schema")
    return cmd


def parse_cli_output(stdout: str, report_dir: Path) -> dict:
    """Normalize the CLI's JSON envelope ({"data": ...} or {"error": ...})."""
    try:
        envelope = json.loads(stdout)
    except ValueError as exc:
        raise UsageError(f"{CLI_NAME} returned non-JSON output: {stdout.strip()[:500]}") from exc
    if "error" in envelope:
        err = envelope["error"]
        raise UsageError(f"{CLI_NAME} failed: {err.get('code')}: {err.get('message')}")
    data = envelope.get("data", {})
    items = []
    for code, group in (data.get("diagnostics") or {}).items():
        for item in group.get("items", []):
            file = item.get("file", "")
            try:
                file = Path(file).resolve().relative_to(report_dir).as_posix() if file else ""
            except ValueError:
                pass
            items.append({
                "severity": group.get("severity", "error"),
                "code": code,
                "message": item.get("message", ""),
                "file": file,
                "path": item.get("path", ""),
            })
    return {
        "engine": CLI_NAME,
        "report": str(report_dir),
        "result": data.get("result", "unknown"),
        "errorCount": int(data.get("errorCount", sum(1 for i in items if i["severity"] == "error"))),
        "warningCount": int(data.get("warningCount", sum(1 for i in items if i["severity"] == "warning"))),
        "diagnostics": items,
    }


def run_cli(cli: str, report_dir: Path, offline: bool) -> dict:
    cmd = build_cli_command(cli, report_dir, offline)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=CLI_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise UsageError(f"could not run {' '.join(cmd)}: {exc}") from exc
    return parse_cli_output(proc.stdout, report_dir)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def format_text(result: dict) -> str:
    if result["engine"] == "structural":
        lines = [f"PBIR validation: structural fallback ({CLI_NAME} not found; schemas and visual "
                 "roles NOT checked — install @microsoft/powerbi-report-authoring-cli)"]
    else:
        lines = [f"PBIR validation: {CLI_NAME} validate"]
    lines.append(f"Report: {result['report']}")
    for d in sorted(result["diagnostics"], key=lambda d: (d["severity"] != "error", d["file"], d["code"])):
        where = d["file"] + (f" @ {d['path']}" if d["path"] else "")
        lines.append(f"{d['severity'].upper():8} [{d['code']}] {d['message']}" + (f"  ({where})" if where else ""))
    lines.append(f"Result: {result['result']} — {result['errorCount']} error(s), {result['warningCount']} warning(s)")
    return "\n".join(lines)


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a PBIR report (CLI if installed, else structural).")
    parser.add_argument("path", type=Path)
    parser.add_argument("--structural-only", action="store_true", help="skip the CLI even if it is installed")
    parser.add_argument("--offline", action="store_true", help="pass --no-schema to the CLI")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    try:
        report_dir = resolve_report(args.path)
        cli = None if args.structural_only else find_cli()
        result = run_cli(cli, report_dir, args.offline) if cli else structural_check(report_dir)
    except UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2) if args.format == "json" else format_text(result))
    return 1 if result["errorCount"] else 0


if __name__ == "__main__":
    sys.exit(main())
