from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class QueryScriptTests(unittest.TestCase):
    def test_list_toc_entries_returns_structured_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
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
                "--root",
                str(root),
                "--domain",
                "api-integration",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["entries"][0]["kind"], "resolved")
            self.assertEqual(payload["entries"][0]["id"], "api-integration-resolved-001")
