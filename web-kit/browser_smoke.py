#!/usr/bin/env python3
"""End-to-end browser smoke for the offline ChatGPT Web skill selector.

Uses an ephemeral loopback HTTP server and installed Playwright/Edge/Chrome.
No external websites or credentials; no package installation.
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
    def log_message(self, fmt, *args):
        pass


def run(screenshot: Path | None = None, *, direct_file: bool = False) -> dict:
    from playwright.sync_api import sync_playwright
    directory = Path(__file__).resolve().parent
    server = ThreadingHTTPServer(("127.0.0.1", 0),
                                 functools.partial(QuietHandler, directory=str(directory)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    checks: list[str] = []
    blocked: list[str] = []
    errors: list[str] = []
    base = "http://127.0.0.1:" + str(server.server_port)
    page_url = (directory / "index.html").as_uri() if direct_file else base + "/index.html"
    try:
        with sync_playwright() as p:
            browser = None
            kind = "unavailable"
            for opts in ({"channel": "msedge"}, {"channel": "chrome"}, {}):
                try:
                    browser = p.chromium.launch(headless=True, **opts)
                    kind = opts.get("channel", "chromium")
                    break
                except Exception:
                    continue
            if browser is None:
                raise RuntimeError("No installed Chromium/Edge/Chrome runtime")
            try:
                context = browser.new_context(viewport={"width": 390, "height": 844},
                                              permissions=["clipboard-read", "clipboard-write"])
                context.route("**/*", lambda route: (
                    route.continue_() if (urlparse(route.request.url).hostname == "127.0.0.1"
                                        or (direct_file and urlparse(route.request.url).scheme == "file"))
                    else (blocked.append(route.request.url), route.abort())
                ))
                page = context.new_page()
                page.on("pageerror", lambda e: errors.append(str(e)))
                response = page.goto(page_url, wait_until="networkidle", timeout=10000)
                assert response is not None and response.status in (0, 200)
                assert page.locator("html").get_attribute("dir") == "rtl"
                assert page.locator("#grid article").count() == 29
                checks.append("29 real selectable skill cards and RTL")

                field = page.get_by_role("searchbox", name="جست‌وجوی مهارت")
                field.fill("skill-evaluation-benchmark")
                assert page.locator("#grid article").count() == 1
                checks.append("Search filters by actual skill identity")

                page.get_by_role("button", name="کپی پرامپت").click()
                page.locator("#status").get_by_text("کپی شد", exact=False).wait_for(timeout=3000)
                clipboard = page.evaluate("navigator.clipboard.readText()")
                assert "skill-evaluation-benchmark" in clipboard
                assert "CHATGPT WEB EXECUTION BOUNDARY" in clipboard
                assert "[Replace with your actual request" in clipboard
                checks.append("Clipboard contains complete, web-safe task prompt")

                field.fill("")
                assert page.locator("#grid article").count() == 29
                assert page.locator("#count").inner_text().startswith("29")
                checks.append("Search reset restores all 29 skills")

                if screenshot is not None:
                    screenshot = screenshot.expanduser().absolute()
                    if screenshot.exists() or screenshot.is_symlink():
                        raise ValueError("Never overwrite existing screenshot")
                    screenshot.parent.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(screenshot), full_page=True)
                    checks.append("Actual browser screenshot saved")

                assert not errors, "Unexpected JavaScript runtime errors: " + str(errors)
                assert not blocked, "Unexpected outbound requests: " + str(blocked)
                checks.append("No JS errors or external traffic")
                context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    return {"browser": kind, "file_mode": direct_file, "checks": checks, "passed": len(checks),
            "external_requests": len(blocked), "javascript_errors": len(errors),
            "note": "Actual local-browser interaction; not a ChatGPT Project integration test."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--file-mode", action="store_true", help="Open index.html directly as an offline file")
    args = parser.parse_args()
    try:
        result = run(args.screenshot, direct_file=args.file_mode)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        parser.exit(1, "WEB_KIT_BROWSER_TEST_FAILED: " + str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
