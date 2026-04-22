from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class WriteScriptTests(unittest.TestCase):
    def _run(self, script_name: str, project_root: Path, extra_args: list[str] | None = None) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            str(REPO_ROOT / "skills" / "exp" / "scripts" / script_name),
            "--project-root",
            str(project_root),
        ]
        if extra_args:
            cmd.extend(extra_args)
        return subprocess.run(cmd, capture_output=True, text=True, check=False)

    def _write_payload(self, path: Path, payload: dict) -> Path:
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def _init(self, project_root: Path):
        result = self._run("init_explib.py", project_root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_create_pending_creates_event_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            self._init(project_root)

            payload_path = self._write_payload(
                project_root / "create_pending.json",
                {
                    "id": "exp-20260422-001",
                    "failure_kind": "api_failure",
                    "failure_signal_source": "api_response",
                    "work_domain": "api-integration",
                    "pattern_guess": "request_schema_mismatch",
                    "root_cause_guess": "payload built from outdated assumptions",
                    "summary": "API request failed with invalid field error",
                    "scene": "Agent called external API during task execution",
                    "error_text": "400 invalid_request_error: unknown field",
                    "raw_feedback": None,
                    "feedback_hint": None,
                    "initial_attempt": {
                        "action": "sent initial request",
                        "result": "failed",
                        "note": "400 invalid_request_error",
                    },
                },
            )

            result = self._run("create_pending.py", project_root, ["--input", str(payload_path)])
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual(payload["event_id"], "exp-20260422-001")
            event_dir = project_root / ".explib" / "pending" / "events" / "exp-20260422-001"
            self.assertTrue((event_dir / "event.json").is_file())
            self.assertTrue((event_dir / "attempts.jsonl").is_file())

    def test_append_attempt_appends_jsonl_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            self._init(project_root)

            create_payload = self._write_payload(
                project_root / "create_pending.json",
                {
                    "id": "exp-20260422-001",
                    "failure_kind": "api_failure",
                    "failure_signal_source": "api_response",
                    "work_domain": "api-integration",
                    "pattern_guess": "request_schema_mismatch",
                    "root_cause_guess": "payload built from outdated assumptions",
                    "summary": "API request failed with invalid field error",
                    "scene": "Agent called external API during task execution",
                    "error_text": "400 invalid_request_error: unknown field",
                    "raw_feedback": None,
                    "feedback_hint": None,
                },
            )
            create = self._run("create_pending.py", project_root, ["--input", str(create_payload)])
            self.assertEqual(create.returncode, 0, msg=create.stderr)

            attempt_payload = self._write_payload(
                project_root / "append_attempt.json",
                {
                    "action": "checked official API docs and removed unsupported field",
                    "result": "signal",
                    "note": "docs show field is not supported",
                },
            )
            result = self._run(
                "append_attempt.py",
                project_root,
                ["--event-id", "exp-20260422-001", "--input", str(attempt_payload)],
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            attempts_path = project_root / ".explib" / "pending" / "events" / "exp-20260422-001" / "attempts.jsonl"
            lines = attempts_path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(json.loads(lines[0])["result"], "signal")

    def test_promote_pending_creates_resolved_entry_updates_index_and_removes_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            self._init(project_root)

            create_payload = self._write_payload(
                project_root / "create_pending.json",
                {
                    "id": "exp-20260422-001",
                    "failure_kind": "api_failure",
                    "failure_signal_source": "api_response",
                    "work_domain": "api-integration",
                    "pattern_guess": "request_schema_mismatch",
                    "root_cause_guess": "payload built from outdated assumptions",
                    "summary": "API request failed with invalid field error",
                    "scene": "Agent called external API during task execution",
                    "error_text": "400 invalid_request_error: unknown field",
                    "raw_feedback": None,
                    "feedback_hint": None,
                },
            )
            create = self._run("create_pending.py", project_root, ["--input", str(create_payload)])
            self.assertEqual(create.returncode, 0, msg=create.stderr)

            promote_payload = self._write_payload(
                project_root / "promote_pending.json",
                {
                    "promotion_reason": "Repeated investigation isolated the root cause and verified the reusable outcome",
                    "verification_summary": [
                        "initial request failed consistently",
                        "official docs confirmed unsupported field",
                        "minimal valid payload succeeded after field removal",
                    ],
                    "open_questions": [],
                    "evidence_refs": [
                        {
                            "ref_type": "official_doc",
                            "ref": "https://example.com/api/docs",
                            "note": "field is not supported",
                        }
                    ],
                    "proposed_entries": [
                        {
                            "id": "api-integration-resolved-001",
                            "kind": "resolved",
                            "failure_kind": "api_failure",
                            "work_domain": "api-integration",
                            "pattern_name": "Request schema mismatch on API call",
                            "summary": "API request fails because fields do not match the documented schema",
                            "recognition_signals": [
                                "400 invalid_request_error",
                                "unknown field",
                            ],
                            "root_cause": "Payload was built from outdated assumptions",
                            "evidence_refs": [],
                            "solution_steps": [
                                "Check the official schema",
                                "Reduce to a minimal valid payload",
                            ],
                            "avoidance_notes": [
                                "Do not guess schema from memory",
                            ],
                        }
                    ],
                },
            )
            result = self._run(
                "promote_pending.py",
                project_root,
                ["--event-id", "exp-20260422-001", "--input", str(promote_payload)],
            )
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            entry_path = project_root / ".explib" / "resolved" / "api-integration" / "api-integration-resolved-001.json"
            index_path = project_root / ".explib" / "domains" / "api-integration" / "toc.index.json"
            toc_path = project_root / ".explib" / "domains" / "api-integration" / "TOC.md"
            event_dir = project_root / ".explib" / "pending" / "events" / "exp-20260422-001"
            self.assertTrue(entry_path.is_file())
            self.assertTrue(index_path.is_file())
            self.assertIn("api-integration-resolved-001", toc_path.read_text(encoding="utf-8"))
            self.assertFalse(event_dir.exists())
            self.assertEqual(payload["promoted_entries"][0]["id"], "api-integration-resolved-001")

    def test_abandon_pending_removes_event_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            self._init(project_root)

            create_payload = self._write_payload(
                project_root / "create_pending.json",
                {
                    "id": "exp-20260422-001",
                    "failure_kind": "api_failure",
                    "failure_signal_source": "api_response",
                    "work_domain": "api-integration",
                    "pattern_guess": "request_schema_mismatch",
                    "root_cause_guess": "payload built from outdated assumptions",
                    "summary": "API request failed with invalid field error",
                    "scene": "Agent called external API during task execution",
                    "error_text": "400 invalid_request_error: unknown field",
                    "raw_feedback": None,
                    "feedback_hint": None,
                },
            )
            create = self._run("create_pending.py", project_root, ["--input", str(create_payload)])
            self.assertEqual(create.returncode, 0, msg=create.stderr)

            result = self._run("abandon_pending.py", project_root, ["--event-id", "exp-20260422-001"])
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            event_dir = project_root / ".explib" / "pending" / "events" / "exp-20260422-001"
            self.assertFalse(event_dir.exists())

    def test_delete_dead_end_removes_entry_and_updates_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            self._init(project_root)

            create_payload = self._write_payload(
                project_root / "create_pending.json",
                {
                    "id": "exp-20260422-001",
                    "failure_kind": "quality_failure",
                    "failure_signal_source": "user_feedback",
                    "work_domain": "frontend-ui",
                    "pattern_guess": "blind_timeout_increase",
                    "root_cause_guess": "trying cosmetic tuning before structural fix",
                    "summary": "Repeated cosmetic tuning did not improve layout quality",
                    "scene": "Agent revised UI styling after negative feedback",
                    "error_text": "",
                    "raw_feedback": "still feels generic",
                    "feedback_hint": "low_quality",
                },
            )
            create = self._run("create_pending.py", project_root, ["--input", str(create_payload)])
            self.assertEqual(create.returncode, 0, msg=create.stderr)

            promote_payload = self._write_payload(
                project_root / "promote_dead_end.json",
                {
                    "promotion_reason": "Repeated attempts showed this path should not continue",
                    "verification_summary": [
                        "multiple cosmetic passes did not improve the layout",
                        "feedback remained low quality",
                    ],
                    "open_questions": [],
                    "evidence_refs": [],
                    "proposed_entries": [
                        {
                            "id": "frontend-ui-dead-end-001",
                            "kind": "dead-end",
                            "failure_kind": "quality_failure",
                            "work_domain": "frontend-ui",
                            "pattern_name": "Blind timeout increase",
                            "summary": "Cosmetic-only revisions do not fix a structurally weak layout",
                            "recognition_signals": [
                                "still feels generic",
                                "multiple cosmetic revisions",
                            ],
                            "root_cause": "The problem is structural, not decorative",
                            "evidence_refs": [],
                            "why_this_path_fails": "The UI remains weak because hierarchy and composition are unchanged",
                            "recommended_pivot": [
                                "rework layout structure first",
                                "change type scale and spacing before color tuning",
                            ],
                        }
                    ],
                },
            )
            promote = self._run(
                "promote_pending.py",
                project_root,
                ["--event-id", "exp-20260422-001", "--input", str(promote_payload)],
            )
            self.assertEqual(promote.returncode, 0, msg=promote.stderr)

            result = self._run(
                "delete_dead_end.py",
                project_root,
                ["--entry-id", "frontend-ui-dead-end-001"],
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            entry_path = project_root / ".explib" / "dead-ends" / "frontend-ui" / "frontend-ui-dead-end-001.json"
            index_path = project_root / ".explib" / "domains" / "frontend-ui" / "toc.index.json"
            self.assertFalse(entry_path.exists())
            index_data = json.loads(index_path.read_text(encoding="utf-8"))
            self.assertEqual(index_data["dead_ends"], [])


if __name__ == "__main__":
    unittest.main()
