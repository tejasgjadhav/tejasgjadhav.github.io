/* Shared runner for the live lab pages.
   Pyodide is pinned to an exact version so the page behaves the same next year.
   Data is fetched same-origin from data/. Nothing else is fetched at run time. */
const PYODIDE_VERSION = "314.0.7";
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v" + PYODIDE_VERSION + "/full/";

const RUNNER = `
import io, contextlib, traceback, json
_ns = dict(_INJECT)
_out = io.StringIO()
_ok = True
try:
    with contextlib.redirect_stdout(_out):
        exec(compile(USER_CODE, "<lab>", "exec"), _ns)
except BaseException:
    _ok = False
    traceback.print_exc(file=_out)
json.dumps({"ok": _ok, "out": _out.getvalue()})
`;

function initLab(cfg) {
  const codeEl = document.getElementById("code");
  const outEl = document.getElementById("out");
  const statusEl = document.getElementById("status");
  const runBtn = document.getElementById("run");
  const resetBtn = document.getElementById("reset");
  const original = codeEl.value;
  let py = null;
  const files = {};

  function busy(msg) { statusEl.className = "status busy"; statusEl.textContent = msg; }
  function idle(msg) { statusEl.className = "status"; statusEl.textContent = msg; }

  async function boot() {
    runBtn.disabled = true;
    busy("Booting Pyodide " + PYODIDE_VERSION + " in your browser. First load pulls about 10 MB, so give it a moment.");
    outEl.textContent = "Waiting for Python to start.";
    py = await loadPyodide({ indexURL: PYODIDE_URL });
    const pkgs = cfg.packages || [];
    if (pkgs.length) {
      busy("Loading " + pkgs.join(", ") + ".");
      await py.loadPackage(pkgs);
    }
    busy("Reading the data snapshot.");
    for (const [name, url] of Object.entries(cfg.data || {})) {
      const r = await fetch(url, { cache: "force-cache" });
      if (!r.ok) throw new Error("could not read " + url + " (" + r.status + ")");
      files[name] = await r.text();
    }
    runBtn.disabled = false;
    idle("Python is ready. Edit the code and press Run.");
  }

  async function run() {
    if (!py) return;
    runBtn.disabled = true;
    busy("Running.");
    outEl.className = "out";
    try {
      const inject = Object.assign({}, files, { PARAMS: cfg.params ? cfg.params() : {} });
      py.globals.set("USER_CODE", codeEl.value);
      py.globals.set("_INJECT", py.toPy(inject));
      const res = JSON.parse(py.runPython(RUNNER));
      outEl.textContent = res.out || "(the code printed nothing)";
      outEl.className = res.ok ? "out" : "out err";
      idle(res.ok ? "Done." : "The code raised an error. The traceback is above.");
    } catch (e) {
      outEl.textContent = String(e);
      outEl.className = "out err";
      idle("Something went wrong before the code ran.");
    }
    runBtn.disabled = false;
    document.body.setAttribute("data-lab-state", "ran");
  }

  runBtn.addEventListener("click", run);
  resetBtn.addEventListener("click", () => {
    codeEl.value = original;
    idle("Code reset to the version this page shipped with.");
  });
  document.querySelectorAll(".controls input, .controls select").forEach(el => {
    el.addEventListener("change", () => { if (py && !runBtn.disabled) run(); });
  });

  boot().then(run).catch(e => {
    outEl.textContent = String(e);
    outEl.className = "out err";
    idle("Pyodide did not start. Check the browser console.");
    document.body.setAttribute("data-lab-state", "failed");
  });
}
