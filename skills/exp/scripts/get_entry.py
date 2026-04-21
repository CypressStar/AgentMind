import argparse
import json
from pathlib import Path

from _shared_paths import get_root


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".explib")
    parser.add_argument("--id", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    root = get_root(args.root)
    matches = list(root.glob(f"resolved/*/{args.id}.json")) + list(root.glob(f"dead-ends/*/{args.id}.json"))
    if not matches:
        print(json.dumps({
            "ok": False,
            "code": "not_found",
            "action": "get_entry",
            "root": root.as_posix(),
            "id": args.id,
        }))
        return 1
    if len(matches) > 1:
        print(json.dumps({
            "ok": False,
            "code": "ambiguous_id",
            "action": "get_entry",
            "root": root.as_posix(),
            "id": args.id,
        }))
        return 1

    path = matches[0]
    entry = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "get_entry",
        "root": root.as_posix(),
        "id": args.id,
        "entry_path": path.as_posix(),
        "kind": entry["kind"],
        "work_domain": entry["work_domain"],
        "failure_kind": entry["failure_kind"],
        "entry": entry,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
