"""Local Edge/Chromium browser smoke budget for a fictional RTL page.

No external URLs; tests DOM/resource budget and two small viewports. Does not
measure LCP, INP, CLS, field RUM or WCAG conformance.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

def assess(metrics:dict, *, max_nodes:int=90, max_resources:int=3)->dict:
 if not isinstance(metrics,dict) or set(metrics)!={"nodes","resources","horizontal_overflow","js_errors","external_requests"}:
  raise ValueError("Unexpected browser measurement structure")
 if any(type(metrics[k]) is not int or metrics[k]<0 for k in ("nodes","resources","horizontal_overflow","js_errors","external_requests")):
  raise ValueError("Invalid measurement")
 failed=[]
 if metrics["nodes"]>max_nodes:failed.append("DOM_NODE_BUDGET")
 if metrics["resources"]>max_resources:failed.append("RESOURCE_COUNT_BUDGET")
 if metrics["horizontal_overflow"]>0:failed.append("MOBILE_HORIZONTAL_OVERFLOW")
 if metrics["js_errors"]>0:failed.append("JS_RUNTIME_ERROR")
 if metrics["external_requests"]>0:failed.append("UNEXPECTED_EXTERNAL_TRAFFIC")
 return {"status":"FAIL" if failed else "PASS_LOCAL_BROWSER_BUDGET","failed":failed,"metrics":metrics,
         "caveat":"No Lighthouse/axe or actual Core Web Vitals, assistive-tech assessment or production RUM."}

def run()->dict:
 from playwright.sync_api import sync_playwright
 target=Path(__file__).resolve().parents[1]/"frontend-rtl"/"index.html"
 errors,external=[],[]
 with sync_playwright() as pw:
  browser=None;engine="unavailable"
  for arg in ({"channel":"msedge"},{"channel":"chrome"},{}):
   try:
    browser=pw.chromium.launch(headless=True,**arg);engine=arg.get("channel","chromium");break
   except Exception:continue
  if browser is None:raise RuntimeError("No supported installed browser")
  try:
   context=browser.new_context(viewport={"width":390,"height":844})
   context.route("**/*",lambda route:(route.continue_() if urlparse(route.request.url).scheme=="file" else (external.append(route.request.url),route.abort())))
   page=context.new_page();page.on("pageerror",lambda e:errors.append(str(e)))
   page.goto(target.as_uri(),wait_until="load",timeout=15000)
   page.locator("#status").wait_for()
   overflow=0
   for width in (390,320):
    page.set_viewport_size({"width":width,"height":844})
    w=page.evaluate("({scroll:document.documentElement.scrollWidth, client:document.documentElement.clientWidth})")
    overflow=max(overflow,max(0,w["scroll"]-w["client"]))
   browser_data=page.evaluate("({nodes:document.getElementsByTagName('*').length,resources:performance.getEntriesByType('resource').length})")
   metrics={"nodes":browser_data["nodes"],"resources":browser_data["resources"],"horizontal_overflow":overflow,
            "js_errors":len(errors),"external_requests":len(external)}
   result=assess(metrics);result["engine"]=engine;result["target"]="file:/// local fictional RTL demo"
   context.close()
  finally:browser.close()
 return result

if __name__=="__main__":
 try:print(json.dumps(run(),indent=2,ensure_ascii=False))
 except Exception as exc:raise SystemExit(f"BROWSER_NOT_VERIFIED: {type(exc).__name__}: {exc}")
