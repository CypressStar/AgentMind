import argparse
import json
import shutil
from pathlib import Path

from _shared_index import load_domain_index, save_domain_index
from _shared_paths import (
    get_domain_index_path,
    get_domain_toc_path,
    get_entry_path,
    get_explib_root,
    get_pending_event_dir,
    get_project_root,
    to_project_relative,
)
from _shared_render import render_domain_toc
from _shared_taxonomy import FAILURE_KINDS, REF_TYPES, WORK_DOMAINS


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
        "action": "promote_pending",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "message": message,
    }))
    return 1


def _validate_evidence_refs(refs: list[dict]) -> bool:
    return all(isinstance(ref, dict) and ref.get("ref_type") in REF_TYPES for ref in refs)


def _build_index_item(project_root: Path, entry: dict) -> dict:
    return {
        "id": entry["id"],
        "pattern_name": entry["pattern_name"],
        "failure_kind": entry["failure_kind"],
        "signals": entry.get("recognition_signals", [])[:2],
        "note": entry["summary"],
        "entry_path": to_project_relative(
            get_entry_path(project_root, entry["kind"], entry["work_domain"], entry["id"]),
            project_root,
        ),
    }


def main():
    args = parse_args()
    project_root = get_project_root(args.project_root)
    explib_root = get_explib_root(project_root)
    payload = load_payload(args.input)

    event_dir = get_pending_event_dir(project_root, args.event_id)
    event_path = event_dir / "event.json"
    if not event_path.is_file():
        return fail(project_root, "event_not_found", "pending event does not exist")

    proposed_entries = payload.get("proposed_entries", [])
    if len(proposed_entries) > 3:
        return fail(project_root, "too_many_proposed_entries", "too many proposed entries")

    for entry in proposed_entries:
        if entry["kind"] not in {"resolved", "dead-end"}:
            return fail(project_root, "invalid_payload", "entry kind is invalid")
        if entry["failure_kind"] not in FAILURE_KINDS:
            return fail(project_root, "invalid_payload", "entry failure_kind is invalid")
        if entry["work_domain"] not in WORK_DOMAINS:
            return fail(project_root, "invalid_payload", "entry work_domain is invalid")
        if not _validate_evidence_refs(entry.get("evidence_refs", [])):
            return fail(project_root, "invalid_payload", "entry evidence_refs are invalid")
        if entry["kind"] == "resolved":
            if "solution_steps" not in entry or "avoidance_notes" not in entry:
                return fail(project_root, "invalid_payload", "resolved entry fields are incomplete")
        if entry["kind"] == "dead-end":
            if "why_this_path_fails" not in entry or "recommended_pivot" not in entry:
                return fail(project_root, "invalid_payload", "dead-end entry fields are incomplete")

    index_updates: dict[str, dict] = {}
    for entry in proposed_entries:
        domain = entry["work_domain"]
        index_path = get_domain_index_path(project_root, domain)
        if not index_path.is_file():
            return fail(project_root, "invalid_state", "domain index is missing")
        index_data = index_updates.get(domain) or load_domain_index(index_path)

        target_key = "resolved" if entry["kind"] == "resolved" else "dead_ends"
        other_key = "dead_ends" if target_key == "resolved" else "resolved"
        if any(item["id"] == entry["id"] for item in index_data[other_key]):
            return fail(project_root, "invalid_transition", "entry id exists in the wrong section")

        item = _build_index_item(project_root, entry)
        updated = False
        for idx, existing in enumerate(index_data[target_key]):
            if existing["id"] == entry["id"]:
                index_data[target_key][idx] = item
                updated = True
                break
        if not updated:
            index_data[target_key].append(item)
        index_updates[domain] = index_data

    updated_files = []
    promoted_entries = []
    for entry in proposed_entries:
        entry_path = get_entry_path(project_root, entry["kind"], entry["work_domain"], entry["id"])
        entry_path.parent.mkdir(parents=True, exist_ok=True)
        entry_path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
        updated_files.append(to_project_relative(entry_path, project_root))
        promoted_entries.append({
            "id": entry["id"],
            "kind": entry["kind"],
            "path": to_project_relative(entry_path, project_root),
        })

    for domain, index_data in index_updates.items():
        index_path = get_domain_index_path(project_root, domain)
        save_domain_index(index_path, index_data)
        toc_path = get_domain_toc_path(project_root, domain)
        toc_path.write_text(render_domain_toc(index_data), encoding="utf-8")
        updated_files.append(to_project_relative(index_path, project_root))
        updated_files.append(to_project_relative(toc_path, project_root))

    shutil.rmtree(event_dir)

    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "promote_pending",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "event_id": args.event_id,
        "promoted_entries": promoted_entries,
        "updated_files": updated_files,
        "removed_paths": [to_project_relative(event_dir, project_root)],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
