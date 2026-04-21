def render_domain_description(domain: str) -> str:
    return f"Use this file to route solved and dead-end experience for {domain} work."


def render_domain_toc(index_data: dict) -> str:
    domain = index_data["domain"]
    return f"""# {domain} TOC

> Generated from `toc.index.json`. Do not edit manually.

{render_domain_description(domain)}

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
"""
