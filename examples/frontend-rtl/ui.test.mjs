import test from "node:test";
import assert from "node:assert/strict";
import { transition, renderStatus, PHASES } from "./ui.mjs";

test("valid state transitions", () => {
  const initial = { phase: "idle", message: "" };
  const loading = transition(initial, { type: "SUBMIT", slot: "morning" });
  assert.equal(loading.phase, "loading");
  assert.equal(transition(loading, { type: "SUBMIT", slot: "evening" }), loading);
  const success = transition(loading, { type: "RESOLVE" });
  assert.equal(success.phase, "success");
  assert.equal(transition(success, { type: "RESET" }).phase, "idle");
});
test("invalid slot does not reserve", () => {
  const result = transition({ phase: "idle", message: "" }, { type: "SUBMIT", slot: "<script>" });
  assert.equal(result.phase, "error");
  assert.match(result.message, /انتخاب/);
});
test("failure and stale responses do not corrupt state", () => {
  const loading = transition({ phase: "idle", message: "" }, { type: "SUBMIT", slot: "evening" });
  assert.equal(transition(loading, { type: "FAIL" }).phase, "error");
  assert.equal(transition({ phase: "idle", message: "" }, { type: "RESOLVE" }).phase, "idle");
});
test("render uses text only, not HTML", () => {
  const el = { textContent: "", dataset: {} };
  renderStatus(el, { phase: "error", message: "<script>bad</script>" });
  assert.equal(el.textContent, "<script>bad</script>");
  assert.equal(el.dataset.phase, "error");
});
test("all UX phases defined", () => assert.deepEqual([...PHASES], ["idle", "loading", "success", "error"]));
