"""GlobalAAR TPS Ops — FastAPI application (LAN web app)."""
import json
from datetime import date, datetime
from pathlib import Path

from fastapi import FastAPI, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import calc, charts, engine
from .models import get_db, get_setting, init_db

APP_DIR = Path(__file__).resolve().parent
app = FastAPI(title="GlobalAAR TPS Ops")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
templates = Jinja2Templates(directory=APP_DIR / "templates")
templates.env.globals.update(hbar=charts.hbar, pareto=charts.pareto, line_trend=charts.line_trend)
templates.env.filters["pct"] = lambda v: "—" if v is None else f"{v*100:.1f}%"
templates.env.filters["num"] = lambda v: "—" if v is None else (f"{v:,.0f}" if abs(v) >= 1000 else f"{v:g}")
templates.env.filters["j"] = lambda v: json.loads(v) if v else []

init_db()


# ---------------------------------------------------------------- helpers
def is_admin(request: Request, con) -> bool:
    return request.cookies.get("aar_admin") == get_setting(con, "admin_pin")


def date_range(request: Request, con):
    """Resolve start/end filters; default = full range of data (falls back to today)."""
    row = con.execute("SELECT MIN(date) a, MAX(date) b FROM shift_entries").fetchone()
    start = request.query_params.get("start") or row["a"] or date.today().isoformat()
    end = request.query_params.get("end") or row["b"] or date.today().isoformat()
    return start, end


def render(request: Request, name: str, con, **ctx):
    ctx.setdefault("admin", is_admin(request, con))
    ctx.setdefault("company", get_setting(con, "company_name"))
    ctx["request"] = request
    return templates.TemplateResponse(request, name, ctx)


def masters_lists(con):
    return {
        "machines": [r["name"] for r in con.execute("SELECT name FROM machines WHERE active=1 ORDER BY name")],
        "operators": [r["name"] for r in con.execute("SELECT name FROM operators WHERE active=1 ORDER BY name")],
        "supervisors": [r["name"] for r in con.execute("SELECT name FROM supervisors WHERE active=1 ORDER BY name")],
        "parts": con.execute("SELECT * FROM parts WHERE active=1 ORDER BY name").fetchall(),
        "defect_types": [r["name"] for r in con.execute("SELECT name FROM defect_types WHERE active=1 ORDER BY sort")],
        "downtime_reasons": [r["name"] for r in con.execute("SELECT name FROM downtime_reasons WHERE active=1 ORDER BY sort")],
    }


# ---------------------------------------------------------------- dashboard
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    con = get_db()
    start, end = date_range(request, con)
    k = con.execute(
        """SELECT SUM(production) p, SUM(ok_qty) ok, SUM(rejection) rej,
                  SUM(total_dt) dt, SUM(total_rm_kg) rm,
                  AVG(eff_pct) eff, AVG(oee) oee, COUNT(*) n
           FROM shift_entries WHERE date BETWEEN ? AND ?""", (start, end)).fetchone()
    daily = con.execute(
        """SELECT date, SUM(production) p, AVG(oee) oee FROM shift_entries
           WHERE date BETWEEN ? AND ? GROUP BY date ORDER BY date""", (start, end)).fetchall()
    mach = con.execute(
        """SELECT machine, AVG(oee) oee FROM shift_entries
           WHERE date BETWEEN ? AND ? AND oee IS NOT NULL GROUP BY machine ORDER BY oee DESC""",
        (start, end)).fetchall()
    top_dt = con.execute(
        """SELECT d.reason, SUM(d.minutes) m FROM entry_downtime d
           JOIN shift_entries e ON e.id=d.entry_id WHERE e.date BETWEEN ? AND ?
           GROUP BY d.reason ORDER BY m DESC LIMIT 6""", (start, end)).fetchall()
    top_def = con.execute(
        """SELECT d.defect, SUM(d.qty) q FROM entry_defects d
           JOIN shift_entries e ON e.id=d.entry_id WHERE e.date BETWEEN ? AND ?
           GROUP BY d.defect ORDER BY q DESC LIMIT 6""", (start, end)).fetchall()
    open_actions = con.execute(
        "SELECT COUNT(*) n FROM actions WHERE status='OPEN'").fetchone()["n"]
    return render(request, "dashboard.html", con, start=start, end=end, k=k,
                  prod_trend=[(r["date"], r["p"]) for r in daily],
                  oee_trend=[(r["date"], r["oee"]) for r in daily],
                  mach_oee=[(r["machine"], round((r["oee"] or 0) * 100, 1)) for r in mach],
                  top_dt=[(r["reason"], r["m"]) for r in top_dt],
                  top_def=[(r["defect"], r["q"]) for r in top_def],
                  open_actions=open_actions,
                  oee_target=float(get_setting(con, "oee_target", "0.85")))


# ---------------------------------------------------------------- shift entry
@app.get("/entry", response_class=HTMLResponse)
@app.get("/entry/{entry_id}/edit", response_class=HTMLResponse)
def entry_form(request: Request, entry_id: int | None = None):
    con = get_db()
    entry, defects, downtime = None, {}, {}
    if entry_id:
        entry = con.execute("SELECT * FROM shift_entries WHERE id=?", (entry_id,)).fetchone()
        defects = {r["defect"]: r["qty"] for r in con.execute(
            "SELECT * FROM entry_defects WHERE entry_id=?", (entry_id,))}
        downtime = {r["reason"]: r["minutes"] for r in con.execute(
            "SELECT * FROM entry_downtime WHERE entry_id=?", (entry_id,))}
    return render(request, "entry_form.html", con, m=masters_lists(con), entry=entry,
                  defects=defects, downtime=downtime, computed=None,
                  today=date.today().isoformat())


@app.post("/entry", response_class=HTMLResponse)
async def entry_save(request: Request):
    con = get_db()
    form = await request.form()
    m = masters_lists(con)
    part = con.execute("SELECT * FROM parts WHERE name=?", (form.get("part"),)).fetchone()
    defects = {d: int(form.get(f"def__{d}") or 0) for d in m["defect_types"]
               if (form.get(f"def__{d}") or "").strip()}
    downtime = {d: float(form.get(f"dt__{d}") or 0) for d in m["downtime_reasons"]
                if (form.get(f"dt__{d}") or "").strip()}
    production = int(form["production"]) if (form.get("production") or "").strip() else None
    planned = float(form["planned_min"]) if (form.get("planned_min") or "").strip() else None
    shift_minutes = float(get_setting(con, "shift_minutes", "720"))
    c = calc.compute_entry(part, planned, production, defects, downtime, shift_minutes) if part else None

    fields = dict(date=form.get("date"), machine=form.get("machine"), shift=form.get("shift"),
                  supervisor=form.get("supervisor"), operator=form.get("operator"),
                  part=form.get("part"), remarks=form.get("remarks"))
    if form.get("action") == "preview" or not part or production is None or not fields["date"]:
        entry = dict(fields, id=form.get("entry_id") or None, production=production,
                     planned_min=planned)
        return render(request, "entry_form.html", con, m=m, entry=entry, defects=defects,
                      downtime=downtime, computed=c, today=date.today().isoformat(),
                      error=None if part and production is not None and fields["date"]
                      else "Date, part and production are required to save.")

    entry_id = form.get("entry_id")
    if entry_id:
        con.execute("DELETE FROM shift_entries WHERE id=?", (entry_id,))
    cur = con.execute(
        """INSERT INTO shift_entries
           (date,machine,shift,supervisor,operator,part,material,cycle_time_s,planned_min,
            production,remarks,total_dt,avail_time,eff_time,tgt_hr,tgt_qty,ok_qty,rejection,
            eff_pct,rej_pct,ok_wt_kg,rej_wt_kg,runner_kg,total_rm_kg,
            availability,performance,quality,oee)
           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (fields["date"], fields["machine"], fields["shift"], fields["supervisor"],
         fields["operator"], fields["part"], part["material_grade"], part["cycle_time_s"],
         planned, production, fields["remarks"],
         c["total_dt"], c["avail_time"], c["eff_time"], c["tgt_hr"], c["tgt_qty"],
         c["ok_qty"], c["rejection"], c["eff_pct"], c["rej_pct"],
         c["ok_wt_kg"], c["rej_wt_kg"], c["runner_kg"], c["total_rm_kg"],
         c["availability"], c["performance"], c["quality"], c["oee"]))
    new_id = cur.lastrowid
    for name, qty in defects.items():
        if qty:
            con.execute("INSERT INTO entry_defects VALUES(?,?,?)", (new_id, name, qty))
    for name, minutes in downtime.items():
        if minutes:
            con.execute("INSERT INTO entry_downtime VALUES(?,?,?)", (new_id, name, minutes))
    con.commit()
    engine.run_engine(con)
    return RedirectResponse(f"/entries?start={fields['date']}&end={fields['date']}", status_code=303)


@app.get("/entries", response_class=HTMLResponse)
def entries(request: Request):
    con = get_db()
    start, end = date_range(request, con)
    machine = request.query_params.get("machine") or ""
    q = "SELECT * FROM shift_entries WHERE date BETWEEN ? AND ?"
    args = [start, end]
    if machine:
        q += " AND machine=?"
        args.append(machine)
    rows = con.execute(q + " ORDER BY date DESC, machine", args).fetchall()
    return render(request, "entries.html", con, rows=rows, start=start, end=end,
                  machine=machine, m=masters_lists(con))


@app.post("/entries/{entry_id}/delete")
def entry_delete(request: Request, entry_id: int):
    con = get_db()
    if is_admin(request, con):
        con.execute("DELETE FROM shift_entries WHERE id=?", (entry_id,))
        con.commit()
    return RedirectResponse("/entries", status_code=303)


# ---------------------------------------------------------------- rework
@app.get("/rework", response_class=HTMLResponse)
def rework(request: Request):
    con = get_db()
    rows = con.execute("SELECT * FROM rework_entries ORDER BY date DESC, id DESC LIMIT 200").fetchall()
    summary = con.execute(
        """SELECT operator, COUNT(*) n, SUM(target_qty) t, SUM(ok_qty) ok, SUM(rej_qty) rej
           FROM rework_entries GROUP BY operator ORDER BY operator""").fetchall()
    thr = float(get_setting(con, "incentive_threshold", "0.85"))
    return render(request, "rework.html", con, rows=rows, summary=summary, thr=thr,
                  m=masters_lists(con), today=date.today().isoformat(), calc=calc)


@app.post("/rework")
def rework_save(request: Request, date_: str = Form(alias="date"), operator: str = Form(...),
                shift: str = Form(""), work_type: str = Form(""), description: str = Form(""),
                target_qty: int = Form(0), ok_qty: int = Form(0), rej_qty: int = Form(0),
                remarks: str = Form("")):
    con = get_db()
    con.execute(
        """INSERT INTO rework_entries(date,operator,shift,work_type,description,
           target_qty,ok_qty,rej_qty,remarks) VALUES(?,?,?,?,?,?,?,?,?)""",
        (date_, operator, shift, work_type, description, target_qty, ok_qty, rej_qty, remarks))
    con.commit()
    return RedirectResponse("/rework", status_code=303)


# ---------------------------------------------------------------- analysis pages
@app.get("/machines", response_class=HTMLResponse)
def machines_page(request: Request):
    con = get_db()
    start, end = date_range(request, con)
    rows = con.execute(
        """SELECT machine, COUNT(*) n, SUM(production) p, SUM(ok_qty) ok, SUM(rejection) rej,
                  AVG(eff_pct) eff, SUM(total_dt) dt, SUM(total_rm_kg) rm,
                  AVG(availability) a, AVG(performance) pf, AVG(quality) q, AVG(oee) oee
           FROM shift_entries WHERE date BETWEEN ? AND ? GROUP BY machine ORDER BY machine""",
        (start, end)).fetchall()
    return render(request, "machines.html", con, rows=rows, start=start, end=end,
                  oee_target=float(get_setting(con, "oee_target", "0.85")))


@app.get("/parts-summary", response_class=HTMLResponse)
def parts_summary(request: Request):
    con = get_db()
    start, end = date_range(request, con)
    rows = con.execute(
        """SELECT e.part, p.customer, e.material, COUNT(*) n, SUM(e.production) prod,
                  SUM(e.ok_qty) ok, SUM(e.rejection) rej, AVG(e.eff_pct) eff,
                  SUM(e.total_rm_kg) rm
           FROM shift_entries e LEFT JOIN parts p ON p.name=e.part
           WHERE e.date BETWEEN ? AND ? GROUP BY e.part ORDER BY prod DESC""",
        (start, end)).fetchall()
    return render(request, "parts_summary.html", con, rows=rows, start=start, end=end)


@app.get("/operators", response_class=HTMLResponse)
def operators_page(request: Request):
    con = get_db()
    start, end = date_range(request, con)
    thr = float(get_setting(con, "incentive_threshold", "0.85"))
    rows = con.execute(
        """SELECT operator, COUNT(*) n, SUM(production) p, SUM(ok_qty) ok, SUM(rejection) rej,
                  AVG(eff_pct) eff, AVG(oee) oee
           FROM shift_entries WHERE date BETWEEN ? AND ? AND operator IS NOT NULL
           GROUP BY operator ORDER BY eff DESC""", (start, end)).fetchall()
    return render(request, "operators.html", con, rows=rows, start=start, end=end, thr=thr)


@app.get("/defects", response_class=HTMLResponse)
def defects_page(request: Request):
    con = get_db()
    start, end = date_range(request, con)
    machine = request.query_params.get("machine") or ""
    extra, args = "", [start, end]
    if machine:
        extra, args = " AND e.machine=?", [start, end, machine]
    rows = con.execute(
        f"""SELECT d.defect, SUM(d.qty) q FROM entry_defects d
            JOIN shift_entries e ON e.id=d.entry_id
            WHERE e.date BETWEEN ? AND ?{extra} GROUP BY d.defect ORDER BY q DESC""",
        args).fetchall()
    by_part = con.execute(
        f"""SELECT e.part, SUM(d.qty) q FROM entry_defects d
            JOIN shift_entries e ON e.id=d.entry_id
            WHERE e.date BETWEEN ? AND ?{extra} GROUP BY e.part ORDER BY q DESC LIMIT 12""",
        args).fetchall()
    return render(request, "defects.html", con, start=start, end=end, machine=machine,
                  items=[(r["defect"], r["q"]) for r in rows],
                  by_part=[(r["part"], r["q"]) for r in by_part], m=masters_lists(con))


@app.get("/downtime", response_class=HTMLResponse)
def downtime_page(request: Request):
    con = get_db()
    start, end = date_range(request, con)
    machine = request.query_params.get("machine") or ""
    extra, args = "", [start, end]
    if machine:
        extra, args = " AND e.machine=?", [start, end, machine]
    rows = con.execute(
        f"""SELECT d.reason, SUM(d.minutes) mnt FROM entry_downtime d
            JOIN shift_entries e ON e.id=d.entry_id
            WHERE e.date BETWEEN ? AND ?{extra} GROUP BY d.reason ORDER BY mnt DESC""",
        args).fetchall()
    by_machine = con.execute(
        f"""SELECT e.machine, SUM(d.minutes) mnt FROM entry_downtime d
            JOIN shift_entries e ON e.id=d.entry_id
            WHERE e.date BETWEEN ? AND ?{extra} GROUP BY e.machine ORDER BY mnt DESC""",
        args).fetchall()
    return render(request, "downtime.html", con, start=start, end=end, machine=machine,
                  items=[(r["reason"], r["mnt"]) for r in rows],
                  by_machine=[(r["machine"], r["mnt"]) for r in by_machine], m=masters_lists(con))


@app.get("/materials", response_class=HTMLResponse)
def materials_page(request: Request):
    con = get_db()
    start, end = date_range(request, con)
    rows = con.execute(
        """SELECT material, SUM(ok_wt_kg) ok, SUM(rej_wt_kg) rej, SUM(runner_kg) run,
                  SUM(total_rm_kg) total
           FROM shift_entries WHERE date BETWEEN ? AND ? AND material IS NOT NULL
           GROUP BY material ORDER BY total DESC""", (start, end)).fetchall()
    return render(request, "materials.html", con, rows=rows, start=start, end=end)


@app.get("/daily", response_class=HTMLResponse)
@app.get("/report/daily", response_class=HTMLResponse)
def daily_page(request: Request):
    con = get_db()
    row = con.execute("SELECT MAX(date) m FROM shift_entries").fetchone()
    d = request.query_params.get("date") or row["m"] or date.today().isoformat()
    rows = con.execute(
        "SELECT * FROM shift_entries WHERE date=? ORDER BY machine, shift", (d,)).fetchall()
    k = con.execute(
        """SELECT SUM(production) p, SUM(ok_qty) ok, SUM(rejection) rej, SUM(total_dt) dt,
                  SUM(total_rm_kg) rm, AVG(eff_pct) eff, AVG(oee) oee
           FROM shift_entries WHERE date=?""", (d,)).fetchone()
    dts = con.execute(
        """SELECT d.reason, SUM(d.minutes) m FROM entry_downtime d
           JOIN shift_entries e ON e.id=d.entry_id WHERE e.date=?
           GROUP BY d.reason ORDER BY m DESC LIMIT 8""", (d,)).fetchall()
    defs = con.execute(
        """SELECT d.defect, SUM(d.qty) q FROM entry_defects d
           JOIN shift_entries e ON e.id=d.entry_id WHERE e.date=?
           GROUP BY d.defect ORDER BY q DESC LIMIT 8""", (d,)).fetchall()
    printable = request.url.path.startswith("/report")
    return render(request, "daily.html", con, d=d, rows=rows, k=k,
                  dts=[(r["reason"], r["m"]) for r in dts],
                  defs=[(r["defect"], r["q"]) for r in defs], printable=printable,
                  plant=get_setting(con, "plant"))


# ---------------------------------------------------------------- actions / PDCA
@app.get("/actions", response_class=HTMLResponse)
def actions_page(request: Request):
    con = get_db()
    show = request.query_params.get("show") or "OPEN"
    q = "SELECT * FROM actions"
    if show != "ALL":
        q += f" WHERE status='{'OPEN' if show == 'OPEN' else 'CLOSED'}'"
    rows = con.execute(q + " ORDER BY status='CLOSED', category, id DESC").fetchall()
    return render(request, "actions.html", con, rows=rows, show=show)


@app.post("/actions/run")
def actions_run(request: Request):
    con = get_db()
    n = len(engine.run_engine(con))
    return RedirectResponse(f"/actions?ran={n}", status_code=303)


@app.post("/actions/new")
def action_new(request: Request, title: str = Form(...), category: str = Form("MANUAL"),
               problem: str = Form(""), owner: str = Form(""), due_date: str = Form("")):
    con = get_db()
    con.execute(
        """INSERT INTO actions(key,date,source,category,title,problem,owner,due_date)
           VALUES(NULL,?, 'MANUAL',?,?,?,?,?)""",
        (date.today().isoformat(), category, title, problem, owner, due_date))
    con.commit()
    return RedirectResponse("/actions", status_code=303)


@app.post("/actions/{action_id}/update")
def action_update(request: Request, action_id: int, pdca: str = Form(None),
                  status: str = Form(None), owner: str = Form(None),
                  due_date: str = Form(None), result: str = Form(None)):
    con = get_db()
    row = con.execute("SELECT * FROM actions WHERE id=?", (action_id,)).fetchone()
    if row:
        closed = date.today().isoformat() if status == "CLOSED" else row["closed_date"]
        con.execute(
            """UPDATE actions SET pdca=COALESCE(?,pdca), status=COALESCE(?,status),
               owner=COALESCE(?,owner), due_date=COALESCE(?,due_date),
               result=COALESCE(?,result), closed_date=? WHERE id=?""",
            (pdca, status, owner, due_date, result, closed, action_id))
        con.commit()
    return RedirectResponse("/actions", status_code=303)


# ---------------------------------------------------------------- quality
@app.get("/quality", response_class=HTMLResponse)
def quality_page(request: Request):
    con = get_db()
    ncrs = con.execute("SELECT * FROM ncr ORDER BY id DESC LIMIT 100").fetchall()
    capas = con.execute("SELECT * FROM capa ORDER BY id DESC LIMIT 100").fetchall()
    return render(request, "quality.html", con, ncrs=ncrs, capas=capas,
                  m=masters_lists(con), today=date.today().isoformat())


@app.post("/quality/ncr")
def ncr_new(request: Request, date_: str = Form(alias="date"), source: str = Form(...),
            customer: str = Form(""), part: str = Form(""), defect: str = Form(""),
            qty: int = Form(0), description: str = Form(""), disposition: str = Form(""),
            raised_by: str = Form("")):
    con = get_db()
    n = con.execute("SELECT COUNT(*) c FROM ncr").fetchone()["c"] + 1
    ncr_no = f"NCR-{date_[:4]}-{n:03d}"
    con.execute(
        """INSERT INTO ncr(ncr_no,date,source,customer,part,defect,qty,description,
           disposition,raised_by) VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (ncr_no, date_, source, customer, part, defect, qty, description, disposition, raised_by))
    con.commit()
    return RedirectResponse("/quality", status_code=303)


@app.post("/quality/ncr/{ncr_id}/close")
def ncr_close(request: Request, ncr_id: int):
    con = get_db()
    con.execute("UPDATE ncr SET status='CLOSED', closed_date=? WHERE id=?",
                (date.today().isoformat(), ncr_id))
    con.commit()
    return RedirectResponse("/quality", status_code=303)


@app.post("/quality/capa/new")
def capa_new(request: Request, ncr_id: int = Form(None), title: str = Form("")):
    con = get_db()
    n = con.execute("SELECT COUNT(*) c FROM capa").fetchone()["c"] + 1
    today = date.today().isoformat()
    if ncr_id and not title:
        ncr = con.execute("SELECT * FROM ncr WHERE id=?", (ncr_id,)).fetchone()
        if ncr:
            title = f"{ncr['ncr_no']}: {ncr['defect'] or ncr['description'] or ncr['part']}"
    cur = con.execute(
        "INSERT INTO capa(ncr_id,capa_no,date,title) VALUES(?,?,?,?)",
        (ncr_id, f"CAPA-{today[:4]}-{n:03d}", today, title))
    con.commit()
    return RedirectResponse(f"/quality/capa/{cur.lastrowid}", status_code=303)


@app.get("/quality/capa/{capa_id}", response_class=HTMLResponse)
def capa_form(request: Request, capa_id: int):
    con = get_db()
    row = con.execute("SELECT * FROM capa WHERE id=?", (capa_id,)).fetchone()
    ncr = con.execute("SELECT * FROM ncr WHERE id=?", (row["ncr_id"],)).fetchone() if row and row["ncr_id"] else None
    return render(request, "capa.html", con, c=row, ncr=ncr)


@app.post("/quality/capa/{capa_id}")
async def capa_save(request: Request, capa_id: int):
    con = get_db()
    form = await request.form()
    con.execute(
        """UPDATE capa SET title=?,d1_team=?,d2_problem=?,d3_containment=?,d4_root_cause=?,
           d5_corrective=?,d6_implemented=?,d7_prevent=?,d8_closure=?,owner=?,due_date=?,status=?
           WHERE id=?""",
        (form.get("title"), form.get("d1_team"), form.get("d2_problem"),
         form.get("d3_containment"), form.get("d4_root_cause"), form.get("d5_corrective"),
         form.get("d6_implemented"), form.get("d7_prevent"), form.get("d8_closure"),
         form.get("owner"), form.get("due_date"), form.get("status") or "OPEN", capa_id))
    con.commit()
    return RedirectResponse(f"/quality/capa/{capa_id}", status_code=303)


@app.get("/quality/checklists", response_class=HTMLResponse)
def checklists(request: Request):
    con = get_db()
    return render(request, "checklists.html", con, m=masters_lists(con),
                  plant=get_setting(con, "plant"))


# ---------------------------------------------------------------- import / masters / settings
@app.get("/import", response_class=HTMLResponse)
def import_page(request: Request):
    con = get_db()
    return render(request, "import.html", con, report=None)


@app.post("/import", response_class=HTMLResponse)
async def import_post(request: Request, file: UploadFile):
    con = get_db()
    if not is_admin(request, con):
        return RedirectResponse("/login?next=/import", status_code=303)
    from .importer import import_workbook
    tmp = APP_DIR.parent / "_upload.xlsx"
    tmp.write_bytes(await file.read())
    try:
        report = import_workbook(con, tmp)
        engine.run_engine(con)
    finally:
        tmp.unlink(missing_ok=True)
    return render(request, "import.html", con, report=report)


@app.get("/masters", response_class=HTMLResponse)
def masters_page(request: Request):
    con = get_db()
    if not is_admin(request, con):
        return RedirectResponse("/login?next=/masters", status_code=303)
    return render(request, "masters.html", con, m=masters_lists(con),
                  all_parts=con.execute("SELECT * FROM parts ORDER BY name").fetchall())


@app.post("/masters/list")
def masters_list_edit(request: Request, table: str = Form(...), name: str = Form(...),
                      op: str = Form("add")):
    con = get_db()
    if is_admin(request, con) and table in ("machines", "operators", "supervisors",
                                            "defect_types", "downtime_reasons"):
        if op == "add":
            con.execute(f"INSERT OR IGNORE INTO {table}(name) VALUES(?)", (name.strip(),))
        else:
            con.execute(f"UPDATE {table} SET active=? WHERE name=?",
                        (1 if op == "activate" else 0, name))
        con.commit()
    return RedirectResponse("/masters", status_code=303)


@app.post("/masters/part")
async def masters_part(request: Request):
    con = get_db()
    if not is_admin(request, con):
        return RedirectResponse("/login", status_code=303)
    f = await request.form()
    vals = (f.get("customer"), f.get("project"), f.get("name"), f.get("part_no"),
            f.get("cycle_time_s") or None, f.get("total_cavity") or None,
            f.get("running_cavity") or None, f.get("shot_wt_g") or None,
            f.get("part_wt_g") or None, f.get("runner_wt_g") or None, f.get("material_grade"))
    if f.get("part_id"):
        con.execute(
            """UPDATE parts SET customer=?,project=?,name=?,part_no=?,cycle_time_s=?,
               total_cavity=?,running_cavity=?,shot_wt_g=?,part_wt_g=?,runner_wt_g=?,
               material_grade=?, active=? WHERE id=?""",
            vals + (1 if f.get("active") else 0, f.get("part_id")))
    else:
        con.execute(
            """INSERT INTO parts(customer,project,name,part_no,cycle_time_s,total_cavity,
               running_cavity,shot_wt_g,part_wt_g,runner_wt_g,material_grade) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            vals)
    con.commit()
    return RedirectResponse("/masters", status_code=303)


@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    con = get_db()
    if not is_admin(request, con):
        return RedirectResponse("/login?next=/settings", status_code=303)
    rows = con.execute("SELECT * FROM settings ORDER BY key").fetchall()
    return render(request, "settings.html", con, rows=rows)


@app.post("/settings")
async def settings_save(request: Request):
    con = get_db()
    if is_admin(request, con):
        form = await request.form()
        for k, v in form.items():
            con.execute("UPDATE settings SET value=? WHERE key=?", (v, k))
        con.commit()
    return RedirectResponse("/settings", status_code=303)


# ---------------------------------------------------------------- auth
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    con = get_db()
    return render(request, "login.html", con, next=request.query_params.get("next", "/"))


@app.post("/login")
def login_post(request: Request, pin: str = Form(...), next_url: str = Form("/", alias="next")):
    con = get_db()
    resp = RedirectResponse(next_url if pin == get_setting(con, "admin_pin") else "/login?bad=1",
                            status_code=303)
    if pin == get_setting(con, "admin_pin"):
        resp.set_cookie("aar_admin", pin, max_age=12 * 3600, httponly=True)
    return resp


@app.get("/logout")
def logout(request: Request):
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie("aar_admin")
    return resp
