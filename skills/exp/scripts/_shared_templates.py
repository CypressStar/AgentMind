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

This file is a lightweight note for unresolved items only.

- Active event folders live under `events/<event-id>/`.
- `events/<event-id>/` is created only when a real unresolved item exists.
- Review mode must not read `pending`.
- Failure-handling mode may consult at most one similar `pending` item when formal entries do not match.
"""


def render_resolved_toc() -> str:
    domain_notes = {
        "api-integration": "Solved API integration failures",
        "tool-usage": "Solved tool invocation and tool result failures",
        "code-implementation": "Solved implementation and code change failures",
        "test-and-verification": "Solved test, build, and verification failures",
        "frontend-ui": "Solved frontend structure and UI quality failures",
        "repo-and-filesystem": "Solved repository and filesystem failures",
        "research-and-analysis": "Solved research and analysis failures",
        "docs-and-content": "Solved documentation and content failures",
    }
    domain_rows = "\n".join(
        f"| {domain} | [TOC](../domains/{domain}/TOC.md) | {domain_notes[domain]} |"
        for domain in WORK_DOMAINS
    )
    return f"""# Resolved TOC

Use this file to route into the correct domain TOC for reusable solved experience.

| work_domain | toc | note |
| --- | --- | --- |
{domain_rows}
"""


def render_dead_ends_toc() -> str:
    domain_notes = {
        "api-integration": "Dead-end API integration paths",
        "tool-usage": "Dead-end tool usage paths",
        "code-implementation": "Dead-end implementation paths",
        "test-and-verification": "Dead-end testing and verification paths",
        "frontend-ui": "Dead-end frontend and UI paths",
        "repo-and-filesystem": "Dead-end repository and filesystem paths",
        "research-and-analysis": "Dead-end research and analysis paths",
        "docs-and-content": "Dead-end documentation and content paths",
    }
    domain_rows = "\n".join(
        f"| {domain} | [TOC](../domains/{domain}/TOC.md) | {domain_notes[domain]} |"
        for domain in WORK_DOMAINS
    )
    return f"""# Dead Ends TOC

Use this file to route into the correct domain TOC for reusable stop-sign experience.

| work_domain | toc | note |
| --- | --- | --- |
{domain_rows}
"""
