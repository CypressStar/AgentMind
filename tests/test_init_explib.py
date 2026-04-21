import json
import importlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.helpers.explib_fixture import make_empty_root
from skills.exp.scripts._shared_templates import (
    empty_domain_index,
    render_dead_ends_toc,
    render_exp_md,
    render_pending_toc,
    render_resolved_toc,
)
from skills.exp.scripts._shared_render import render_domain_toc
from skills.exp.scripts._shared_taxonomy import FAILURE_SIGNAL_SOURCES


class InitExplibSupportTests(unittest.TestCase):
    def test_fixture_make_empty_root_creates_explib_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_empty_root(Path(tmp))
            self.assertTrue(root.exists())
            self.assertTrue(root.is_dir())
            self.assertEqual(root.name, ".explib")

    def test_empty_domain_index_has_expected_shape(self):
        data = empty_domain_index("api-integration")
        self.assertEqual(data["domain"], "api-integration")
        self.assertEqual(data["resolved"], [])
        self.assertEqual(data["dead_ends"], [])

    def test_render_exp_md_includes_signal_source_taxonomy(self):
        text = render_exp_md()
        self.assertIn("## Failure Signal Sources", text)
        for value in FAILURE_SIGNAL_SOURCES:
            self.assertIn(value, text)

    def test_top_level_toc_templates_include_guidance_and_routing(self):
        pending_text = render_pending_toc()
        resolved_text = render_resolved_toc()
        dead_ends_text = render_dead_ends_toc()

        self.assertIn("events/<event-id>/", pending_text)
        self.assertIn("Review mode must not read `pending`.", pending_text)
        self.assertIn("| work_domain | toc | note |", resolved_text)
        self.assertIn("| work_domain | toc | note |", dead_ends_text)

    def test_render_domain_toc_uses_generated_header_and_sections(self):
        text = render_domain_toc(
            {
                "domain": "api-integration",
                "resolved": [],
                "dead_ends": [],
            }
        )
        self.assertIn("> Generated from `toc.index.json`.", text)
        self.assertIn("## Resolved", text)
        self.assertIn("## Dead Ends", text)

    def test_render_domain_toc_escapes_markdown_table_metacharacters(self):
        text = render_domain_toc(
            {
                "domain": "api-integration",
                "resolved": [
                    {
                        "id": "api-integration-resolved-001",
                        "pattern_name": "Pipe | Name",
                        "failure_kind": "api_failure",
                        "signals": ["first|signal", "second\nsignal", "ignored"],
                        "note": "line one\nline two | note",
                    }
                ],
                "dead_ends": [],
            }
        )
        self.assertIn("Pipe \\| Name", text)
        self.assertIn("first\\|signal, second signal", text)
        self.assertIn("line one line two \\| note", text)

    def test_shared_templates_imports_in_script_mode(self):
        scripts_dir = Path(__file__).resolve().parents[1] / "skills" / "exp" / "scripts"
        before_path = list(sys.path)
        try:
            sys.path.insert(0, str(scripts_dir))
            sys.modules.pop("_shared_templates", None)
            module = importlib.import_module("_shared_templates")
            self.assertTrue(hasattr(module, "render_exp_md"))
        finally:
            sys.modules.pop("_shared_templates", None)
            sys.path[:] = before_path


REPO_ROOT = Path(__file__).resolve().parents[1]


class InitExplibScriptTests(unittest.TestCase):
    def _run_init(self, root: Path, check: bool = False) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            str(REPO_ROOT / "skills" / "exp" / "scripts" / "init_explib.py"),
            "--root",
            str(root),
        ]
        if check:
            cmd.append("--check")
        return subprocess.run(cmd, capture_output=True, text=True, check=False)

    def test_init_explib_creates_required_skeleton(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            result = self._run_init(root)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue((root / "EXP.md").is_file())
            self.assertTrue((root / "domains" / "api-integration" / "toc.index.json").is_file())
            self.assertTrue((root / "domains" / "api-integration" / "TOC.md").is_file())
            self.assertFalse((root / "resolved" / "api-integration").exists())
            self.assertFalse((root / "pending" / "events").exists())

    def test_init_explib_check_mode_reports_missing_items_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            result = self._run_init(root, check=True)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(root.exists())
            self.assertIn(".explib/EXP.md", "\n".join(payload["missing_files"]))
            self.assertNotIn(".explib/pending/events", "\n".join(payload["missing_dirs"]))

    def test_init_explib_rerun_preserves_rendered_domain_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            first = self._run_init(root)
            self.assertEqual(first.returncode, 0, msg=first.stderr)

            index_path = root / "domains" / "api-integration" / "toc.index.json"
            index_data = json.loads(index_path.read_text(encoding="utf-8"))
            index_data["resolved"] = [
                {
                    "id": "R-0001",
                    "pattern_name": "Handle flaky auth retries",
                    "failure_kind": "api_failure",
                    "signals": ["api_response", "tool_execution", "user_feedback"],
                    "note": "Retry once and refresh token first.",
                }
            ]
            index_data["dead_ends"] = [
                {
                    "id": "D-0001",
                    "pattern_name": "Blind timeout increase",
                    "failure_kind": "quality_failure",
                    "signals": ["user_feedback", "test_or_validation"],
                    "note": "Raised latency without fixing root cause.",
                }
            ]
            index_path.write_text(json.dumps(index_data, indent=2), encoding="utf-8")

            second = self._run_init(root)
            self.assertEqual(second.returncode, 0, msg=second.stderr)
            toc_path = root / "domains" / "api-integration" / "TOC.md"
            expected_resolved_row = (
                "| R-0001 | [Handle flaky auth retries](../../resolved/api-integration/R-0001.json) "
                "| api_failure | api_response, tool_execution | Retry once and refresh token first. |"
            )
            expected_dead_end_row = (
                "| D-0001 | [Blind timeout increase](../../dead-ends/api-integration/D-0001.json) "
                "| quality_failure | user_feedback, test_or_validation | Raised latency without fixing root cause. |"
            )
            rendered = toc_path.read_text(encoding="utf-8")
            self.assertIn(expected_resolved_row, rendered)
            self.assertIn(expected_dead_end_row, rendered)

            third = self._run_init(root)
            self.assertEqual(third.returncode, 0, msg=third.stderr)
            rerendered = toc_path.read_text(encoding="utf-8")
            self.assertIn(expected_resolved_row, rerendered)
            self.assertIn(expected_dead_end_row, rerendered)

    def test_init_explib_check_mode_reports_missing_domain_index_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            missing_index = root / "domains" / "api-integration" / "toc.index.json"
            missing_index.unlink()

            check = self._run_init(root, check=True)
            payload = json.loads(check.stdout)
            self.assertEqual(check.returncode, 1)
            self.assertIn(missing_index.as_posix(), payload["missing_files"])

    def test_init_explib_check_mode_reports_missing_domain_toc_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            missing_toc = root / "domains" / "api-integration" / "TOC.md"
            missing_toc.unlink()

            check = self._run_init(root, check=True)
            payload = json.loads(check.stdout)
            self.assertEqual(check.returncode, 1)
            self.assertIn(missing_toc.as_posix(), payload["missing_files"])

    def test_init_explib_check_mode_reports_drifted_top_level_toc_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            drifted = root / "resolved" / "TOC.md"
            drifted.write_text("# drifted\n", encoding="utf-8")

            check = self._run_init(root, check=True)
            payload = json.loads(check.stdout)
            self.assertEqual(check.returncode, 1)
            self.assertIn(drifted.as_posix(), payload["missing_files"])

    def test_init_explib_check_mode_reports_drifted_domain_toc_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            drifted = root / "domains" / "api-integration" / "TOC.md"
            drifted.write_text("# drifted\n", encoding="utf-8")

            check = self._run_init(root, check=True)
            payload = json.loads(check.stdout)
            self.assertEqual(check.returncode, 1)
            self.assertIn(drifted.as_posix(), payload["missing_files"])

    def test_init_explib_check_mode_reports_invalid_index_shape_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            invalid_index = root / "domains" / "api-integration" / "toc.index.json"
            invalid_index.write_text(
                json.dumps(
                    {
                        "domain": "api-integration",
                        "resolved": ["bad"],
                        "dead_ends": [],
                    }
                ),
                encoding="utf-8",
            )

            check = self._run_init(root, check=True)
            payload = json.loads(check.stdout)
            self.assertEqual(check.returncode, 1)
            self.assertIn(invalid_index.as_posix(), payload["missing_files"])


if __name__ == "__main__":
    unittest.main()
