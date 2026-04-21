from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidateExplibTests(unittest.TestCase):
    def test_validate_reports_missing_required_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            root.mkdir(parents=True)
            cmd = [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "validate_explib.py"),
                "--root",
                str(root),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
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
