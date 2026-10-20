#!/usr/bin/env python3
"""Static SVG asset and local rights metadata lint; NOT a visual/rights certification."""
from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SVG = "{http://www.w3.org/2000/svg}"
FORBIDDEN = {"script", "foreignObject", "image"}


def srgb_linear(v: float) -> float:
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", hex_color):
        raise ValueError("Color must be 6-digit hex")
    vals = [int(hex_color[x:x+2], 16) for x in (1, 3, 5)]
    linear = [srgb_linear(x) for x in vals]
    return sum(x * weight for x, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(foreground: str, background: str) -> float:
    values = sorted((luminance(foreground), luminance(background)))
    return (values[1] + 0.05) / (values[0] + 0.05)


def validate(svg_text: str, rights: dict) -> dict:
    failures = []
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        raise ValueError("Unparseable SVG") from exc
    if root.tag != SVG + "svg":
        failures.append("Root must be SVG")
    if root.get("viewBox") != "0 0 1200 630" or root.get("width") != "1200" or root.get("height") != "630":
        failures.append("Geometry must match 1200x630 SVG design brief")
    if root.get("role") != "img" or not root.get("aria-labelledby"):
        failures.append("Missing accessible graphic role/label relation")
    ids = {node.get("id") for node in root.iter() if node.get("id")}
    labels = root.get("aria-labelledby", "").split()
    if not labels or any(x not in ids for x in labels):
        failures.append("Accessible title/description reference missing")
    for target in ("title", "desc"):
        if not any(x.tag == SVG + target and x.text and x.text.strip() for x in root.iter()):
            failures.append("Missing accessible " + target)
    for node in root.iter():
        name = node.tag.split("}")[-1]
        if name in FORBIDDEN:
            failures.append("Active/external content tag prohibited: " + name)
        for key, value in node.attrib.items():
            key_l = key.lower()
            if (key_l.startswith("on") or "href" in key_l or "url(" in value.lower()
                    or re.search(r"https?://", value, flags=re.I)):
                failures.append("External/active SVG attribute prohibited: " + key)
    if "javascript:" in svg_text.lower():
        failures.append("Executable SVG reference found")
    background = next((n.get("fill") for n in root.iter()
                       if n.tag == SVG + "rect" and n.get("width") == "1200"
                       and n.get("height") == "630"), None)
    if not background:
        failures.append("Missing explicit full-canvas background")
    else:
        for node in root.iter():
            if node.tag != SVG + "text":
                continue
            foreground = node.get("fill")
            try:
                ratio = contrast(foreground, background)
            except (ValueError, TypeError):
                ratio = 0
            if ratio < 4.5:
                failures.append("Typography contrast below 4.5: " + str(node.text)[:20])
    if rights.get("license") != "MIT":
        failures.append("Missing explicit original asset license")
    if rights.get("external_media") != [] or rights.get("origin") != "original_vector_created_in_this_repository":
        failures.append("Asset rights source not established by local declaration")
    if rights.get("source_editable") is not True or rights.get("width_px") != 1200 or rights.get("height_px") != 630:
        failures.append("Editable source or exported geometry mismatch")
    if rights.get("human_visual_approval") not in ("NOT_RUN", "APPROVED", "REJECTED"):
        failures.append("Missing real review status")
    return {"decision": "PASS_STATIC_CHECK" if not failures else "BLOCK", "failures": failures,
            "contrast_white_on_background": round(contrast("#ffffff", "#102a21"), 2),
            "caveat": "Does not certify exact rendering, typeface shaping, license ownership, printer output or legal claims."}


def main() -> int:
    folder = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svg", type=Path, default=folder / "booking-social.svg")
    parser.add_argument("--rights", type=Path, default=folder / "rights.json")
    args = parser.parse_args()
    try:
        result = validate(args.svg.read_text(encoding="utf-8"), json.loads(args.rights.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["decision"] == "PASS_STATIC_CHECK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
