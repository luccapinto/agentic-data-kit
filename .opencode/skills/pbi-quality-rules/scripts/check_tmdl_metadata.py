#!/usr/bin/env python3
"""
check_tmdl_metadata.py — deterministic TMDL measure-metadata gate.

Mirrors the data-goblin "measure metadata enforcement" hook: every measure should
declare a Description, a DisplayFolder, and a FormatString. This is a *deterministic*
check (pure pattern matching, no LLM judgement) meant to run as a Claude Code
PostToolUse hook on TMDL edits — and equally on the command line or in CI.

Usage
-----
  # Manual / CI: pass one or more .tmdl files or folders
  python check_tmdl_metadata.py path/to/Model.SemanticModel
  python check_tmdl_metadata.py tables/Sales.tmdl

  # Claude Code hook: receives the tool payload as JSON on stdin
  echo '{"tool_input":{"file_path":"tables/Sales.tmdl"}}' | python check_tmdl_metadata.py

Config
------
`hooks-config.yaml` next to this script (flat keys):
  enabled: true            # master switch
  mode: warn               # warn = report only (exit 0) | block = exit 2 (Claude sees it)
  require_description: true
  require_display_folder: true
  require_format_string: true

Exit codes: 0 = clean or warn-mode; 2 = block-mode with violations (blocks the tool
and feeds stderr back to Claude). Non-TMDL paths are ignored (exit 0).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("hooks-config.yaml")

DEFAULT_CONFIG = {
    "enabled": True,
    "mode": "warn",
    "require_description": True,
    "require_display_folder": True,
    "require_format_string": True,
}

MEASURE_RE = re.compile(r"^(\s*)measure\s+('[^']+'|\"[^\"]+\"|\S+)\s*=", re.IGNORECASE)


def load_config() -> dict:
    """Tiny flat-YAML reader (no PyYAML dependency at hook runtime)."""
    cfg = dict(DEFAULT_CONFIG)
    if not CONFIG_PATH.exists():
        return cfg
    for line in CONFIG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip().strip("'\"")
        if key not in cfg:
            continue
        cfg[key] = val.lower() in ("true", "1", "yes") if key != "mode" else val.lower()
    return cfg


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def check_file(path: Path, cfg: dict) -> list[str]:
    """Return a list of human-readable violation strings for one .tmdl file."""
    violations: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return violations

    i = 0
    while i < len(lines):
        m = MEASURE_RE.match(lines[i])
        if not m:
            i += 1
            continue

        base_indent = len(m.group(1))
        name = m.group(2).strip("'\"")

        # Description: /// comment lines immediately preceding the measure.
        has_desc = False
        j = i - 1
        while j >= 0 and lines[j].strip().startswith("///"):
            has_desc = True
            j -= 1

        # Collect the measure's child block (lines indented deeper than the measure).
        block: list[str] = []
        k = i + 1
        while k < len(lines):
            cur = lines[k]
            if cur.strip() == "":
                block.append(cur)
                k += 1
                continue
            if indent_of(cur) <= base_indent:
                break
            block.append(cur)
            k += 1

        block_text = "\n".join(block)
        if "///" in block_text:
            has_desc = True
        has_folder = bool(re.search(r"^\s*displayFolder\s*:", block_text, re.MULTILINE | re.IGNORECASE))
        has_format = bool(re.search(r"^\s*formatString\s*:", block_text, re.MULTILINE | re.IGNORECASE))

        missing = []
        if cfg["require_description"] and not has_desc:
            missing.append("Description")
        if cfg["require_display_folder"] and not has_folder:
            missing.append("DisplayFolder")
        if cfg["require_format_string"] and not has_format:
            missing.append("FormatString")
        if missing:
            violations.append(f"{path}:{i + 1}  measure '{name}' — missing: {', '.join(missing)}")

        i = k

    return violations


def resolve_targets(args: list[str]) -> list[Path]:
    """Expand CLI args (files/folders) into .tmdl files. Falls back to hook stdin JSON."""
    paths: list[Path] = []
    if args:
        for a in args:
            p = Path(a)
            if p.is_dir():
                paths.extend(sorted(p.rglob("*.tmdl")))
            elif p.suffix.lower() == ".tmdl":
                paths.append(p)
        return paths

    # No args → Claude Code hook mode: read tool payload from stdin.
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return paths
    fp = (payload.get("tool_input") or {}).get("file_path")
    if fp and Path(fp).suffix.lower() == ".tmdl":
        paths.append(Path(fp))
    return paths


def main() -> int:
    cfg = load_config()
    if not cfg["enabled"]:
        return 0

    targets = resolve_targets(sys.argv[1:])
    if not targets:
        return 0  # nothing relevant to check

    all_violations: list[str] = []
    for path in targets:
        all_violations.extend(check_file(path, cfg))

    if not all_violations:
        return 0

    header = (
        f"[pbi-quality-rules] {len(all_violations)} measure(s) missing required metadata "
        f"(Description / DisplayFolder / FormatString):"
    )
    print(header, file=sys.stderr)
    for v in all_violations:
        print("  - " + v, file=sys.stderr)

    if cfg["mode"] == "block":
        print("Mode=block: add the missing metadata, then re-save.", file=sys.stderr)
        return 2  # Claude Code: blocks the tool and surfaces stderr to the model
    return 0  # warn mode: report only, don't block


if __name__ == "__main__":
    sys.exit(main())
