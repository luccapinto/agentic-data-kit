import shutil
import subprocess
import unittest

from helpers import ROOT, TempDirMixin

NODE = shutil.which("node")
HAS_DEPS = (ROOT / "node_modules" / "commander").is_dir()


@unittest.skipUnless(NODE and HAS_DEPS, "node and `npm install` are required for CLI tests")
class Init(TempDirMixin, unittest.TestCase):
    def init(self, target, *extra):
        return subprocess.run(
            [NODE, str(ROOT / "bin" / "cli.js"), "init", "--target", target, "--path", str(self.tmp), *extra],
            capture_output=True, text=True, timeout=60,
        )

    def assert_files(self, *rels):
        for rel in rels:
            self.assertTrue((self.tmp / rel).is_file(), f"missing {rel}")

    def test_each_target_installs_its_native_layout(self):
        expected = {
            "claude": [".claude/CLAUDE.md", ".claude/agents/pbi-visual-reviewer.md",
                       ".claude/commands/validate-pbi.md", ".claude/skills/pbi-quality-rules/scripts/run_bpa.py"],
            "copilot": [".github/copilot-instructions.md", ".github/agents/pbi-visual-reviewer.agent.md",
                        ".github/prompts/validate-pbi.prompt.md", ".github/skills/pbi-quality-rules/bpa-rules.json"],
            "opencode": ["AGENTS.md", ".opencode/agents/pbi-visual-reviewer.md",
                         ".opencode/skills/pbi-semantic-layer-tmdl/SKILL.md"],
            "cursor": [".cursor/rules/agentic-data-kit.mdc", ".cursor/commands/validate-pbi.md",
                       ".cursor/skills/pbi-report-layer-pbir/SKILL.md"],
            "antigravity": [".agent/rules/rules.md", ".agent/agents/pbi-visual-reviewer.md", "scripts/sync_agents.py"],
        }
        for target, files in expected.items():
            with self.subTest(target=target):
                shutil.rmtree(self.tmp)
                self.tmp.mkdir()
                proc = self.init(target)
                self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
                self.assert_files(*files)
                self.assertEqual(list(self.tmp.rglob("__pycache__")), [])

    def test_copilot_merges_into_an_existing_github_folder(self):
        own = self.tmp / ".github" / "workflows" / "ci.yml"
        own.parent.mkdir(parents=True)
        own.write_text("on: push\n", encoding="utf-8")
        proc = self.init("copilot")
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertEqual(own.read_text(encoding="utf-8"), "on: push\n")
        self.assertFalse((self.tmp / ".github" / "workflows" / "sync-check.yml").exists(),
                         "the kit's own CI workflow must never be installed")
        self.assertNotEqual(self.init("copilot").returncode, 0, "second run without --force must refuse")
        forced = self.init("copilot", "--force")
        self.assertEqual(forced.returncode, 0, forced.stderr)
        self.assertTrue(own.exists(), "--force must only replace the kit's own entries")

    def test_opencode_refuses_to_overwrite_an_existing_agents_md(self):
        (self.tmp / "AGENTS.md").write_text("mine", encoding="utf-8")
        proc = self.init("opencode")
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual((self.tmp / "AGENTS.md").read_text(encoding="utf-8"), "mine")

    def test_unknown_target(self):
        proc = self.init("emacs")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("cursor", proc.stderr)


if __name__ == "__main__":
    unittest.main()
