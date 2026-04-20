---
name: exp
description: Use when a clear failure has already happened and the goal is to reuse prior error experience from EXP. Also use when the user explicitly asks to review existing experience. Do not use this skill as proactive prevention.
---

# EXP

## Purpose

Use this skill after a concrete failure to retrieve reusable solved paths or reusable dead ends from `EXP`.

Read taxonomy and navigation from [`../../EXP/EXP.md`](../../EXP/EXP.md).

This skill is passive. It does not preload experience during normal work.

## Trigger Rules

- Use when a clear failure has already happened.
- Use only if the failure maps to existing taxonomy.
- Use when the user explicitly asks to review or summarize existing experience.
- Do not use for speculative low-confidence self-doubt.
- Do not use as a proactive checklist before failure.

## Failure-Handling Mode

1. Detect the failure.
2. Split the problem into failure clusters.
3. For each independent cluster, route through `EXP.md`.
4. Enter one `work_domain`.
5. Read one relevant domain `TOC.md`.
6. Read at most three formal entries per failure cluster.
7. If no formal hit exists, read at most one similar `pending` item.
8. Reuse the fix, stop a dead path, or create/update `pending`.

## Review Mode

- Review mode is read-only.
- Do not read `pending` in review mode.
- Read only `EXP.md`, relevant TOCs, and formal entries.
- If the user asks for all experience, default to a high-level summary by `work_domain`.
- Expand specific entries only when the user asks for that domain or entry.

## Pending Rules

- Create `pending` only after a clear classified failure.
- Keep one active event per same-task ongoing issue.
- Open a new event for a similar issue in a different task.
- Re-read `EXP` only when the root-cause guess, `work_domain`, or retrieval evidence materially changes.

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
