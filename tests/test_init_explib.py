import json
import importlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.helpers.explib_fixture import make_empty_root
from skills.exp.scripts._shared_templates import empty_domain_index, render_exp_md
from skills.exp.scripts._shared_render import render_domain_toc
from skills.exp.scripts._shared_taxonomy import FAILURE_SIGNAL_SOURCES


class InitExplibSupportTests(unittest.TestCase):
    def test_fixture_make_empty_root_creates_explib_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_empty_root(Path(tmp))
            self.assertTrue(root.exists())
            self.assertTrue(root.is_dir())
            self.assertEqual(root.name, ".explib")

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

    def test_shared_templates_imports_in_script_mode(self):
        scripts_dir = Path(__file__).resolve().parents[1] / "skills" / "exp" / "scripts"
        before_path = list(sys.path)
        try:
            sys.path.insert(0, str(scripts_dir))
            sys.modules.pop("_shared_templates", None)
            module = importlib.import_module("_shared_templates")
            self.assertTrue(hasattr(module, "render_exp_md"))
        finally:
            sys.modules.pop("_shared_templates", None)
            sys.path[:] = before_path


REPO_ROOT = Path(__file__).resolve().parents[1]


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
            self.assertIn(".explib/EXP.md", "\n".join(payload["missing_files"]))


if __name__ == "__main__":
    unittest.main()
