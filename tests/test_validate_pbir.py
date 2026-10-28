import contextlib
import io
import json
import os
import shutil
import unittest
from pathlib import Path
from unittest import mock

from helpers import FIXTURE, PBIR_SCRIPTS, TempDirMixin, clean_env, copy_fixture, load_module, stub_args, write_stub

vp = load_module(PBIR_SCRIPTS / "validate_pbir.py", "validate_pbir")

PAGE = "e087e4b90fb242dfb36a"
CARD = "1c9e5a7d3b2f4e6a8d01"


def run_main(args, env=None):
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.dict(os.environ, env if env is not None else clean_env(), clear=True), \
            contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = vp.main([str(a) for a in args])
    return code, out.getvalue(), err.getvalue()


def codes(result, severity=None):
    return sorted(d["code"] for d in result["diagnostics"] if severity in (None, d["severity"]))


class Structural(TempDirMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.project = copy_fixture(self.tmp)
        self.report = self.project / "SalesSample.Report"
        self.pages = self.report / "definition" / "pages"

    def edit_json(self, path: Path, change):
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def check(self):
        return vp.structural_check(self.report)

    def test_fixture_is_clean(self):
        result = self.check()
        self.assertEqual((result["result"], result["errorCount"], result["warningCount"]), ("succeeded", 0, 0))

    def test_pages_json_out_of_sync_with_folders(self):
        self.edit_json(self.pages / "pages.json", lambda d: d.update(pageOrder=["ghost"], activePageName="other"))
        result = self.check()
        self.assertEqual(codes(result, "error"), ["ACTIVE_PAGE_UNKNOWN", "PAGE_MISSING"])
        self.assertEqual(codes(result, "warning"), ["PAGE_NOT_IN_ORDER"])

    def test_visual_problems(self):
        visual = self.pages / PAGE / "visuals" / CARD / "visual.json"

        def break_visual(d):
            d["name"] = "renamed"
            del d["position"]["height"]
            del d["visual"]["visualType"]
        self.edit_json(visual, break_visual)
        result = self.check()
        self.assertEqual(codes(result), ["NAME_MISMATCH", "POSITION_INVALID", "VISUAL_TYPE_MISSING"])
        self.assertTrue(all(d["file"] == f"definition/pages/{PAGE}/visuals/{CARD}/visual.json" for d in result["diagnostics"]))

    def test_visual_outside_canvas_is_a_warning(self):
        visual = self.pages / PAGE / "visuals" / CARD / "visual.json"
        self.edit_json(visual, lambda d: d["position"].update(x=1200))
        result = self.check()
        self.assertEqual((codes(result, "warning"), result["errorCount"]), (["OUTSIDE_CANVAS"], 0))
        self.assertEqual(result["result"], "succeededWithWarnings")

    def test_invalid_json_is_reported_once(self):
        (self.pages / PAGE / "visuals" / CARD / "visual.json").write_text("{ not json", encoding="utf-8")
        self.assertEqual(codes(self.check()), ["JSON_INVALID"])

    def test_broken_model_binding(self):
        shutil.rmtree(self.project / "SalesSample.SemanticModel")
        self.assertEqual(codes(self.check()), ["MODEL_BINDING_BROKEN"])

    def test_registered_resources_must_exist(self):
        (self.report / "StaticResources" / "SharedResources" / "BaseThemes" / "Fluent2-CY26SU10.json").unlink()

        def custom_theme(d):
            d["themeCollection"]["customTheme"] = {"name": "Brand-1a2b3c.json", "type": "RegisteredResources"}
        self.edit_json(self.report / "definition" / "report.json", custom_theme)
        self.assertEqual(codes(self.check()), ["RESOURCE_MISSING", "THEME_NOT_REGISTERED"])

    def test_pbir_legacy_layout(self):
        shutil.rmtree(self.report / "definition")
        (self.report / "report.json").write_text("{}", encoding="utf-8")
        self.assertEqual(codes(self.check()), ["PBIR_LEGACY_FORMAT"])

    def test_cli_exit_codes(self):
        code, out, _ = run_main([self.project, "--structural-only"])
        self.assertEqual(code, 0)
        self.assertIn("structural fallback", out)
        (self.pages / PAGE / "visuals" / CARD / "visual.json").write_text("{", encoding="utf-8")
        self.assertEqual(run_main([self.project, "--structural-only"])[0], 1)
        self.assertEqual(run_main([self.tmp / "nope"])[0], 2)

    def test_report_resolution(self):
        expected = self.report.resolve()
        for path in (self.project / "SalesSample.pbip", self.project, self.report):
            with self.subTest(path=path):
                self.assertEqual(vp.resolve_report(path), expected)


# Real envelopes captured from powerbi-report-author 0.5.0.
CLI_FAILED = {"data": {"result": "failed", "errorCount": 1, "warningCount": 1, "reportPath": "R", "diagnostics": {
    "PBIR_VISUAL_TYPE_UNKNOWN": {"severity": "warning", "items": [
        {"message": "Unknown visualType \"cardd\"", "file": "{report}/definition/pages/p/visuals/v1/visual.json",
         "path": "visual.visualType"}]},
    "PBIR_SCHEMA_VALIDATION_ERROR": {"severity": "error", "items": [
        {"message": "Schema validation: /position must have required property 'height'",
         "file": "{report}/definition/pages/p/visuals/v1/visual.json", "path": "/position"}]},
}}}
CLI_ERROR = {"error": {"message": "Path does not exist: /x", "code": "REPORT_PATH_NOT_FOUND", "retryable": False}}


class ReportAuthorCli(TempDirMixin, unittest.TestCase):
    def envelope(self, data, report: Path) -> str:
        return json.dumps(data).replace("{report}", str(report))

    def test_parses_diagnostics_relative_to_the_report(self):
        report = FIXTURE / "SalesSample.Report"
        result = vp.parse_cli_output(self.envelope(CLI_FAILED, report.resolve()), report.resolve())
        self.assertEqual((result["errorCount"], result["warningCount"], result["result"]), (1, 1, "failed"))
        self.assertEqual({d["file"] for d in result["diagnostics"]}, {"definition/pages/p/visuals/v1/visual.json"})
        self.assertEqual(codes(result, "error"), ["PBIR_SCHEMA_VALIDATION_ERROR"])

    def test_error_envelope_is_a_tool_failure(self):
        with self.assertRaises(vp.UsageError):
            vp.parse_cli_output(json.dumps(CLI_ERROR), FIXTURE)

    def test_uses_the_cli_when_configured(self):
        report = (FIXTURE / "SalesSample.Report").resolve()
        cli = write_stub(self.tmp, "powerbi-report-author", self.envelope(CLI_FAILED, report), exit_code=1)
        code, out, _ = run_main([FIXTURE / "SalesSample.pbip", "--offline", "--format", "json"],
                                env=clean_env(PBIR_AUTHOR_CLI=str(cli)))
        self.assertEqual(stub_args(self.tmp, "powerbi-report-author"), ["validate", str(report), "--no-schema"])
        self.assertEqual(json.loads(out)["engine"], "powerbi-report-author")
        self.assertEqual(code, 1)

    def test_structural_only_ignores_the_cli(self):
        cli = write_stub(self.tmp, "powerbi-report-author", json.dumps(CLI_ERROR))
        code, out, _ = run_main([FIXTURE, "--structural-only"], env=clean_env(PBIR_AUTHOR_CLI=str(cli)))
        self.assertEqual(code, 0)
        self.assertFalse((self.tmp / "powerbi-report-author.args").exists())


REAL_CLI = vp.find_cli()


@unittest.skipUnless(REAL_CLI, "powerbi-report-author not installed (set PBIR_AUTHOR_CLI or add it to PATH)")
class RealCli(unittest.TestCase):
    def test_fixture_passes_microsoft_validate(self):
        report = vp.resolve_report(FIXTURE)
        result = vp.run_cli(REAL_CLI, report, offline=True)
        self.assertEqual((result["result"], result["errorCount"]), ("succeeded", 0), result["diagnostics"])


if __name__ == "__main__":
    unittest.main()
