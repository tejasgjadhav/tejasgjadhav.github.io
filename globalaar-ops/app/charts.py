"""Server-side SVG chart helpers — no JS dependency, prints cleanly, works offline."""
from html import escape

INK = "var(--ink)"
MUTED = "var(--muted)"
GRID = "var(--grid)"


def _fmt(v):
    if v >= 10000:
        return f"{v:,.0f}"
    if v >= 100:
        return f"{v:.0f}"
    return f"{v:g}"


def hbar(items, width=680, bar_h=26, gap=8, color="var(--c1)", pct_of=None, label_w=230):
    """Horizontal bar chart. items = [(label, value), ...]"""
    if not items:
        return '<p class="empty">No data</p>'
    vmax = max(v for _, v in items) or 1
    total = pct_of if pct_of is not None else sum(v for _, v in items) or 1
    h = len(items) * (bar_h + gap)
    plot_w = width - label_w - 90
    rows = []
    for i, (label, v) in enumerate(items):
        y = i * (bar_h + gap)
        w = max(2, v / vmax * plot_w)
        share = v / total if total else 0
        rows.append(
            f'<text x="{label_w-8}" y="{y+bar_h*0.7}" text-anchor="end" class="clabel">{escape(str(label)[:34])}</text>'
            f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="3" fill="{color}"/>'
            f'<text x="{label_w+w+6}" y="{y+bar_h*0.7}" class="cval">{_fmt(v)} ({share*100:.0f}%)</text>')
    return (f'<svg viewBox="0 0 {width} {h}" class="chart" role="img">' + "".join(rows) + "</svg>")


def pareto(items, width=680, height=260, color="var(--c1)"):
    """Vertical Pareto: bars + cumulative % line. items sorted desc."""
    items = [(l, v) for l, v in items if v > 0]
    if not items:
        return '<p class="empty">No data</p>'
    total = sum(v for _, v in items) or 1
    vmax = max(v for _, v in items) or 1
    n = len(items)
    pad_l, pad_r, pad_t, pad_b = 46, 40, 14, 78
    pw, ph = width - pad_l - pad_r, height - pad_t - pad_b
    bw = pw / n * 0.66
    parts, cum, pts = [], 0.0, []
    for i, (label, v) in enumerate(items):
        x = pad_l + pw / n * (i + 0.5)
        bh = v / vmax * ph
        cum += v
        cy = pad_t + ph - (cum / total) * ph
        pts.append(f"{x:.1f},{cy:.1f}")
        parts.append(
            f'<rect x="{x-bw/2:.1f}" y="{pad_t+ph-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="2" fill="{color}"/>'
            f'<text x="{x:.1f}" y="{pad_t+ph-bh-4:.1f}" text-anchor="middle" class="cval">{_fmt(v)}</text>'
            f'<text transform="translate({x:.1f},{pad_t+ph+10}) rotate(38)" class="clabel xs">{escape(str(label)[:18])}</text>')
    line = (f'<polyline points="{" ".join(pts)}" fill="none" stroke="var(--c2)" stroke-width="2"/>'
            + "".join(f'<circle cx="{p.split(",")[0]}" cy="{p.split(",")[1]}" r="3" fill="var(--c2)"/>'
                      for p in pts))
    axis = (f'<line x1="{pad_l}" y1="{pad_t+ph}" x2="{pad_l+pw}" y2="{pad_t+ph}" stroke="{GRID}"/>'
            f'<text x="{width-4}" y="{pad_t+8}" text-anchor="end" class="clabel xs">cumulative %</text>')
    return f'<svg viewBox="0 0 {width} {height}" class="chart" role="img">{axis}{"".join(parts)}{line}</svg>'


def line_trend(points, width=680, height=200, color="var(--c1)", fmt_pct=False):
    """points = [(label, value), ...] in order."""
    points = [(l, v) for l, v in points if v is not None]
    if len(points) < 2:
        return '<p class="empty">Not enough data for a trend</p>'
    vals = [v for _, v in points]
    vmin, vmax = min(vals), max(vals)
    if vmax == vmin:
        vmax = vmin + 1
    pad_l, pad_r, pad_t, pad_b = 52, 14, 12, 34
    pw, ph = width - pad_l - pad_r, height - pad_t - pad_b
    n = len(points)
    pts = []
    for i, (_, v) in enumerate(points):
        x = pad_l + pw * i / (n - 1)
        y = pad_t + ph - (v - vmin) / (vmax - vmin) * ph
        pts.append((x, y, v))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in pts)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{color}"/>' for x, y, _ in pts)
    lab = lambda v: f"{v*100:.0f}%" if fmt_pct else _fmt(v)
    ylab = (f'<text x="{pad_l-6}" y="{pad_t+8}" text-anchor="end" class="clabel xs">{lab(vmax)}</text>'
            f'<text x="{pad_l-6}" y="{pad_t+ph}" text-anchor="end" class="clabel xs">{lab(vmin)}</text>')
    step = max(1, n // 8)
    xlab = "".join(
        f'<text x="{pad_l + pw*i/(n-1):.1f}" y="{height-8}" text-anchor="middle" class="clabel xs">{escape(str(points[i][0])[-5:])}</text>'
        for i in range(0, n, step))
    grid = "".join(f'<line x1="{pad_l}" y1="{pad_t+ph*f:.1f}" x2="{pad_l+pw}" y2="{pad_t+ph*f:.1f}" stroke="{GRID}" stroke-dasharray="3 3"/>'
                   for f in (0, 0.5, 1))
    return (f'<svg viewBox="0 0 {width} {height}" class="chart" role="img">{grid}{ylab}{xlab}'
            f'<polyline points="{poly}" fill="none" stroke="{color}" stroke-width="2.5"/>{dots}</svg>')
