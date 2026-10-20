#!/usr/bin/env python3
"""Optional real-browser geometry check of an authored SVG asset; no internet."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


def run(output: Path | None) -> dict:
    from playwright.sync_api import sync_playwright
    target = Path(__file__).resolve().parent / "booking-social.svg"
    errors, external = [], []
    with sync_playwright() as p:
        browser = None
        runtime = ""
        for opts in ({"channel": "msedge"}, {"channel": "chrome"}, {}):
            try:
                browser = p.chromium.launch(headless=True, **opts)
                runtime = opts.get("channel", "chromium")
                break
            except Exception:
                continue
        if browser is None:
            raise RuntimeError("No installed browser engine; visual browser check NOT RUN")
        try:
            context = browser.new_context(viewport={"width": 1200, "height": 630},
                                          device_scale_factor=1)
            context.route("**/*", lambda route: (
                route.continue_() if urlparse(route.request.url).scheme == "file"
                else (external.append(route.request.url), route.abort())
            ))
            page = context.new_page()
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(target.as_uri(), wait_until="load", timeout=15000)
            assert page.locator("svg").count() == 1
            svg = page.locator("svg")
            assert svg.get_attribute("viewBox") == "0 0 1200 630"
            assert svg.get_attribute("role") == "img"
            assert page.locator("svg title").count() == 1
            assert page.locator("svg desc").count() == 1
            assert page.locator("svg text").count() == 3
            assert svg.evaluate("(e) => { const r=e.getBoundingClientRect(); return [Math.round(r.width),Math.round(r.height)] }") == [1200, 630]
            if output:
                path = output.expanduser().absolute()
                if path.exists() or path.is_symlink():
                    raise ValueError("Refusing to overwrite existing browser evidence")
                path.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(path))
            assert not errors, "Browser error(s): " + str(errors)
            assert not external, "Unexpected outside network: " + str(external)
            context.close()
        finally:
            browser.close()
    return {"browser": runtime, "svg_geometry": "1200x630", "visible_text_nodes": 3,
            "javascript_errors": len(errors), "external_requests": len(external),
            "status": "PASS_BROWSER_GEOMETRY",
            "warning": "Not a human visual audit or color/print/typeface compliance proof."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshot", type=Path)
    args = parser.parse_args()
    try:
        result = run(args.screenshot)
    except Exception as exc:
        parser.exit(1, "SVG_BROWSER_FAILED: " + type(exc).__name__ + ": " + str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
