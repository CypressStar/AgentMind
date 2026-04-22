from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class QueryScriptTests(unittest.TestCase):
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

    def test_list_toc_entries_returns_structured_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            root = project_root / ".explib"
            root.mkdir(parents=True)
            (root / "domains" / "api-integration").mkdir(parents=True)
            (root / "domains" / "api-integration" / "toc.index.json").write_text(
                json.dumps(
                    {
                        "domain": "api-integration",
                        "resolved": [
                            {
                                "id": "api-integration-resolved-001",
                                "pattern_name": "Request schema mismatch on API call",
                                "failure_kind": "api_failure",
                                "signals": ["400 invalid_request_error", "unknown field"],
                                "note": "Outdated schema assumptions cause payload rejection",
                                "entry_path": ".explib/resolved/api-integration/api-integration-resolved-001.json",
                            }
                        ],
                        "dead_ends": [],
                    }
                ),
                encoding="utf-8",
            )
            cmd = [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "list_toc_entries.py"),
                "--project-root",
                str(project_root),
                "--domain",
                "api-integration",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["project_root"], project_root.as_posix())
            self.assertEqual(payload["explib_root"], root.as_posix())
            self.assertEqual(payload["entries"][0]["kind"], "resolved")
            self.assertEqual(payload["entries"][0]["id"], "api-integration-resolved-001")

    def test_get_entry_returns_structured_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            root = project_root / ".explib"
            init = self._run_init(project_root)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            entry_dir = root / "resolved" / "api-integration"
            entry_dir.mkdir(parents=True, exist_ok=True)
            entry_path = entry_dir / "api-integration-resolved-001.json"
            entry_path.write_text(
                json.dumps(
                    {
                        "id": "api-integration-resolved-001",
                        "kind": "resolved",
                        "failure_kind": "api_failure",
                        "work_domain": "api-integration",
                        "pattern_name": "Request schema mismatch on API call",
                        "summary": "API request fails because fields do not match the documented schema",
                        "recognition_signals": ["400 invalid_request_error", "unknown field"],
                        "root_cause": "Payload was built from outdated assumptions",
                        "evidence_refs": [],
                        "solution_steps": [
                            "Check the official schema",
                            "Reduce to a minimal valid payload",
                        ],
                        "avoidance_notes": ["Do not guess schema from memory"],
                    }
                ),
                encoding="utf-8",
            )

            cmd = [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "get_entry.py"),
                "--project-root",
                str(project_root),
                "--id",
                "api-integration-resolved-001",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["project_root"], project_root.as_posix())
            self.assertEqual(payload["explib_root"], root.as_posix())
            self.assertEqual(payload["entry_path"], ".explib/resolved/api-integration/api-integration-resolved-001.json")
            self.assertEqual(payload["entry"]["id"], "api-integration-resolved-001")
