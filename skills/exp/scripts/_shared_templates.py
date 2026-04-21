try:
    from ._shared_taxonomy import FAILURE_KINDS, FAILURE_SIGNAL_SOURCES, WORK_DOMAINS
except ImportError:  # Script-mode import from skills/exp/scripts/
    from _shared_taxonomy import FAILURE_KINDS, FAILURE_SIGNAL_SOURCES, WORK_DOMAINS


def render_exp_md() -> str:
    work_domain_lines = "\n".join(
        f"- [`{name}`](domains/{name}/TOC.md)" for name in WORK_DOMAINS
    )
    failure_kind_lines = "\n".join(f"- `{name}`" for name in FAILURE_KINDS)
    signal_lines = "\n".join(f"- `{name}`" for name in FAILURE_SIGNAL_SOURCES)
    return f"""# EXP

## Overview

`EXP` is a passive, post-failure experience library. It is used after a clear failure or when the user explicitly asks to review existing experience. It is not a proactive checklist, not a memory replacement, and not a general logging store.

## Flow

1. Detect a clear failure.
2. Split the problem into failure clusters.
3. Route into one `work_domain`.
4. Read the matching domain `TOC.md`.
5. Read a small number of formal entries.
6. If no formal hit exists, failure-handling mode may consult one similar `pending` item.

## Failure Kinds

{failure_kind_lines}

## Failure Signal Sources

{signal_lines}

## Work Domains

{work_domain_lines}

## Rules

- Use `EXP` only after a clear failure, or in explicit user-requested review mode.
- Do not create new top-level classes.
- Do not create new `work_domain` values.
- If a failure does not map to the closed taxonomy, do not store it in `EXP`.
- Do not save external evidence snapshots.

## Manual Taxonomy Extension

Only the user may add or revise taxonomy. If taxonomy changes, update this file, the relevant TOCs, and `skills/exp/SKILL.md` together.
"""


def empty_domain_index(domain: str) -> dict:
    return {"domain": domain, "resolved": [], "dead_ends": []}


def render_pending_toc() -> str:
    return """# Pending TOC

Use this file to track unresolved items that may be useful in later failure-handling.

## Rules

- Pending items are unresolved and should not be treated as proven fixes.
- Keep entries concise so they are easy to scan during failure triage.
- Prefer lazy event capture: only add an event when it materially improves future debugging.

## Events

See `pending/events/` for event snapshots captured only when needed.
"""


def render_resolved_toc() -> str:
    domain_rows = "\n".join(
        f"| `{domain}` | [TOC](../domains/{domain}/TOC.md) |" for domain in WORK_DOMAINS
    )
    return f"""# Resolved TOC

Resolved patterns are routed by `work_domain`.

| work_domain | domain_toc |
| --- | --- |
{domain_rows}
"""


def render_dead_ends_toc() -> str:
    domain_rows = "\n".join(
        f"| `{domain}` | [TOC](../domains/{domain}/TOC.md) |" for domain in WORK_DOMAINS
    )
    return f"""# Dead Ends TOC

Dead ends are routed by `work_domain`.

| work_domain | domain_toc |
| --- | --- |
{domain_rows}
"""
