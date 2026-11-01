#!/usr/bin/env python3
"""Tests for the Free LLM Starter Kit static site build.

Run: python3 -m unittest discover -s tests -v
or:  python3 tests/test_build.py
"""

from __future__ import annotations

import html.parser
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BUILD_SCRIPT = ROOT / "scripts" / "build_site.py"

EXPECTED_PAGES = ["index.html", "getting-started.html", "model-cards.html",
                  "ollama-cheatsheet.html", "prompt-starters.html",
                  "privacy-basics.html", "LICENSE.html"]

REQUIRED_CONTENT = {
    "index.html": ["Free LLM Starter Kit", "Asdale Dynamics, LLC", "No account", "Ollama"],
    "getting-started.html": ["Getting Started", "local LLM", "RAM", "Ollama Setup Cheat Sheet"],
    "model-cards.html": ["Model Cards", "Llama 3.2", "ollama run llama3.2", "RAM"],
    "ollama-cheatsheet.html": ["Ollama Setup Cheat Sheet", "ollama run llama3.2", "ollama list"],
    "prompt-starters.html": ["Prompt Starters", "education only", "never medical advice"],
    "privacy-basics.html": ["Privacy Basics", "stay on your computer", "No account"],
}

SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"-----BEGIN [A-Z ]+",
    r"api_key\s*=\s*[\"'][^\"']+[\"']",
    r"secret\s*=\s*[\"'][^\"']+[\"']",
]


class SiteBuildTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT)],
            capture_output=True, text=True,
        )
        cls.build_stdout = result.stdout
        cls.build_stderr = result.stderr
        cls.build_returncode = result.returncode

    def test_build_exits_cleanly(self):
        self.assertEqual(self.build_returncode, 0, self.build_stderr)

    def test_build_produces_all_pages(self):
        for page in EXPECTED_PAGES:
            path = SITE / page
            self.assertTrue(path.exists(), f"missing {page}")

    def test_pages_contain_required_content(self):
        for page, needles in REQUIRED_CONTENT.items():
            text = (SITE / page).read_text(encoding="utf-8")
            for needle in needles:
                self.assertIn(needle, text, f"{page} missing {needle!r}")

    def test_credit_and_copyright_appear(self):
        for page in EXPECTED_PAGES:
            text = (SITE / page).read_text(encoding="utf-8")
            self.assertIn("Asdale Dynamics, LLC", text, f"{page} lacks Asdale Dynamics credit")
        license_html = (SITE / "LICENSE.html").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", license_html)

    def test_navigation_links_resolve(self):
        for page in EXPECTED_PAGES:
            text = (SITE / page).read_text(encoding="utf-8")
            for href in re.findall(r'href="([^"]+\.html)"', text):
                target = SITE / href
                self.assertTrue(target.exists(), f"{page} links to missing {href}")

    def test_generated_html_parses(self):
        for page in EXPECTED_PAGES:
            text = (SITE / page).read_text(encoding="utf-8")
            parser = html.parser.HTMLParser()
            errors = []

            class CollectingParser(html.parser.HTMLParser):
                def error(self, message):
                    errors.append(message)

            CollectingParser().feed(text)
            # HTMLParser rarely raises; just confirm it feeds without exception.
            self.assertEqual(len(errors), 0, f"{page} parser errors: {errors}")

    def test_tables_render(self):
        text = (SITE / "model-cards.html").read_text(encoding="utf-8")
        self.assertIn("<table>", text)

    def test_code_blocks_render(self):
        text = (SITE / "ollama-cheatsheet.html").read_text(encoding="utf-8")
        self.assertIn("<pre>", text)
        self.assertIn("code", text)

    def test_no_secret_patterns_in_docs(self):
        for path in list(ROOT.glob("*.md")) + list((ROOT / "docs").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for pattern in SECRET_PATTERNS:
                self.assertNotRegex(text, pattern,
                                    f"possible secret pattern {pattern!r} in {path}")

    def test_license_exact_copyright_line(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)

    def test_readme_credits_llc(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", text)


if __name__ == "__main__":
    unittest.main()
