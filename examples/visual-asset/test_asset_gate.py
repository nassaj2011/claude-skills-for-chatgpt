import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual_gate", HERE / "asset_gate.py")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class SvgGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.svg = (HERE / "booking-social.svg").read_text(encoding="utf-8")
        cls.rights = json.loads((HERE / "rights.json").read_text(encoding="utf-8"))

    def test_clean_vector_source(self):
        self.assertEqual(mod.validate(self.svg, self.rights)["decision"], "PASS_STATIC_CHECK")

    def test_accessible_title_required(self):
        self.assertEqual(mod.validate(self.svg.replace("<title ", "<metadata ").replace("</title>", "</metadata>"), self.rights)["decision"], "BLOCK")

    def test_external_asset_references_disallowed(self):
        tampered = self.svg.replace("</svg>", '<image href="https://example.invalid/track.svg"/></svg>')
        self.assertIn("BLOCK", mod.validate(tampered, self.rights)["decision"])

    def test_script_tags_disallowed(self):
        self.assertEqual(mod.validate(self.svg.replace("</svg>", "<script>1</script></svg>"), self.rights)["decision"], "BLOCK")

    def test_rights_undocumented_blocks(self):
        rights = dict(self.rights, external_media=["unknown-source"])
        self.assertEqual(mod.validate(self.svg, rights)["decision"], "BLOCK")

    def test_contrast_is_above_threshold(self):
        self.assertGreater(mod.contrast("#ffffff", "#102a21"), 4.5)

    def test_bad_geometry_blocked(self):
        self.assertEqual(mod.validate(self.svg.replace('width="1200"', 'width="800"', 1), self.rights)["decision"], "BLOCK")

    def test_color_change_breaks_contrast(self):
        changed = self.svg.replace('font-size="68" font-weight="700" fill="#ffffff"',
                                   'font-size="68" font-weight="700" fill="#102a21"')
        self.assertEqual(mod.validate(changed, self.rights)["decision"], "BLOCK")

    def test_undocumented_license_blocks(self):
        self.assertEqual(mod.validate(self.svg, dict(self.rights, license="UNKNOWN"))["decision"], "BLOCK")


if __name__ == "__main__":
    unittest.main()
