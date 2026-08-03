"""All derived-number formulas, transcribed 1:1 from the Excel MIS workbook
(DATA ENTRY sheet). Single source of truth — the entry form, the importer and
every dashboard use these functions, so the app always agrees with itself.

Excel column mapping (row r):
  BH TOTAL DT        = SUM(downtime AL:BG)
  I  AVAIL TIME      = MAX(0, planned − TOTAL DT)
  J  TGT/HR          = ROUND(3600/cycle × running_cavity)
  BM EFFECTIVE TIME  = MAX(0, planned − POWER FAILURE)      (power NA excluded from OEE)
  K  TGT QTY         = ROUND(TGT/HR × EFFECTIVE TIME / 60)
  N  REJECTION       = SUM(defects Q:AK)
  M  OK QTY          = PRODUCTION − REJECTION
  O  EFF %           = PRODUCTION / TGT QTY
  P  REJ %           = REJECTION / PRODUCTION
  BI OK WT kg        = ROUND(OK × part_wt/1000, 2)
  BJ REJ WT kg       = ROUND(REJ × part_wt/1000, 2)
  BK RUNNER kg       = ROUND(PRODUCTION/MAX(1,cav) × runner_wt/1000, 2)
  BL TOTAL RM kg     = ROUND(BI+BJ+BK, 2)
  BN AVAILABILITY    = MIN(1, AVAIL TIME / EFFECTIVE TIME)
  BO PERFORMANCE     = MIN(1.5, PRODUCTION / (TGT/HR × AVAILABILITY × EFFECTIVE TIME/60))
  BP QUALITY         = OK / PRODUCTION
  BQ OEE             = BN × BO × BP
"""
import math


def xl_round(x, digits=0):
    """Excel ROUND: half away from zero (Python round() is banker's)."""
    if x is None:
        return None
    factor = 10 ** digits
    return math.floor(abs(x) * factor + 0.5) / factor * (1 if x >= 0 else -1)


def compute_entry(part_row, planned_min, production, defects, downtime, shift_minutes=720.0):
    """Compute all derived fields for one shift entry.

    part_row: dict/Row with cycle_time_s, running_cavity, part_wt_g, runner_wt_g
    planned_min: per-row override or None (falls back to shift_minutes)
    defects: {defect_name: qty}, downtime: {reason: minutes}
    Returns dict of computed columns.
    """
    planned = planned_min if planned_min not in (None, "", 0) else shift_minutes
    cycle = part_row["cycle_time_s"] or 0
    cav = part_row["running_cavity"] or 1
    part_wt = part_row["part_wt_g"] or 0
    runner_wt = part_row["runner_wt_g"] or 0

    total_dt = sum(v for v in downtime.values() if v) if downtime else 0.0
    avail_time = max(0.0, planned - total_dt)
    power_fail = downtime.get("POWER FAILURE", 0) or 0
    eff_time = max(0.0, planned - power_fail)

    tgt_hr = xl_round(3600.0 / cycle * max(1, cav)) if cycle > 0 else None
    tgt_qty = xl_round(tgt_hr * eff_time / 60.0) if tgt_hr is not None else None

    rejection = int(sum(v for v in defects.values() if v)) if defects else 0
    production = int(production) if production is not None else None
    ok_qty = production - rejection if production is not None else None

    eff_pct = production / tgt_qty if (production is not None and tgt_qty) else None
    rej_pct = rejection / production if (production or 0) > 0 else None

    ok_wt = xl_round((ok_qty or 0) * part_wt / 1000.0, 2) if ok_qty is not None else None
    rej_wt = xl_round(rejection * part_wt / 1000.0, 2) if production is not None else None
    runner_kg = (xl_round((production or 0) / max(1, cav) * runner_wt / 1000.0, 2)
                 if production is not None else None)
    total_rm = (xl_round((ok_wt or 0) + (rej_wt or 0) + (runner_kg or 0), 2)
                if production is not None else None)

    availability = min(1.0, avail_time / eff_time) if eff_time > 0 else None
    performance = None
    if (tgt_hr and production is not None and availability is not None
            and availability * eff_time > 0):
        performance = min(1.5, production / (tgt_hr * availability * eff_time / 60.0))
    quality = ok_qty / production if (production or 0) > 0 else None
    oee = (availability * performance * quality
           if None not in (availability, performance, quality) else None)

    return {
        "total_dt": total_dt, "avail_time": avail_time, "eff_time": eff_time,
        "tgt_hr": tgt_hr, "tgt_qty": tgt_qty,
        "ok_qty": ok_qty, "rejection": rejection,
        "eff_pct": eff_pct, "rej_pct": rej_pct,
        "ok_wt_kg": ok_wt, "rej_wt_kg": rej_wt,
        "runner_kg": runner_kg, "total_rm_kg": total_rm,
        "availability": availability, "performance": performance,
        "quality": quality, "oee": oee,
    }


def rework_eff(target_qty, ok_qty):
    """REWORK EFFICIENCY sheet: EFF = ACTUAL OK / TARGET."""
    return ok_qty / target_qty if target_qty else None
