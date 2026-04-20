# EXP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first working `EXP` repository structure, routing docs, domain TOCs, validation tests, and `skills/exp/SKILL.md` from the approved design.

**Architecture:** Keep runtime behavior in [`skills/exp/SKILL.md`](E:/Git/AgentMind/skills/exp/SKILL.md) and keep taxonomy plus navigation in [`EXP/EXP.md`](E:/Git/AgentMind/EXP/EXP.md). Formal entries stay as `json` files under `EXP/resolved/` and `EXP/dead-ends/`, while shared domain navigation lives under `EXP/domains/<work-domain>/TOC.md`. Use a small Python `unittest` suite to validate the structure and document invariants without adding new dependencies.

**Tech Stack:** Markdown, JSON/JSONL conventions, Python 3 `unittest`, PowerShell, Git

---

## File Structure

**Modify**

- `E:/Git/AgentMind/docs/superpowers/specs/2026-04-20-exp-design.md`
- `E:/Git/AgentMind/README.md`
- `E:/Git/AgentMind/README.zh-CN.md`

**Create**

- `E:/Git/AgentMind/tests/test_exp_layout.py`
- `E:/Git/AgentMind/EXP/EXP.md`
- `E:/Git/AgentMind/EXP/pending/TOC.md`
- `E:/Git/AgentMind/EXP/resolved/TOC.md`
- `E:/Git/AgentMind/EXP/dead-ends/TOC.md`
- `E:/Git/AgentMind/EXP/domains/api-integration/TOC.md`
- `E:/Git/AgentMind/EXP/domains/tool-usage/TOC.md`
- `E:/Git/AgentMind/EXP/domains/code-implementation/TOC.md`
- `E:/Git/AgentMind/EXP/domains/test-and-verification/TOC.md`
- `E:/Git/AgentMind/EXP/domains/frontend-ui/TOC.md`
- `E:/Git/AgentMind/EXP/domains/repo-and-filesystem/TOC.md`
- `E:/Git/AgentMind/EXP/domains/research-and-analysis/TOC.md`
- `E:/Git/AgentMind/EXP/domains/docs-and-content/TOC.md`
- `E:/Git/AgentMind/skills/exp/SKILL.md`

**Create later, only on first real entry**

- `E:/Git/AgentMind/EXP/pending/events/<event-id>/`
- `E:/Git/AgentMind/EXP/resolved/<work-domain>/`
- `E:/Git/AgentMind/EXP/dead-ends/<work-domain>/`

Reason:

- Git cannot track empty directories.
- The approved clarification moved human navigation to `EXP/domains/<work-domain>/TOC.md`.
- Leaf storage directories should appear only when a real `pending`, `resolved`, or `dead-end` entry exists.

## Task 1: Align The Spec With The Shared Domain Router Layout

**Files:**
- Modify: `E:/Git/AgentMind/docs/superpowers/specs/2026-04-20-exp-design.md`
- Create: `E:/Git/AgentMind/tests/test_exp_layout.py`
- Test: `E:/Git/AgentMind/tests/test_exp_layout.py`

- [ ] **Step 1: Write the failing spec-alignment test**

Create `E:/Git/AgentMind/tests/test_exp_layout.py` with this initial content:

```python
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = REPO_ROOT / "docs" / "superpowers" / "specs" / "2026-04-20-exp-design.md"


class ExpLayoutTests(unittest.TestCase):
    def test_spec_mentions_shared_domain_router_and_lazy_leaf_dirs(self):
        text = SPEC_PATH.read_text(encoding="utf-8")
        self.assertIn("EXP/domains/<work-domain>/TOC.md", text)
        self.assertIn(
            "Formal leaf directories under `resolved/` and `dead-ends/` are created lazily",
            text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- `FAIL: test_spec_mentions_shared_domain_router_and_lazy_leaf_dirs`
- Missing `EXP/domains/<work-domain>/TOC.md` text in the spec

- [ ] **Step 3: Update the approved spec to reflect the clarified layout**

Edit `E:/Git/AgentMind/docs/superpowers/specs/2026-04-20-exp-design.md` so the directory layout section and notes include the shared router layer and lazy leaf creation. The final relevant excerpt should read like this:

````md
```text
EXP/
  EXP.md
  pending/
    TOC.md
  resolved/
    TOC.md
  dead-ends/
    TOC.md
  domains/
    <work-domain>/
      TOC.md
```

Notes:

- `archive/` does not exist.
- `pending` holds only active unresolved items.
- `EXP/domains/<work-domain>/TOC.md` is the shared navigation layer for both `resolved` and `dead-ends`.
- Formal leaf directories under `resolved/` and `dead-ends/` are created lazily when the first real entry is written.
- `pending/events/<event-id>/` is also created lazily when the first unresolved event is opened.
- Closed events are deleted after promotion or abandonment.
- Final experience history is left to `git`, not duplicated inside `EXP`.
```
````

- [ ] **Step 4: Run the spec-alignment test again**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- `ok` for `test_spec_mentions_shared_domain_router_and_lazy_leaf_dirs`

- [ ] **Step 5: Commit the spec clarification**

Run:

```powershell
git add docs/superpowers/specs/2026-04-20-exp-design.md tests/test_exp_layout.py
git commit -m "docs: align EXP spec with shared domain routers"
```

## Task 2: Add The Initial EXP Skeleton And Existence Validation

**Files:**
- Modify: `E:/Git/AgentMind/tests/test_exp_layout.py`
- Create: `E:/Git/AgentMind/EXP/EXP.md`
- Create: `E:/Git/AgentMind/EXP/pending/TOC.md`
- Create: `E:/Git/AgentMind/EXP/resolved/TOC.md`
- Create: `E:/Git/AgentMind/EXP/dead-ends/TOC.md`
- Create: `E:/Git/AgentMind/EXP/domains/api-integration/TOC.md`
- Create: `E:/Git/AgentMind/EXP/domains/tool-usage/TOC.md`
- Create: `E:/Git/AgentMind/EXP/domains/code-implementation/TOC.md`
- Create: `E:/Git/AgentMind/EXP/domains/test-and-verification/TOC.md`
- Create: `E:/Git/AgentMind/EXP/domains/frontend-ui/TOC.md`
- Create: `E:/Git/AgentMind/EXP/domains/repo-and-filesystem/TOC.md`
- Create: `E:/Git/AgentMind/EXP/domains/research-and-analysis/TOC.md`
- Create: `E:/Git/AgentMind/EXP/domains/docs-and-content/TOC.md`
- Test: `E:/Git/AgentMind/tests/test_exp_layout.py`

- [ ] **Step 1: Extend the test file with filesystem existence checks**

Add these constants near the top of `E:/Git/AgentMind/tests/test_exp_layout.py`, directly under `SPEC_PATH`:

```python
DOMAIN_NAMES = [
    "api-integration",
    "tool-usage",
    "code-implementation",
    "test-and-verification",
    "frontend-ui",
    "repo-and-filesystem",
    "research-and-analysis",
    "docs-and-content",
]

REQUIRED_DIRS = [
    REPO_ROOT / "EXP",
    REPO_ROOT / "EXP" / "pending",
    REPO_ROOT / "EXP" / "resolved",
    REPO_ROOT / "EXP" / "dead-ends",
    REPO_ROOT / "EXP" / "domains",
] + [REPO_ROOT / "EXP" / "domains" / name for name in DOMAIN_NAMES]

REQUIRED_FILES = [
    REPO_ROOT / "EXP" / "EXP.md",
    REPO_ROOT / "EXP" / "pending" / "TOC.md",
    REPO_ROOT / "EXP" / "resolved" / "TOC.md",
    REPO_ROOT / "EXP" / "dead-ends" / "TOC.md",
] + [REPO_ROOT / "EXP" / "domains" / name / "TOC.md" for name in DOMAIN_NAMES]
```

Then add this method inside the existing `ExpLayoutTests` class:

```python
    def test_initial_exp_skeleton_paths_exist(self):
        for path in REQUIRED_DIRS:
            self.assertTrue(path.is_dir(), f"Missing directory: {path}")
        for path in REQUIRED_FILES:
            self.assertTrue(path.is_file(), f"Missing file: {path}")
```

- [ ] **Step 2: Run the expanded test suite and confirm it fails**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- `FAIL: test_initial_exp_skeleton_paths_exist`
- First missing path under `EXP/`

- [ ] **Step 3: Create the directory tree and minimal tracked files**

Create the directories:

```powershell
New-Item -ItemType Directory -Force "EXP" | Out-Null
New-Item -ItemType Directory -Force "EXP/pending" | Out-Null
New-Item -ItemType Directory -Force "EXP/resolved" | Out-Null
New-Item -ItemType Directory -Force "EXP/dead-ends" | Out-Null
New-Item -ItemType Directory -Force "EXP/domains/api-integration" | Out-Null
New-Item -ItemType Directory -Force "EXP/domains/tool-usage" | Out-Null
New-Item -ItemType Directory -Force "EXP/domains/code-implementation" | Out-Null
New-Item -ItemType Directory -Force "EXP/domains/test-and-verification" | Out-Null
New-Item -ItemType Directory -Force "EXP/domains/frontend-ui" | Out-Null
New-Item -ItemType Directory -Force "EXP/domains/repo-and-filesystem" | Out-Null
New-Item -ItemType Directory -Force "EXP/domains/research-and-analysis" | Out-Null
New-Item -ItemType Directory -Force "EXP/domains/docs-and-content" | Out-Null
```

Create these minimal tracked files:

`E:/Git/AgentMind/EXP/EXP.md`

```md
# EXP
```

`E:/Git/AgentMind/EXP/pending/TOC.md`

```md
# Pending TOC
```

`E:/Git/AgentMind/EXP/resolved/TOC.md`

```md
# Resolved TOC
```

`E:/Git/AgentMind/EXP/dead-ends/TOC.md`

```md
# Dead Ends TOC
```

For each file below, create this minimal content:

- `E:/Git/AgentMind/EXP/domains/api-integration/TOC.md`
- `E:/Git/AgentMind/EXP/domains/tool-usage/TOC.md`
- `E:/Git/AgentMind/EXP/domains/code-implementation/TOC.md`
- `E:/Git/AgentMind/EXP/domains/test-and-verification/TOC.md`
- `E:/Git/AgentMind/EXP/domains/frontend-ui/TOC.md`
- `E:/Git/AgentMind/EXP/domains/repo-and-filesystem/TOC.md`
- `E:/Git/AgentMind/EXP/domains/research-and-analysis/TOC.md`
- `E:/Git/AgentMind/EXP/domains/docs-and-content/TOC.md`

```md
# TOC
```

- [ ] **Step 4: Run the existence tests again**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- `ok` for both current tests

- [ ] **Step 5: Commit the skeleton**

Run:

```powershell
git add EXP tests/test_exp_layout.py
git commit -m "feat: add initial EXP skeleton"
```

## Task 3: Write EXP Root Routing Docs And Top-Level TOCs

**Files:**
- Modify: `E:/Git/AgentMind/tests/test_exp_layout.py`
- Modify: `E:/Git/AgentMind/EXP/EXP.md`
- Modify: `E:/Git/AgentMind/EXP/pending/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/resolved/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/dead-ends/TOC.md`
- Test: `E:/Git/AgentMind/tests/test_exp_layout.py`

- [ ] **Step 1: Add content tests for the root routing docs**

Append these test methods inside `ExpLayoutTests`:

```python
    def test_exp_md_contains_closed_taxonomy_and_manual_extension_rules(self):
        text = (REPO_ROOT / "EXP" / "EXP.md").read_text(encoding="utf-8")
        self.assertIn("## Failure Kinds", text)
        self.assertIn("## Work Domains", text)
        self.assertIn("runtime_error", text)
        self.assertIn("docs-and-content", text)
        self.assertIn("Only the user may add or revise taxonomy", text)

    def test_top_level_tocs_route_by_domain(self):
        for relative_path in ["resolved/TOC.md", "dead-ends/TOC.md"]:
            text = (REPO_ROOT / "EXP" / relative_path).read_text(encoding="utf-8")
            self.assertIn("| work_domain | toc | note |", text)
            for name in DOMAIN_NAMES:
                self.assertIn(name, text)

    def test_pending_toc_explains_lazy_event_creation(self):
        text = (REPO_ROOT / "EXP" / "pending" / "TOC.md").read_text(encoding="utf-8")
        self.assertIn("events/<event-id>/", text)
        self.assertIn("created only when a real unresolved item exists", text)
```

- [ ] **Step 2: Run the tests and confirm they fail on missing content**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- failures in the new content tests because the current files only contain one-line placeholders

- [ ] **Step 3: Replace `EXP/EXP.md` with the real taxonomy and routing document**

Write `E:/Git/AgentMind/EXP/EXP.md` as:

```md
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
```

- [ ] **Step 4: Replace the top-level TOCs with real routing docs**

Write `E:/Git/AgentMind/EXP/pending/TOC.md` as:

```md
# Pending TOC

This file is a lightweight note for unresolved items only.

- Active event folders live under `events/<event-id>/`.
- `events/<event-id>/` is created only when a real unresolved item exists.
- Review mode must not read `pending`.
- Failure-handling mode may consult at most one similar `pending` item when formal entries do not match.
```

Write `E:/Git/AgentMind/EXP/resolved/TOC.md` as:

```md
# Resolved TOC

Use this file to route into the correct domain TOC for reusable solved experience.

| work_domain | toc | note |
| --- | --- | --- |
| api-integration | [TOC](../domains/api-integration/TOC.md) | Solved API integration failures |
| tool-usage | [TOC](../domains/tool-usage/TOC.md) | Solved tool invocation and tool result failures |
| code-implementation | [TOC](../domains/code-implementation/TOC.md) | Solved implementation and code change failures |
| test-and-verification | [TOC](../domains/test-and-verification/TOC.md) | Solved test, build, and verification failures |
| frontend-ui | [TOC](../domains/frontend-ui/TOC.md) | Solved frontend structure and UI quality failures |
| repo-and-filesystem | [TOC](../domains/repo-and-filesystem/TOC.md) | Solved repository and filesystem failures |
| research-and-analysis | [TOC](../domains/research-and-analysis/TOC.md) | Solved research and analysis failures |
| docs-and-content | [TOC](../domains/docs-and-content/TOC.md) | Solved documentation and content failures |
```

Write `E:/Git/AgentMind/EXP/dead-ends/TOC.md` as:

```md
# Dead Ends TOC

Use this file to route into the correct domain TOC for reusable stop-sign experience.

| work_domain | toc | note |
| --- | --- | --- |
| api-integration | [TOC](../domains/api-integration/TOC.md) | Dead-end API integration paths |
| tool-usage | [TOC](../domains/tool-usage/TOC.md) | Dead-end tool usage paths |
| code-implementation | [TOC](../domains/code-implementation/TOC.md) | Dead-end implementation paths |
| test-and-verification | [TOC](../domains/test-and-verification/TOC.md) | Dead-end testing and verification paths |
| frontend-ui | [TOC](../domains/frontend-ui/TOC.md) | Dead-end frontend and UI paths |
| repo-and-filesystem | [TOC](../domains/repo-and-filesystem/TOC.md) | Dead-end repository and filesystem paths |
| research-and-analysis | [TOC](../domains/research-and-analysis/TOC.md) | Dead-end research and analysis paths |
| docs-and-content | [TOC](../domains/docs-and-content/TOC.md) | Dead-end documentation and content paths |
```

- [ ] **Step 5: Run the content tests again**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- the three new content tests pass

- [ ] **Step 6: Commit the root routing docs**

Run:

```powershell
git add EXP tests/test_exp_layout.py
git commit -m "docs: add EXP routing and top-level TOCs"
```

## Task 4: Add Domain TOC Templates For All Eight Work Domains

**Files:**
- Modify: `E:/Git/AgentMind/tests/test_exp_layout.py`
- Modify: `E:/Git/AgentMind/EXP/domains/api-integration/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/domains/tool-usage/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/domains/code-implementation/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/domains/test-and-verification/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/domains/frontend-ui/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/domains/repo-and-filesystem/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/domains/research-and-analysis/TOC.md`
- Modify: `E:/Git/AgentMind/EXP/domains/docs-and-content/TOC.md`
- Test: `E:/Git/AgentMind/tests/test_exp_layout.py`

- [ ] **Step 1: Add tests for the shared domain TOC template**

Append this test method inside `ExpLayoutTests`:

```python
    def test_each_domain_toc_uses_the_shared_two_section_template(self):
        expected_header = "| id | pattern_name | failure_kind | signals | note |"
        for name in DOMAIN_NAMES:
            text = (REPO_ROOT / "EXP" / "domains" / name / "TOC.md").read_text(encoding="utf-8")
            self.assertIn("## Resolved", text, msg=name)
            self.assertIn("## Dead Ends", text, msg=name)
            self.assertEqual(text.count(expected_header), 2, msg=name)
```

- [ ] **Step 2: Run the tests and confirm the new template test fails**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- `FAIL: test_each_domain_toc_uses_the_shared_two_section_template`

- [ ] **Step 3: Replace all eight domain TOCs with the shared template**

Write `E:/Git/AgentMind/EXP/domains/api-integration/TOC.md` as:

```md
# api-integration TOC

Use this file to route solved and dead-end experience for API integration work.

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

Write `E:/Git/AgentMind/EXP/domains/tool-usage/TOC.md` as:

```md
# tool-usage TOC

Use this file to route solved and dead-end experience for tool usage work.

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

Write `E:/Git/AgentMind/EXP/domains/code-implementation/TOC.md` as:

```md
# code-implementation TOC

Use this file to route solved and dead-end experience for code implementation work.

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

Write `E:/Git/AgentMind/EXP/domains/test-and-verification/TOC.md` as:

```md
# test-and-verification TOC

Use this file to route solved and dead-end experience for test and verification work.

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

Write `E:/Git/AgentMind/EXP/domains/frontend-ui/TOC.md` as:

```md
# frontend-ui TOC

Use this file to route solved and dead-end experience for frontend UI work.

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

Write `E:/Git/AgentMind/EXP/domains/repo-and-filesystem/TOC.md` as:

```md
# repo-and-filesystem TOC

Use this file to route solved and dead-end experience for repository and filesystem work.

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

Write `E:/Git/AgentMind/EXP/domains/research-and-analysis/TOC.md` as:

```md
# research-and-analysis TOC

Use this file to route solved and dead-end experience for research and analysis work.

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

Write `E:/Git/AgentMind/EXP/domains/docs-and-content/TOC.md` as:

```md
# docs-and-content TOC

Use this file to route solved and dead-end experience for docs and content work.

## Resolved

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |

## Dead Ends

| id | pattern_name | failure_kind | signals | note |
| --- | --- | --- | --- | --- |
```

- [ ] **Step 4: Run the domain TOC test again**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- `ok` for `test_each_domain_toc_uses_the_shared_two_section_template`

- [ ] **Step 5: Commit the domain routers**

Run:

```powershell
git add EXP tests/test_exp_layout.py
git commit -m "docs: add EXP domain TOC templates"
```

## Task 5: Author The EXP Skill Runtime Rules

**Files:**
- Modify: `E:/Git/AgentMind/tests/test_exp_layout.py`
- Create: `E:/Git/AgentMind/skills/exp/SKILL.md`
- Test: `E:/Git/AgentMind/tests/test_exp_layout.py`

- [ ] **Step 1: Add tests for the EXP skill runtime contract**

Append this test method inside `ExpLayoutTests`:

```python
    def test_exp_skill_captures_runtime_rules_without_duplicating_taxonomy(self):
        text = (REPO_ROOT / "skills" / "exp" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Use when a clear failure has already happened", text)
        self.assertIn("Review mode", text)
        self.assertIn("Do not read `pending` in review mode", text)
        self.assertIn("Read at most three formal entries per failure cluster", text)
        self.assertIn("../../EXP/EXP.md", text)
        self.assertNotIn("## Failure Kinds", text)
```

- [ ] **Step 2: Run the tests and confirm the new skill test fails**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- `FAIL: test_exp_skill_captures_runtime_rules_without_duplicating_taxonomy`
- missing `skills/exp/SKILL.md`

- [ ] **Step 3: Write `skills/exp/SKILL.md`**

Create `E:/Git/AgentMind/skills/exp/SKILL.md` with this content:

```md
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
```

- [ ] **Step 4: Run the full test suite**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- the skill contract test passes

- [ ] **Step 5: Commit the skill**

Run:

```powershell
git add skills/exp/SKILL.md tests/test_exp_layout.py
git commit -m "feat: add EXP skill runtime rules"
```

## Task 6: Update Project READMEs And Run Final Validation

**Files:**
- Modify: `E:/Git/AgentMind/tests/test_exp_layout.py`
- Modify: `E:/Git/AgentMind/README.md`
- Modify: `E:/Git/AgentMind/README.zh-CN.md`
- Test: `E:/Git/AgentMind/tests/test_exp_layout.py`

- [ ] **Step 1: Add README coverage tests**

Append this test method inside `ExpLayoutTests`:

```python
    def test_readmes_reference_exp_skill_and_repository_layout(self):
        readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (REPO_ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("EXP", readme_en)
        self.assertIn("skills/exp/SKILL.md", readme_en)
        self.assertIn("EXP", readme_zh)
        self.assertIn("skills/exp/SKILL.md", readme_zh)
```

- [ ] **Step 2: Run the tests and confirm the README test fails**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- `FAIL: test_readmes_reference_exp_skill_and_repository_layout`

- [ ] **Step 3: Update the English README**

Add a new `EXP` subsection to `E:/Git/AgentMind/README.md` near the current skill list, and expand the repository structure list. The inserted content should read:

```md
### `exp`

The second public skill in this repository is [`exp`](./skills/exp/SKILL.md).

`exp` is a passive, post-failure experience library. It does not try to stop the model from ever making mistakes. Instead, it makes repeated mistakes cheaper by retrieving solved paths and reusable dead ends after a concrete failure has already happened.

It separates runtime rules from experience content:

- [`skills/exp/SKILL.md`](./skills/exp/SKILL.md): runtime trigger rules, failure triage, retrieval budget, `pending` rules, and promotion rules
- [`EXP/EXP.md`](./EXP/EXP.md): closed taxonomy, navigation, and manual extension rules
- [`EXP/domains/`](./EXP/domains/): shared domain TOCs for resolved and dead-end experience
```

Also add this repository structure bullet:

```md
- [`EXP/`](./EXP/): EXP routing docs, top-level TOCs, and domain navigation
```

- [ ] **Step 4: Update the Chinese README**

Add a new `EXP` subsection to `E:/Git/AgentMind/README.zh-CN.md` near the current skill list, and expand the repository structure list. The inserted content should read:

```md
### `exp`

当前仓库中的第二个公开技能是 [`exp`](./skills/exp/SKILL.md)。

`exp` 是一个被动触发、面向失败后的经验库。它不试图提前阻止模型犯错，而是在具体失败已经发生之后，帮助模型检索过往的已解决路径和可复用的 dead-end 经验，减少在同类问题上的重复试错成本。

它把运行时规则和经验内容分开：

- [`skills/exp/SKILL.md`](./skills/exp/SKILL.md)：触发条件、失败分簇、检索预算、`pending` 规则、晋升规则
- [`EXP/EXP.md`](./EXP/EXP.md)：封闭分类法、导航入口、手动扩展说明
- [`EXP/domains/`](./EXP/domains/)：resolved 和 dead-end 共用的 domain 级 TOC
```

Also add this repository structure bullet:

```md
- [`EXP/`](./EXP/)：EXP 路由文档、顶层 TOC 与 domain 导航
```

- [ ] **Step 5: Run the final validation suite**

Run:

```powershell
python -m unittest discover -s tests -p "test_exp_layout.py" -v
```

Expected:

- all tests `ok`

Then run:

```powershell
git status --short
```

Expected:

- only the intended README and test changes are present

- [ ] **Step 6: Commit the README updates and final validated state**

Run:

```powershell
git add README.md README.zh-CN.md tests/test_exp_layout.py
git commit -m "docs: document EXP skill and layout"
```

## Final Verification Checklist

- `python -m unittest discover -s tests -p "test_exp_layout.py" -v` passes
- `E:/Git/AgentMind/EXP/EXP.md` contains the approved closed taxonomy
- `E:/Git/AgentMind/EXP/pending/TOC.md` explains lazy event creation
- `E:/Git/AgentMind/EXP/resolved/TOC.md` and `E:/Git/AgentMind/EXP/dead-ends/TOC.md` route by domain
- every `E:/Git/AgentMind/EXP/domains/<work-domain>/TOC.md` uses the two-section table template
- `E:/Git/AgentMind/skills/exp/SKILL.md` references `E:/Git/AgentMind/EXP/EXP.md` instead of repeating taxonomy prose
- both READMEs mention `EXP` and link to `skills/exp/SKILL.md`

## Notes For Execution

- Keep leaf data directories lazy. Do not create tracked empty `EXP/resolved/<work-domain>/` or `EXP/dead-ends/<work-domain>/` directories during this implementation pass.
- Do not add helper scripts, `.gitkeep` files, screenshots, or extra placeholders. The approved design is intentionally narrow.
- If the validation test becomes brittle because of wording changes, prefer adjusting assertions to check stable headings and required strings, not exact paragraph text.
