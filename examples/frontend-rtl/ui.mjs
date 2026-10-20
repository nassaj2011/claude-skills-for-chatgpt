// Dependency-free, inspectable UX state machine; NEVER used for server authorization.
export const PHASES = Object.freeze(["idle", "loading", "success", "error"]);

export function transition(state, action) {
  if (!PHASES.includes(state.phase)) throw new Error("Unknown UI phase");
  if (action.type === "RESET") return { phase: "idle", message: "" };
  if (action.type === "SUBMIT") {
    if (state.phase === "loading") return state;
    if (!["morning", "evening"].includes(action.slot))
      return { phase: "error", message: "لطفاً یک سانس معتبر انتخاب کنید." };
    return { phase: "loading", message: "در حال ثبت درخواست آزمایشی…" };
  }
  if (action.type === "RESOLVE" && state.phase === "loading")
    return { phase: "success", message: "درخواست نمونه ثبت شد؛ رزرو واقعی انجام نشده است." };
  if (action.type === "FAIL" && state.phase === "loading")
    return { phase: "error", message: "ثبت درخواست ممکن نبود. دوباره تلاش کنید." };
  return state;
}

export function renderStatus(element, state) {
  element.textContent = state.message; // no unsafe HTML injection
  element.dataset.phase = state.phase;
}

export function attachDemo(document) {
  const form = document.getElementById("booking-form");
  if (!form) return;
  const select = document.getElementById("slot");
  const submit = document.getElementById("submit");
  const status = document.getElementById("status");
  let state = { phase: "idle", message: "" };
  let generation = 0;
  function update(action) {
    state = transition(state, action);
    submit.disabled = state.phase === "loading";
    renderStatus(status, state);
  }
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (state.phase === "loading") return;
    const token = ++generation;
    update({ type: "SUBMIT", slot: select.value });
    if (state.phase !== "loading") return;
    await Promise.resolve(); // illustrative async boundary; NO API request
    if (token === generation) update({ type: "RESOLVE" });
  });
  document.getElementById("reset").addEventListener("click", () => {
    generation++;
    form.reset();
    update({ type: "RESET" });
    select.focus();
  });
  renderStatus(status, state);
}
if (typeof document !== "undefined") attachDemo(document);
