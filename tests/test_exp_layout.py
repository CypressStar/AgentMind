from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = REPO_ROOT / "docs" / "superpowers" / "specs" / "2026-04-20-exp-design.md"
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


class ExpLayoutTests(unittest.TestCase):
    def test_initial_exp_skeleton_paths_exist(self):
        for path in REQUIRED_DIRS:
            self.assertTrue(path.is_dir(), f"Missing directory: {path}")
        for path in REQUIRED_FILES:
            self.assertTrue(path.is_file(), f"Missing file: {path}")

    def test_spec_mentions_shared_domain_router_and_lazy_leaf_dirs(self):
        text = SPEC_PATH.read_text(encoding="utf-8")
        self.assertIn("EXP/domains/<work-domain>/TOC.md", text)
        self.assertRegex(
            text,
            r"(?s)leaf directories under .*`resolved/`.*`dead-ends/`.*created lazily",
        )
        self.assertRegex(
            text,
            r"(?s)`pending/events/<event-id>/`.*created lazily",
        )

    def test_exp_md_contains_closed_taxonomy_and_manual_extension_rules(self):
        text = (REPO_ROOT / "EXP" / "EXP.md").read_text(encoding="utf-8")
        failure_kinds = {
            "runtime_error",
            "test_failure",
            "api_failure",
            "tool_failure",
            "quality_failure",
            "reasoning_failure",
        }
        for kind in failure_kinds:
            self.assertRegex(text, rf"`{re.escape(kind)}`")

        for name in DOMAIN_NAMES:
            self.assertRegex(text, rf"`{re.escape(name)}`")

        self.assertRegex(
            text,
            r"(?is)only\s+the\s+user\s+may\s+.*(add|revise).*taxonomy",
        )

    def test_top_level_tocs_route_by_domain(self):
        for relative_path in ["resolved/TOC.md", "dead-ends/TOC.md"]:
            text = (REPO_ROOT / "EXP" / relative_path).read_text(encoding="utf-8")
            self.assertIn("| work_domain | toc | note |", text)
            for name in DOMAIN_NAMES:
                self.assertRegex(
                    text,
                    rf"\|\s*{re.escape(name)}\s*\|\s*\[TOC\]\(\.\./domains/{re.escape(name)}/TOC\.md\)\s*\|",
                )

    def test_pending_toc_explains_lazy_event_creation(self):
        text = (REPO_ROOT / "EXP" / "pending" / "TOC.md").read_text(encoding="utf-8")
        lower = text.lower()
        self.assertIn("events/<event-id>/", text)
        self.assertIn("created", lower)
        self.assertIn("unresolved", lower)
        self.assertIn("only", lower)
        self.assertTrue(
            re.search(r"created.*unresolved", lower, re.DOTALL)
            or re.search(r"unresolved.*created", lower, re.DOTALL),
            "Pending TOC should describe lazy creation tied to unresolved items.",
        )


if __name__ == "__main__":
    unittest.main()
