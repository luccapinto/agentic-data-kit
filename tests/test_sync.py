import shutil
import unittest

import yaml

from helpers import ROOT, TempDirMixin, load_module

sync = load_module(ROOT / "scripts" / "sync_agents.py", "sync_agents")


def frontmatter(path):
    meta, _ = sync.parse_frontmatter(path.read_text(encoding="utf-8"))
    return meta


class GeneratedFolders(TempDirMixin, unittest.TestCase):
    def test_committed_generated_folders_match_the_source(self):
        self.assertEqual(sync.check(), [], "run: python3 scripts/sync_agents.py")

    def test_check_reports_every_kind_of_drift(self):
        expected, actual = self.tmp / "expected", self.tmp / "actual"
        sync.build(expected)
        shutil.copytree(expected, actual)
        (actual / ".claude" / "CLAUDE.md").write_text("hand edit", encoding="utf-8")
        (actual / ".cursor" / "commands" / "old.md").write_text("stale", encoding="utf-8")
        (actual / "AGENTS.md").unlink()
        (actual / ".opencode" / "AGENTS.md").write_text("legacy", encoding="utf-8")
        self.assertEqual(
            sorted(sync.stale_paths(expected, actual)),
            sorted([
                "outdated .claude/CLAUDE.md",
                "extra    .cursor/commands/old.md",
                "missing  AGENTS.md",
                "legacy   .opencode/AGENTS.md",
            ]),
        )

    def test_sync_keeps_unmanaged_github_files(self):
        workflow = self.tmp / ".github" / "workflows" / "ci.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text("on: push\n", encoding="utf-8")
        stale = self.tmp / ".github" / "agents" / "removed-agent.agent.md"
        stale.parent.mkdir(parents=True)
        stale.write_text("old", encoding="utf-8")
        sync.sync(self.tmp)
        self.assertTrue(workflow.exists())
        self.assertFalse(stale.exists(), "agents deleted from .agent/ must disappear from generated folders")
        self.assertEqual(sync.stale_paths(self.tmp, self.tmp), [])


class ReviewerToolRestrictions(TempDirMixin, unittest.TestCase):
    """The reviewer is read-only; every generated format must keep it read-only."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        from pathlib import Path
        cls._out = tempfile.TemporaryDirectory(prefix="adk-sync-")
        cls.out = Path(cls._out.name)
        sync.build(cls.out)

    @classmethod
    def tearDownClass(cls):
        cls._out.cleanup()

    def test_claude_keeps_the_source_allow_list(self):
        self.assertEqual(frontmatter(self.out / ".claude/agents/pbi-visual-reviewer.md")["tools"], "Read, Grep, Glob")

    def test_copilot_gets_mapped_aliases(self):
        meta = frontmatter(self.out / ".github/agents/pbi-visual-reviewer.agent.md")
        self.assertEqual(meta["tools"], ["read", "search"])

    def test_opencode_denies_edit_and_bash(self):
        meta = frontmatter(self.out / ".opencode/agents/pbi-visual-reviewer.md")
        self.assertEqual((meta["mode"], meta["permission"]), ("subagent", {"edit": "deny", "bash": "deny"}))

    def test_cursor_gets_skills_rule_and_commands(self):
        self.assertTrue((self.out / ".cursor/skills/pbi-report-layer-pbir/scripts/validate_pbir.py").is_file())
        rule = yaml.safe_load((self.out / ".cursor/rules/agentic-data-kit.mdc").read_text(encoding="utf-8").split("---")[1])
        self.assertIs(rule["alwaysApply"], True)
        self.assertTrue((self.out / ".cursor/commands/validate-pbi.md").is_file())

    def test_unknown_tool_name_fails_instead_of_widening_access(self):
        with self.assertRaises(SystemExit):
            sync.copilot_tools("Read, Teleport", "x")
        self.assertEqual(sync.copilot_tools("Read, Grep, Glob, Edit, Write, Bash", "x"),
                         ["read", "search", "edit", "execute"])
        self.assertEqual(sync.opencode_permission("Read, Write"), {"edit": "allow", "bash": "deny"})


if __name__ == "__main__":
    unittest.main()
