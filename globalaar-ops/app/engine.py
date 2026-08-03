"""Autonomous problem engine — deterministic TPS rules over the shift data.

Runs after every save/import and on demand. Each rule that fires produces a
countermeasure card (problem, evidence, likely root causes, recommended
countermeasures, suggested owner) inserted into the PDCA action tracker.
Cards dedupe on a stable key: a card is not re-raised while an action with the
same key is still OPEN.
"""
import json
from datetime import date, timedelta

from .models import get_setting

# ---------------------------------------------------------------- knowledge base
# Injection-moulding defect troubleshooting (standard IM process causes/checks)
DEFECT_KB = {
    "RESTART UP REJ": {
        "causes": ["No standardized startup procedure — parameters drift between stops",
                   "Excessive warm-up shots before first OK part",
                   "Barrel temperature not stabilized before restart",
                   "First-piece approval discipline not enforced"],
        "counters": ["Create a one-page Startup Standard per mould (purge shots, parameter sheet, first-piece check)",
                     "Save proven machine parameter sets and reload on restart (no manual re-tuning)",
                     "Track startup rejects per restart event; target <5 shots to first OK part",
                     "Link restarts to the power-failure countermeasure — fewer stops = fewer startup rejects"],
        "owner": "Production Head"},
    "SETTING REJ": {
        "causes": ["Trial-and-error parameter setting instead of standard parameter sheets",
                   "Setter skill gaps; no first-off approval before running"],
        "counters": ["Master parameter sheet per part/mould, laminated at machine",
                     "First-piece approval (hourly patrol check) before bulk production",
                     "Setter skill matrix + training plan"],
        "owner": "Production Head"},
    "SHORT SHOT": {
        "causes": ["Insufficient injection pressure/speed or shot size",
                   "Melt temperature too low; nozzle/gate partially blocked",
                   "Vent blockage trapping air; cavity imbalance"],
        "counters": ["Verify shot size & cushion; raise injection pressure/speed stepwise",
                     "Check melt temperature profile vs material datasheet",
                     "Clean vents and gates; record parameters on control plan"],
        "owner": "Production Head"},
    "SINK MARK": {
        "causes": ["Hold pressure/time too low; gate freezing before packing completes",
                   "Wall-thickness variation; melt too hot / cooling too short"],
        "counters": ["Increase hold pressure & time until sink disappears, then standardize",
                     "Check gate size vs part weight; review cooling time"],
        "owner": "Production Head"},
    "SILVER MARK": {
        "causes": ["Moisture in resin — insufficient pre-drying (esp. ABS/PC-ABS)",
                   "Melt temperature too high causing degradation; excessive injection speed"],
        "counters": ["Enforce drying standard: temperature/time per material grade, dew-point check",
                     "Audit hopper dryer daily (checklist); reduce melt temp/injection speed"],
        "owner": "Quality Head"},
    "DUST": {
        "causes": ["Open part handling & storage; airborne dust near machines",
                   "Poor packaging hygiene; parts touched with dirty gloves"],
        "counters": ["Cover conveyors/bins; lidded storage; clean-glove standard",
                     "5S zone around press; tack-mats at moulding bay entry"],
        "owner": "Quality Head"},
    "BLACK SPOT": {
        "causes": ["Degraded material burning in barrel dead spots / long residence time",
                   "Contaminated regrind or material handling",
                   "Screw & barrel wear or inadequate purging on colour change"],
        "counters": ["Scheduled purge routine (purging compound) at colour/material change",
                     "Screw-and-barrel cleaning PM; check residence time vs machine size",
                     "Audit regrind ratio & storage — covered, labelled, FIFO"],
        "owner": "Maintenance Head"},
    "BURN MARK": {
        "causes": ["Trapped air igniting (dieseling) — blocked vents",
                   "Injection speed too high at end of fill"],
        "counters": ["Clean/add vents at last-fill areas; reduce final injection speed",
                     "Add decompression; check clamp venting gap"],
        "owner": "Production Head"},
    "WELD LINE": {
        "causes": ["Melt/mould temperature too low where fronts meet",
                   "Flow path too long; vent missing at weld location"],
        "counters": ["Raise melt & mould temperature stepwise; increase injection speed",
                     "Vent at weld position; review gate location with toolmaker"],
        "owner": "Production Head"},
    "FLOW MARK": {
        "causes": ["Cold slug entering cavity; melt/mould temp low",
                   "Improper injection speed profile"],
        "counters": ["Check cold-slug well; raise nozzle temp",
                     "Profile injection speed (slow-fast); increase mould temp"],
        "owner": "Production Head"},
    "GAS MARK": {
        "causes": ["Volatiles from moisture/degraded melt; poor venting"],
        "counters": ["Verify drying; lower melt temp; clean vents"],
        "owner": "Production Head"},
    "WARPAGE": {
        "causes": ["Differential cooling between mould halves; uneven wall thickness",
                   "Hold/cooling time too short; ejection too early"],
        "counters": ["Balance core/cavity cooling temperatures",
                     "Increase cooling time trial; use cooling fixtures for prone parts"],
        "owner": "Production Head"},
    "FLASH": {
        "causes": ["Clamp force insufficient vs projected area; parting-line wear/damage",
                   "Injection pressure too high; melt too hot (low viscosity)"],
        "counters": ["Verify clamp tonnage vs part; inspect parting line — send mould for repair",
                     "Reduce injection pressure/speed; add to mould PM history card"],
        "owner": "Maintenance Head"},
    "OIL MARK": {
        "causes": ["Hydraulic/lubrication oil leak reaching parts; over-greased slides"],
        "counters": ["Fix machine oil leaks (maintenance ticket); wipe-down standard",
                     "Grease-quantity standard for mould slides"],
        "owner": "Maintenance Head"},
    "CATCHING": {
        "causes": ["Part sticking on ejection — insufficient draft/polish, cooling imbalance"],
        "counters": ["Polish sticking area; review ejection speed/pattern",
                     "Adjust cooling; mould-maker review if chronic"],
        "owner": "Maintenance Head"},
    "INSERT FLASH": {
        "causes": ["Insert not seating fully in cavity; insert dimensional variation"],
        "counters": ["Poka-yoke insert seating check; incoming inspection on inserts",
                     "Fixture/locating pin wear check"],
        "owner": "Quality Head"},
    "INSERT OUTSIDE": {
        "causes": ["Operator loading error — insert missed or misplaced",
                   "No verification step before mould close"],
        "counters": ["Poka-yoke: sensor/vision check or count verification before cycle start",
                     "Standard work with photo of correct loading; operator training"],
        "owner": "Production Head"},
    "DENT": {"causes": ["Handling/packing damage after moulding"],
             "counters": ["Part-specific packing standard; soft-lined bins; layer separators"],
             "owner": "Quality Head"},
    "DAMAGE": {"causes": ["Rough handling, part-on-part contact, ejection drop"],
               "counters": ["Drop-height check at ejection; padded chutes; packing SOP"],
               "owner": "Quality Head"},
    "SCRATCH & CRACK": {"causes": ["Part-to-part rubbing in bins; forced ejection stress"],
                        "counters": ["Single-layer packing for A-surface parts; review ejection balance"],
                        "owner": "Quality Head"},
}

DOWNTIME_KB = {
    "POWER FAILURE": {
        "causes": ["Grid supply instability at Ranjangaon MIDC; no changeover buffer",
                   "No auto-restart / parameter-retention plan, so every outage also causes startup rejects"],
        "counters": ["Power audit: log every outage (time, duration, feeder) for one month — data for MSEB/MIDC escalation",
                     "Evaluate DG set / high-capacity UPS for critical machines: compare monthly downtime cost vs amortized DG cost",
                     "Machine restart standard: saved parameter sets + restart sequence card at every press",
                     "Stagger restart of barrel heaters to avoid demand spike tripping"],
        "owner": "Plant Head"},
    "NO MANPOWER": {
        "causes": ["Absenteeism without buffer; skills tied to specific operators",
                   "No cross-training — one absence idles a whole press"],
        "counters": ["Skill matrix (ILUO) per operator × machine; close gaps with cross-training plan",
                     "Absenteeism tracking with reason codes; buffer/relief operator per shift",
                     "Incentive linkage: attendance + efficiency (data already tracked in this system)"],
        "owner": "Production Head"},
    "MOULD CHANGE": {
        "causes": ["Internal work done while machine stopped (no SMED separation)",
                   "Moulds/tools not pre-staged before changeover"],
        "counters": ["SMED workshop: video one changeover, split internal/external work",
                     "Pre-stage next mould, pre-heated, with fittings, before stop",
                     "Standard changeover time target per tonnage class; track every changeover"],
        "owner": "Production Head"},
    "MACHINE PROBLEM": {
        "causes": ["Reactive maintenance — no PM calendar or daily checks"],
        "counters": ["Preventive-maintenance calendar per machine (Phase-2 module)",
                     "Daily operator autonomous-maintenance checklist (CLIT: clean, lubricate, inspect, tighten)",
                     "Log every breakdown with cause → MTBF/MTTR tracking"],
        "owner": "Maintenance Head"},
    "MOULD PROBLEM": {
        "causes": ["No mould PM schedule or history cards; running damaged tools"],
        "counters": ["Mould history card + PM after every N shots",
                     "Spare inserts/pins for chronic moulds; toolroom capacity review"],
        "owner": "Maintenance Head"},
    "NO PLAN": {
        "causes": ["Production plan gaps leave machines idle",
                   "Planning not levelled against confirmed orders (no heijunka)"],
        "counters": ["Weekly levelled production plan (heijunka board) by machine",
                     "Daily plan-vs-actual review in morning meeting; escalate gaps to marketing"],
        "owner": "Plant Head"},
    "RM PREHEATING": {
        "causes": ["Material drying started after shift start instead of before"],
        "counters": ["Pre-shift drying schedule: dryers loaded by prior shift",
                     "Drying time/temperature chart per material at the dryer"],
        "owner": "Production Head"},
    "BARREL HEATING": {
        "causes": ["Heating started at shift start; no staggered pre-heat"],
        "counters": ["Auto-timer barrel pre-heat before shift start",
                     "Restart sequence after power cuts (linked to power-failure card)"],
        "owner": "Production Head"},
    "LUNCH/DINNER TIME": {
        "causes": ["Machines stopped for meal breaks — no relief coverage"],
        "counters": ["Staggered meal relief: one relief operator keeps presses running",
                     "Prioritize bottleneck machines for relief coverage"],
        "owner": "Production Head"},
    "MTC PROBLEM": {
        "causes": ["Mould temperature controller faults — scaling, pump wear"],
        "counters": ["MTC descaling & pump PM schedule; spare MTC unit"],
        "owner": "Maintenance Head"},
    "HRTC B/D": {
        "causes": ["Hot-runner temperature controller failures"],
        "counters": ["HRTC zone-check PM; spare cards/thermocouples stocked"],
        "owner": "Maintenance Head"},
    "COLOUR/MAT CHANGE": {
        "causes": ["Long purge cycles at colour/material change; poor sequencing"],
        "counters": ["Sequence planning light→dark colours; purging-compound standard",
                     "Batch same-colour jobs together in weekly plan"],
        "owner": "Production Head"},
}
GENERIC_DOWNTIME = {
    "causes": ["Recurring stoppage without a standard countermeasure"],
    "counters": ["5-Why on the top 3 occurrences; standardize the fix",
                 "Add to daily management board review"],
    "owner": "Production Head"}

# ---------------------------------------------------------------- rules


def run_engine(con, days=31):
    """Evaluate all rules over the trailing window. Returns list of new action ids."""
    row = con.execute("SELECT MAX(date) m FROM shift_entries").fetchone()
    if not row["m"]:
        return []
    # anchor the window to the data, not the clock, so older imports still analyze
    anchor = min(row["m"], date.today().isoformat())
    since = (date.fromisoformat(anchor) - timedelta(days=days)).isoformat()
    oee_target = float(get_setting(con, "oee_target", "0.85"))
    inc_thr = float(get_setting(con, "incentive_threshold", "0.85"))
    findings = []
    findings += _rule_downtime(con, since)
    findings += _rule_defects(con, since)
    findings += _rule_machine_oee(con, since, oee_target)
    findings += _rule_operators(con, since, inc_thr)
    findings += _rule_parts(con, since)
    created = []
    today = date.today().isoformat()
    for f in findings:
        open_same = con.execute(
            "SELECT 1 FROM actions WHERE key=? AND status='OPEN'", (f["key"],)).fetchone()
        if open_same:
            continue
        cur = con.execute(
            """INSERT INTO actions(key,date,source,category,title,problem,evidence,
                                   root_causes,countermeasures,owner,pdca,status)
               VALUES(?,?,?,?,?,?,?,?,?,?, 'PLAN','OPEN')""",
            (f["key"], today, "ENGINE", f["category"], f["title"], f["problem"],
             f["evidence"], json.dumps(f["causes"]), json.dumps(f["counters"]), f["owner"]))
        created.append(cur.lastrowid)
    con.commit()
    return created


def _pct(x):
    return f"{x * 100:.1f}%"


def _rule_downtime(con, since):
    rows = con.execute(
        """SELECT d.reason, SUM(d.minutes) m FROM entry_downtime d
           JOIN shift_entries e ON e.id=d.entry_id WHERE e.date>=?
           GROUP BY d.reason ORDER BY m DESC""", (since,)).fetchall()
    total = sum(r["m"] for r in rows) or 0
    out = []
    for r in rows:
        share = r["m"] / total if total else 0
        if share >= 0.15 and r["m"] >= 300:  # ≥15% share and ≥5 machine-hours lost
            kb = DOWNTIME_KB.get(r["reason"], GENERIC_DOWNTIME)
            out.append({
                "key": f"downtime:{r['reason']}",
                "category": "DOWNTIME",
                "title": f"{r['reason']} is a top downtime loss ({_pct(share)} of all downtime)",
                "problem": f"{r['reason']} caused {r['m']:.0f} minutes "
                           f"({r['m']/60:.1f} machine-hours) of downtime since {since}.",
                "evidence": f"{r['m']:.0f} min of {total:.0f} min total downtime = {_pct(share)} (Pareto rank {rows.index(r)+1}).",
                "causes": kb["causes"], "counters": kb["counters"], "owner": kb["owner"]})
    return out


def _rule_defects(con, since):
    rows = con.execute(
        """SELECT d.defect, SUM(d.qty) q FROM entry_defects d
           JOIN shift_entries e ON e.id=d.entry_id WHERE e.date>=?
           GROUP BY d.defect ORDER BY q DESC""", (since,)).fetchall()
    total = sum(r["q"] for r in rows) or 0
    out = []
    for r in rows:
        share = r["q"] / total if total else 0
        if share >= 0.10 and r["q"] >= 50:
            kb = DEFECT_KB.get(r["defect"])
            if not kb:
                continue
            out.append({
                "key": f"defect:{r['defect']}",
                "category": "QUALITY",
                "title": f"{r['defect']} is a top rejection cause ({_pct(share)} of all rejects)",
                "problem": f"{r['q']} parts rejected for {r['defect']} since {since} "
                           f"({_pct(share)} of {total} total rejects).",
                "evidence": f"{r['q']} of {total} rejects = {_pct(share)} (Pareto rank {rows.index(r)+1}).",
                "causes": kb["causes"], "counters": kb["counters"], "owner": kb["owner"]})
    return out


def _rule_machine_oee(con, since, target):
    rows = con.execute(
        """SELECT machine, COUNT(*) n, AVG(oee) oee, AVG(availability) a,
                  AVG(performance) p, AVG(quality) q, SUM(total_dt) dt
           FROM shift_entries WHERE date>=? AND oee IS NOT NULL
           GROUP BY machine HAVING n>=3 ORDER BY oee""", (since,)).fetchall()
    out = []
    for r in rows:
        if r["oee"] >= target * 0.9:  # only flag clearly-below-target machines
            continue
        losses = {"availability": 1 - (r["a"] or 1), "performance": 1 - min(1, r["p"] or 1),
                  "quality": 1 - (r["q"] or 1)}
        worst = max(losses, key=losses.get)
        cm = {
            "availability": ["Attack this machine's top downtime reasons (see downtime Pareto filtered to this machine)",
                             "Review changeover and startup time on this press (SMED)"],
            "performance": ["Cycle-time audit: actual vs standard cycle for parts on this machine",
                            "Check for slow cycles: cooling time padding, manual part removal delays, semi-auto running"],
            "quality": ["Review this machine's top defects and apply the defect countermeasure cards",
                        "First-piece approval + hourly patrol inspection on this press"],
        }[worst]
        out.append({
            "key": f"oee:{r['machine']}",
            "category": "OEE",
            "title": f"{r['machine']} OEE {_pct(r['oee'])} vs target {_pct(target)}",
            "problem": f"{r['machine']} averaged {_pct(r['oee'])} OEE over {r['n']} shifts since {since}; "
                       f"biggest loss is {worst}.",
            "evidence": (f"Availability {_pct(r['a'] or 0)}, Performance {_pct(min(1.5, r['p'] or 0))}, "
                         f"Quality {_pct(r['q'] or 0)}; downtime {r['dt']:.0f} min."),
            "causes": [f"Dominant loss category: {worst}"],
            "counters": cm, "owner": "Production Head"})
    return out


def _rule_operators(con, since, thr):
    rows = con.execute(
        """SELECT operator, COUNT(*) n, AVG(eff_pct) eff, SUM(production) p, SUM(rejection) rej
           FROM shift_entries WHERE date>=? AND eff_pct IS NOT NULL AND operator IS NOT NULL
           GROUP BY operator HAVING n>=3 AND eff<? ORDER BY eff LIMIT 5""",
        (since, thr * 0.8)).fetchall()  # flag well below the incentive line
    out = []
    for r in rows:
        out.append({
            "key": f"operator:{r['operator']}",
            "category": "MANPOWER",
            "title": f"Operator {r['operator']} efficiency {_pct(r['eff'])} — needs support",
            "problem": f"{r['operator']} averaged {_pct(r['eff'])} efficiency over {r['n']} shifts "
                       f"(incentive threshold {_pct(thr)}).",
            "evidence": f"{r['p'] or 0} produced, {r['rej'] or 0} rejected over {r['n']} shifts since {since}.",
            "causes": ["Possible skill gap on assigned machines/parts",
                       "May be assigned to problem machines — check machine OEE before judging the operator",
                       "Target may be wrong if cycle time master is outdated"],
            "counters": ["Review with supervisor: machine allocation vs skill matrix",
                         "Pair with a high-efficiency operator for one week (on-the-job training)",
                         "Verify standard cycle time of the parts they run before concluding"],
            "owner": "Production Head"})
    return out


def _rule_parts(con, since):
    plant = con.execute(
        "SELECT SUM(rejection)*1.0/SUM(production) r FROM shift_entries WHERE date>=? AND production>0",
        (since,)).fetchone()["r"] or 0
    rows = con.execute(
        """SELECT part, SUM(production) p, SUM(rejection) rej,
                  SUM(rejection)*1.0/SUM(production) r
           FROM shift_entries WHERE date>=? AND production>0
           GROUP BY part HAVING p>=200 AND rej>=30 AND r > ? ORDER BY r DESC LIMIT 5""",
        (since, max(plant * 2, 0.05))).fetchall()
    out = []
    for r in rows:
        top = con.execute(
            """SELECT d.defect, SUM(d.qty) q FROM entry_defects d
               JOIN shift_entries e ON e.id=d.entry_id
               WHERE e.date>=? AND e.part=? GROUP BY d.defect ORDER BY q DESC LIMIT 1""",
            (since, r["part"])).fetchone()
        topname = top["defect"] if top else "—"
        kb = DEFECT_KB.get(topname, {})
        out.append({
            "key": f"part:{r['part']}",
            "category": "QUALITY",
            "title": f"Part '{r['part']}' rejection {_pct(r['r'])} vs plant {_pct(plant)}",
            "problem": f"'{r['part']}' rejected {r['rej']} of {r['p']} since {since} "
                       f"({_pct(r['r'])}); top defect: {topname}.",
            "evidence": f"Plant average rejection {_pct(plant)}; this part runs {_pct(r['r'])}.",
            "causes": kb.get("causes", ["Part-specific process instability"]),
            "counters": (["Set up a focused improvement (QC story) on this part"]
                         + kb.get("counters", [])),
            "owner": kb.get("owner", "Quality Head")})
    return out
