---
name: exp
description: Use when a clear failure has already happened and the goal is to reuse prior error experience from `.explib`. Also use when the user explicitly asks to review existing experience. Do not use this skill as proactive prevention.
---

# EXP

## Purpose

Use this skill after a concrete failure to retrieve reusable solved paths or reusable dead ends from `.explib`.

Read taxonomy and navigation from [`../../.explib/EXP.md`](../../.explib/EXP.md).

This skill is passive. It does not preload experience during normal work.

## Script Usage

Use the scripts in [`scripts/`](./scripts/) as the execution layer for `.explib`.

`.explib` belongs to the active project root, not to the skill installation directory.
When scripts are available, pass or infer the current project root and operate on that project's `.explib`.

Default order:

1. Run `init_explib.py` to create or repair the fixed `.explib` skeleton in the active project.
2. Run `validate_explib.py` before relying on library state.
3. For retrieval, use `list_toc_entries.py` to get structured candidates.
4. After choosing a candidate, use `get_entry.py` for the final entry payload.
5. For write-path actions, use the dedicated scripts:
   - `create_pending.py`
   - `append_attempt.py`
   - `promote_pending.py`
   - `abandon_pending.py`
   - `delete_dead_end.py`

Do not treat `TOC.md` as the primary machine-readable source when the scripts are available.
Use script output first, and fall back to direct file reading only when needed.

If `validate_explib.py` reports blocking issues, stop relying on `.explib` until the library state is corrected.

## Trigger Rules

- Use when a clear failure has already happened.
- Use only if the failure maps to existing taxonomy.
- Use when the user explicitly asks to review or summarize existing experience.
- Do not use for speculative low-confidence self-doubt.
- Do not use as a proactive checklist before failure.

## Failure-Handling Mode

1. Detect the failure.
2. Split the problem into failure clusters.
3. For each independent cluster, route through `.explib/EXP.md`.
4. Enter one `work_domain`.
5. Use `list_toc_entries.py` for structured candidates in that domain.
6. Read at most three formal entries per failure cluster.
7. Use `get_entry.py` for the chosen entry payload.
8. If no formal hit exists, read at most one similar `pending` item directly.
9. If new pending state must be created or updated, use the write-path scripts instead of ad-hoc file edits.
10. Reuse the fix or stop a dead path.

## Review Mode

- Review mode is read-only.
- Do not read `pending` in review mode.
- Read `.explib/EXP.md`, then use `list_toc_entries.py` and `get_entry.py` when possible.
- If the user asks for all experience, default to a high-level summary by `work_domain`.
- Expand specific entries only when the user asks for that domain or entry.

## Pending Rules

- Create `pending` only after a clear classified failure.
- Keep one active event per same-task ongoing issue.
- Open a new event for a similar issue in a different task.
- Re-read `.explib` only when the root-cause guess, `work_domain`, or retrieval evidence materially changes.
- Use `create_pending.py` and `append_attempt.py` for pending-state writes when automation is appropriate.

## Promotion Rules

- `resolved` proves a path works.
- `dead-end` proves a path should not continue under current constraints.
- `dead-end` requires review and either hard external evidence or at least two materially different failed attempts.
- Delete the active event directory when it closes.
- Delete overturned `dead-end` entries rather than preserving them.

## Forbidden Behaviors

- Do not create new top-level classes.
- Do not create new `work_domain` values.
- Do not force a failure into taxonomy just to store it.
- Do not save evidence snapshots.
- Do not keep permanent process history in final entries.
