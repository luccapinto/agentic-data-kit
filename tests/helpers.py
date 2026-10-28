"""Shared paths and loaders for the test suite (stdlib unittest; run with `npm test`)."""

import importlib.util
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "SalesSample"
QUALITY_SCRIPTS = ROOT / ".agent" / "skills" / "pbi-quality-rules" / "scripts"
PBIR_SCRIPTS = ROOT / ".agent" / "skills" / "pbi-report-layer-pbir" / "scripts"


def load_module(path: Path, name: str):
    """Import a script file as a module (scripts are not a package)."""
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def copy_fixture(tmp: Path) -> Path:
    """Copy the SalesSample fixture into `tmp` and return the copy's project folder."""
    dest = tmp / "SalesSample"
    shutil.copytree(FIXTURE, dest, ignore=shutil.ignore_patterns(".pbi"))
    return dest


def write_stub(folder: Path, name: str, stdout: str, exit_code: int = 0) -> Path:
    """Create an executable that records its argv to <name>.args and prints `stdout`."""
    script = folder / name
    out_file = folder / f"{name}.out"
    out_file.write_text(stdout, encoding="utf-8")
    script.write_text(
        f"#!{sys.executable}\n"
        "import sys, pathlib\n"
        f"pathlib.Path({str(folder / (name + '.args'))!r}).write_text('\\n'.join(sys.argv[1:]))\n"
        f"sys.stdout.write(pathlib.Path({str(out_file)!r}).read_text(encoding='utf-8'))\n"
        f"sys.exit({exit_code})\n",
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return script


def stub_args(folder: Path, name: str) -> list:
    return (folder / f"{name}.args").read_text(encoding="utf-8").split("\n")


class TempDirMixin:
    def setUp(self):
        super().setUp()
        self._tmp = tempfile.TemporaryDirectory(prefix="adk-test-")
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()
        super().tearDown()


def clean_env(**overrides) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in ("TABULAR_EDITOR_PATH", "PBIR_AUTHOR_CLI")}
    env.update(overrides)
    return env
