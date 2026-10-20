"""Stdlib tests for original Agent Skills manifests and safe installation."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_skills import validate_all, validate_one  # noqa: E402
from install import plan  # noqa: E402


class SkillCatalogTests(unittest.TestCase):
    def test_all_manifests(self) -> None:
        count, problems = validate_all(ROOT / "skills")
        self.assertGreaterEqual(count, 20)
        self.assertEqual(problems, [])

    def test_invalid_manifest_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "bad-skill"
            directory.mkdir()
            (directory / "SKILL.md").write_text(
                "---\nname: Wrong Name\ndescription: short\n---\n\n# Bad\n",
                encoding="utf-8",
            )
            self.assertTrue(validate_one(directory))

    def test_installer_never_plans_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            existing = destination / "product-business-analyst"
            existing.mkdir()
            entries = plan(ROOT / "skills", destination, ["product-business-analyst", "software-architect"])
            self.assertEqual(entries[0][3], "SKIP (already exists)")
            self.assertEqual(entries[1][3], "COPY")
            self.assertFalse((destination / "software-architect").exists(), "Preview mutated filesystem")

    def test_unknown_selection_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                plan(ROOT / "skills", Path(tmp), ["does-not-exist"])


if __name__ == "__main__":
    unittest.main()
