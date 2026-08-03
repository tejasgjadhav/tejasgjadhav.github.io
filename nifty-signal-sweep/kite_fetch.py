"""
Pull NIFTY 50 5-minute history from Kite and cache it.

Kite caps a single 5-minute historical request at ~100 days, so this walks the
range in 90-day chunks and concatenates. Cached to CSV so the harness can be
re-run without re-hitting the API (and without needing a live token).

  python kite_fetch.py [start_year]      default 2019
"""
import os, sys, time, pathlib, datetime as dt
import pandas as pd
from kiteconnect import KiteConnect

HERE = pathlib.Path(__file__).parent
OUT = HERE/'nifty_5m.csv'
START_YEAR = int(sys.argv[1]) if len(sys.argv) > 1 else 2019

kv = dict(l.split('=', 1) for l in (HERE/'.env').read_text().splitlines() if '=' in l)
kite = KiteConnect(api_key=kv['KITE_API_KEY'])
kite.set_access_token(kv['KITE_ACCESS_TOKEN'])

ins = kite.instruments("NSE")
tok = next(i['instrument_token'] for i in ins if i['tradingsymbol'] == 'NIFTY 50')
print(f"NIFTY 50 instrument token: {tok}")

start = dt.date(START_YEAR, 1, 1)
end = dt.date.today()
chunks, cur = [], start
while cur < end:
    nxt = min(cur + dt.timedelta(days=90), end)
    for attempt in range(3):
        try:
            c = kite.historical_data(tok, cur, nxt, "5minute")
            if c:
                chunks.append(pd.DataFrame(c))
            print(f"  {cur} -> {nxt}: {len(c) if c else 0} bars")
            break
        except Exception as e:
            if attempt == 2:
                print(f"  {cur} -> {nxt}: FAILED {e}")
            else:
                time.sleep(1.5)
    cur = nxt + dt.timedelta(days=1)
    time.sleep(0.4)          # Kite allows ~3 req/s; stay well under

if not chunks:
    sys.exit("no data returned")

df = pd.concat(chunks, ignore_index=True).drop_duplicates(subset='date').sort_values('date')
df.to_csv(OUT, index=False)
print(f"\n{len(df)} bars  {df['date'].iloc[0]} -> {df['date'].iloc[-1]}")
print(f"volume nonzero: {(df['volume'] > 0).sum()} of {len(df)}")
print(f"cached -> {OUT}")
