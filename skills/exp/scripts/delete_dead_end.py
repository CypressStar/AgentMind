import argparse
import json

from _shared_index import load_domain_index, save_domain_index
from _shared_paths import get_domain_index_path, get_domain_toc_path, get_explib_root, get_project_root, to_project_relative
from _shared_render import render_domain_toc


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root")
    parser.add_argument("--entry-id", required=True)
    return parser.parse_args()


def fail(project_root, code: str, message: str) -> int:
    explib_root = get_explib_root(project_root)
    print(json.dumps({
        "ok": False,
        "code": code,
        "action": "delete_dead_end",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "message": message,
    }))
    return 1


def main():
    args = parse_args()
    project_root = get_project_root(args.project_root)
    explib_root = get_explib_root(project_root)
    matches = list(explib_root.glob(f"dead-ends/*/{args.entry_id}.json"))
    if not matches:
        return fail(project_root, "entry_not_found", "dead-end entry does not exist")
    if len(matches) > 1:
        return fail(project_root, "ambiguous_id", "multiple dead-end entries match this id")

    entry_path = matches[0]
    domain = entry_path.parent.name
    index_path = get_domain_index_path(project_root, domain)
    index_data = load_domain_index(index_path)
    before = len(index_data["dead_ends"])
    index_data["dead_ends"] = [item for item in index_data["dead_ends"] if item["id"] != args.entry_id]
    if len(index_data["dead_ends"]) == before:
        return fail(project_root, "invalid_state", "entry is missing from the domain index")

    entry_path.unlink()
    save_domain_index(index_path, index_data)
    toc_path = get_domain_toc_path(project_root, domain)
    toc_path.write_text(render_domain_toc(index_data), encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "delete_dead_end",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "entry_id": args.entry_id,
        "removed_paths": [to_project_relative(entry_path, project_root)],
        "updated_files": [
            to_project_relative(index_path, project_root),
            to_project_relative(toc_path, project_root),
        ],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
