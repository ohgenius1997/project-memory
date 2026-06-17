from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "project-memory" / "scripts"


def run_script(name: str, *args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        cwd=ROOT,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class ProjectMemoryScriptsTest(unittest.TestCase):
    def test_skill_metadata_is_valid(self) -> None:
        skill = ROOT / "skills" / "project-memory" / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        _, frontmatter, _body = text.split("---", 2)
        fields = {}
        for line in frontmatter.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip()
        self.assertEqual(fields.get("name"), "project-memory")
        self.assertTrue(fields.get("description"))

    def test_minimal_init_creates_only_agents_router(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = run_script(
                "init_docs.py",
                "--target",
                str(target),
                "--project-name",
                "Minimal Smoke",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            files = sorted(path.relative_to(target).as_posix() for path in target.rglob("*") if path.is_file())
            self.assertEqual(files, ["AGENTS.md"])

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("- Profile: minimal", agents)
            self.assertIn("- Dynamic memory: agentmemory", agents)
            self.assertIn("## Git Tracking Policy", agents)

    def test_init_rejects_existing_file_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "not-a-directory"
            target.write_text("not a project directory", encoding="utf-8")

            result = run_script("init_docs.py", "--target", str(target))

            self.assertEqual(result.returncode, 2)
            self.assertIn("Target exists but is not a directory", result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "not a project directory")

    def test_standard_without_dynamic_memory_creates_sparse_log_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = run_script(
                "init_docs.py",
                "--target",
                str(target),
                "--profile",
                "standard",
                "--dynamic-memory",
                "none",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "PROJECT_STATUS.md").exists())
            self.assertTrue((target / "docs" / "DECISIONS.md").exists())
            self.assertTrue((target / "docs" / "LOG.md").exists())
            self.assertFalse((target / "docs" / "ENVIRONMENT.md").exists())

    def test_unknown_addon_fails_without_writing_router(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = run_script(
                "init_docs.py",
                "--target",
                str(target),
                "--addons",
                "unknown-addon",
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("Unknown addon(s): unknown-addon", result.stderr)
            self.assertFalse((target / "AGENTS.md").exists())

    def test_brief_json_recommends_minimal_read_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            init = run_script("init_docs.py", "--target", str(target), "--profile", "standard")
            self.assertEqual(init.returncode, 0, init.stderr)

            result = run_script("brief_memory.py", "--target", str(target), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)

            self.assertEqual(payload["status"]["profile"], "standard")
            self.assertIn("AGENTS.md", payload["recommended_reads"])
            self.assertIn("PROJECT_STATUS.md", payload["recommended_reads"])

    def test_inspect_handles_space_and_unicode_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "项目 memory smoke"
            target.mkdir()
            init = run_script("init_docs.py", "--target", str(target), "--project-name", "Unicode Smoke")
            self.assertEqual(init.returncode, 0, init.stderr)

            result = run_script("inspect_project.py", "--target", str(target), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)

            self.assertEqual(payload["project_name"], "Unicode Smoke")
            self.assertEqual(payload["git"]["health"], "ok")

    def test_diagnose_reports_broken_git_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            init = run_script("init_docs.py", "--target", str(target))
            self.assertEqual(init.returncode, 0, init.stderr)
            (target / ".git").write_text("gitdir: /definitely/missing/gitdir\n", encoding="utf-8")

            result = run_script("diagnose_memory.py", "--target", str(target), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)

            codes = {item["code"] for item in payload}
            self.assertIn("git-pointer-invalid", codes)

    def test_status_sync_accepts_stdin_summary_and_does_not_modify_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            init = run_script("init_docs.py", "--target", str(target), "--profile", "standard")
            self.assertEqual(init.returncode, 0, init.stderr)
            status_path = target / "PROJECT_STATUS.md"
            before = status_path.read_text(encoding="utf-8")

            result = run_script(
                "status_sync_proposal.py",
                "--target",
                str(target),
                "--agentmemory-summary",
                "-",
                input_text="Latest durable summary from dynamic memory.",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Mode: read-only; no files were modified", result.stdout)
            self.assertIn("Latest durable summary from dynamic memory.", result.stdout)
            self.assertEqual(status_path.read_text(encoding="utf-8"), before)

    def test_migrate_agents_keeps_generated_router_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            init = run_script("init_docs.py", "--target", str(target))
            self.assertEqual(init.returncode, 0, init.stderr)

            result = run_script("migrate_agents.py", "--target", str(target), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)

            git_policy = [
                item for item in payload if "## Git Tracking Policy" in item["excerpt"]
            ]
            self.assertTrue(git_policy)
            self.assertTrue(all(item["action"] == "keep" for item in git_policy))

    def test_compact_memory_flags_long_legacy_docs_with_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            init = run_script("init_docs.py", "--target", str(target), "--profile", "standard")
            self.assertEqual(init.returncode, 0, init.stderr)

            roadmap = target / "docs" / "ROADMAP.md"
            roadmap.write_text(
                "# Roadmap\n"
                + "\n".join(
                    f"- Phase {index}: next step, branch handoff, decision, and validation detail."
                    for index in range(260)
                )
                + "\n",
                encoding="utf-8",
            )
            before = roadmap.read_text(encoding="utf-8")

            result = run_script("compact_memory.py", "--target", str(target), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)

            legacy_items = [
                item for item in payload if item["action"] == "legacy-migrate-or-archive"
            ]
            self.assertTrue(legacy_items)
            self.assertEqual(legacy_items[0]["path"], "docs/ROADMAP.md")
            self.assertIn("PROJECT_STATUS.md", legacy_items[0]["suggested_targets"])
            self.assertEqual(roadmap.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
