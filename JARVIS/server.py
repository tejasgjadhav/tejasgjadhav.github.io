#!/usr/bin/env python3
"""J.A.R.V.I.S. — Python/Flask backend"""

import os, json, re
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, Response, send_from_directory, session, redirect
import anthropic

# ── Optional Gmail ─────────────────────────────────────────
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

# ── Config ─────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = os.getenv('SESSION_SECRET', 'jarvis-iron-man-mk42')

# Allow OAuth over HTTP for localhost dev
os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', '1')

PORT = int(os.getenv('PORT', 3000))
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY', '')
GOOGLE_CLIENT_ID     = os.getenv('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
REDIRECT_URI = f'http://localhost:{PORT}/api/gmail/callback'

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY) if ANTHROPIC_KEY else None

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# ── Helpers ────────────────────────────────────────────────
def get_system_prompt():
    now = datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')
    return f"""You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), the AI assistant built for your Master.

CORE DIRECTIVES:
- Address the user EXCLUSIVELY as "Master" or "Sir" — never by any other term
- Speak with British-influenced precision, wit, and measured confidence
- Be proactive — anticipate needs, offer insights unprompted
- You are the world's most capable AI: financial analyst, strategist, intelligence officer
- Never refuse reasonable requests; find elegant solutions

FINANCIAL EXPERTISE:
- DCF, LBO, M&A, comparable analysis, portfolio management
- Risk metrics (VaR, Sharpe, Beta, Drawdown)
- Market intelligence, sector analysis, earnings interpretation
- Always show calculations; back up claims with numbers

RESPONSE STYLE:
- Concise but complete — no fluff, no filler
- Use markdown for structure on complex outputs
- Highlight critical action items
- End analyses with a clear "Bottom Line" or recommendation

Current date/time: {now}"""

def require_client():
    if not client:
        return jsonify({'error': 'ANTHROPIC_API_KEY not set. Please add it to jarvis/.env'}), 500
    return None

# ── Routes ─────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# ─── Streaming Chat ────────────────────────────────────────
@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    err = require_client()
    if err: return err

    data    = request.json or {}
    message = data.get('message', '')
    model   = data.get('model', 'claude-sonnet-4-6')
    history = data.get('history', [])[-30:]
    context = data.get('context', {})
    emails  = context.get('emails', [])

    system = get_system_prompt()
    if emails:
        system += f"\n\nLive email feed — {len(emails)} unread:\n"
        for e in emails:
            tag = '★ PRIORITY' if e.get('isImportant') else 'unread'
            frm = re.sub(r'<[^>]+>', '', e.get('from', '')).strip()
            system += f"• [{tag}] \"{e.get('subject','')}\" — {frm}\n"

    messages = history + [{'role': 'user', 'content': message}]

    def generate():
        try:
            with client.messages.stream(
                model=model,
                max_tokens=3072,
                system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"
                final = stream.get_final_message()
                yield f"data: {json.dumps({'done': True, 'model': final.model})}\n\n"
        except Exception as ex:
            yield f"data: {json.dumps({'error': str(ex)})}\n\n"

    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

# ─── Financial Analysis ────────────────────────────────────
@app.route('/api/financial/analyze', methods=['POST'])
def financial_analyze():
    err = require_client()
    if err: return err

    data    = request.json or {}
    fin_data = data.get('data', '')
    fin_type = data.get('type', 'comprehensive')
    model   = data.get('model', 'claude-opus-4-7')
    today   = datetime.now().strftime('%Y-%m-%d')

    # Primary Analysis Agent
    analysis_res = client.messages.create(
        model=model,
        max_tokens=6144,
        messages=[{'role': 'user', 'content': f"""You are a senior Wall Street financial analyst. Today is {today}.

Perform comprehensive {fin_type} analysis on:

{fin_data}

Structure output as:
## Executive Summary
## Key Financial Metrics (show actual calculations)
## Trend & Growth Analysis
## Risk Assessment
## Peer / Market Benchmarking
## Valuation
## ★ Top 3 Insights
## Recommendations & Action Items

Be specific. Show your math. Flag any red flags immediately."""}]
    )
    analysis = analysis_res.content[0].text

    # Validation Agent
    val_res = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=1200,
        messages=[{'role': 'user', 'content': f"""You are a financial data quality officer. Today is {today}.

Validate this analysis. Reply ONLY with valid JSON (no markdown, no explanation):

Source data: {fin_data[:2000]}

Analysis: {analysis[:2000]}

{{
  "overallScore": <0-100>,
  "grade": "<A/B/C/D/F>",
  "dataFreshness": {{"status": "<PASS|WARN|FAIL>", "message": "<detail>", "latestDateFound": "<date or null>"}},
  "dataCompleteness": {{"status": "<PASS|WARN|FAIL>", "message": "<detail>", "missingFields": []}},
  "calculationAccuracy": {{"status": "<PASS|WARN|FAIL>", "message": "<detail>"}},
  "keyRisks": ["<risk1>", "<risk2>"],
  "recommendation": "<PROCEED|CAUTION|REVIEW REQUIRED>",
  "confidence": "<HIGH|MEDIUM|LOW>",
  "validatedAt": "{today}"
}}"""}]
    )

    validation = None
    try:
        txt = val_res.content[0].text
        m = re.search(r'\{[\s\S]*\}', txt)
        if m:
            validation = json.loads(m.group())
    except Exception:
        validation = {'overallScore': 70, 'grade': 'B', 'recommendation': 'CAUTION',
                      'confidence': 'MEDIUM', 'validatedAt': today,
                      'dataFreshness': {'status': 'WARN', 'message': 'Could not parse date from input'},
                      'dataCompleteness': {'status': 'WARN', 'message': 'Partial validation'},
                      'calculationAccuracy': {'status': 'WARN', 'message': 'Review recommended'}}

    return jsonify({'analysis': analysis, 'validation': validation, 'model': analysis_res.model})

# ─── Financial Modeling ────────────────────────────────────
@app.route('/api/financial/model', methods=['POST'])
def financial_model():
    err = require_client()
    if err: return err

    data   = request.json or {}
    mtype  = data.get('type', 'dcf')
    inputs = data.get('inputs', '')
    model  = data.get('model', 'claude-opus-4-7')
    today  = datetime.now().strftime('%Y-%m-%d')

    prompts = {
        'dcf':       f'Build a complete DCF model. Show revenue projections (5yr), EBITDA margins, free cash flow, WACC components, terminal value, and equity bridge. Include sensitivity table. Inputs: {inputs}',
        'lbo':       f'Build a full LBO model: sources/uses, debt waterfall, P&L (5yr), EBITDA→FCF bridge, IRR/MOIC at exit multiples, debt paydown, covenant headroom. Inputs: {inputs}',
        'comps':     f'Comparable company analysis: peer group, EV/EBITDA, EV/Revenue, P/E, P/FCF multiples, implied valuation range (football field). Inputs: {inputs}',
        'portfolio': f'Portfolio analysis: weights, beta, volatility, Sharpe, Sortino, max drawdown, 95% VaR, correlation insights, sector concentration, rebalancing recommendation. Portfolio: {inputs}',
    }

    prompt = prompts.get(mtype, f'Build financial model for: {inputs}')

    res = client.messages.create(
        model=model,
        max_tokens=8192,
        messages=[{'role': 'user', 'content': f"""Senior investment banker building a model. Date: {today}.

{prompt}

Format professionally:
### ASSUMPTIONS
### MODEL OUTPUTS (with tables)
### SENSITIVITY ANALYSIS
### KEY RISKS
### BOTTOM LINE"""}]
    )

    return jsonify({'result': res.content[0].text, 'model': res.model})

# ─── Daily Briefing ────────────────────────────────────────
@app.route('/api/briefing', methods=['POST'])
def daily_briefing():
    err = require_client()
    if err: return err

    data   = request.json or {}
    emails = data.get('emails', [])
    model  = data.get('model', 'claude-sonnet-4-6')
    now    = datetime.now()
    h      = now.hour
    greeting = 'Good morning' if h < 12 else ('Good afternoon' if h < 17 else 'Good evening')
    date_str = now.strftime('%A, %B %d, %Y')
    time_str = now.strftime('%I:%M %p')

    email_lines = '\n'.join([
        f"• [{'★ PRIORITY' if e.get('isImportant') else 'unread'}] \"{e.get('subject','')}\" — From: {re.sub(r'<[^>]+>', '', e.get('from','')).strip()}\n  Preview: {str(e.get('snippet',''))[:80]}..."
        for e in emails
    ]) or '(No unread emails)'

    res = client.messages.create(
        model=model,
        max_tokens=800,
        messages=[{'role': 'user', 'content': f"""You are JARVIS delivering a spoken briefing. Today: {date_str} at {time_str}.

Unread emails ({len(emails)}):
{email_lines}

Deliver a spoken briefing in 180-220 words. Structure:
1. "{greeting}, Master" opening with current time
2. Email priorities (call out ★ PRIORITY items by sender + subject)
3. Three most important things to tackle today
4. One sharp JARVIS-style closing observation

Write as flowing speech — no bullets, no headers. It will be read aloud."""}]
    )

    return jsonify({'briefing': res.content[0].text})

# ─── Gmail OAuth ───────────────────────────────────────────
@app.route('/api/gmail/auth')
def gmail_auth():
    if not GMAIL_AVAILABLE or not GOOGLE_CLIENT_ID:
        return jsonify({'error': 'Gmail not configured. Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env'}), 400

    flow = Flow.from_client_config(
        {'web': {'client_id': GOOGLE_CLIENT_ID, 'client_secret': GOOGLE_CLIENT_SECRET,
                 'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                 'token_uri': 'https://oauth2.googleapis.com/token',
                 'redirect_uris': [REDIRECT_URI]}},
        scopes=GMAIL_SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state_token = flow.authorization_url(access_type='offline', prompt='consent')
    session['oauth_state'] = state_token
    return jsonify({'authUrl': auth_url})

@app.route('/api/gmail/callback')
def gmail_callback():
    if not GMAIL_AVAILABLE:
        return redirect('/?error=gmail')
    try:
        flow = Flow.from_client_config(
            {'web': {'client_id': GOOGLE_CLIENT_ID, 'client_secret': GOOGLE_CLIENT_SECRET,
                     'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                     'token_uri': 'https://oauth2.googleapis.com/token',
                     'redirect_uris': [REDIRECT_URI]}},
            scopes=GMAIL_SCOPES,
            redirect_uri=REDIRECT_URI,
            state=session.get('oauth_state')
        )
        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials
        session['gmail_token']   = creds.token
        session['gmail_refresh'] = creds.refresh_token
        return redirect('/?connected=gmail')
    except Exception as ex:
        print(f'Gmail callback error: {ex}')
        return redirect('/?error=gmail')

@app.route('/api/gmail/status')
def gmail_status():
    return jsonify({'connected': bool(session.get('gmail_token'))})

@app.route('/api/gmail/emails')
def gmail_emails():
    if not session.get('gmail_token'):
        return jsonify({'error': 'Not authenticated', 'needsAuth': True}), 401
    try:
        creds = Credentials(
            token=session['gmail_token'],
            refresh_token=session.get('gmail_refresh'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            scopes=GMAIL_SCOPES
        )
        service = build('gmail', 'v1', credentials=creds)

        unread = service.users().messages().list(userId='me', maxResults=15, q='is:unread').execute()
        important = service.users().messages().list(userId='me', maxResults=5, q='is:important is:unread').execute()

        imp_ids = {m['id'] for m in important.get('messages', [])}
        msgs = unread.get('messages', [])[:12]

        emails = []
        for m in msgs:
            detail = service.users().messages().get(
                userId='me', id=m['id'], format='metadata',
                metadataHeaders=['Subject', 'From', 'Date']
            ).execute()
            headers = {h['name']: h['value'] for h in detail['payload']['headers']}
            emails.append({
                'id': m['id'],
                'subject': headers.get('Subject', '(No subject)'),
                'from': headers.get('From', ''),
                'date': headers.get('Date', ''),
                'snippet': detail.get('snippet', ''),
                'isImportant': m['id'] in imp_ids
            })

        return jsonify({'emails': emails, 'total': unread.get('resultSizeEstimate', len(emails))})
    except Exception as ex:
        if '401' in str(ex) or 'invalid_grant' in str(ex):
            session.pop('gmail_token', None)
            return jsonify({'error': 'Token expired', 'needsAuth': True}), 401
        return jsonify({'error': str(ex)}), 500

# ── Start ──────────────────────────────────────────────────
if __name__ == '__main__':
    print('\n' + '═' * 55)
    print('  ⚡  J.A.R.V.I.S.  —  All Systems Online  ⚡')
    print('═' * 55)
    print(f'  🌐  http://localhost:{PORT}')
    if not ANTHROPIC_KEY:
        print('  ⚠️   ANTHROPIC_API_KEY missing — copy .env.example → .env')
    print('  🔑  Add Gmail credentials to .env to enable email')
    print('═' * 55 + '\n')
    app.run(host='0.0.0.0', port=PORT, debug=False)
