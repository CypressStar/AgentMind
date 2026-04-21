import argparse
import json

from _shared_paths import get_root
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
    parser.add_argument("--root", default=".explib")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    root = get_root(args.root)

    required_dirs = [
        root,
        root / "pending",
        root / "resolved",
        root / "dead-ends",
        root / "domains",
    ] + [root / "domains" / name for name in WORK_DOMAINS]

    required_files = {
        root / "EXP.md": render_exp_md(),
        root / "pending" / "TOC.md": render_pending_toc(),
        root / "resolved" / "TOC.md": render_resolved_toc(),
        root / "dead-ends" / "TOC.md": render_dead_ends_toc(),
    }
    required_domain_index_files = [
        root / "domains" / domain / "toc.index.json" for domain in WORK_DOMAINS
    ]
    required_domain_toc_files = [root / "domains" / domain / "TOC.md" for domain in WORK_DOMAINS]

    created_dirs = []
    missing_dirs = []
    created_files = []
    missing_files = []
    created_index_files = []
    rendered_tocs = []

    if args.check:
        for path in required_dirs:
            if not path.exists():
                missing_dirs.append(path.as_posix())
        for path, content in required_files.items():
            if not path.is_file():
                missing_files.append(path.as_posix())
            elif path.read_text(encoding="utf-8") != content:
                missing_files.append(path.as_posix())
        for path in required_domain_index_files:
            if not path.is_file():
                missing_files.append(path.as_posix())
        for domain, path in zip(WORK_DOMAINS, required_domain_toc_files):
            if not path.is_file():
                missing_files.append(path.as_posix())
                continue
            index_path = root / "domains" / domain / "toc.index.json"
            if not index_path.is_file():
                continue
            try:
                index_data = load_domain_index(index_path)
            except json.JSONDecodeError:
                missing_files.append(index_path.as_posix())
                continue
            if path.read_text(encoding="utf-8") != render_domain_toc(index_data):
                missing_files.append(path.as_posix())
        code = "ok" if not missing_dirs and not missing_files else "validation_failed"
        ok = code == "ok"
        print(
            json.dumps(
                {
                    "ok": ok,
                    "code": code,
                    "action": "init_explib",
                    "root": root.as_posix(),
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
            created_dirs.append(path.as_posix())

    for path, content in required_files.items():
        if not path.is_file():
            path.write_text(content, encoding="utf-8")
            created_files.append(path.as_posix())
        elif path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")

    for domain in WORK_DOMAINS:
        index_path = root / "domains" / domain / "toc.index.json"
        if not index_path.is_file():
            save_domain_index(index_path, empty_domain_index(domain))
            created_index_files.append(index_path.as_posix())
        index_data = load_domain_index(index_path)
        toc_path = root / "domains" / domain / "TOC.md"
        rendered = render_domain_toc(index_data)
        current = toc_path.read_text(encoding="utf-8") if toc_path.exists() else None
        if current != rendered:
            toc_path.write_text(rendered, encoding="utf-8")
            rendered_tocs.append(toc_path.as_posix())

    print(
        json.dumps(
            {
                "ok": True,
                "code": "ok",
                "action": "init_explib",
                "root": root.as_posix(),
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
