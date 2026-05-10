import streamlit as st


def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', system-ui, sans-serif !important; }

.stApp { background: #07080f; }

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    max-width: 800px;
    padding-top: 0 !important;
    padding-bottom: 5rem !important;
}

/* ── Header ───────────────────────────────────── */
.ra-header { text-align: center; padding: 3.5rem 0 2.25rem; }

.ra-pill {
    display: inline-block;
    background: rgba(99,102,241,.1);
    border: 1px solid rgba(99,102,241,.35);
    color: #818cf8;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 100px;
    margin-bottom: 1.4rem;
}

.ra-title {
    font-size: 3.8rem;
    font-weight: 800;
    letter-spacing: -.04em;
    background: linear-gradient(135deg, #c7d2fe 0%, #a5b4fc 40%, #67e8f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.05;
}

.ra-sub { margin-top: .9rem; color: #3d4860; font-size: 1rem; }

/* ── Input card ───────────────────────────────── */
.ra-card {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px;
    padding: 2rem 2.25rem 1.75rem;
    margin-bottom: 1.25rem;
}

/* ── Text input ───────────────────────────────── */
.stTextInput > label {
    color: #4b5563 !important;
    font-size: .72rem !important;
    font-weight: 600 !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
}
.stTextInput input {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.09) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: .98rem !important;
    padding: .75rem 1rem !important;
    caret-color: #818cf8;
    transition: border .15s, box-shadow .15s;
}
.stTextInput input:focus {
    border-color: rgba(99,102,241,.55) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important;
    outline: none !important;
}
.stTextInput input::placeholder { color: #2a3244 !important; }

/* ── Radio ────────────────────────────────────── */
.stRadio > label {
    color: #4b5563 !important;
    font-size: .72rem !important;
    font-weight: 600 !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
}

/* ── Run button ───────────────────────────────── */
.stButton button {
    background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: .95rem !important;
    font-weight: 600 !important;
    letter-spacing: .03em !important;
    padding: .7rem 2rem !important;
    width: 100% !important;
    transition: opacity .2s, transform .2s, box-shadow .2s !important;
}
.stButton button:hover:not(:disabled) {
    opacity: .85 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,.35) !important;
}
.stButton button:disabled { opacity: .3 !important; }

/* ── Download button ──────────────────────────── */
.stDownloadButton button {
    background: rgba(16,185,129,.08) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16,185,129,.28) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
    padding: .6rem 1.75rem !important;
    transition: all .2s !important;
}
.stDownloadButton button:hover {
    background: rgba(16,185,129,.18) !important;
    border-color: rgba(16,185,129,.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Activity log ─────────────────────────────── */
.ra-log-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,.04);
    animation: fadeUp .22s ease-out both;
}
.ra-log-row:last-child { border-bottom: none; }
.ra-log-ico { font-size: .9rem; min-width: 20px; line-height: 1.6; }
.ra-log-msg { color: #94a3b8; font-size: .875rem; line-height: 1.6; }
.ra-log-msg b { color: #e2e8f0; font-weight: 600; }
.ra-log-msg code {
    background: rgba(99,102,241,.18);
    color: #a5b4fc;
    padding: 1px 7px;
    border-radius: 5px;
    font-size: .82rem;
}
.ra-ok   { color: #34d399; font-weight: 600; }
.ra-warn { color: #f59e0b; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(5px); }
    to   { opacity: 1; transform: translateY(0);   }
}

/* ── Progress bar ─────────────────────────────── */
.stProgress > div > div {
    background: rgba(255,255,255,.06) !important;
    border-radius: 100px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #67e8f9) !important;
    border-radius: 100px !important;
    transition: width .4s ease !important;
}

/* ── Status widget ────────────────────────────── */
[data-testid="stStatusWidget"],
div[data-testid="stExpander"] {
    background: rgba(255,255,255,.02) !important;
    border: 1px solid rgba(255,255,255,.07) !important;
    border-radius: 14px !important;
}

/* ── Section divider ──────────────────────────── */
.ra-section {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 2.75rem 0 1.25rem;
}
.ra-section-title { color: #e2e8f0; font-size: 1rem; font-weight: 600; white-space: nowrap; }
.ra-section-line  { flex: 1; height: 1px; background: rgba(255,255,255,.07); }
.ra-section-badge {
    background: rgba(16,185,129,.1);
    border: 1px solid rgba(16,185,129,.28);
    color: #34d399;
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: 2px 10px;
    border-radius: 100px;
    white-space: nowrap;
}

/* ── Stats row ────────────────────────────────── */
.ra-stats { display: flex; gap: 12px; margin-bottom: 1.5rem; }
.ra-stat {
    flex: 1;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    padding: .9rem 1rem;
    text-align: center;
}
.ra-stat-n {
    font-size: 1.8rem;
    font-weight: 700;
    color: #a5b4fc;
    line-height: 1;
    margin-bottom: .3rem;
}
.ra-stat-l {
    color: #374151;
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
}

/* ── Report body ──────────────────────────────── */
.ra-report {
    background: rgba(255,255,255,.018);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    line-height: 1.8;
}
.ra-report h1 {
    font-size: 1.75rem; font-weight: 700; color: #e2e8f0;
    letter-spacing: -.025em; margin-bottom: 1.25rem;
    padding-bottom: .75rem; border-bottom: 1px solid rgba(255,255,255,.07);
}
.ra-report h2 {
    font-size: 1.1rem; font-weight: 600; color: #a5b4fc;
    margin-top: 2rem; margin-bottom: .7rem;
    padding-bottom: .35rem; border-bottom: 1px solid rgba(165,180,252,.12);
}
.ra-report h3 { font-size: .95rem; font-weight: 600; color: #64748b; margin-top: 1.25rem; }
.ra-report p  { color: #94a3b8; margin-bottom: .85rem; }
.ra-report ul, .ra-report ol { color: #94a3b8; padding-left: 1.5rem; }
.ra-report li { margin-bottom: .35rem; }
.ra-report a  { color: #67e8f9; text-decoration: none; }
.ra-report a:hover { text-decoration: underline; }
.ra-report strong { color: #e2e8f0; font-weight: 600; }
.ra-report em { color: #64748b; }
.ra-report code {
    background: rgba(99,102,241,.15); color: #a5b4fc;
    padding: 2px 7px; border-radius: 5px; font-size: .84em;
}
.ra-report pre {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 8px; padding: 1rem 1.25rem; overflow-x: auto;
}
.ra-report blockquote {
    border-left: 3px solid rgba(99,102,241,.45);
    margin: 1rem 0; padding: .4rem 0 .4rem 1.25rem;
    color: #4b5563; font-style: italic;
}
.ra-report hr { border: none; border-top: 1px solid rgba(255,255,255,.06); margin: 1.5rem 0; }
.ra-report table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
.ra-report th {
    background: rgba(99,102,241,.12); color: #a5b4fc;
    font-size: .78rem; letter-spacing: .06em; text-transform: uppercase;
    padding: .6rem .9rem; text-align: left;
    border-bottom: 1px solid rgba(99,102,241,.2);
}
.ra-report td { color: #94a3b8; padding: .55rem .9rem; border-bottom: 1px solid rgba(255,255,255,.04); }
.ra-report tr:hover td { background: rgba(255,255,255,.02); }
</style>
""", unsafe_allow_html=True)


def header():
    st.markdown("""
<div class="ra-header">
    <div class="ra-pill">⚡ Groq &nbsp;·&nbsp; LLaMA 3.3 70B &nbsp;·&nbsp; DuckDuckGo</div>
    <h1 class="ra-title">ResearchAgent</h1>
    <p class="ra-sub">Enter a topic — the agent searches, reads, and writes a full report autonomously.</p>
</div>
""", unsafe_allow_html=True)


def card_open():
    st.markdown('<div class="ra-card">', unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def spacer(rem=1):
    st.markdown(f"<div style='height:{rem}rem'></div>", unsafe_allow_html=True)


def log(icon, msg_html):
    st.markdown(f"""
<div class="ra-log-row">
  <span class="ra-log-ico">{icon}</span>
  <span class="ra-log-msg">{msg_html}</span>
</div>""", unsafe_allow_html=True)


def section(title, badge="Complete"):
    st.markdown(f"""
<div class="ra-section">
  <span class="ra-section-title">{title}</span>
  <span class="ra-section-line"></span>
  <span class="ra-section-badge">{badge}</span>
</div>""", unsafe_allow_html=True)


def stats(n_iter, n_src, n_facts):
    st.markdown(f"""
<div class="ra-stats">
  <div class="ra-stat">
    <div class="ra-stat-n">{n_iter}</div>
    <div class="ra-stat-l">Iterations</div>
  </div>
  <div class="ra-stat">
    <div class="ra-stat-n">{n_src}</div>
    <div class="ra-stat-l">Sources read</div>
  </div>
  <div class="ra-stat">
    <div class="ra-stat-n">{n_facts}</div>
    <div class="ra-stat-l">Facts extracted</div>
  </div>
</div>""", unsafe_allow_html=True)


def report(html_str):
    st.markdown(f'<div class="ra-report">{html_str}</div>', unsafe_allow_html=True)
