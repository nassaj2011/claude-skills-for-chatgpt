"""Ensure the ChatGPT Web distribution stays portable and in sync with all skills."""
from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_web_kit", ROOT / "scripts/build_web_kit.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class WebKitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = mod.skill_data()
        cls.files = mod.expected_files(cls.skills)

    def test_29_complete_skill_cards(self):
        self.assertEqual(len(self.skills), 29)
        cards = [f for f in self.files if f.parent == mod.DEST / "cards"]
        self.assertEqual(len(cards), 29)
        for path in cards:
            content = self.files[path]
            self.assertIn("CHATGPT WEB EXECUTION BOUNDARY", content)
            self.assertIn("NOT EXECUTED", content)
            self.assertIn("[Replace with your actual request", content)
            self.assertIn("## Specialist workflow", content)

    def test_project_instructions_do_not_require_codex(self):
        text = self.files[mod.DEST / "PROJECT_INSTRUCTIONS.txt"]
        self.assertIn("ChatGPT web", text)
        self.assertIn("NOT EXECUTED", text)
        self.assertIn("Do not transmit", text)

    def test_uploadable_plaintext_matches_markdown(self):
        self.assertEqual(self.files[mod.DEST / "CHATGPT_WEB_LIBRARY.txt"],
                         self.files[mod.DEST / "CHATGPT_WEB_LIBRARY.md"])
        self.assertGreater(len(self.files[mod.DEST / "CHATGPT_WEB_LIBRARY.txt"]), 20000)

    def test_portal_has_no_external_scripts_or_tracking(self):
        html = self.files[mod.DEST / "index.html"]
        self.assertIn('type="application/json"', html)
        self.assertIn('id="search"', html)
        self.assertIn("navigator.clipboard", html)
        self.assertNotIn("<script src=", html)
        self.assertNotIn("fetch(", html)
        self.assertNotIn("XMLHttpRequest", html)
        self.assertNotIn("sendBeacon", html)

    def test_portal_embedded_json_has_full_prompts(self):
        html = self.files[mod.DEST / "index.html"]
        found = re.search(r'<script id="catalog" type="application/json">(.*?)</script>', html, flags=re.S)
        self.assertIsNotNone(found)
        catalog = json.loads(found.group(1))
        self.assertEqual(len(catalog), 29)
        self.assertEqual([x["name"] for x in catalog], [s["name"] for s in self.skills])
        self.assertTrue(all(x["prompt"].startswith("# ChatGPT Web:") for x in catalog))

    def test_generated_files_are_up_to_date(self):
        for path, expected in self.files.items():
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file(), path)
                self.assertEqual(path.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
