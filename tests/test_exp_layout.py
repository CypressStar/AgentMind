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
