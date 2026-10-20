#!/usr/bin/env python3
"""Real Chromium/Playwright smoke checks against an ephemeral loopback server.

No browser packages installed, no external websites used, no server left running.
Requires playwright Python and a locally installed Chromium browser runtime.
"""
from __future__ import annotations

import argparse
import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def run(screenshot: Path | None = None) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright Python is not installed; browser test NOT RUN") from exc

    root = Path(__file__).resolve().parent
    handler = functools.partial(QuietHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    browser = None
    checks: list[str] = []
    errors: list[str] = []
    blocked: list[str] = []
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as pw:
            launch_failures = []
            for options in ({}, {"channel": "msedge"}, {"channel": "chrome"}):
                try:
                    browser = pw.chromium.launch(headless=True, **options)
                    browser_channel = options.get("channel", "bundled chromium")
                    break
                except Exception as exc:
                    launch_failures.append(f"{options or 'bundled'}: {type(exc).__name__}")
            if browser is None:
                raise RuntimeError("No supported installed Chromium/Edge/Chrome runtime; browser test NOT RUN: " + ", ".join(launch_failures))

            context = browser.new_context(viewport={"width": 390, "height": 844},
                                          device_scale_factor=1, reduced_motion="reduce")
            context.route("**/*", lambda route: (
                route.continue_() if urlparse(route.request.url).hostname == "127.0.0.1"
                else (blocked.append(route.request.url), route.abort())
            ))
            page = context.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            resp = page.goto(base + "/index.html", wait_until="networkidle", timeout=15000)
            assert resp and resp.status == 200, "HTML not served successfully"
            assert page.locator("html").get_attribute("lang") == "fa"
            assert page.locator("html").get_attribute("dir") == "rtl"
            checks.append("Persian lang and RTL semantics")

            form_button = page.get_by_role("button", name="درخواست رزرو")
            assert form_button.is_visible()
            assert page.locator("#slot").is_visible()
            checks.append("Accessible form and labels")

            form_button.click()
            assert "انتخاب" in page.locator("#status").inner_text()
            assert page.locator("#status").get_attribute("data-phase") == "error"
            checks.append("Missing slot reports visible accessible error")

            page.locator("#slot").select_option("morning")
            form_button.click()
            page.locator("#status[data-phase='success']").wait_for(timeout=3000)
            assert "واقعی انجام نشده" in page.locator("#status").inner_text()
            checks.append("Valid demo request reports a non-production success")

            page.get_by_role("button", name="بازنشانی").click()
            assert page.locator("#slot").input_value() == ""
            assert page.locator("#slot").evaluate("(e) => document.activeElement === e")
            assert page.locator("#status").get_attribute("data-phase") == "idle"
            checks.append("Reset clears state and returns keyboard focus")

            for width in [390, 320]:
                page.set_viewport_size({"width": width, "height": 844})
                page.wait_for_timeout(30)
                layout = page.evaluate("({scroll:document.documentElement.scrollWidth,view:document.documentElement.clientWidth})")
                assert layout["scroll"] <= layout["view"] + 1, f"Horizontal overflow at {width}px: {layout}"
                checks.append(f"No horizontal overflow at {width}px")

            page.set_viewport_size({"width": 390, "height": 844})
            if screenshot:
                screenshot = screenshot.expanduser().absolute()
                if screenshot.exists() or screenshot.is_symlink():
                    raise ValueError("Will not overwrite an existing screenshot evidence file")
                screenshot.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(screenshot), full_page=True)
                checks.append("Saved actual Chromium screenshot")

            assert not errors, f"JavaScript exceptions: {errors}"
            assert not blocked, f"Unexpected external requests: {blocked}"
            checks.append("No JavaScript exceptions or external requests")
            context.close()
            browser.close()
            browser = None
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    return {"browser": browser_channel, "target": "ephemeral localhost", "checks": checks,
            "passed": len(checks), "external_requests_blocked": len(blocked),
            "javascript_exceptions": len(errors),
            "screenshot": screenshot.as_posix() if screenshot else None,
            "note": "Actual browser smoke test, not a full WCAG or visual-regression audit."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshot", type=Path)
    args = parser.parse_args()
    try:
        result = run(args.screenshot)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        parser.exit(1, f"BROWSER_SMOKE_FAILED: {type(exc).__name__}: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
