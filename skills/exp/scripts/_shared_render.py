def render_domain_description(domain: str) -> str:
    return f"Use this file to route solved and dead-end experience for {domain} work."


def _escape_cell(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ").replace("|", "\\|").strip()


def _render_signals(entry: dict) -> str:
    signals = entry.get("signals", [])
    if isinstance(signals, list):
        return _escape_cell(", ".join(str(value) for value in signals[:2]))
    return _escape_cell(str(signals))


def _render_rows(entries: list[dict], base_dir: str, domain: str) -> str:
    rows = []
    for entry in entries:
        entry_id = str(entry.get("id", ""))
        pattern_name = _escape_cell(str(entry.get("pattern_name", "")))
        failure_kind = str(entry.get("failure_kind", ""))
        signals = _render_signals(entry)
        note = _escape_cell(str(entry.get("note", "")))
        row = (
            f"| {entry_id} | [{pattern_name}](../../{base_dir}/{domain}/{entry_id}.json) "
            f"| {failure_kind} | {signals} | {note} |"
        )
        rows.append(row)
    return "\n".join(rows)


def render_domain_toc(index_data: dict) -> str:
    domain = index_data["domain"]
    resolved_rows = _render_rows(index_data.get("resolved", []), "resolved", domain)
    dead_end_rows = _render_rows(index_data.get("dead_ends", []), "dead-ends", domain)
    return f"""# {domain} TOC

> Generated from `toc.index.json`. Do not edit manually.

{render_domain_description(domain)}

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
{resolved_rows}

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
{dead_end_rows}
"""
