import json


def load_domain_index(path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_domain_index(data: dict) -> dict:
    return {
        "domain": data["domain"],
        "resolved": sorted(data["resolved"], key=lambda item: item["id"]),
        "dead_ends": sorted(data["dead_ends"], key=lambda item: item["id"]),
    }


def save_domain_index(path, data: dict) -> None:
    normalized = normalize_domain_index(data)
    path.write_text(
        json.dumps(normalized, indent=2) + "\n",
        encoding="utf-8",
    )
