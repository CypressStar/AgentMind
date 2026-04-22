import argparse
import json
import shutil

from _shared_paths import get_explib_root, get_pending_event_dir, get_project_root, to_project_relative


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root")
    parser.add_argument("--event-id", required=True)
    return parser.parse_args()


def fail(project_root, code: str, message: str) -> int:
    explib_root = get_explib_root(project_root)
    print(json.dumps({
        "ok": False,
        "code": code,
        "action": "abandon_pending",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "message": message,
    }))
    return 1


def main():
    args = parse_args()
    project_root = get_project_root(args.project_root)
    explib_root = get_explib_root(project_root)
    event_dir = get_pending_event_dir(project_root, args.event_id)
    if not event_dir.is_dir():
        return fail(project_root, "event_not_found", "pending event does not exist")

    shutil.rmtree(event_dir)
    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "abandon_pending",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "event_id": args.event_id,
        "removed_paths": [to_project_relative(event_dir, project_root)],
        "updated_files": [],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
