"""SQLite schema, connection and seeding for GlobalAAR TPS Ops."""
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "globalaar.db"

# Order matches the Excel DATA ENTRY columns Q..AK
DEFECT_TYPES = [
    "RESTART UP REJ", "SETTING REJ", "SHORT SHOT", "SINK MARK", "SILVER MARK",
    "DUST", "BLACK SPOT", "BURN MARK", "WELD LINE", "DENT", "SCRATCH & CRACK",
    "FLOW MARK", "GAS MARK", "DAMAGE", "WARPAGE", "FLASH", "OIL MARK",
    "CATCHING", "INSERT FLASH", "INSERT OUTSIDE", "OTHER",
]

# Order matches the Excel DATA ENTRY columns AL..BG
DOWNTIME_REASONS = [
    "NO MANPOWER", "POWER FAILURE", "COLOUR/MAT CHANGE", "MACHINE PROBLEM",
    "MOULD PROBLEM", "MTC PROBLEM", "HRTC B/D", "RM PREHEATING",
    "LUNCH/DINNER TIME", "MOULD CHANGE", "MOULD CLEANING", "BARREL HEATING",
    "MATERIAL PROBLEM", "NO PLAN", "RUNNER STICKING", "NOZZLE BLOCK", "5S",
    "NO SKILLED OPERATOR", "OPERATOR LATE", "PACKAGING MATERIAL SHORT",
    "MACHINE PM", "OTHERS",
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY,
    customer TEXT, project TEXT,
    name TEXT UNIQUE NOT NULL,
    part_no TEXT,
    cycle_time_s REAL, total_cavity INTEGER, running_cavity INTEGER,
    shot_wt_g REAL, part_wt_g REAL, runner_wt_g REAL,
    material_grade TEXT,
    active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS machines (
    id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS operators (
    id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS supervisors (
    id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS defect_types (
    id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, sort INTEGER, active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS downtime_reasons (
    id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, sort INTEGER, active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS shift_entries (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,               -- YYYY-MM-DD
    machine TEXT NOT NULL,
    shift TEXT NOT NULL,              -- A / B
    supervisor TEXT, operator TEXT,
    part TEXT NOT NULL,
    material TEXT, cycle_time_s REAL,
    planned_min REAL,                 -- NULL = settings shift_minutes
    production INTEGER,
    remarks TEXT,
    -- computed snapshot (calc.py)
    total_dt REAL, avail_time REAL, eff_time REAL,
    tgt_hr REAL, tgt_qty REAL,
    ok_qty INTEGER, rejection INTEGER,
    eff_pct REAL, rej_pct REAL,
    ok_wt_kg REAL, rej_wt_kg REAL, runner_kg REAL, total_rm_kg REAL,
    availability REAL, performance REAL, quality REAL, oee REAL
);
CREATE TABLE IF NOT EXISTS entry_defects (
    entry_id INTEGER NOT NULL REFERENCES shift_entries(id) ON DELETE CASCADE,
    defect TEXT NOT NULL, qty INTEGER NOT NULL,
    PRIMARY KEY (entry_id, defect)
);
CREATE TABLE IF NOT EXISTS entry_downtime (
    entry_id INTEGER NOT NULL REFERENCES shift_entries(id) ON DELETE CASCADE,
    reason TEXT NOT NULL, minutes REAL NOT NULL,
    PRIMARY KEY (entry_id, reason)
);
CREATE TABLE IF NOT EXISTS rework_entries (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL, operator TEXT NOT NULL, shift TEXT,
    work_type TEXT, description TEXT,
    target_qty INTEGER, ok_qty INTEGER, rej_qty INTEGER,
    remarks TEXT
);
CREATE TABLE IF NOT EXISTS ncr (
    id INTEGER PRIMARY KEY,
    ncr_no TEXT, date TEXT NOT NULL,
    source TEXT NOT NULL,             -- CUSTOMER COMPLAINT / IN-PROCESS / INCOMING / FINAL INSPECTION
    customer TEXT, part TEXT, defect TEXT,
    qty INTEGER, description TEXT,
    disposition TEXT,                 -- REWORK / SCRAP / USE-AS-IS / RETURN
    raised_by TEXT,
    status TEXT DEFAULT 'OPEN',       -- OPEN / CLOSED
    closed_date TEXT
);
CREATE TABLE IF NOT EXISTS capa (
    id INTEGER PRIMARY KEY,
    ncr_id INTEGER REFERENCES ncr(id),
    capa_no TEXT, date TEXT,
    title TEXT,
    d1_team TEXT, d2_problem TEXT, d3_containment TEXT, d4_root_cause TEXT,
    d5_corrective TEXT, d6_implemented TEXT, d7_prevent TEXT, d8_closure TEXT,
    owner TEXT, due_date TEXT,
    status TEXT DEFAULT 'OPEN'
);
CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY,
    key TEXT,                         -- engine dedupe key; NULL for manual actions
    date TEXT NOT NULL,
    source TEXT DEFAULT 'MANUAL',     -- ENGINE / MANUAL
    category TEXT,                    -- DOWNTIME / QUALITY / OEE / MANPOWER / PLANNING
    title TEXT NOT NULL,
    problem TEXT, evidence TEXT,
    root_causes TEXT,                 -- JSON list
    countermeasures TEXT,             -- JSON list
    owner TEXT, due_date TEXT,
    pdca TEXT DEFAULT 'PLAN',         -- PLAN / DO / CHECK / ACT
    status TEXT DEFAULT 'OPEN',       -- OPEN / CLOSED
    closed_date TEXT, result TEXT
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY, value TEXT
);
"""

DEFAULT_SETTINGS = {
    "shift_minutes": "720",
    "incentive_threshold": "0.85",
    "oee_target": "0.85",
    "admin_pin": "2026",
    "company_name": "GLOBAL AAR TECHNOPLAST PVT LTD",
    "plant": "Ranjangaon MIDC, Pune",
}


def get_db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con


def init_db() -> None:
    con = get_db()
    con.executescript(SCHEMA)
    for k, v in DEFAULT_SETTINGS.items():
        con.execute("INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)", (k, v))
    for i, name in enumerate(DEFECT_TYPES):
        con.execute("INSERT OR IGNORE INTO defect_types(name,sort) VALUES(?,?)", (name, i))
    for i, name in enumerate(DOWNTIME_REASONS):
        con.execute("INSERT OR IGNORE INTO downtime_reasons(name,sort) VALUES(?,?)", (name, i))
    seed_file = BASE_DIR / "seed_masters.json"
    if seed_file.exists():
        seed = json.loads(seed_file.read_text())
        for p in seed.get("parts", []):
            # [sno, customer, project, name, part_no, cycle, tot_cav, run_cav, shot, part, runner, material]
            con.execute(
                """INSERT OR IGNORE INTO parts
                   (customer,project,name,part_no,cycle_time_s,total_cavity,running_cavity,
                    shot_wt_g,part_wt_g,runner_wt_g,material_grade)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (p[1], p[2], p[3], p[4],
                 _num(p[5]), _num(p[6]), _num(p[7]), _num(p[8]), _num(p[9]), _num(p[10]), p[11]),
            )
        for name in seed.get("mcs", []):
            con.execute("INSERT OR IGNORE INTO machines(name) VALUES(?)", (name,))
        for name in seed.get("sups", []):
            con.execute("INSERT OR IGNORE INTO supervisors(name) VALUES(?)", (name,))
        for name in seed.get("ops", []):
            if name and not name.startswith("↑"):  # skip the "add here" hint row
                con.execute("INSERT OR IGNORE INTO operators(name) VALUES(?)", (name,))
    con.commit()
    con.close()


def _num(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def get_setting(con, key, default=None):
    row = con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default
