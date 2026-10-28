#!/usr/bin/env python3
"""Run the Best Practice Analyzer with Tabular Editor 2; fall back to Python when it is absent.

Usage:
  python3 run_bpa.py <model> [--rules bpa-rules.json] [--te PATH] [--format text|json] [--no-fallback]

<model>: .pbip, project folder, <Name>.SemanticModel, its definition/ folder, or model.bim.

Tabular Editor 2 is located in this order: --te, $TABULAR_EDITOR_PATH, TabularEditor(.exe) on
PATH, then the default Windows install folders. It runs as

  TabularEditor.exe <definition-folder|model.bim> -A <rules> -V

(-A: analyze with this rules file only, plus rules embedded in the model; -V: Azure DevOps
logging lines, which carry the severity). Without TE2 the script runs bpa_fallback.py and says so.

Disk is the input: with Power BI Desktop open, save first (Ctrl+S) so the TMDL is current.

Exit codes: 0 = no error-severity violations, 1 = error-severity violations (or rule errors),
2 = usage error / Tabular Editor could not run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpa_fallback  # noqa: E402

DEFAULT_RULES = bpa_fallback.DEFAULT_RULES
TE_TIMEOUT_SECONDS = 600

# "##vso[task.logissue type=warning;]Measure 'Sales'[x] violates rule "Rule name""
_VSO = re.compile(r"^##vso\[task\.logissue type=(?P<level>error|warning)[^\]]*\](?P<text>.*)$")
_VIOLATION = re.compile(r'^(?P<type>.+?) (?P<object>(?:\'|\[).*) violates rule "(?P<rule>.*)"$')
_VIOLATION_LOOSE = re.compile(r'^(?P<type>\S+) (?P<object>.+?) violates rule "(?P<rule>.*)"$')
_RULE_ERROR = re.compile(r"^Error on rule '(?P<rule>.*?)': (?P<error>.*)$")


def find_tabular_editor(explicit: Optional[str] = None, env: Optional[dict] = None) -> Optional[str]:
    env = os.environ if env is None else env
    for candidate in (explicit, env.get("TABULAR_EDITOR_PATH")):
        if candidate:
            return candidate if Path(candidate).is_file() else None
    for name in ("TabularEditor.exe", "TabularEditor"):
        found = shutil.which(name)
        if found:
            return found
    for base in (env.get("ProgramFiles(x86)"), env.get("ProgramFiles"), env.get("LOCALAPPDATA")):
        if base:
            exe = Path(base) / "Tabular Editor" / "TabularEditor.exe"
            if exe.is_file():
                return str(exe)
    return None


def build_command(te_path: str, model_target: Path, rules: Path) -> list:
    return [te_path, str(model_target), "-A", str(rules), "-V"]


def parse_te_output(stdout: str, rules: list, model_label: str) -> dict:
    """Turn TE2 console output (-A ... -V) into the same result shape as the fallback."""
    by_name = {r.get("Name"): r for r in rules}
    violations, rule_errors = [], []
    for raw in stdout.splitlines():
        line = raw.strip()
        if not line or line.startswith("##vso[task.complete"):
            continue
        level = "info"
        match = _VSO.match(line)
        if match:
            level, line = match.group("level"), match.group("text").strip()
        rule_error = _RULE_ERROR.match(line)
        if rule_error:
            rule_errors.append({"rule_name": rule_error.group("rule"), "error": rule_error.group("error")})
            continue
        found = _VIOLATION.match(line) or _VIOLATION_LOOSE.match(line)
        if not found:
            continue
        rule = by_name.get(found.group("rule"), {})
        violations.append({
            "rule_id": rule.get("ID", ""),
            "rule_name": found.group("rule"),
            "category": rule.get("Category", ""),
            "severity": level,
            "object_type": found.group("type"),
            "object": found.group("object"),
        })
    summary = {s: sum(1 for v in violations if v["severity"] == s) for s in ("error", "warning", "info")}
    return {
        "engine": "tabular-editor-2",
        "model": model_label,
        "violations": violations,
        "rule_errors": rule_errors,
        "skipped_rules": [],
        "summary": summary,
    }


def run_tabular_editor(te_path: str, model_target: Path, rules_path: Path, rules: list) -> dict:
    cmd = build_command(te_path, model_target, rules_path)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TE_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise bpa_fallback.UsageError(f"Tabular Editor failed to run ({' '.join(cmd)}): {exc}") from exc
    result = parse_te_output(proc.stdout, rules, str(model_target))
    loaded = "Running Best Practice Analyzer" in proc.stdout
    if proc.returncode != 0 and not loaded:
        detail = (proc.stderr or proc.stdout).strip()[-2000:]
        raise bpa_fallback.UsageError(f"Tabular Editor exited {proc.returncode} before the BPA ran:\n{detail}")
    return result


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the BPA via Tabular Editor 2 (Python fallback if absent).")
    parser.add_argument("model", type=Path)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--te", help="path to TabularEditor.exe (overrides $TABULAR_EDITOR_PATH)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--no-fallback", action="store_true", help="fail (exit 2) instead of using the Python fallback")
    args = parser.parse_args(argv)

    try:
        rules = bpa_fallback.load_rules(args.rules)
        kind, target = bpa_fallback.resolve_model(args.model)
        te_path = find_tabular_editor(args.te)
        if te_path:
            result = run_tabular_editor(te_path, target, args.rules.resolve(), rules)
        elif args.no_fallback or args.te:
            raise bpa_fallback.UsageError("Tabular Editor 2 not found (use --te or $TABULAR_EDITOR_PATH)")
        else:
            print("Tabular Editor 2 not found; using the Python fallback.", file=sys.stderr)
            parsed = bpa_fallback.parse_tmdl_folder(target) if kind == "tmdl" else bpa_fallback.parse_bim(target)
            result = bpa_fallback.analyze(parsed, rules)
    except bpa_fallback.UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(bpa_fallback.format_text(result))
        for err in result.get("rule_errors", []):
            print(f"RULE-ERR [{err['rule_name']}] {err['error']}")
    has_errors = result["summary"]["error"] > 0 or bool(result.get("rule_errors"))
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
