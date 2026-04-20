# EXP Design

## Status

Approved design draft for the first version of the `EXP` skill and repository layout.

## Summary

`EXP` is a passive, post-failure experience library for AI work. It exists to reduce repeated payment on the same class of mistakes by making prior failures, stop-signs, and verified fixes retrievable after a concrete failure has already happened.

`EXP` is not a memory system, not a proactive preflight checklist, and not a general logging store. It only engages after a clear failure signal, or in a user-requested read-only review mode.

The design uses progressive disclosure:

1. [`EXP.md`](../../../EXP/EXP.md) routes the model into the right classification branch.
2. Domain [`TOC.md`](../../../EXP/) files narrow retrieval to a small set of candidates.
3. Final experience entries in `json` carry the reusable result.

Unresolved problems may temporarily exist as active `pending` records. Once a problem is closed, only the final result remains. Intermediate process files are deleted.

## Goals

- Keep a physical repository of reusable failure experience outside the normal memory system.
- Trigger only after clear failure, not as proactive prevention.
- Make repeated and similar failures cheaper to resolve.
- Preserve high precision by enforcing a closed taxonomy.
- Keep active unresolved records temporary.
- Keep the final library result-oriented, not process-oriented.

## Non-Goals

- Do not preload large experience context into normal tasks.
- Do not store every odd or unclassifiable issue.
- Do not become a generic RAG store or evidence warehouse.
- Do not persist external evidence snapshots.
- Do not preserve permanent process history inside `EXP`.

## Core Model

`EXP` has two operating modes.

### 1. Failure Handling Mode

Trigger conditions:

- A clear failure happened.
- The failure maps to an existing `failure_kind`.
- The failure maps to an existing `work_domain`.

Flow:

1. Detect the failure.
2. Perform `failure triage` and split into failure clusters.
3. For each independent cluster, route through `EXP.md`.
4. Read the relevant domain `TOC.md`.
5. Read up to three formal entries.
6. If no formal hit exists, optionally read one similar `pending` item.
7. Reuse a fix, stop a dead path, or create/update a `pending` record.

### 2. Review Mode

Trigger condition:

- The user explicitly asks to review, summarize, or inspect past experience.

Rules:

- Read-only.
- Read only `EXP.md`, relevant `TOC.md`, and formal entries.
- Never read `pending`.
- Never create or update `pending`.
- Never mutate the library unless the user separately asks for changes.

## Failure Triage

Before retrieval, the model must split the current problem into failure clusters.

Treat as one cluster when:

- The issues share a root cause.
- The issues share the same reusable fix path.
- One issue is mainly a symptom or downstream result of another.
- Fixing one has a high chance to remove the others.

Treat as separate clusters when:

- They need independent fixes.
- They do not share the same root cause.
- They only happen in the same task by coincidence.

If uncertain, default to separate clusters rather than forced merge.

If `failure_kind` differs but the root cause is clearly the same, still treat them as one cluster.

## Retrieval Budget

Budget applies per independent failure cluster, not per user turn.

For one cluster:

- Read [`EXP.md`](../../../EXP/EXP.md)
- Enter only one `work_domain`
- Read only one relevant domain `TOC.md`
- Read at most three formal entries
- If no formal hit exists, optionally read one similar `pending` record
- Stop retrieval after budget exhaustion

If a task contains three independent clusters, that is three separate retrieval sessions. If multiple visible failures are the same root-cause chain, that remains one retrieval session.

## Closed Taxonomy

### Failure Kinds

The model may select only from this closed set:

- `runtime_error`
- `test_failure`
- `api_failure`
- `tool_failure`
- `quality_failure`
- `reasoning_failure`

The model may not add, rename, or remove values.

### Failure Signal Source

Each `pending` item stores exactly one signal source: the first source that triggered `EXP` handling for that cluster.

Closed set:

- `system_or_runtime`
- `test_or_validation`
- `api_response`
- `tool_execution`
- `user_feedback`

Later signal sources do not replace or expand this field.

### Work Domains

The model may select only from this closed set:

- `api-integration`
- `tool-usage`
- `code-implementation`
- `test-and-verification`
- `frontend-ui`
- `repo-and-filesystem`
- `research-and-analysis`
- `docs-and-content`

Rules:

- One event has one primary `work_domain`.
- The model may not add, rename, or remove values.
- If a failure does not fit the closed taxonomy, it does not enter `EXP`.
- The model must continue handling the user problem normally without mentioning the non-entry decision.

## Pattern Layer

`pattern_name` is not a closed enum, but it is high-friction to create.

Rules:

- Prefer updating an existing pattern over creating a new one.
- If root cause is the same, merge.
- If root cause differs, split.
- Variant conditions should stay inside an existing pattern when the main reusable fix remains the same.
- A new pattern is justified only when root cause and fix path materially differ.

## Directory Layout

```text
EXP/
  EXP.md
  pending/
    TOC.md
    events/
      <event-id>/
        event.json
        attempts.jsonl
        promotion.json
  resolved/
    TOC.md
    <work-domain>/
      TOC.md
      <entry-id>.json
  dead-ends/
    TOC.md
    <work-domain>/
      TOC.md
      <entry-id>.json
```

Notes:

- `archive/` does not exist.
- `pending` holds only active unresolved items.
- Closed events are deleted after promotion or abandonment.
- Final experience history is left to `git`, not duplicated inside `EXP`.

## Pending Lifecycle

### Minimum Entry Conditions

Create or update a `pending` item only when all are true:

- A clear failure occurred.
- It maps to existing `failure_kind`.
- It maps to existing `work_domain`.
- There is enough information to record a reusable unresolved problem.
- It is not merely a duplicate continuation of the same active event.

### Deduplication

- Same task, same ongoing issue: continue the same `pending` item.
- Different task, similar issue: create a new `pending` item.
- Pattern-level merge happens later at formal-entry time, not at `pending` time.

### Re-Read Rule

Once a cluster already used `EXP`, do not re-read by default. Re-read only if one of these happens:

- Root cause guess changes materially.
- Primary `work_domain` changes materially.
- A previously matched formal entry is disproved by later evidence.
- There was no previous hit and a new failure signal materially changes the retrieval keys.

### Closing States

An active `pending` item can end in exactly one of these ways:

- `promoted_resolved`
- `promoted_dead_end`
- `abandoned`

Behavior:

- `promoted_resolved`: write or update a formal entry, then delete the `pending` directory.
- `promoted_dead_end`: write a dead-end entry, then delete the `pending` directory.
- `abandoned`: delete the `pending` directory without creating a formal entry.

### Active Event Status

While an event directory exists, `event.json.status` may only be:

- `pending`
- `promotion_candidate`

Rules:

- `pending` means unresolved and still under normal investigation.
- `promotion_candidate` means `promotion.json` exists and the item is waiting for review.
- Review may be done by the main agent or by a subagent/task if the environment supports it.
- Final closing states are not stored in surviving files because the whole event directory is deleted when the event closes.

## Dead-End Standard

`dead-end` is intentionally stricter than `resolved`.

Definition:

- `resolved` proves a path works.
- `dead-end` proves a path should not continue under the current constraints.
- `abandoned` means the work stopped without proving the path itself is wrong.

A `dead-end` promotion requires:

- A clear failure already recorded.
- Substantial investigation or attempts already happened.
- A clear reason that can be written into `why_this_path_fails`.
- A usable pivot direction that can be written into `recommended_pivot`.
- Review before promotion.
- At least one of:
  - hard external evidence
  - at least two materially different failed attempts pointing to the same conclusion

If a `dead-end` is later overturned by new evidence:

- delete the `dead-end` formal entry
- if a reusable solution now exists, write or update a `resolved` entry

No permanent overturned marker is kept in `EXP`.

## File Rules

`EXP` is a whitelist-based file tree.

Allowed files only:

### Active Pending Event Directory

- `event.json`
- `attempts.jsonl`
- `promotion.json`

### Formal Experience Directory

- `<entry-id>.json`

Everything else is forbidden.

No screenshots, notes, copied articles, evidence snapshots, or extra files are allowed.

## File Schemas

### `event.json`

Purpose:

- minimal unresolved problem summary

Minimum fields:

- `id`
- `status`
- `failure_kind`
- `failure_signal_source`
- `work_domain`
- `pattern_guess`
- `root_cause_guess`
- `summary`
- `scene`
- `error_text`
- `raw_feedback`
- `feedback_hint`

Notes:

- No time fields.
- `raw_feedback` and `feedback_hint` are used only when applicable.
- `pattern_guess` is provisional and may be empty.
- `root_cause_guess` is provisional and may change while unresolved.

### `attempts.jsonl`

One line per attempt.

Fields:

- `action`
- `result`
- `note`

`result` is a closed enum:

- `failed`
- `passed`
- `signal`

This file exists only while the problem is unresolved.

### `promotion.json`

Purpose:

- narrow review packet for a candidate promotion

Fields:

- `promotion_reason`
- `verification_summary`
- `open_questions`
- `evidence_refs`
- `proposed_entries`

Rules:

- No `status` field.
- `proposed_entries` maximum length is `3`.
- Exists only while review is pending.
- Deleted with the rest of the event directory when the event closes.

### Formal Entry Base Fields

All formal entries share these fields:

- `id`
- `kind`
- `failure_kind`
- `work_domain`
- `pattern_name`
- `summary`
- `recognition_signals`
- `root_cause`
- `evidence_refs`

No `source_event_ids`.
No revision log.
No timestamps.

### `resolved` Extra Fields

- `solution_steps`
- `avoidance_notes`

### `dead-end` Extra Fields

- `why_this_path_fails`
- `recommended_pivot`

Formal entries are updated in place.

## Evidence References

`EXP` stores only lightweight evidence references.

`evidence_refs[]` items use:

- `ref_type`
- `ref`
- `note`

`ref_type` is a closed enum:

- `official_doc`
- `api_error`
- `tool_limit`
- `user_constraint`
- `test_result`

Rules:

- No local snapshot of external material.
- No copied article excerpts.
- If an external source changes later, handle it through a new failure event, not through frozen snapshots.

## User Feedback Fields

When user feedback is the signal source, preserve:

- `raw_feedback`
- `feedback_hint`

`feedback_hint` is a closed enum:

- `not_resolved`
- `wrong_direction`
- `misunderstood_request`
- `too_generic`
- `low_quality`
- `format_or_output_mismatch`

Use short labels only. Do not add free-form interpretation essays.

## TOC Design

`TOC.md` is the correct navigation format for this library.

Reasons:

- human-readable
- AI-readable
- link-friendly
- supports section headers and short notes
- stable in git diff

Each domain `TOC.md` has exactly two sections:

- `## Resolved`
- `## Dead Ends`

Recommended table shape:

```md
## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

Rules:

- `id` and `pattern_name` stay separate.
- `pattern_name` is the Markdown link to the target `json`.
- No extra `path` column.
- `signals` should stay short.
- `note` should stay one sentence.
- `TOC.md` is navigation only, not a second copy of the experience body.

Top-level `resolved/TOC.md` and `dead-ends/TOC.md` should work as domain routers, not as full entry dumps. They should link to each `work_domain` directory and keep only short domain-level notes.

## `SKILL.md` vs `EXP.md`

### `skills/exp/SKILL.md`

Owns runtime behavior:

- when to trigger
- when not to trigger
- failure triage
- retrieval budget
- read-mode differences
- `pending` write rules
- promotion rules
- closing rules
- forbidden behaviors

### `EXP/EXP.md`

Owns static navigation and taxonomy:

- overview of what `EXP` is and is not
- high-level flow
- closed `failure_kind` list
- closed `work_domain` list
- links into the library
- user instructions for manual taxonomy extension

`SKILL.md` should reference `EXP.md` rather than duplicate taxonomy prose.

## Manual Taxonomy Extension

The model may not extend taxonomy.

Only the user may manually add or revise `failure_kind` and `work_domain`.

If taxonomy is extended, update all of:

- [`EXP/EXP.md`](../../../EXP/EXP.md)
- relevant top-level `TOC.md`
- relevant domain directories
- `skills/exp/SKILL.md` rules if routing behavior changes

The system should prefer stable, low-overlap categories over expressive but expanding categories.

## Hard Constraints

- No proactive loading in normal work.
- No automatic new top-level classes.
- No automatic new `work_domain`.
- No forced classification to make something enter `EXP`.
- No unclassified bucket.
- No evidence snapshots.
- No archive tree.
- No permanent process history in final entries.
- No reading `pending` in review mode.
- No reading more than one similar `pending` item in failure-handling mode.
- No more than three formal-entry reads per failure cluster.

## Recommended Next Step

After this design document is approved, create the initial repository skeleton and draft [`skills/exp/SKILL.md`](../../../skills/exp/SKILL.md) plus the top-level `EXP` routing documents from this spec.
