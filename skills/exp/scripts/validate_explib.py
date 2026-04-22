import argparse
import json

from _shared_paths import get_explib_root, get_project_root, to_project_relative
from _shared_render import render_domain_toc
from _shared_taxonomy import WORK_DOMAINS
from _shared_validate import make_issue


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root")
    return parser.parse_args()


def main():
    args = parse_args()
    project_root = get_project_root(args.project_root)
    explib_root = get_explib_root(project_root)
    issues = []

    required_files = [
        explib_root / "EXP.md",
        explib_root / "pending" / "TOC.md",
        explib_root / "resolved" / "TOC.md",
        explib_root / "dead-ends" / "TOC.md",
    ]
    for path in required_files:
        if not path.is_file():
            issues.append(
                make_issue(
                    "error",
                    "missing_required_file",
                    to_project_relative(path, project_root),
                    "Required file is missing",
                    ai_action="run_init",
                )
            )

    for domain in WORK_DOMAINS:
        toc_path = explib_root / "domains" / domain / "TOC.md"
        if not toc_path.is_file():
            issues.append(
                make_issue(
                    "error",
                    "missing_domain_toc",
                    to_project_relative(toc_path, project_root),
                    "Domain TOC file is missing",
                )
            )

        index_path = explib_root / "domains" / domain / "toc.index.json"
        if not index_path.is_file():
            issues.append(
                make_issue(
                    "error",
                    "missing_toc_index",
                    to_project_relative(index_path, project_root),
                    "Domain index file is missing",
                )
            )
            continue

        try:
            index_data = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            issues.append(
                make_issue(
                    "error",
                    "invalid_index_json",
                    to_project_relative(index_path, project_root),
                    "Domain index file is not valid JSON",
                )
            )
            continue

        if not isinstance(index_data, dict) or not isinstance(index_data.get("domain"), str) or not isinstance(index_data.get("resolved"), list) or not isinstance(index_data.get("dead_ends"), list):
            issues.append(
                make_issue(
                    "error",
                    "invalid_index_json",
                    to_project_relative(index_path, project_root),
                    "Domain index file does not match the expected schema",
                )
            )
            continue

        if any(not isinstance(item, dict) for item in index_data["resolved"]) or any(
            not isinstance(item, dict) for item in index_data["dead_ends"]
        ):
            issues.append(
                make_issue(
                    "error",
                    "invalid_index_json",
                    to_project_relative(index_path, project_root),
                    "Domain index file entries must be objects",
                )
            )
            continue

        if toc_path.is_file():
            expected_toc = render_domain_toc(index_data)
            actual_toc = toc_path.read_text(encoding="utf-8")
            if actual_toc != expected_toc:
                issues.append(
                    make_issue(
                        "error",
                        "toc_render_out_of_sync",
                        to_project_relative(toc_path, project_root),
                        "Domain TOC does not match the rendered index",
                    )
                )

    payload = {
        "ok": not issues,
        "code": "ok" if not issues else "validation_failed",
        "action": "validate_explib",
        "project_root": project_root.as_posix(),
        "explib_root": explib_root.as_posix(),
        "summary": {
            "error_count": sum(1 for issue in issues if issue["level"] == "error"),
            "warning_count": sum(1 for issue in issues if issue["level"] == "warning"),
        },
        "issues": issues,
    }
    print(json.dumps(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
