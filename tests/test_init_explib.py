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
