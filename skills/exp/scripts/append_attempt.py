import argparse
import json
from pathlib import Path

from _shared_paths import get_explib_root, get_pending_event_dir, get_project_root, to_project_relative
from _shared_taxonomy import ATTEMPT_RESULTS


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root")
    parser.add_argument("--event-id", required=True)
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
        "action": "append_attempt",
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

    if payload["result"] not in ATTEMPT_RESULTS:
        return fail(project_root, "invalid_payload", "attempt result is invalid")

    event_dir = get_pending_event_dir(project_root, args.event_id)
    event_path = event_dir / "event.json"
    attempts_path = event_dir / "attempts.jsonl"
    if not event_path.is_file():
        return fail(project_root, "event_not_found", "pending event does not exist")

    with attempts_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")

    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "append_attempt",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "event_id": args.event_id,
        "attempts_path": to_project_relative(attempts_path, project_root),
        "updated_files": [to_project_relative(attempts_path, project_root)],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
