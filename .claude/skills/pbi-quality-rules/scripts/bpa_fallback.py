#!/usr/bin/env python3
"""Best Practice Analyzer fallback: the rules of bpa-rules.json, evaluated in Python.

Use this only when Tabular Editor 2 is not available (run_bpa.py calls it automatically).
It reads the semantic model straight from disk — TMDL (PBIP `definition/` folder) or a
`model.bim` — and re-implements each shipped rule by its ID. It is an approximation of the
real BPA engine: rules without a Python implementation are reported as skipped, never as passed.

Usage:
  python3 bpa_fallback.py <model> [--rules bpa-rules.json] [--format text|json]

<model> may be a .pbip file, a project folder, a <Name>.SemanticModel folder, its
definition/ folder, or a model.bim file.

Exit codes: 0 = no error-severity violations, 1 = error-severity violations, 2 = usage error.
Python 3.9+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

DEFAULT_RULES = Path(__file__).resolve().parent.parent / "bpa-rules.json"
SEVERITY_NAMES = {1: "info", 2: "warning", 3: "error"}
AUTO_DATE_PREFIXES = ("LocalDateTable_", "DateTableTemplate_")


class UsageError(Exception):
    """Bad input path or file; maps to exit code 2."""


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
@dataclass
class Measure:
    table: str
    name: str
    expression: str = ""
    description: str = ""
    display_folder: str = ""
    is_hidden: bool = False


@dataclass
class Column:
    table: str
    name: str
    description: str = ""
    is_hidden: bool = False


@dataclass
class Table:
    name: str
    description: str = ""
    is_hidden: bool = False
    measures: list = field(default_factory=list)
    columns: list = field(default_factory=list)


@dataclass
class Relationship:
    name: str
    from_table: str = ""
    from_column: str = ""
    to_table: str = ""
    to_column: str = ""
    cross_filtering: str = "oneDirection"


@dataclass
class Model:
    source: Path
    kind: str  # "tmdl" | "bim"
    tables: list = field(default_factory=list)
    relationships: list = field(default_factory=list)

    @property
    def measures(self):
        return [m for t in self.tables for m in t.measures]

    @property
    def columns(self):
        return [c for t in self.tables for c in t.columns]


# ---------------------------------------------------------------------------
# Locating the model on disk
# ---------------------------------------------------------------------------
def _is_tmdl_folder(path: Path) -> bool:
    return path.is_dir() and any((path / n).is_file() for n in ("model.tmdl", "database.tmdl"))


def _from_semantic_model_dir(path: Path) -> Optional[tuple]:
    if _is_tmdl_folder(path / "definition"):
        return "tmdl", path / "definition"
    if (path / "model.bim").is_file():
        return "bim", path / "model.bim"
    return None


def _semantic_model_from_pbip(pbip: Path) -> Optional[Path]:
    sibling = pbip.with_name(pbip.stem + ".SemanticModel")
    if sibling.is_dir():
        return sibling
    try:
        data = json.loads(pbip.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None
    for artifact in data.get("artifacts", []):
        report = artifact.get("report", {}).get("path")
        if not report:
            continue
        pbir = pbip.parent / report / "definition.pbir"
        try:
            ref = json.loads(pbir.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        by_path = ref.get("datasetReference", {}).get("byPath", {}).get("path")
        if by_path:
            candidate = (pbir.parent / by_path).resolve()
            if candidate.is_dir():
                return candidate
    return None


def resolve_model(path: Path) -> tuple:
    """Return (kind, path) where kind is 'tmdl' (definition folder) or 'bim' (model.bim)."""
    path = Path(path)
    if not path.exists():
        raise UsageError(f"path does not exist: {path}")
    if path.is_file():
        if path.suffix.lower() == ".bim":
            return "bim", path
        if path.suffix.lower() == ".pbip":
            sm = _semantic_model_from_pbip(path)
            found = _from_semantic_model_dir(sm) if sm else None
            if found:
                return found
            raise UsageError(f"no semantic model found for {path.name} (thin report?)")
        if path.name.lower() == "definition.pbism":
            return resolve_model(path.parent)
        raise UsageError(f"unsupported file: {path.name} (use .pbip, model.bim or a folder)")
    if _is_tmdl_folder(path):
        return "tmdl", path
    found = _from_semantic_model_dir(path)
    if found:
        return found
    models = sorted(p for p in path.glob("*.SemanticModel") if p.is_dir())
    if len(models) == 1:
        found = _from_semantic_model_dir(models[0])
        if found:
            return found
    if len(models) > 1:
        names = ", ".join(p.name for p in models)
        raise UsageError(f"several semantic models in {path}: {names}; pass one explicitly")
    raise UsageError(f"no TMDL definition or model.bim found under {path}")


# ---------------------------------------------------------------------------
# TMDL parser (the subset the rules need)
# ---------------------------------------------------------------------------
_PROPERTY = re.compile(r"^([A-Za-z][A-Za-z0-9_]*)\s*(?::\s*(.*))?$")


def _depth(line: str) -> int:
    expanded = line[: len(line) - len(line.lstrip())].replace("\t", "    ")
    return len(expanded) // 4


def _read_name(text: str) -> tuple:
    """Read one TMDL object name from the start of `text`. Returns (name, rest)."""
    text = text.lstrip()
    if text.startswith("'"):
        out, i = [], 1
        while i < len(text):
            if text[i] == "'":
                if i + 1 < len(text) and text[i + 1] == "'":
                    out.append("'")
                    i += 2
                    continue
                return "".join(out), text[i + 1 :]
            out.append(text[i])
            i += 1
        return "".join(out), ""
    match = re.match(r"[^\s=.]+", text)
    if not match:
        return "", text
    return match.group(0), text[match.end() :]


def _split_column_ref(ref: str) -> tuple:
    """`Sales.DateKey` / `'Sales Table'.'Date Key'` -> (table, column)."""
    table, rest = _read_name(ref)
    rest = rest.lstrip()
    if rest.startswith("."):
        column, _ = _read_name(rest[1:])
        return table, column
    return "", table


def _unquote_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('""', '"')
    return value


def parse_tmdl_folder(folder: Path) -> Model:
    model = Model(source=folder, kind="tmdl")
    tables: dict = {}
    for file in sorted(folder.rglob("*.tmdl")):
        _parse_tmdl_file(file.read_text(encoding="utf-8-sig"), model, tables)
    model.tables = list(tables.values())
    return model


def _parse_tmdl_file(text: str, model: Model, tables: dict) -> None:
    table: Optional[Table] = None
    obj = None  # Measure | Column | Relationship | Table (for table-level properties)
    obj_depth = 0
    other_depth: Optional[int] = None  # inside an object we do not model (partition, ...)
    expr_lines: Optional[list] = None
    expr_fenced = False
    pending_doc: list = []

    def finish_expression():
        nonlocal expr_lines
        if expr_lines is not None and isinstance(obj, Measure):
            obj.expression = "\n".join(expr_lines).strip()
        expr_lines = None

    for raw in text.splitlines():
        stripped = raw.strip()
        depth = _depth(raw)

        if expr_lines is not None:
            if expr_fenced:
                if stripped.startswith("```"):
                    finish_expression()
                else:
                    expr_lines.append(stripped)
                continue
            if not stripped or depth > obj_depth + 1:
                expr_lines.append(stripped)
                continue
            finish_expression()

        if not stripped:
            continue
        if stripped.startswith("///"):
            pending_doc.append(stripped[3:].strip())
            continue
        if stripped.startswith("//"):
            continue

        if other_depth is not None:
            if depth > other_depth:
                continue
            other_depth = None

        doc = " ".join(pending_doc).strip()
        pending_doc = []
        keyword, _, rest = stripped.partition(" ")

        if depth == 0:
            obj = None
            table = None
            if keyword == "table":
                name, _ = _read_name(rest)
                table = tables.setdefault(name, Table(name=name))
                if doc:
                    table.description = doc
                obj, obj_depth = table, 0
            elif keyword == "relationship":
                name, _ = _read_name(rest)
                obj, obj_depth = Relationship(name=name), 0
                model.relationships.append(obj)
            else:
                other_depth = 0
            continue

        if table is not None and depth == 1 and keyword in ("measure", "column"):
            name, after = _read_name(rest)
            after = after.strip()
            if keyword == "measure":
                obj = Measure(table=table.name, name=name, description=doc)
                table.measures.append(obj)
            else:
                obj = Column(table=table.name, name=name, description=doc)
                table.columns.append(obj)
            obj_depth = 1
            if after.startswith("="):
                inline = after[1:].strip()
                if inline.startswith("```"):
                    expr_lines, expr_fenced = [], True
                elif inline:
                    if isinstance(obj, Measure):
                        obj.expression = inline
                else:
                    expr_lines, expr_fenced = [], False
            continue

        if obj is not None and depth == obj_depth + 1:
            match = _PROPERTY.match(stripped)
            if match and (match.group(2) is not None or " " not in stripped):
                _set_property(obj, match.group(1), match.group(2))
                continue

        if table is not None and depth == 1:
            # Table-level property after members (e.g. `isHidden`, `lineageTag: …`).
            obj, obj_depth = table, 0
            match = _PROPERTY.match(stripped)
            if match and (match.group(2) is not None or " " not in stripped):
                _set_property(table, match.group(1), match.group(2))
                continue

        # Any other nested object (partition, hierarchy, annotation, ...): skip its body.
        other_depth = depth

    finish_expression()


def _set_property(obj, key: str, value: Optional[str]) -> None:
    flag = value is None or value.strip().lower() == "true"
    if key == "isHidden" and hasattr(obj, "is_hidden"):
        obj.is_hidden = flag
    elif key == "description" and hasattr(obj, "description") and value is not None:
        obj.description = _unquote_value(value)
    elif key == "displayFolder" and isinstance(obj, Measure) and value is not None:
        obj.display_folder = _unquote_value(value)
    elif isinstance(obj, Relationship) and value is not None:
        if key == "fromColumn":
            obj.from_table, obj.from_column = _split_column_ref(value)
        elif key == "toColumn":
            obj.to_table, obj.to_column = _split_column_ref(value)
        elif key == "crossFilteringBehavior":
            obj.cross_filtering = value.strip()


# ---------------------------------------------------------------------------
# model.bim (TMSL JSON)
# ---------------------------------------------------------------------------
def _text(value) -> str:
    if isinstance(value, list):
        return "\n".join(str(v) for v in value)
    return str(value or "")


def parse_bim(path: Path) -> Model:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except ValueError as exc:
        raise UsageError(f"{path} is not valid JSON: {exc}") from exc
    raw_model = data.get("model", data)
    model = Model(source=path, kind="bim")
    for t in raw_model.get("tables", []):
        table = Table(name=t.get("name", ""), description=_text(t.get("description")),
                      is_hidden=bool(t.get("isHidden")))
        for m in t.get("measures", []):
            table.measures.append(Measure(
                table=table.name, name=m.get("name", ""), expression=_text(m.get("expression")),
                description=_text(m.get("description")), display_folder=m.get("displayFolder", "") or "",
                is_hidden=bool(m.get("isHidden"))))
        for c in t.get("columns", []):
            if c.get("type") == "rowNumber":
                continue
            table.columns.append(Column(table=table.name, name=c.get("name", ""),
                                        description=_text(c.get("description")),
                                        is_hidden=bool(c.get("isHidden"))))
        model.tables.append(table)
    for r in raw_model.get("relationships", []):
        model.relationships.append(Relationship(
            name=r.get("name", ""), from_table=r.get("fromTable", ""), from_column=r.get("fromColumn", ""),
            to_table=r.get("toTable", ""), to_column=r.get("toColumn", ""),
            cross_filtering=r.get("crossFilteringBehavior", "oneDirection")))
    return model


def load_model(path: Path) -> Model:
    kind, resolved = resolve_model(path)
    return parse_tmdl_folder(resolved) if kind == "tmdl" else parse_bim(resolved)


# ---------------------------------------------------------------------------
# Rules — one Python predicate per rule ID in bpa-rules.json
# ---------------------------------------------------------------------------
def _blank(text: str) -> bool:
    return not (text or "").strip()


def _tables_in_relationships(model: Model) -> set:
    return {t for r in model.relationships for t in (r.from_table, r.to_table)}


# rule ID -> (scope, predicate(obj, model) -> True when the object VIOLATES the rule)
CHECKS: dict = {
    "NAMING_MEASURE_PASCAL": ("Measure", lambda m, _: bool(re.match(r"^[a-z]", m.name))),
    "NAMING_MEASURE_DISPLAYFOLDER": ("Measure", lambda m, _: not m.display_folder),
    "DAX_EMPTY_EXPRESSION": ("Measure", lambda m, _: _blank(m.expression)
                             or m.expression.replace(" ", "").upper() == "BLANK()"),
    "DAX_IFERROR_USAGE": ("Measure", lambda m, _: "IFERROR" in m.expression.upper()),
    "MODEL_BIDIRECTIONAL": ("Relationship", lambda r, _: r.cross_filtering.lower() == "bothdirections"),
    "MODEL_ISLAND_TABLE": ("Table", lambda t, model: t.name not in _tables_in_relationships(model)
                           and not t.name.startswith(AUTO_DATE_PREFIXES)),
    "PERF_AUTO_DATETIME": ("Table", lambda t, _: t.name.startswith(AUTO_DATE_PREFIXES)),
    "DOC_TABLE_DESCRIPTION": ("Table", lambda t, _: _blank(t.description)),
    "DOC_MEASURE_DESCRIPTION": ("Measure", lambda m, _: _blank(m.description)),
    "DOC_KEY_COLUMN_HIDDEN": ("Column", lambda c, _: bool(re.search(r"ID$", c.name)) and not c.is_hidden),
}


def _quote(name: str) -> str:
    return "'" + name.replace("'", "''") + "'"


def object_label(obj) -> str:
    if isinstance(obj, Table):
        return _quote(obj.name)
    if isinstance(obj, (Measure, Column)):
        return f"{_quote(obj.table)}[{obj.name}]"
    if isinstance(obj, Relationship):
        return f"{_quote(obj.from_table)}[{obj.from_column}] -> {_quote(obj.to_table)}[{obj.to_column}]"
    return str(obj)


def _objects(model: Model, scope: str) -> list:
    return {
        "Measure": model.measures,
        "Column": model.columns,
        "Table": model.tables,
        "Relationship": model.relationships,
    }[scope]


def load_rules(path: Path) -> list:
    try:
        rules = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise UsageError(f"cannot read rules file {path}: {exc}") from exc
    if not isinstance(rules, list):
        raise UsageError(f"rules file {path} must contain a JSON array")
    return rules


def analyze(model: Model, rules: list) -> dict:
    violations, skipped = [], []
    for rule in rules:
        check: Optional[tuple] = CHECKS.get(rule.get("ID"))
        if check is None:
            skipped.append(rule.get("ID") or rule.get("Name"))
            continue
        scope, predicate = check
        predicate: Callable
        severity = SEVERITY_NAMES.get(int(rule.get("Severity", 1)), "info")
        for obj in _objects(model, scope):
            if predicate(obj, model):
                violations.append({
                    "rule_id": rule["ID"],
                    "rule_name": rule.get("Name", rule["ID"]),
                    "category": rule.get("Category", ""),
                    "severity": severity,
                    "object_type": scope,
                    "object": object_label(obj),
                })
    order = {"error": 0, "warning": 1, "info": 2}
    violations.sort(key=lambda v: (order[v["severity"]], v["category"], v["rule_id"], v["object"]))
    return {
        "engine": "python-fallback",
        "model": str(model.source),
        "violations": violations,
        "skipped_rules": skipped,
        "summary": {s: sum(1 for v in violations if v["severity"] == s) for s in ("error", "warning", "info")},
    }


def format_text(result: dict) -> str:
    lines = []
    if result["engine"] == "python-fallback":
        lines.append("BPA engine: Python fallback (approximate). Install Tabular Editor 2 for the real BPA.")
    else:
        lines.append("BPA engine: Tabular Editor 2")
    lines.append(f"Model: {result['model']}")
    for v in result["violations"]:
        lines.append(f"{v['severity'].upper():8} [{v['rule_id']}] {v['object_type']} {v['object']} — {v['rule_name']}")
    if not result["violations"]:
        lines.append("No objects in violation of the rules.")
    for rule_id in result.get("skipped_rules", []):
        lines.append(f"SKIPPED  [{rule_id}] no implementation in this engine")
    s = result["summary"]
    lines.append(f"Summary: {s['error']} error(s), {s['warning']} warning(s), {s['info']} info")
    return "\n".join(lines)


def emit(result: dict, fmt: str) -> int:
    print(json.dumps(result, indent=2) if fmt == "json" else format_text(result))
    return 1 if result["summary"]["error"] else 0


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="BPA rules evaluated in Python over TMDL/model.bim.")
    parser.add_argument("model", type=Path, help=".pbip, project folder, .SemanticModel, definition/ or model.bim")
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES, help="BPA rules JSON (default: bpa-rules.json)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        result = analyze(load_model(args.model), load_rules(args.rules))
    except UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return emit(result, args.format)


if __name__ == "__main__":
    sys.exit(main())
