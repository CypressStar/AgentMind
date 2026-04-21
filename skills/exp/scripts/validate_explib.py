import argparse
import json
from pathlib import Path

from _shared_paths import get_root
from _shared_render import render_domain_toc
from _shared_taxonomy import WORK_DOMAINS
from _shared_validate import make_issue


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".explib")
    return parser.parse_args()


def main():
    args = parse_args()
    root = get_root(args.root)
    issues = []

    required_files = [
        root / "EXP.md",
        root / "pending" / "TOC.md",
        root / "resolved" / "TOC.md",
        root / "dead-ends" / "TOC.md",
    ]
    for path in required_files:
        if not path.is_file():
            issues.append(
                make_issue(
                    "error",
                    "missing_required_file",
                    path.as_posix(),
                    "Required file is missing",
                    ai_action="run_init",
                )
            )

    for domain in WORK_DOMAINS:
        toc_path = root / "domains" / domain / "TOC.md"
        if not toc_path.is_file():
            issues.append(
                make_issue(
                    "error",
                    "missing_domain_toc",
                    toc_path.as_posix(),
                    "Domain TOC file is missing",
                )
            )

        index_path = root / "domains" / domain / "toc.index.json"
        if not index_path.is_file():
            issues.append(
                make_issue(
                    "error",
                    "missing_toc_index",
                    index_path.as_posix(),
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
                    index_path.as_posix(),
                    "Domain index file is not valid JSON",
                )
            )
            continue

        if not isinstance(index_data, dict) or not isinstance(index_data.get("domain"), str) or not isinstance(index_data.get("resolved"), list) or not isinstance(index_data.get("dead_ends"), list):
            issues.append(
                make_issue(
                    "error",
                    "invalid_index_json",
                    index_path.as_posix(),
                    "Domain index file does not match the expected schema",
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
                        toc_path.as_posix(),
                        "Domain TOC does not match the rendered index",
                    )
                )

    payload = {
        "ok": not issues,
        "code": "ok" if not issues else "validation_failed",
        "action": "validate_explib",
        "root": root.as_posix(),
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
