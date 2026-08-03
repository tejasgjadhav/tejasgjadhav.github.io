"""
Kite access-token helper.

Kite access tokens expire daily, and minting one requires a Zerodha login with
2FA. That login is yours to do — this script only brackets it:

  step 1:  python kite_auth.py url
           prints the login URL. Open it, log in, and Zerodha redirects you to
           your registered redirect URL carrying ?request_token=XXXX

  step 2:  python kite_auth.py exchange <request_token>
           swaps that one-time request_token for an access_token and stores it
           in this directory's .env (chmod 600). Reads API key/secret from
           institutional-trader/.env at runtime; never copies them anywhere.

The request_token is single-use and dies in minutes, so run step 2 promptly.
"""
import os, sys, stat, pathlib

HERE = pathlib.Path(__file__).parent
TRADER_ENV = pathlib.Path.home()/'files/institutional-trader/.env'
OUT_ENV = HERE/'.env'


def load_creds():
    if not TRADER_ENV.exists():
        sys.exit(f"cannot find {TRADER_ENV}")
    kv = {}
    for line in TRADER_ENV.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        kv[k.strip()] = v.strip().strip('"').strip("'")
    key, sec = kv.get('KITE_API_KEY'), kv.get('KITE_API_SECRET')
    if not key or not sec:
        sys.exit("KITE_API_KEY / KITE_API_SECRET not found in institutional-trader/.env")
    return key, sec


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    key, sec = load_creds()
    from kiteconnect import KiteConnect
    kite = KiteConnect(api_key=key)

    if cmd == 'url':
        print("\nOpen this, log in, then copy the request_token from the redirect URL:\n")
        print("  " + kite.login_url())
        print("\nThen run:  python kite_auth.py exchange <request_token>\n")

    elif cmd == 'exchange':
        if len(sys.argv) < 3:
            sys.exit("usage: python kite_auth.py exchange <request_token>")
        data = kite.generate_session(sys.argv[2], api_secret=sec)
        tok = data['access_token']
        OUT_ENV.write_text(f"KITE_API_KEY={key}\nKITE_ACCESS_TOKEN={tok}\n")
        os.chmod(OUT_ENV, stat.S_IRUSR | stat.S_IWUSR)   # 600
        print(f"access token stored in {OUT_ENV} (mode 600)")
        print(f"user: {data.get('user_name')}  valid until ~6am tomorrow")

    elif cmd == 'check':
        if not OUT_ENV.exists():
            sys.exit("no .env here yet — run 'url' then 'exchange' first")
        kv = dict(l.split('=', 1) for l in OUT_ENV.read_text().splitlines() if '=' in l)
        kite.set_access_token(kv['KITE_ACCESS_TOKEN'])
        try:
            p = kite.profile()
            print(f"token OK — {p.get('user_name')}")
        except Exception as e:
            sys.exit(f"token rejected: {e}")
        # Historical data is a separate paid Kite subscription; check it explicitly
        # so a missing add-on is not mistaken for a broken token.
        try:
            import datetime as dt
            ins = kite.instruments("NSE")
            tok_nifty = next(i['instrument_token'] for i in ins if i['tradingsymbol'] == 'NIFTY 50')
            to = dt.date.today(); frm = to - dt.timedelta(days=5)
            c = kite.historical_data(tok_nifty, frm, to, "5minute")
            print(f"historical API OK — {len(c)} 5-min bars for the last 5 days")
        except Exception as e:
            print(f"historical API NOT available: {e}")
            print("  (Kite historical data is a paid add-on, separate from the trading API)")
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
