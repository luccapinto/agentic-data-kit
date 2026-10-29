import contextlib
import io
import json
import unittest
from pathlib import Path
from unittest import mock

from helpers import FIXTURE, QUALITY_SCRIPTS, TempDirMixin, copy_fixture, load_module, stub_args, write_stub

bpa = load_module(QUALITY_SCRIPTS / "bpa_fallback.py", "bpa_fallback")
run_bpa = load_module(QUALITY_SCRIPTS / "run_bpa.py", "run_bpa")

# The fixture carries exactly these violations on purpose (see tests/fixtures/SalesSample).
FIXTURE_VIOLATIONS = {
    ("DAX_EMPTY_EXPRESSION", "'Sales'[Forecast]", "error"),
    ("DAX_IFERROR_USAGE", "'Sales'[Margin %]", "warning"),
    ("DOC_MEASURE_DESCRIPTION", "'Sales'[total cost]", "warning"),
    ("NAMING_MEASURE_DISPLAYFOLDER", "'Sales'[total cost]", "warning"),
    ("NAMING_MEASURE_PASCAL", "'Sales'[total cost]", "warning"),
    ("DOC_TABLE_DESCRIPTION", "'Product'", "warning"),
    ("MODEL_BIDIRECTIONAL", "'Sales'[ProductID] -> 'Product'[ProductID]", "warning"),
    ("MODEL_ISLAND_TABLE", "'Targets'", "warning"),
    ("DOC_KEY_COLUMN_HIDDEN", "'Sales'[ProductID]", "info"),
}


def run_main(module, args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = module.main([str(a) for a in args])
    return code, out.getvalue(), err.getvalue()


def triples(result):
    return {(v["rule_id"], v["object"], v["severity"]) for v in result["violations"]}


class FallbackOnFixture(unittest.TestCase):
    def test_reports_exactly_the_planted_violations(self):
        code, out, _ = run_main(bpa, [FIXTURE / "SalesSample.pbip", "--format", "json"])
        result = json.loads(out)
        self.assertEqual(triples(result), FIXTURE_VIOLATIONS)
        self.assertEqual(result["summary"], {"error": 1, "warning": 7, "info": 1})
        self.assertEqual(result["skipped_rules"], [])
        self.assertEqual(code, 1, "an error-severity violation must fail the run")

    def test_every_shipped_rule_has_a_fallback_implementation(self):
        rule_ids = {r["ID"] for r in bpa.load_rules(bpa.DEFAULT_RULES)}
        self.assertEqual(rule_ids - set(bpa.CHECKS), set())

    def test_all_model_path_forms_resolve_to_the_same_model(self):
        sm = FIXTURE / "SalesSample.SemanticModel"
        expected = ("tmdl", sm / "definition")
        for path in (FIXTURE / "SalesSample.pbip", FIXTURE, sm, sm / "definition", sm / "definition.pbism"):
            with self.subTest(path=path):
                kind, resolved = bpa.resolve_model(path)
                self.assertEqual((kind, resolved.resolve()), (expected[0], expected[1].resolve()))

    def test_missing_path_is_a_usage_error(self):
        code, _, err = run_main(bpa, ["/definitely/not/here"])
        self.assertEqual(code, 2)
        self.assertIn("does not exist", err)


class TmdlParser(TempDirMixin, unittest.TestCase):
    def write_model(self, files):
        definition = self.tmp / "M.SemanticModel" / "definition"
        (definition / "tables").mkdir(parents=True)
        (definition / "model.tmdl").write_text("model Model\n\tculture: en-US\n", encoding="utf-8")
        for name, text in files.items():
            (definition / name).write_text(text, encoding="utf-8")
        return definition

    def test_multiline_fenced_and_quoted_constructs(self):
        definition = self.write_model({
            "tables/Facts.tmdl": (
                "/// Facts table.\n"
                "table 'Fact''s Table'\n"
                "\n"
                "\t/// Multi-line, empty after all.\n"
                "\tmeasure Empty =\n"
                "\t\t\tBLANK()\n"
                "\t\tdisplayFolder: X\n"
                "\n"
                "\tmeasure 'Fenced' = ```\n"
                "\t\t\tVAR x = 1\n"
                "\t\t\tRETURN IFERROR(x, 0)\n"
                "\t\t\t```\n"
                "\t\tdescription: \"Has a description property\"\n"
                "\t\tdisplayFolder: \"Quoted Folder\"\n"
                "\n"
                "\tcolumn CustomerID\n"
                "\t\tdataType: int64\n"
                "\t\tsourceColumn: CustomerID\n"
                "\n"
                "\tpartition P = m\n"
                "\t\tmode: import\n"
                "\t\tsource =\n"
                "\t\t\t\tlet x = 1 in x\n"
                "\n"
                "\tisHidden\n"
            ),
            "tables/LocalDateTable_abc.tmdl": "table LocalDateTable_abc\n\tisHidden\n",
            "relationships.tmdl": (
                "relationship r1\n"
                "\tcrossFilteringBehavior: bothDirections\n"
                "\tfromColumn: 'Fact''s Table'.CustomerID\n"
                "\ttoColumn: 'Fact''s Table'.'CustomerID'\n"
            ),
        })
        model = bpa.parse_tmdl_folder(definition)
        tables = {t.name: t for t in model.tables}
        facts = tables["Fact's Table"]
        self.assertEqual(facts.description, "Facts table.")
        self.assertTrue(facts.is_hidden, "table-level isHidden after members must be read")
        measures = {m.name: m for m in facts.measures}
        self.assertEqual(measures["Empty"].expression, "BLANK()")
        self.assertEqual(measures["Empty"].description, "Multi-line, empty after all.")
        self.assertIn("IFERROR", measures["Fenced"].expression)
        self.assertEqual(measures["Fenced"].description, "Has a description property")
        self.assertEqual(measures["Fenced"].display_folder, "Quoted Folder")
        self.assertEqual([c.name for c in facts.columns], ["CustomerID"])
        rel = model.relationships[0]
        self.assertEqual((rel.from_table, rel.from_column, rel.to_table), ("Fact's Table", "CustomerID", "Fact's Table"))

        result = bpa.analyze(model, bpa.load_rules(bpa.DEFAULT_RULES))
        got = triples(result)
        self.assertIn(("DAX_EMPTY_EXPRESSION", "'Fact''s Table'[Empty]", "error"), got)
        self.assertIn(("DAX_IFERROR_USAGE", "'Fact''s Table'[Fenced]", "warning"), got)
        self.assertIn(("PERF_AUTO_DATETIME", "'LocalDateTable_abc'", "warning"), got)
        self.assertIn(("DOC_KEY_COLUMN_HIDDEN", "'Fact''s Table'[CustomerID]", "info"), got)
        island = {o for r, o, _ in got if r == "MODEL_ISLAND_TABLE"}
        self.assertEqual(island, set(), "auto-date tables and related tables are not islands")

    def test_model_bim_is_supported(self):
        bim = self.tmp / "model.bim"
        bim.write_text(json.dumps({"model": {
            "tables": [{"name": "T", "description": "d", "measures": [
                {"name": "m", "expression": ["IFERROR(1,", "0)"], "displayFolder": "F"}]}],
            "relationships": [],
        }}), encoding="utf-8")
        result = bpa.analyze(bpa.load_model(bim), bpa.load_rules(bpa.DEFAULT_RULES))
        self.assertEqual(
            {(r, o) for r, o, _ in triples(result)},
            {("NAMING_MEASURE_PASCAL", "'T'[m]"), ("DAX_IFERROR_USAGE", "'T'[m]"),
             ("DOC_MEASURE_DESCRIPTION", "'T'[m]"), ("MODEL_ISLAND_TABLE", "'T'")},
        )

    def test_rule_without_fallback_is_skipped_not_passed(self):
        rules = self.tmp / "rules.json"
        rules.write_text(json.dumps([{"ID": "CUSTOM_X", "Name": "x", "Severity": 3, "Scope": "Measure",
                                      "Expression": "true"}]), encoding="utf-8")
        code, out, _ = run_main(bpa, [FIXTURE, "--rules", rules])
        self.assertEqual(code, 0)
        self.assertIn("SKIPPED  [CUSTOM_X]", out)


TE_OUTPUT = """Loading model...
Running Best Practice Analyzer...
=================================
##vso[task.logissue type=error;]Measure 'Sales'[Forecast] violates rule "Measure has an empty expression"
##vso[task.logissue type=warning;]Calculated Column 'Sales'[Margin] violates rule "Avoid IFERROR (masks underlying errors)"
##vso[task.logissue type=warning;]Relationship 'Sales'[ProductID] --> 'Product'[ProductID] violates rule "Bidirectional relationship"
Column 'Sales'[ProductID] violates rule "Key columns should be hidden"
##vso[task.logissue type=error;]Error on rule 'Broken rule': Unknown identifier 'Foo'
=================================
##vso[task.complete result=Failed;]Done.
"""


class TabularEditorRunner(TempDirMixin, unittest.TestCase):
    def test_command_line(self):
        cmd = run_bpa.build_command("TE.exe", Path("M/definition"), Path("rules.json"))
        self.assertEqual(cmd, ["TE.exe", str(Path("M/definition")), "-A", "rules.json", "-V"])

    def test_parses_severity_type_object_and_rule_errors(self):
        rules = bpa.load_rules(bpa.DEFAULT_RULES)
        result = run_bpa.parse_te_output(TE_OUTPUT, rules, "m")
        self.assertEqual(
            [(v["severity"], v["object_type"], v["object"], v["rule_id"]) for v in result["violations"]],
            [
                ("error", "Measure", "'Sales'[Forecast]", "DAX_EMPTY_EXPRESSION"),
                ("warning", "Calculated Column", "'Sales'[Margin]", "DAX_IFERROR_USAGE"),
                ("warning", "Relationship", "'Sales'[ProductID] --> 'Product'[ProductID]", "MODEL_BIDIRECTIONAL"),
                ("info", "Column", "'Sales'[ProductID]", "DOC_KEY_COLUMN_HIDDEN"),
            ],
        )
        self.assertEqual(result["rule_errors"], [{"rule_name": "Broken rule", "error": "Unknown identifier 'Foo'"}])
        self.assertEqual(result["summary"], {"error": 1, "warning": 2, "info": 1})

    def test_clean_run_exits_zero(self):
        te = write_stub(self.tmp, "TabularEditor", "Running Best Practice Analyzer...\nNo objects in violation of Best Practices.\n")
        code, out, _ = run_main(run_bpa, [FIXTURE, "--te", te])
        self.assertEqual(code, 0)
        self.assertIn("BPA engine: Tabular Editor 2", out)

    def test_runs_te_against_the_definition_folder(self):
        te = write_stub(self.tmp, "TabularEditor", TE_OUTPUT, exit_code=1)
        project = copy_fixture(self.tmp)
        code, out, _ = run_main(run_bpa, [project / "SalesSample.pbip", "--te", te, "--format", "json"])
        args = stub_args(self.tmp, "TabularEditor")
        self.assertEqual(Path(args[0]).resolve(), (project / "SalesSample.SemanticModel" / "definition").resolve())
        self.assertEqual(args[1:3], ["-A", str(bpa.DEFAULT_RULES.resolve())])
        self.assertEqual(args[3], "-V")
        self.assertEqual(json.loads(out)["engine"], "tabular-editor-2")
        self.assertEqual(code, 1)

    def test_te_crash_before_bpa_is_a_tool_failure(self):
        te = write_stub(self.tmp, "TabularEditor", "Error loading model: boom\n", exit_code=1)
        code, _, err = run_main(run_bpa, [FIXTURE, "--te", te])
        self.assertEqual(code, 2)
        self.assertIn("before the BPA ran", err)

    def test_without_te_uses_the_fallback_or_fails_when_told_to(self):
        with mock.patch.object(run_bpa, "find_tabular_editor", return_value=None):
            code, out, err = run_main(run_bpa, [FIXTURE, "--format", "json"])
            self.assertEqual(json.loads(out)["engine"], "python-fallback")
            self.assertIn("Python fallback", err)
            self.assertEqual(code, 1)
            code, _, err = run_main(run_bpa, [FIXTURE, "--no-fallback"])
            self.assertEqual(code, 2)

    def test_locator_precedence(self):
        exe = write_stub(self.tmp, "te-env", "")
        self.assertEqual(run_bpa.find_tabular_editor(None, {"TABULAR_EDITOR_PATH": str(exe)}), str(exe))
        self.assertIsNone(run_bpa.find_tabular_editor(str(self.tmp / "missing.exe"), {"TABULAR_EDITOR_PATH": str(exe)}))
        install = self.tmp / "pf" / "Tabular Editor"
        install.mkdir(parents=True)
        (install / "TabularEditor.exe").write_text("")
        with mock.patch.object(run_bpa.shutil, "which", return_value=None):
            found = run_bpa.find_tabular_editor(None, {"ProgramFiles(x86)": str(self.tmp / "pf")})
        self.assertEqual(found, str(install / "TabularEditor.exe"))


if __name__ == "__main__":
    unittest.main()
