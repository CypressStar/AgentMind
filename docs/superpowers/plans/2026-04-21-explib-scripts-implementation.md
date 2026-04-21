# EXP `.explib` Scripts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current `EXP/`-based repository contract with a `.explib/`-based experience-library contract and implement the first four supporting scripts: `init_explib.py`, `validate_explib.py`, `list_toc_entries.py`, and `get_entry.py`.

**Architecture:** Keep the skill itself at [`skills/exp/SKILL.md`](E:/Git/AgentMind/skills/exp/SKILL.md), but move the experience-library root to [`.explib/`](E:/Git/AgentMind/.explib). Put all executable scripts and shared helpers under [`skills/exp/scripts/`](E:/Git/AgentMind/skills/exp/scripts/), with `_shared_*` modules holding paths, taxonomy, templates, index handling, rendering, and validation helpers. Use Python `unittest` with temporary directories so the script tests do not depend on the real repo state.

**Tech Stack:** Python 3, `unittest`, Markdown, JSON, PowerShell, Git

---

## File Structure

**Modify**

- `E:/Git/AgentMind/README.md`
- `E:/Git/AgentMind/README.zh-CN.md`
- `E:/Git/AgentMind/skills/exp/SKILL.md`
- `E:/Git/AgentMind/tests/test_exp_layout.py`

**Create**

- `E:/Git/AgentMind/skills/exp/scripts/init_explib.py`
- `E:/Git/AgentMind/skills/exp/scripts/validate_explib.py`
- `E:/Git/AgentMind/skills/exp/scripts/list_toc_entries.py`
- `E:/Git/AgentMind/skills/exp/scripts/get_entry.py`
- `E:/Git/AgentMind/skills/exp/scripts/_shared_paths.py`
- `E:/Git/AgentMind/skills/exp/scripts/_shared_taxonomy.py`
- `E:/Git/AgentMind/skills/exp/scripts/_shared_templates.py`
- `E:/Git/AgentMind/skills/exp/scripts/_shared_index.py`
- `E:/Git/AgentMind/skills/exp/scripts/_shared_render.py`
- `E:/Git/AgentMind/skills/exp/scripts/_shared_validate.py`
- `E:/Git/AgentMind/tests/test_init_explib.py`
- `E:/Git/AgentMind/tests/test_validate_explib.py`
- `E:/Git/AgentMind/tests/test_explib_query_scripts.py`
- `E:/Git/AgentMind/tests/helpers/explib_fixture.py`

**Not In Scope**

- P2 write-path scripts:
  - `create_pending.py`
  - `append_attempt.py`
  - `promote_pending.py`
  - `abandon_pending.py`
  - `delete_dead_end.py`
- Automatic migration or deletion of the existing `EXP/` directory

## Task 1: Migrate The Repository Contract From `EXP/` To `.explib/`

**Files:**
- Modify: `E:/Git/AgentMind/tests/test_exp_layout.py`
- Modify: `E:/Git/AgentMind/README.md`
- Modify: `E:/Git/AgentMind/README.zh-CN.md`
- Modify: `E:/Git/AgentMind/skills/exp/SKILL.md`
- Test: `E:/Git/AgentMind/tests/test_exp_layout.py`

- [ ] **Step 1: Write the failing path-migration assertions**

Update `E:/Git/AgentMind/tests/test_exp_layout.py` so the current path constants and string assertions target `.explib` instead of `EXP`. Replace the top-level path constants with:

```python
EXPLIB_ROOT = REPO_ROOT / ".explib"
SPEC_PATH = REPO_ROOT / "docs" / "superpowers" / "specs" / "2026-04-20-exp-design.md"

REQUIRED_DIRS = [
    EXPLIB_ROOT,
    EXPLIB_ROOT / "pending",
    EXPLIB_ROOT / "resolved",
    EXPLIB_ROOT / "dead-ends",
    EXPLIB_ROOT / "domains",
] + [EXPLIB_ROOT / "domains" / name for name in DOMAIN_NAMES]

REQUIRED_FILES = [
    EXPLIB_ROOT / "EXP.md",
    EXPLIB_ROOT / "pending" / "TOC.md",
    EXPLIB_ROOT / "resolved" / "TOC.md",
    EXPLIB_ROOT / "dead-ends" / "TOC.md",
] + [EXPLIB_ROOT / "domains" / name / "TOC.md" for name in DOMAIN_NAMES]
```

Also update string checks so they reference:

- `.explib/domains/<work-domain>/TOC.md`
- `.explib/EXP.md`
- `./.explib/`

- [ ] **Step 2: Run the migrated contract test and confirm it fails**

Run:

```powershell
uv run -m unittest tests.test_exp_layout -v
```

Expected:

- failures because the repo still documents and expects `EXP/`

- [ ] **Step 3: Update the user-facing docs and skill references**

Modify `E:/Git/AgentMind/skills/exp/SKILL.md` so taxonomy/navigation references point to `.explib/EXP.md` instead of `EXP/EXP.md`. The key line should become:

```md
Read taxonomy and navigation from [`../../.explib/EXP.md`](../../.explib/EXP.md).
```

Modify `E:/Git/AgentMind/README.md` so the `exp` subsection and repository structure point to `.explib`:

```md
- [`.explib/EXP.md`](./.explib/EXP.md): closed taxonomy, navigation, and manual extension rules
- [`.explib/domains/`](./.explib/domains/): shared domain TOCs for resolved and dead-end experience
```

And the repository structure bullet:

```md
- [`.explib/`](./.explib/): experience-library routing docs, top-level TOCs, and domain navigation
```

Modify `E:/Git/AgentMind/README.zh-CN.md` with the matching `.explib` links:

```md
- [`.explib/EXP.md`](./.explib/EXP.md)：封闭分类法、导航入口、手动扩展说明
- [`.explib/domains/`](./.explib/domains/)：resolved 和 dead-end 共用的 domain 级 TOC
```

And:

```md
- [`.explib/`](./.explib/)：经验库路由文档、顶层 TOC 与 domain 导航
```

- [ ] **Step 4: Re-run the migrated contract test**

Run:

```powershell
uv run -m unittest tests.test_exp_layout -v
```

Expected:

- path and README/skill reference assertions now pass
- structure assertions that require actual `.explib/` files still fail, which is acceptable until Task 3

- [ ] **Step 5: Commit the `.explib` contract migration**

Run:

```powershell
git add README.md README.zh-CN.md skills/exp/SKILL.md tests/test_exp_layout.py
git commit -m "refactor: point EXP skill docs to .explib"
```

## Task 2: Add Shared Script Modules For Paths, Taxonomy, Templates, Indexes, And Rendering

**Files:**
- Create: `E:/Git/AgentMind/skills/exp/scripts/_shared_paths.py`
- Create: `E:/Git/AgentMind/skills/exp/scripts/_shared_taxonomy.py`
- Create: `E:/Git/AgentMind/skills/exp/scripts/_shared_templates.py`
- Create: `E:/Git/AgentMind/skills/exp/scripts/_shared_index.py`
- Create: `E:/Git/AgentMind/skills/exp/scripts/_shared_render.py`
- Create: `E:/Git/AgentMind/tests/helpers/explib_fixture.py`
- Test: `E:/Git/AgentMind/tests/test_init_explib.py`

- [ ] **Step 1: Write the failing shared-module tests**

Create `E:/Git/AgentMind/tests/test_init_explib.py` with this initial contract:

```python
from pathlib import Path
import tempfile
import unittest

from tests.helpers.explib_fixture import make_empty_root
from skills.exp.scripts._shared_templates import empty_domain_index, render_exp_md
from skills.exp.scripts._shared_render import render_domain_toc
from skills.exp.scripts._shared_taxonomy import FAILURE_SIGNAL_SOURCES, WORK_DOMAINS


class InitExplibSupportTests(unittest.TestCase):
    def test_empty_domain_index_has_expected_shape(self):
        data = empty_domain_index("api-integration")
        self.assertEqual(data["domain"], "api-integration")
        self.assertEqual(data["resolved"], [])
        self.assertEqual(data["dead_ends"], [])

    def test_render_exp_md_includes_signal_source_taxonomy(self):
        text = render_exp_md()
        self.assertIn("## Failure Signal Sources", text)
        for value in FAILURE_SIGNAL_SOURCES:
            self.assertIn(value, text)

    def test_render_domain_toc_uses_generated_header_and_sections(self):
        text = render_domain_toc(
            {
                "domain": "api-integration",
                "resolved": [],
                "dead_ends": [],
            }
        )
        self.assertIn("> Generated from `toc.index.json`.", text)
        self.assertIn("## Resolved", text)
        self.assertIn("## Dead Ends", text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the shared-module tests and confirm import failures**

Run:

```powershell
uv run -m unittest tests.test_init_explib -v
```

Expected:

- import errors because the shared modules do not exist yet

- [ ] **Step 3: Create the shared modules and fixture helper**

Create `E:/Git/AgentMind/skills/exp/scripts/_shared_taxonomy.py` with:

```python
FAILURE_KINDS = [
    "runtime_error",
    "test_failure",
    "api_failure",
    "tool_failure",
    "quality_failure",
    "reasoning_failure",
]

FAILURE_SIGNAL_SOURCES = [
    "system_or_runtime",
    "test_or_validation",
    "api_response",
    "tool_execution",
    "user_feedback",
]

WORK_DOMAINS = [
    "api-integration",
    "tool-usage",
    "code-implementation",
    "test-and-verification",
    "frontend-ui",
    "repo-and-filesystem",
    "research-and-analysis",
    "docs-and-content",
]
```

Create `E:/Git/AgentMind/skills/exp/scripts/_shared_templates.py` with:

```python
from ._shared_taxonomy import FAILURE_KINDS, FAILURE_SIGNAL_SOURCES, WORK_DOMAINS


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
```

Create `E:/Git/AgentMind/skills/exp/scripts/_shared_render.py` with:

```python
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
```

Create `E:/Git/AgentMind/skills/exp/scripts/_shared_paths.py` with:

```python
from pathlib import Path


def get_root(root_arg: str | None) -> Path:
    return Path(root_arg or ".explib")
```

Create `E:/Git/AgentMind/skills/exp/scripts/_shared_index.py` with:

```python
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
```

Create `E:/Git/AgentMind/tests/helpers/explib_fixture.py` with:

```python
from pathlib import Path


def make_empty_root(tmpdir: Path) -> Path:
    root = tmpdir / ".explib"
    root.mkdir(parents=True, exist_ok=True)
    return root
```

- [ ] **Step 4: Run the shared-module tests again**

Run:

```powershell
uv run -m unittest tests.test_init_explib -v
```

Expected:

- all tests pass

- [ ] **Step 5: Commit the shared module foundation**

Run:

```powershell
git add skills/exp/scripts tests/test_init_explib.py tests/helpers/explib_fixture.py
git commit -m "feat: add .explib shared script helpers"
```

## Task 3: Implement `init_explib.py` And Its End-To-End Tests

**Files:**
- Create: `E:/Git/AgentMind/skills/exp/scripts/init_explib.py`
- Modify: `E:/Git/AgentMind/tests/test_init_explib.py`
- Test: `E:/Git/AgentMind/tests/test_init_explib.py`

- [ ] **Step 1: Add the failing init script tests**

Append these tests to `E:/Git/AgentMind/tests/test_init_explib.py`:

```python
import json
import subprocess
import sys
import tempfile


class InitExplibScriptTests(unittest.TestCase):
    def test_init_explib_creates_required_skeleton(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            cmd = [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "init_explib.py"),
                "--root",
                str(root),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue((root / "EXP.md").is_file())
            self.assertTrue((root / "domains" / "api-integration" / "toc.index.json").is_file())
            self.assertTrue((root / "domains" / "api-integration" / "TOC.md").is_file())
            self.assertFalse((root / "resolved" / "api-integration").exists())

    def test_init_explib_check_mode_reports_missing_items_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            cmd = [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "init_explib.py"),
                "--root",
                str(root),
                "--check",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(root.exists())
            self.assertIn(".explib/EXP.md", "\\n".join(payload["missing_files"]))
```

- [ ] **Step 2: Run the init tests and confirm they fail**

Run:

```powershell
uv run -m unittest tests.test_init_explib -v
```

Expected:

- subprocess failures because `init_explib.py` does not exist yet

- [ ] **Step 3: Implement `init_explib.py`**

Create `E:/Git/AgentMind/skills/exp/scripts/init_explib.py` with:

```python
import argparse
import json
from pathlib import Path

from _shared_paths import get_root
from _shared_render import render_domain_toc
from _shared_taxonomy import WORK_DOMAINS
from _shared_templates import (
    empty_domain_index,
    render_dead_ends_toc,
    render_exp_md,
    render_pending_toc,
    render_resolved_toc,
)
from _shared_index import load_domain_index, save_domain_index


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".explib")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    root = get_root(args.root)

    required_dirs = [
        root,
        root / "pending",
        root / "pending" / "events",
        root / "resolved",
        root / "dead-ends",
        root / "domains",
    ] + [root / "domains" / name for name in WORK_DOMAINS]

    required_files = {
        root / "EXP.md": render_exp_md(),
        root / "pending" / "TOC.md": render_pending_toc(),
        root / "resolved" / "TOC.md": render_resolved_toc(),
        root / "dead-ends" / "TOC.md": render_dead_ends_toc(),
    }

    created_dirs = []
    missing_dirs = []
    created_files = []
    missing_files = []
    created_index_files = []
    rendered_tocs = []

    if args.check:
        for path in required_dirs:
            if not path.exists():
                missing_dirs.append(path.as_posix())
        for path in required_files:
            if not path.exists():
                missing_files.append(path.as_posix())
        code = "ok" if not missing_dirs and not missing_files else "validation_failed"
        ok = code == "ok"
        print(json.dumps({
            "ok": ok,
            "code": code,
            "action": "init_explib",
            "root": root.as_posix(),
            "mode": "check",
            "missing_dirs": missing_dirs,
            "missing_files": missing_files,
        }))
        return 0 if ok else 1

    for path in required_dirs:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(path.as_posix())

    for path, content in required_files.items():
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created_files.append(path.as_posix())

    for domain in WORK_DOMAINS:
        index_path = root / "domains" / domain / "toc.index.json"
        if not index_path.exists():
            save_domain_index(index_path, empty_domain_index(domain))
            created_index_files.append(index_path.as_posix())
        index_data = load_domain_index(index_path)
        toc_path = root / "domains" / domain / "TOC.md"
        rendered = render_domain_toc(index_data)
        current = toc_path.read_text(encoding="utf-8") if toc_path.exists() else None
        if current != rendered:
            toc_path.write_text(rendered, encoding="utf-8")
            rendered_tocs.append(toc_path.as_posix())

    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "init_explib",
        "root": root.as_posix(),
        "mode": "init",
        "created_dirs": created_dirs,
        "created_files": created_files,
        "created_index_files": created_index_files,
        "rendered_tocs": rendered_tocs,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the init tests again**

Run:

```powershell
uv run -m unittest tests.test_init_explib -v
```

Expected:

- all init tests pass

- [ ] **Step 5: Commit `init_explib.py`**

Run:

```powershell
git add skills/exp/scripts/init_explib.py tests/test_init_explib.py
git commit -m "feat: add .explib init script"
```

## Task 4: Implement `validate_explib.py` With Issue Codes And Blocking Decisions

**Files:**
- Create: `E:/Git/AgentMind/skills/exp/scripts/_shared_validate.py`
- Create: `E:/Git/AgentMind/skills/exp/scripts/validate_explib.py`
- Create: `E:/Git/AgentMind/tests/test_validate_explib.py`
- Test: `E:/Git/AgentMind/tests/test_validate_explib.py`

- [ ] **Step 1: Write the failing validation tests**

Create `E:/Git/AgentMind/tests/test_validate_explib.py` with:

```python
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidateExplibTests(unittest.TestCase):
    def test_validate_reports_missing_required_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            root.mkdir(parents=True)
            cmd = [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "validate_explib.py"),
                "--root",
                str(root),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["code"], "validation_failed")
            self.assertTrue(any(issue["issue_code"] == "missing_required_file" for issue in payload["issues"]))
```

- [ ] **Step 2: Run the validation test and confirm it fails**

Run:

```powershell
uv run -m unittest tests.test_validate_explib -v
```

Expected:

- subprocess failure because `validate_explib.py` does not exist yet

- [ ] **Step 3: Implement `_shared_validate.py` and `validate_explib.py`**

Create `E:/Git/AgentMind/skills/exp/scripts/_shared_validate.py` with:

```python
def make_issue(level, issue_code, path, message, *, target=None, field=None, value=None, blocking=True, ai_action="stop_and_fix"):
    return {
        "level": level,
        "issue_code": issue_code,
        "path": path,
        "target": target,
        "field": field,
        "value": value,
        "blocking": blocking,
        "ai_action": ai_action,
        "message": message,
    }
```

Create `E:/Git/AgentMind/skills/exp/scripts/validate_explib.py` with:

```python
import argparse
import json
from pathlib import Path

from _shared_paths import get_root
from _shared_taxonomy import WORK_DOMAINS
from _shared_validate import make_issue


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".explib")
    return parser.parse_args()


def main():
    args = parse_args()
    root = get_root(args.root)
    issues = []

    required_files = [
        root / "EXP.md",
        root / "pending" / "TOC.md",
        root / "resolved" / "TOC.md",
        root / "dead-ends" / "TOC.md",
    ]
    for path in required_files:
        if not path.exists():
            issues.append(
                make_issue(
                    "error",
                    "missing_required_file",
                    path.as_posix(),
                    "Required file is missing",
                    ai_action="run_init",
                )
            )

    for domain in WORK_DOMAINS:
        index_path = root / "domains" / domain / "toc.index.json"
        if not index_path.exists():
            issues.append(
                make_issue(
                    "error",
                    "missing_toc_index",
                    index_path.as_posix(),
                    "Domain index file is missing",
                )
            )

    payload = {
        "ok": not issues,
        "code": "ok" if not issues else "validation_failed",
        "action": "validate_explib",
        "root": root.as_posix(),
        "summary": {
            "error_count": sum(1 for issue in issues if issue["level"] == "error"),
            "warning_count": sum(1 for issue in issues if issue["level"] == "warning"),
        },
        "issues": issues,
    }
    print(json.dumps(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the validation tests again**

Run:

```powershell
uv run -m unittest tests.test_validate_explib -v
```

Expected:

- validation test passes

- [ ] **Step 5: Commit the validation layer**

Run:

```powershell
git add skills/exp/scripts/_shared_validate.py skills/exp/scripts/validate_explib.py tests/test_validate_explib.py
git commit -m "feat: add .explib validation script"
```

## Task 5: Implement Query Helpers `list_toc_entries.py` And `get_entry.py`

**Files:**
- Create: `E:/Git/AgentMind/skills/exp/scripts/list_toc_entries.py`
- Create: `E:/Git/AgentMind/skills/exp/scripts/get_entry.py`
- Create: `E:/Git/AgentMind/tests/test_explib_query_scripts.py`
- Test: `E:/Git/AgentMind/tests/test_explib_query_scripts.py`

- [ ] **Step 1: Write the failing query-script tests**

Create `E:/Git/AgentMind/tests/test_explib_query_scripts.py` with:

```python
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class QueryScriptTests(unittest.TestCase):
    def test_list_toc_entries_returns_structured_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".explib"
            root.mkdir(parents=True)
            (root / "domains" / "api-integration").mkdir(parents=True)
            (root / "domains" / "api-integration" / "toc.index.json").write_text(
                json.dumps(
                    {
                        "domain": "api-integration",
                        "resolved": [
                            {
                                "id": "api-integration-resolved-001",
                                "pattern_name": "Request schema mismatch on API call",
                                "failure_kind": "api_failure",
                                "signals": ["400 invalid_request_error", "unknown field"],
                                "note": "Outdated schema assumptions cause payload rejection",
                                "entry_path": ".explib/resolved/api-integration/api-integration-resolved-001.json",
                            }
                        ],
                        "dead_ends": [],
                    }
                ),
                encoding="utf-8",
            )
            cmd = [
                sys.executable,
                str(REPO_ROOT / "skills" / "exp" / "scripts" / "list_toc_entries.py"),
                "--root",
                str(root),
                "--domain",
                "api-integration",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["entries"][0]["kind"], "resolved")
            self.assertEqual(payload["entries"][0]["id"], "api-integration-resolved-001")
```

- [ ] **Step 2: Run the query tests and confirm they fail**

Run:

```powershell
uv run -m unittest tests.test_explib_query_scripts -v
```

Expected:

- subprocess failures because the scripts do not exist yet

- [ ] **Step 3: Implement the query scripts**

Create `E:/Git/AgentMind/skills/exp/scripts/list_toc_entries.py` with:

```python
import argparse
import json

from _shared_index import load_domain_index
from _shared_paths import get_root


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".explib")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--section", choices=["resolved", "dead_end"])
    parser.add_argument("--failure-kind")
    return parser.parse_args()


def main():
    args = parse_args()
    root = get_root(args.root)
    index_path = root / "domains" / args.domain / "toc.index.json"
    data = load_domain_index(index_path)

    entries = []
    if args.section in (None, "resolved"):
        for item in data["resolved"]:
            enriched = dict(item)
            enriched["kind"] = "resolved"
            entries.append(enriched)
    if args.section in (None, "dead_end"):
        for item in data["dead_ends"]:
            enriched = dict(item)
            enriched["kind"] = "dead_end"
            entries.append(enriched)

    if args.failure_kind:
        entries = [item for item in entries if item["failure_kind"] == args.failure_kind]

    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "list_toc_entries",
        "root": root.as_posix(),
        "domain": args.domain,
        "section": args.section,
        "filters": {"failure_kind": args.failure_kind},
        "entries": entries,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `E:/Git/AgentMind/skills/exp/scripts/get_entry.py` with:

```python
import argparse
import json
from pathlib import Path

from _shared_paths import get_root


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".explib")
    parser.add_argument("--id", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    root = get_root(args.root)
    matches = list(root.glob(f"resolved/*/{args.id}.json")) + list(root.glob(f"dead-ends/*/{args.id}.json"))
    if not matches:
        print(json.dumps({
            "ok": False,
            "code": "not_found",
            "action": "get_entry",
            "root": root.as_posix(),
            "id": args.id,
        }))
        return 1
    if len(matches) > 1:
        print(json.dumps({
            "ok": False,
            "code": "ambiguous_id",
            "action": "get_entry",
            "root": root.as_posix(),
            "id": args.id,
        }))
        return 1

    path = matches[0]
    entry = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps({
        "ok": True,
        "code": "ok",
        "action": "get_entry",
        "root": root.as_posix(),
        "id": args.id,
        "entry_path": path.as_posix(),
        "kind": entry["kind"],
        "work_domain": entry["work_domain"],
        "failure_kind": entry["failure_kind"],
        "entry": entry,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the query tests again**

Run:

```powershell
uv run -m unittest tests.test_explib_query_scripts -v
```

Expected:

- query test passes

- [ ] **Step 5: Commit the query scripts**

Run:

```powershell
git add skills/exp/scripts/list_toc_entries.py skills/exp/scripts/get_entry.py tests/test_explib_query_scripts.py
git commit -m "feat: add .explib query scripts"
```

## Final Verification Checklist

- `uv run -m unittest tests.test_exp_layout tests.test_init_explib tests.test_validate_explib tests.test_explib_query_scripts -v` passes
- `skills/exp/SKILL.md` references `.explib/EXP.md`
- README files reference `.explib/` and `skills/exp/`
- `init_explib.py` is idempotent and creates `.explib/domains/<domain>/toc.index.json`
- `validate_explib.py` returns structured issues with `issue_code`
- `list_toc_entries.py` returns structured entries with `kind`
- `get_entry.py` returns `not_found` and `ambiguous_id` correctly

## Notes For Execution

- Do not add write-path scripts in this pass.
- Do not add automatic migration logic from `EXP/` to `.explib/`.
- Keep `_shared_*` modules minimal; do not smuggle in future P2 logic.
- If the user deletes `EXP/` manually during implementation, treat `.explib/` as the only supported path going forward.
