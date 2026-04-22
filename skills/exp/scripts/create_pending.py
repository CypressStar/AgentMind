import argparse
import json
from pathlib import Path

from _shared_paths import get_explib_root, get_pending_event_dir, get_project_root, to_project_relative
from _shared_taxonomy import ATTEMPT_RESULTS, FAILURE_KINDS, FAILURE_SIGNAL_SOURCES, FEEDBACK_HINTS, WORK_DOMAINS


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root")
    parser.add_argument("--input", required=True)
    return parser.parse_args()


def load_payload(input_arg: str) -> dict:
    if input_arg == "-":
        return json.loads(input())
    return json.loads(Path(input_arg).read_text(encoding="utf-8"))


def fail(project_root: Path, code: str, message: str) -> int:
    explib_root = get_explib_root(project_root)
    print(json.dumps({
        "ok": False,
        "code": code,
        "action": "create_pending",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "message": message,
    }))
    return 1


def main():
    args = parse_args()
    project_root = get_project_root(args.project_root)
    explib_root = get_explib_root(project_root)
    payload = load_payload(args.input)

    if payload["failure_kind"] not in FAILURE_KINDS:
        return fail(project_root, "invalid_payload", "failure_kind is invalid")
    if payload["failure_signal_source"] not in FAILURE_SIGNAL_SOURCES:
        return fail(project_root, "invalid_payload", "failure_signal_source is invalid")
    if payload["work_domain"] not in WORK_DOMAINS:
        return fail(project_root, "invalid_payload", "work_domain is invalid")
    if payload.get("feedback_hint") is not None and payload["feedback_hint"] not in FEEDBACK_HINTS:
        return fail(project_root, "invalid_payload", "feedback_hint is invalid")
    if payload.get("initial_attempt") and payload["initial_attempt"]["result"] not in ATTEMPT_RESULTS:
        return fail(project_root, "invalid_payload", "initial_attempt.result is invalid")

    if not (explib_root / "EXP.md").is_file():
        return fail(project_root, "invalid_state", ".explib is not initialized")

    event_dir = get_pending_event_dir(project_root, payload["id"])
    if event_dir.exists():
        return fail(project_root, "already_exists", "pending event already exists")

    event_dir.mkdir(parents=True, exist_ok=True)
    event_path = event_dir / "event.json"
    attempts_path = event_dir / "attempts.jsonl"

    event_doc = {
        "id": payload["id"],
        "status": "pending",
        "failure_kind": payload["failure_kind"],
        "failure_signal_source": payload["failure_signal_source"],
        "work_domain": payload["work_domain"],
        "pattern_guess": payload.get("pattern_guess"),
        "root_cause_guess": payload.get("root_cause_guess"),
        "summary": payload["summary"],
        "scene": payload["scene"],
        "error_text": payload.get("error_text", ""),
        "raw_feedback": payload.get("raw_feedback"),
        "feedback_hint": payload.get("feedback_hint"),
    }
    event_path.write_text(json.dumps(event_doc, indent=2) + "\n", encoding="utf-8")

    updated_files = [to_project_relative(event_path, project_root)]
    if payload.get("initial_attempt"):
        attempts_path.write_text(json.dumps(payload["initial_attempt"]) + "\n", encoding="utf-8")
        updated_files.append(to_project_relative(attempts_path, project_root))

    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "create_pending",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "event_id": payload["id"],
        "event_path": to_project_relative(event_path, project_root),
        "attempts_path": to_project_relative(attempts_path, project_root),
        "updated_files": updated_files,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
