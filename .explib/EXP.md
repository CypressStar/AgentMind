# EXP

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

- `runtime_error`
- `test_failure`
- `api_failure`
- `tool_failure`
- `quality_failure`
- `reasoning_failure`

## Failure Signal Sources

- `system_or_runtime`
- `test_or_validation`
- `api_response`
- `tool_execution`
- `user_feedback`

## Work Domains

- [`api-integration`](domains/api-integration/TOC.md)
- [`tool-usage`](domains/tool-usage/TOC.md)
- [`code-implementation`](domains/code-implementation/TOC.md)
- [`test-and-verification`](domains/test-and-verification/TOC.md)
- [`frontend-ui`](domains/frontend-ui/TOC.md)
- [`repo-and-filesystem`](domains/repo-and-filesystem/TOC.md)
- [`research-and-analysis`](domains/research-and-analysis/TOC.md)
- [`docs-and-content`](domains/docs-and-content/TOC.md)

## Rules

- Use `EXP` only after a clear failure, or in explicit user-requested review mode.
- Do not create new top-level classes.
- Do not create new `work_domain` values.
- If a failure does not map to the closed taxonomy, do not store it in `EXP`.
- Do not save external evidence snapshots.

## Manual Taxonomy Extension

Only the user may add or revise taxonomy. If taxonomy changes, update this file, the relevant TOCs, and `skills/exp/SKILL.md` together.
