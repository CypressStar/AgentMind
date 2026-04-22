import argparse
import json

from _shared_paths import get_explib_root, get_project_root, to_project_relative
from _shared_render import render_domain_toc
from _shared_taxonomy import WORK_DOMAINS
from _shared_templates import (
    render_dead_ends_toc,
    empty_domain_index,
    render_exp_md,
    render_pending_toc,
    render_resolved_toc,
)
from _shared_index import load_domain_index, save_domain_index


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    project_root = get_project_root(args.project_root)
    explib_root = get_explib_root(project_root)

    required_dirs = [
        explib_root,
        explib_root / "pending",
        explib_root / "resolved",
        explib_root / "dead-ends",
        explib_root / "domains",
    ] + [explib_root / "domains" / name for name in WORK_DOMAINS]

    required_files = {
        explib_root / "EXP.md": render_exp_md(),
        explib_root / "pending" / "TOC.md": render_pending_toc(),
        explib_root / "resolved" / "TOC.md": render_resolved_toc(),
        explib_root / "dead-ends" / "TOC.md": render_dead_ends_toc(),
    }
    required_domain_index_files = [
        explib_root / "domains" / domain / "toc.index.json" for domain in WORK_DOMAINS
    ]
    required_domain_toc_files = [explib_root / "domains" / domain / "TOC.md" for domain in WORK_DOMAINS]

    created_dirs = []
    missing_dirs = []
    created_files = []
    missing_files = []
    created_index_files = []
    rendered_tocs = []

    if args.check:
        for path in required_dirs:
            if not path.exists():
                missing_dirs.append(to_project_relative(path, project_root))
        for path, content in required_files.items():
            if not path.is_file():
                missing_files.append(to_project_relative(path, project_root))
            elif path.read_text(encoding="utf-8") != content:
                missing_files.append(to_project_relative(path, project_root))
        for path in required_domain_index_files:
            if not path.is_file():
                missing_files.append(to_project_relative(path, project_root))
        for domain, path in zip(WORK_DOMAINS, required_domain_toc_files):
            if not path.is_file():
                missing_files.append(to_project_relative(path, project_root))
                continue
            index_path = explib_root / "domains" / domain / "toc.index.json"
            if not index_path.is_file():
                continue
            try:
                index_data = load_domain_index(index_path)
                rendered = render_domain_toc(index_data)
            except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
                missing_files.append(to_project_relative(index_path, project_root))
                continue
            if path.read_text(encoding="utf-8") != rendered:
                missing_files.append(to_project_relative(path, project_root))
        code = "ok" if not missing_dirs and not missing_files else "validation_failed"
        ok = code == "ok"
        print(
            json.dumps(
                {
                    "ok": ok,
                    "code": code,
                    "action": "init_explib",
                    "project_root": project_root.as_posix(),
                    "explib_root": explib_root.as_posix(),
                    "mode": "check",
                    "missing_dirs": missing_dirs,
                    "missing_files": missing_files,
                }
            )
        )
        return 0 if ok else 1

    for path in required_dirs:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(to_project_relative(path, project_root))

    for path, content in required_files.items():
        if not path.is_file():
            path.write_text(content, encoding="utf-8")
            created_files.append(to_project_relative(path, project_root))
        elif path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")

    for domain in WORK_DOMAINS:
        index_path = explib_root / "domains" / domain / "toc.index.json"
        if not index_path.is_file():
            save_domain_index(index_path, empty_domain_index(domain))
            created_index_files.append(to_project_relative(index_path, project_root))
        try:
            index_data = load_domain_index(index_path)
            rendered = render_domain_toc(index_data)
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
            missing_files.append(to_project_relative(index_path, project_root))
            continue
        toc_path = explib_root / "domains" / domain / "TOC.md"
        current = toc_path.read_text(encoding="utf-8") if toc_path.exists() else None
        if current != rendered:
            toc_path.write_text(rendered, encoding="utf-8")
            rendered_tocs.append(to_project_relative(toc_path, project_root))

    if missing_files:
        print(
            json.dumps(
                {
                    "ok": False,
                    "code": "validation_failed",
                    "action": "init_explib",
                    "project_root": project_root.as_posix(),
                    "explib_root": explib_root.as_posix(),
                    "mode": "init",
                    "created_dirs": created_dirs,
                    "created_files": created_files,
                    "created_index_files": created_index_files,
                    "rendered_tocs": rendered_tocs,
                    "missing_files": missing_files,
                }
            )
        )
        return 1

    print(
        json.dumps(
            {
                "ok": True,
                "code": "ok",
                "action": "init_explib",
                "project_root": project_root.as_posix(),
                "explib_root": explib_root.as_posix(),
                "mode": "init",
                "created_dirs": created_dirs,
                "created_files": created_files,
                "created_index_files": created_index_files,
                "rendered_tocs": rendered_tocs,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
