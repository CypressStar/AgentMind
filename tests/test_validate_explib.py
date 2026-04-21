from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidateExplibTests(unittest.TestCase):
    def _run_init(self, root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "init_explib.py"),
                "--root",
                str(root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def _run_validate(self, root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "validate_explib.py"),
                "--root",
                str(root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_validate_reports_missing_required_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            root.mkdir(parents=True)
            result = self._run_validate(root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["code"], "validation_failed")
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "missing_required_file"
            )
            self.assertEqual(target_issue["level"], "error")
            self.assertTrue(target_issue["blocking"])
            self.assertEqual(target_issue["ai_action"], "run_init")
            self.assertEqual(target_issue["path"], (root / "EXP.md").as_posix())

    def test_validate_reports_missing_domain_toc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            missing_toc = root / "domains" / "api-integration" / "TOC.md"
            missing_toc.unlink()

            result = self._run_validate(root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "missing_domain_toc"
            )
            self.assertEqual(target_issue["path"], missing_toc.as_posix())

    def test_validate_reports_invalid_index_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            invalid_index = root / "domains" / "api-integration" / "toc.index.json"
            invalid_index.write_text("{not-json", encoding="utf-8")

            result = self._run_validate(root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "invalid_index_json"
            )
            self.assertEqual(target_issue["path"], invalid_index.as_posix())

    def test_validate_reports_invalid_index_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            invalid_index = root / "domains" / "api-integration" / "toc.index.json"
            invalid_index.write_text(json.dumps({"foo": "bar"}), encoding="utf-8")

            result = self._run_validate(root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "invalid_index_json"
            )
            self.assertEqual(target_issue["path"], invalid_index.as_posix())

    def test_validate_reports_drifted_domain_toc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            init = self._run_init(root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            drifted_toc = root / "domains" / "api-integration" / "TOC.md"
            drifted_toc.write_text("# drifted\n", encoding="utf-8")

            result = self._run_validate(root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            target_issue = next(
                issue
                for issue in payload["issues"]
                if issue["issue_code"] == "toc_render_out_of_sync"
            )
            self.assertEqual(target_issue["path"], drifted_toc.as_posix())
