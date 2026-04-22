from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidateExplibTests(unittest.TestCase):
    def _run_init(self, project_root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "init_explib.py"),
                "--project-root",
                str(project_root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def _run_validate(self, project_root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "validate_explib.py"),
                "--project-root",
                str(project_root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_validate_reports_missing_required_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            root = project_root / ".explib"
            root.mkdir(parents=True)
            result = self._run_validate(project_root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["code"], "validation_failed")
            self.assertEqual(payload["project_root"], project_root.as_posix())
            self.assertEqual(payload["explib_root"], root.as_posix())
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "missing_required_file"
            )
            self.assertEqual(target_issue["level"], "error")
            self.assertTrue(target_issue["blocking"])
            self.assertEqual(target_issue["ai_action"], "run_init")
            self.assertEqual(target_issue["path"], ".explib/EXP.md")

    def test_validate_reports_missing_domain_toc(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            root = project_root / ".explib"
            init = self._run_init(project_root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            missing_toc = root / "domains" / "api-integration" / "TOC.md"
            missing_toc.unlink()

            result = self._run_validate(project_root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "missing_domain_toc"
            )
            self.assertEqual(target_issue["path"], ".explib/domains/api-integration/TOC.md")

    def test_validate_reports_invalid_index_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            root = project_root / ".explib"
            init = self._run_init(project_root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            invalid_index = root / "domains" / "api-integration" / "toc.index.json"
            invalid_index.write_text("{not-json", encoding="utf-8")

            result = self._run_validate(project_root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "invalid_index_json"
            )
            self.assertEqual(target_issue["path"], ".explib/domains/api-integration/toc.index.json")

    def test_validate_reports_invalid_index_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            root = project_root / ".explib"
            init = self._run_init(project_root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            invalid_index = root / "domains" / "api-integration" / "toc.index.json"
            invalid_index.write_text(json.dumps({"foo": "bar"}), encoding="utf-8")

            result = self._run_validate(project_root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "invalid_index_json"
            )
            self.assertEqual(target_issue["path"], ".explib/domains/api-integration/toc.index.json")

    def test_validate_reports_drifted_domain_toc(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            root = project_root / ".explib"
            init = self._run_init(project_root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            drifted_toc = root / "domains" / "api-integration" / "TOC.md"
            drifted_toc.write_text("# drifted\n", encoding="utf-8")

            result = self._run_validate(project_root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "toc_render_out_of_sync"
            )
            self.assertEqual(target_issue["path"], ".explib/domains/api-integration/TOC.md")

    def test_validate_reports_invalid_index_entry_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            root = project_root / ".explib"
            init = self._run_init(project_root)
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

            result = self._run_validate(project_root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "invalid_index_json"
            )
            self.assertEqual(target_issue["path"], ".explib/domains/api-integration/toc.index.json")
