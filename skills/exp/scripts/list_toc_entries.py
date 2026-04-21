import argparse
import json

from _shared_index import load_domain_index
from _shared_paths import get_root


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".explib")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--section", choices=["resolved", "dead_end"])
    parser.add_argument("--failure-kind")
    return parser.parse_args()


def main():
    args = parse_args()
    root = get_root(args.root)
    index_path = root / "domains" / args.domain / "toc.index.json"
    data = load_domain_index(index_path)

    entries = []
    if args.section in (None, "resolved"):
        for item in data["resolved"]:
            enriched = dict(item)
            enriched["kind"] = "resolved"
            entries.append(enriched)
    if args.section in (None, "dead_end"):
        for item in data["dead_ends"]:
            enriched = dict(item)
            enriched["kind"] = "dead_end"
            entries.append(enriched)

    if args.failure_kind:
        entries = [item for item in entries if item["failure_kind"] == args.failure_kind]

    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "list_toc_entries",
        "root": root.as_posix(),
        "domain": args.domain,
        "section": args.section,
        "filters": {"failure_kind": args.failure_kind},
        "entries": entries,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
