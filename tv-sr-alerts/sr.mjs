/**
 * Live support/resistance on TradingView.
 *
 * Reads OHLCV from whatever symbol the TradingView chart is on, derives S/R
 * zones from swing pivots, draws them, and (in --watch mode) fires a macOS
 * notification when price approaches or breaks one.
 *
 * Data comes from the chart itself, which is what was asked for. Note the
 * chart exposes ~300 bars, so zones are derived from that window only.
 *
 *   node sr.mjs                     compute + draw on the current chart
 *   node sr.mjs --symbol NSE:NIFTY  switch symbol first
 *   node sr.mjs --dry-run           print zones, draw nothing
 *   node sr.mjs --watch             draw, then poll and alert
 *   node sr.mjs --watch --interval 30
 */
import { spawn } from 'node:child_process';
import { execFile } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';

const MCP_CWD = path.join(os.homedir(), 'tradingview-mcp-jackson');
const argv = process.argv.slice(2);
const flag = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 && argv[i+1] && !argv[i+1].startsWith('--') ? argv[i+1] : d; };
const has = n => argv.includes(`--${n}`);

const SYMBOL     = flag('symbol', null);
const PIVOT_K    = Number(flag('pivot', 3));      // bars each side for a swing pivot
const CLUSTER_PCT= Number(flag('cluster', 0.25)); // merge pivots within this % into one zone
const MIN_TOUCH  = Number(flag('touches', 2));    // pivots needed to call it a zone
const TOP_N      = Number(flag('top', 6));
const MAX_DIST   = Number(flag('max-dist', 5));   // ignore zones further than this % from spot
const NEAR_PCT   = Number(flag('near', 0.15));    // alert when price within this % of a zone
const INTERVAL   = Number(flag('interval', 60));  // seconds between polls in --watch
const UNTIL      = flag('until', null);           // "15:30" — exit at this local time (for launchd)
const DRY        = has('dry-run');
const WATCH      = has('watch');

// Under launchd there is no terminal to notice a hang, so fail loudly and early
// if TradingView is not running with the CDP port open.
async function preflight() {
  try {
    const r = await fetch('http://127.0.0.1:9222/json/version', { signal: AbortSignal.timeout(4000) });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
  } catch (e) {
    console.error(`[${new Date().toISOString()}] TradingView CDP not reachable on 127.0.0.1:9222 (${e.message}).`);
    console.error('Launch it with: ~/tradingview-mcp-jackson/scripts/launch_tv_debug_mac.sh');
    process.exit(1);
  }
}
await preflight();

// ---- MCP plumbing -----------------------------------------------------------
const proc = spawn('node', ['src/server.js'], { cwd: MCP_CWD, stdio: ['pipe','pipe','pipe'] });
let id = 10, buf = '';
const pend = new Map();
proc.stdout.on('data', d => {
  buf += d; let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const l = buf.slice(0, i); buf = buf.slice(i + 1);
    if (!l.trim()) continue;
    let m; try { m = JSON.parse(l); } catch { continue; }
    if (pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
  }
});
const rpc = (method, params) => new Promise(r => { const i = ++id; pend.set(i, r); proc.stdin.write(JSON.stringify({jsonrpc:'2.0',id:i,method,params})+'\n'); });
const call = async (name, args = {}) => {
  const r = await rpc('tools/call', { name, arguments: args });
  const t = r.result?.content?.[0]?.text;
  try { return JSON.parse(t); } catch { return { success: false, raw: t }; }
};

const notify = (title, msg) => execFile('osascript', ['-e',
  `display notification ${JSON.stringify(msg)} with title ${JSON.stringify(title)} sound name "Submarine"`]);

// ---- S/R derivation ---------------------------------------------------------
/** A swing pivot: a bar whose high (or low) is the most extreme within +/- k bars. */
function pivots(bars, k) {
  const hi = [], lo = [];
  for (let i = k; i < bars.length - k; i++) {
    let isHi = true, isLo = true;
    for (let j = i - k; j <= i + k; j++) {
      if (j === i) continue;
      if (bars[j].high >= bars[i].high) isHi = false;
      if (bars[j].low  <= bars[i].low)  isLo = false;
    }
    if (isHi) hi.push({ price: bars[i].high, idx: i });
    if (isLo) lo.push({ price: bars[i].low,  idx: i });
  }
  return { hi, lo };
}

/** Merge pivots that sit within CLUSTER_PCT of each other into a single zone. */
function cluster(points, lastIdx) {
  const sorted = [...points].sort((a, b) => a.price - b.price);
  const zones = [];
  for (const p of sorted) {
    const z = zones[zones.length - 1];
    if (z && Math.abs(p.price - z.mean) / z.mean * 100 <= CLUSTER_PCT) {
      z.members.push(p);
      z.mean = z.members.reduce((s, m) => s + m.price, 0) / z.members.length;
      z.lo = Math.min(z.lo, p.price); z.hi = Math.max(z.hi, p.price);
      z.lastIdx = Math.max(z.lastIdx, p.idx);
    } else {
      zones.push({ members: [p], mean: p.price, lo: p.price, hi: p.price, lastIdx: p.idx });
    }
  }
  return zones
    .filter(z => z.members.length >= MIN_TOUCH)
    // Rank by touch count, then by how recent the most recent touch was.
    .map(z => ({ ...z, touches: z.members.length, recency: z.lastIdx / lastIdx }))
    .sort((a, b) => (b.touches - a.touches) || (b.recency - a.recency));
}

// ---- main -------------------------------------------------------------------
(async () => {
  await rpc('initialize', { protocolVersion:'2024-11-05', capabilities:{}, clientInfo:{name:'sr',version:'1'} });
  proc.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})+'\n');

  if (SYMBOL) {
    const s = await call('chart_set_symbol', { symbol: SYMBOL });
    if (!s.success) { console.log(`FAILED to load ${SYMBOL}: ${s.error}`); proc.kill(); process.exit(1); }
    await new Promise(r => setTimeout(r, 3500));
  }

  const state = await call('chart_get_state');
  const data  = await call('data_get_ohlcv', { count: 300 });
  if (!data.success || !data.bars?.length) { console.log('no bars'); proc.kill(); process.exit(1); }
  const bars = data.bars;
  const last = bars[bars.length - 1];
  const spot = last.close;

  const { hi, lo } = pivots(bars, PIVOT_K);
  // Zones far from spot can't trigger anything today, so drop them BEFORE taking
  // the top N — otherwise a heavily-touched zone 7% away crowds out a live one.
  const inRange = z => Math.abs(z.mean / spot - 1) * 100 <= MAX_DIST;
  const byPrice = (a, b) => b.mean - a.mean;
  const resistance = cluster(hi, bars.length).filter(z => z.mean > spot).filter(inRange).slice(0, TOP_N).sort(byPrice);
  const support    = cluster(lo, bars.length).filter(z => z.mean < spot).filter(inRange).slice(0, TOP_N).sort(byPrice);

  console.log(`\n${state.symbol} · ${state.resolution} · ${bars.length} bars · spot ${spot}`);
  console.log(`pivots: ${hi.length} highs, ${lo.length} lows  (k=${PIVOT_K}, cluster ${CLUSTER_PCT}%, min touches ${MIN_TOUCH})\n`);
  const show = (label, zs) => {
    console.log(`  ${label}`);
    for (const z of zs) console.log(`    ${z.mean.toFixed(2).padStart(10)}  touches ${z.touches}  band ${z.lo.toFixed(2)}-${z.hi.toFixed(2)}  ${((z.mean/spot-1)*100).toFixed(2)}%`);
    if (!zs.length) console.log('    (none)');
  };
  show('RESISTANCE (above spot)', resistance);
  show('SUPPORT (below spot)', support);

  if (DRY) { proc.kill(); process.exit(0); }

  // Without this a scheduled daily run stacks a fresh set of lines on top of
  // yesterday's until the chart is unreadable.
  if (has('clear')) await call('draw_clear');

  for (const [zs, color] of [[resistance, '#e53935'], [support, '#43a047']]) {
    for (const z of zs) {
      await call('draw_shape', {
        shape: 'horizontal_line',
        point: { time: last.time, price: Number(z.mean.toFixed(2)) },
        overrides: JSON.stringify({
          linecolor: color, linewidth: Math.min(3, z.touches), linestyle: 0,
          showLabel: true, text: `${z.touches}x ${z.mean.toFixed(2)}`,
          textcolor: color, horzLabelsAlign: 'right', showPrice: true,
        }),
      });
    }
  }
  console.log(`\ndrew ${resistance.length + support.length} zones`);

  if (!WATCH) { proc.kill(); process.exit(0); }

  const zones = [...resistance.map(z => ({...z, kind:'RESISTANCE'})), ...support.map(z => ({...z, kind:'SUPPORT'}))];
  const fired = new Map();   // zone mean -> last state, so one alert per transition not per poll
  console.log(`\nwatching every ${INTERVAL}s — Ctrl-C to stop\n`);

  let stopAt = null;
  if (UNTIL) {
    const [hh, mm] = UNTIL.split(':').map(Number);
    stopAt = new Date(); stopAt.setHours(hh, mm, 0, 0);
    if (stopAt <= new Date()) stopAt.setDate(stopAt.getDate() + 1);
    console.log(`will exit at ${stopAt.toLocaleTimeString('en-IN')}`);
  }

  const tick = async () => {
    if (stopAt && new Date() >= stopAt) {
      console.log(`reached ${UNTIL} — exiting`);
      proc.kill(); process.exit(0);
    }
    const q = await call('quote_get');
    if (!q.success) { console.log(`  quote failed: ${q.error || q.raw}`); return; }
    const p = q.last;
    for (const z of zones) {
      const distPct = (p - z.mean) / z.mean * 100;
      const side = distPct > 0 ? 'above' : 'below';
      const near = Math.abs(distPct) <= NEAR_PCT;
      const key = z.mean.toFixed(2);
      const prev = fired.get(key);
      const now = near ? `near:${side}` : side;
      if (prev && prev !== now) {
        const crossed = prev.replace('near:','') !== side;
        const msg = crossed
          ? `${q.symbol} ${p} BROKE ${z.kind} ${key} (${z.touches} touches)`
          : `${q.symbol} ${p} approaching ${z.kind} ${key} (${distPct.toFixed(2)}%)`;
        if (crossed || near) { console.log(`  ALERT  ${msg}`); notify('TradingView S/R', msg); }
      }
      fired.set(key, now);
    }
    console.log(`  ${new Date().toLocaleTimeString('en-IN')}  ${q.symbol} ${p}`);
  };
  await tick();
  setInterval(tick, INTERVAL * 1000);
})();
