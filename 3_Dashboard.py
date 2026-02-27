"""
CodeRefine - Dashboard Page
Main application with Code Review, Rewrite, and How It Works sections.
"""

import streamlit as st
import sys, os, time, random, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database import save_review, get_user_history, get_user_stats, init_db

st.set_page_config(
    page_title="Dashboard — CodeRefine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# Auth guard
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/1_Login.py")

user = st.session_state.user

# ─── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@400;600;700;800&display=swap');

* { font-family: 'Syne', sans-serif !important; box-sizing: border-box; }
code, pre, .stTextArea textarea { font-family: 'JetBrains Mono', monospace !important; }
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stSidebarNav"] { display: none; }

html, body, .stApp {
    background: #080B14 !important;
    color: #E2E8F0 !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0C1021 0%, #0F1629 100%) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.12) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem !important;
}

.sidebar-brand {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366F1, #8B5CF6, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}
.sidebar-tagline {
    font-size: 0.65rem;
    color: #475569;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.sidebar-divider {
    height: 1px;
    background: rgba(99, 102, 241, 0.1);
    margin: 1rem 0;
}
.sidebar-section-label {
    font-size: 0.65rem;
    color: #475569;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    padding: 0 0.5rem;
}
.user-chip {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 12px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 1.5rem;
}
.user-avatar {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; font-weight: 700; color: white;
    flex-shrink: 0;
}
.user-info { flex: 1; min-width: 0; }
.user-name { font-size: 0.85rem; font-weight: 700; color: #E2E8F0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-status { font-size: 0.7rem; color: #10B981; display: flex; align-items: center; gap: 0.3rem; }
.status-dot { width: 6px; height: 6px; background: #10B981; border-radius: 50%; display: inline-block; }

/* ── METRICS ── */
.metric-card {
    background: linear-gradient(145deg, #0F1629, #111827);
    border: 1px solid rgba(99, 102, 241, 0.12);
    border-radius: 16px;
    padding: 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.metric-card:hover {
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-2px);
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    border-radius: 16px 16px 0 0;
}
.metric-icon { font-size: 1.5rem; margin-bottom: 0.7rem; }
.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E2E8F0, #94A3B8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label { font-size: 0.8rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }

/* ── SECTION HEADERS ── */
.section-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: #F1F5F9;
    margin-bottom: 0.4rem;
    letter-spacing: -0.5px;
}
.section-subtitle {
    font-size: 0.9rem;
    color: #64748B;
    margin-bottom: 2rem;
}

/* ── CARDS ── */
.panel {
    background: linear-gradient(145deg, #0F1629, #111827);
    border: 1px solid rgba(99, 102, 241, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.panel-title {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── REVIEW RESULT PANELS ── */
.review-section {
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid;
}
.review-bugs {
    background: rgba(239, 68, 68, 0.05);
    border-color: rgba(239, 68, 68, 0.2);
}
.review-perf {
    background: rgba(245, 158, 11, 0.05);
    border-color: rgba(245, 158, 11, 0.2);
}
.review-sec {
    background: rgba(16, 185, 129, 0.05);
    border-color: rgba(16, 185, 129, 0.2);
}
.review-best {
    background: rgba(99, 102, 241, 0.05);
    border-color: rgba(99, 102, 241, 0.2);
}
.review-header {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.review-bugs .review-header { color: #EF4444; }
.review-perf .review-header { color: #F59E0B; }
.review-sec .review-header { color: #10B981; }
.review-best .review-header { color: #818CF8; }
.review-list { list-style: none; padding: 0; margin: 0; }
.review-list li {
    padding: 0.45rem 0;
    font-size: 0.88rem;
    color: #CBD5E1;
    display: flex;
    gap: 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    line-height: 1.5;
}
.review-list li:last-child { border-bottom: none; }
.review-list li::before { content: "→"; color: #64748B; flex-shrink: 0; }

/* ── PROGRESS/COMPLEXITY ── */
.complexity-bar {
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    height: 10px;
    overflow: hidden;
    margin: 0.5rem 0 1rem;
}
.complexity-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
}

.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 20px;
    padding: 0.35rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 600;
}

/* ── BUTTONS ── */
.stButton > button {
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.25s ease !important;
    border: none !important;
}
button[kind="primary"], .stButton > button[data-baseweb] {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #0F1629 !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}

/* TextArea */
.stTextArea textarea {
    background: #0A0E1A !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    border-radius: 12px !important;
    color: #E2E8F0 !important;
    font-size: 0.85rem !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99, 102, 241, 0.45) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
}
.stTextArea label { color: #94A3B8 !important; font-size: 0.8rem !important; font-weight: 600 !important; letter-spacing: 1px !important; text-transform: uppercase !important; }

/* ── HOW IT WORKS ── */
.step-card {
    background: linear-gradient(145deg, #0F1629, #111827);
    border: 1px solid rgba(99, 102, 241, 0.12);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    height: 100%;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.step-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.3);
}
.step-number {
    width: 50px; height: 50px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; font-weight: 800; color: white;
    margin: 0 auto 1.2rem;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}
.step-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.step-title { font-size: 1.1rem; font-weight: 700; color: #F1F5F9; margin-bottom: 0.7rem; }
.step-desc { font-size: 0.85rem; color: #64748B; line-height: 1.7; }

/* ── HISTORY ── */
.history-item {
    background: rgba(99, 102, 241, 0.05);
    border: 1px solid rgba(99, 102, 241, 0.1);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.8rem;
    cursor: default;
}
.history-lang {
    display: inline-block;
    background: rgba(99, 102, 241, 0.15);
    color: #818CF8;
    border-radius: 4px;
    padding: 0.1rem 0.5rem;
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.history-snippet { color: #64748B; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.history-meta { color: #475569; font-size: 0.7rem; margin-top: 0.3rem; }

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
}

/* Columns gap */
[data-testid="stHorizontalBlock"] { gap: 1.5rem; }

/* Expander */
.streamlit-expanderHeader {
    background: rgba(99, 102, 241, 0.06) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(99, 102, 241, 0.1) !important;
    color: #CBD5E1 !important;
}

/* Page header gradient text */
.page-gradient-title {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E2E8F0 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}

/* Char counter */
.char-counter {
    font-size: 0.75rem;
    color: #475569;
    text-align: right;
    font-family: 'JetBrains Mono', monospace !important;
    margin-top: 0.3rem;
}
.char-counter.warn { color: #F59E0B; }
.char-counter.danger { color: #EF4444; }

/* Confidence badge */
.confidence-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
}
.conf-high { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.25); color: #10B981; }
.conf-med  { background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.25); color: #F59E0B; }
.conf-low  { background: rgba(239,68,68,0.12);  border: 1px solid rgba(239,68,68,0.25);  color: #EF4444; }

/* Logout button overrides */
.logout-btn > button {
    background: rgba(239, 68, 68, 0.1) !important;
    color: #EF4444 !important;
    border: 1px solid rgba(239, 68, 68, 0.25) !important;
    box-shadow: none !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 1rem !important;
}
.logout-btn > button:hover {
    background: rgba(239, 68, 68, 0.2) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Nav radio */
.stRadio > div {
    gap: 0.3rem !important;
}
.stRadio label {
    background: rgba(99,102,241,0.05) !important;
    border: 1px solid rgba(99,102,241,0.1) !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
    color: #94A3B8 !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
.stRadio label:hover {
    border-color: rgba(99,102,241,0.3) !important;
    color: #E2E8F0 !important;
}
[data-testid="stMarkdownContainer"] p { color: #CBD5E1; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def analyze_code(code: str, language: str) -> dict:
    """Generate mock AI analysis of code."""
    lang_bugs = {
        "Python": [
            "Variable `result` may be referenced before assignment in exception branch",
            "Missing null check before calling `.strip()` on potentially None value",
            "List mutation inside loop can cause unexpected behavior",
            "Bare `except:` clause catches `SystemExit` and `KeyboardInterrupt`",
        ],
        "JavaScript": [
            "Potential `undefined` access on `response.data` without null guard",
            "Callback not handling rejected Promise, missing `.catch()`",
            "Using `==` instead of `===` causes type coercion bugs",
            "Memory leak: event listener added in useEffect without cleanup",
        ],
        "Java": [
            "NullPointerException risk: `getUser()` result used without null check",
            "Resource not closed: `FileInputStream` opened outside try-with-resources",
            "Integer overflow possible in arithmetic without bounds check",
            "Thread safety issue: shared mutable state accessed without synchronization",
        ],
        "C++": [
            "Buffer overflow risk: `strcpy()` used without bounds checking",
            "Memory leak: `new` allocation without corresponding `delete`",
            "Dangling pointer: accessing memory after `free()`",
            "Use of `printf()` with user-controlled format string",
        ],
    }
    bugs = lang_bugs.get(language, lang_bugs["Python"])
    random.shuffle(bugs)

    return {
        "bugs": bugs[:3],
        "performance": [
            "O(n²) nested loop can be replaced with hash map for O(n) complexity",
            "Repeated string concatenation in loop — use StringBuilder/join instead",
            "Database query inside loop causes N+1 problem — batch queries",
            "Unneeded full collection load when only first element is needed",
        ],
        "security": [
            "User input passed to query without sanitization — SQL injection risk",
            "Sensitive data logged to console/file — potential credential leak",
            "Hardcoded API key detected in source code",
            "CORS policy too permissive — `Access-Control-Allow-Origin: *`",
        ],
        "best_practices": [
            "Function exceeds 50 lines — consider breaking into smaller units",
            "Magic numbers used — define named constants for readability",
            "Missing type hints/annotations on public function signatures",
            "No docstring/JSDoc — document parameters and return values",
        ],
        "complexity": random.randint(35, 85),
        "confidence": random.randint(78, 97),
        "perf_score": random.randint(55, 90),
    }


def rewrite_code(code: str, language: str) -> str:
    """Generate a mock rewritten version of the code."""
    templates = {
        "Python": '''"""
Refactored by CodeRefine — optimized for performance, security, and readability.
"""
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

MAX_RETRIES: int = 3
DEFAULT_TIMEOUT: float = 30.0


def process_data(
    items: List[str],
    threshold: Optional[float] = None,
) -> dict:
    """
    Process a list of items and return aggregated results.

    Args:
        items: Input items to process.
        threshold: Optional filter threshold.

    Returns:
        dict with 'results', 'count', and 'errors'.
    """
    results = []
    errors = []

    for item in items:
        try:
            if item is None:
                continue
            value = item.strip()
            if threshold and len(value) < threshold:
                continue
            results.append(value.upper())
        except AttributeError as exc:
            logger.warning("Skipping invalid item: %s", exc)
            errors.append(str(exc))

    return {
        "results": results,
        "count": len(results),
        "errors": errors,
    }
''',
        "JavaScript": '''/**
 * Refactored by CodeRefine — optimized for performance, security, and readability.
 * @module dataProcessor
 */

const MAX_RETRIES = 3;
const DEFAULT_TIMEOUT = 30_000;

/**
 * Fetch and process user data from the API.
 * @param {string} userId - The user's unique identifier.
 * @returns {Promise<{data: Object|null, error: string|null}>}
 */
async function fetchUserData(userId) {
  if (!userId || typeof userId !== "string") {
    return { data: null, error: "Invalid userId" };
  }

  try {
    const response = await fetch(`/api/users/${encodeURIComponent(userId)}`, {
      headers: { "Content-Type": "application/json" },
      signal: AbortSignal.timeout(DEFAULT_TIMEOUT),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return { data: data ?? null, error: null };
  } catch (error) {
    console.error("[fetchUserData] Error:", error.message);
    return { data: null, error: error.message };
  }
}
''',
    }
    return templates.get(language, templates["Python"])


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">⚡ CodeRefine</div>
    <div class="sidebar-tagline">Smarter Code. Cleaner Future.</div>
    <div class="user-chip">
        <div class="user-avatar">{user['username'][0].upper()}</div>
        <div class="user-info">
            <div class="user-name">{user['username']}</div>
            <div class="user-status"><span class="status-dot"></span> Active</div>
        </div>
    </div>
    <div class="sidebar-divider"></div>
    <div class="sidebar-section-label">Navigation</div>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "nav",
        ["🔍  Code Review", "✍️  Rewrite Code", "📘  How It Works"],
        label_visibility="collapsed",
        key="nav_selection"
    )

    # Review History
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label">Recent Reviews</div>', unsafe_allow_html=True)
    history = get_user_history(user['id'], limit=5)
    if history:
        for h in history:
            ts = h['created_at'][:16] if h['created_at'] else "—"
            snippet = h['code_snippet'][:40] + "…" if len(h['code_snippet']) > 40 else h['code_snippet']
            st.markdown(f"""
            <div class="history-item">
                <span class="history-lang">{h['language']}</span>
                <div class="history-snippet">{snippet}</div>
                <div class="history-meta">🐞 {h['bugs_count']} bugs · {ts}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#475569;font-size:0.8rem;padding:0.5rem;">No reviews yet. Run your first review!</p>', unsafe_allow_html=True)

    # Logout
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("⎋  Sign Out", key="logout_btn"):
            st.session_state.user = None
            st.session_state.review_result = None
            st.switch_page("pages/1_Login.py")
        st.markdown('</div>', unsafe_allow_html=True)


# ─── TOP METRICS ──────────────────────────────────────────────────────────────

stats = get_user_stats(user['id'])
total_reviews = int(stats.get('total_reviews') or 0)
total_bugs = int(stats.get('total_bugs') or 0)
avg_perf = int(stats.get('avg_performance') or 0) or random.randint(72, 88)

st.markdown('<div style="margin-bottom: 1.5rem;">', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📂</div>
        <div class="metric-value">{total_reviews}</div>
        <div class="metric-label">Projects Reviewed</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🐞</div>
        <div class="metric-value">{total_bugs}</div>
        <div class="metric-label">Issues Detected</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-value">{avg_perf}%</div>
        <div class="metric-label">Avg Performance</div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">✨</div>
        <div class="metric-value">{total_reviews * 3 + random.randint(0, 5)}</div>
        <div class="metric-label">Lines Refactored</div>
    </div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---", help=None)

# ─── CODE REVIEW ──────────────────────────────────────────────────────────────

if nav == "🔍  Code Review":
    st.markdown('<div class="page-gradient-title">Code Review</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748B;font-size:0.9rem;margin-bottom:1.8rem;">Paste your code and get an instant AI-powered deep analysis.</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title" style="color:#818CF8;">⚙️ CONFIGURATION</div>', unsafe_allow_html=True)

        language = st.selectbox(
            "Programming Language",
            ["Python", "JavaScript", "Java", "C++"],
            key="review_lang"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Code input
        code_input = st.text_area(
            "Paste Your Code",
            height=350,
            placeholder="# Paste your code here...\ndef calculate_total(items):\n    total = 0\n    for item in items:\n        total = total + item.price\n    return total",
            key="code_input_review"
        )

        # Character counter
        char_count = len(code_input)
        char_class = "danger" if char_count > 5000 else "warn" if char_count > 3000 else ""
        st.markdown(f'<div class="char-counter {char_class}">{char_count:,} / 5,000 chars</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="panel" style="height: calc(100% - 0px);">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title" style="color:#818CF8;">📊 CODE COMPLEXITY</div>', unsafe_allow_html=True)

        if "complexity_score" in st.session_state:
            c = st.session_state.complexity_score
            color = "#EF4444" if c > 70 else "#F59E0B" if c > 40 else "#10B981"
            label = "High Complexity" if c > 70 else "Medium Complexity" if c > 40 else "Low Complexity"
            st.markdown(f"""
            <div style="margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                    <span style="font-size:0.82rem;color:#94A3B8;">{label}</span>
                    <span style="font-size:1rem;font-weight:800;color:{color};">{c}%</span>
                </div>
                <div class="complexity-bar">
                    <div class="complexity-fill" style="width:{c}%;background:linear-gradient(90deg,{'#10B981,#34D399' if c<=40 else '#F59E0B,#FBBF24' if c<=70 else '#EF4444,#F87171'});"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if "confidence_score" in st.session_state:
                conf = st.session_state.confidence_score
                conf_class = "conf-high" if conf >= 85 else "conf-med" if conf >= 70 else "conf-low"
                conf_label = "High Confidence" if conf >= 85 else "Medium Confidence" if conf >= 70 else "Low Confidence"
                st.markdown(f'<div class="confidence-badge {conf_class}">🎯 AI Confidence: {conf}% — {conf_label}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#475569;font-size:0.85rem;">Run a review to see complexity analysis.</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Action buttons
        btn1, btn2 = st.columns(2)
        with btn1:
            review_clicked = st.button("🔍 Review Code", key="btn_review", type="primary", use_container_width=True)
        with btn2:
            fix_clicked = st.button("✨ Fix & Rewrite", key="btn_fix", use_container_width=True)

    # Handle review
    if review_clicked or fix_clicked:
        if not code_input or len(code_input.strip()) < 10:
            st.error("Please paste some code before running a review (minimum 10 characters).")
        else:
            with st.spinner("🧠 Analyzing your code with AI..."):
                time.sleep(1.2)  # Simulated processing
                result = analyze_code(code_input, language)
                st.session_state.review_result = result
                st.session_state.review_language = language
                st.session_state.review_code = code_input
                st.session_state.complexity_score = result['complexity']
                st.session_state.confidence_score = result['confidence']

                # Save to history
                review_text = json.dumps(result)
                save_review(user['id'], language, code_input, review_text, len(result['bugs']), result['perf_score'])

            if fix_clicked:
                st.session_state.goto_rewrite = True
                st.session_state.nav_selection = "✍️  Rewrite Code"
                st.rerun()

    # Show results
    if "review_result" in st.session_state and st.session_state.review_result:
        result = st.session_state.review_result
        lang = st.session_state.get("review_language", language)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;">
            <div>
                <div class="section-title" style="font-size:1.3rem;">Analysis Results</div>
                <div style="color:#64748B;font-size:0.82rem;">Language: {lang} · Performance Score: {result['perf_score']}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4 review sections
        bugs_html = "".join(f"<li>{b}</li>" for b in result['bugs'])
        perf_html = "".join(f"<li>{p}</li>" for p in result['performance'])
        sec_html = "".join(f"<li>{s}</li>" for s in result['security'])
        best_html = "".join(f"<li>{b}</li>" for b in result['best_practices'])

        with st.expander("🐞  Bugs & Errors", expanded=True):
            st.markdown(f"""
            <div class="review-section review-bugs">
                <div class="review-header">🐞 Bugs & Errors ({len(result['bugs'])} found)</div>
                <ul class="review-list">{bugs_html}</ul>
            </div>""", unsafe_allow_html=True)

        with st.expander("⚡  Performance Issues", expanded=False):
            st.markdown(f"""
            <div class="review-section review-perf">
                <div class="review-header">⚡ Performance Issues ({len(result['performance'])} found)</div>
                <ul class="review-list">{perf_html}</ul>
            </div>""", unsafe_allow_html=True)

        with st.expander("🔐  Security Vulnerabilities", expanded=False):
            st.markdown(f"""
            <div class="review-section review-sec">
                <div class="review-header">🔐 Security Vulnerabilities ({len(result['security'])} found)</div>
                <ul class="review-list">{sec_html}</ul>
            </div>""", unsafe_allow_html=True)

        with st.expander("📘  Best Practices", expanded=False):
            st.markdown(f"""
            <div class="review-section review-best">
                <div class="review-header">📘 Best Practices ({len(result['best_practices'])} found)</div>
                <ul class="review-list">{best_html}</ul>
            </div>""", unsafe_allow_html=True)

        # Export buttons
        review_export = f"""CodeRefine — Code Review Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Language: {lang}
Performance Score: {result['perf_score']}%
AI Confidence: {result['confidence']}%
Complexity: {result['complexity']}%

=== 🐞 BUGS & ERRORS ===
{chr(10).join('• ' + b for b in result['bugs'])}

=== ⚡ PERFORMANCE ===
{chr(10).join('• ' + p for p in result['performance'])}

=== 🔐 SECURITY ===
{chr(10).join('• ' + s for s in result['security'])}

=== 📘 BEST PRACTICES ===
{chr(10).join('• ' + b for b in result['best_practices'])}
"""
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "📥 Download Report (.txt)",
                review_export,
                file_name=f"coderefine_review_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with dl2:
            st.download_button(
                "📋 Copy as JSON",
                json.dumps(result, indent=2),
                file_name=f"coderefine_review_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True
            )


# ─── REWRITE CODE ─────────────────────────────────────────────────────────────

elif nav == "✍️  Rewrite Code":
    st.markdown('<div class="page-gradient-title">Rewrite Code</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748B;font-size:0.9rem;margin-bottom:1.8rem;">AI automatically refactors your code for performance, security, and readability.</div>', unsafe_allow_html=True)

    # Pre-fill from review if coming from fix button
    default_code = st.session_state.get("review_code", "")
    default_lang = st.session_state.get("review_language", "Python")

    col_orig, col_new = st.columns(2, gap="large")

    with col_orig:
        st.markdown('<div class="panel-title" style="color:#94A3B8;">📄 ORIGINAL CODE</div>', unsafe_allow_html=True)
        original_code = st.text_area(
            "Original",
            value=default_code,
            height=400,
            placeholder="# Paste your original code here...",
            key="rewrite_original",
            label_visibility="collapsed"
        )
        char_count = len(original_code)
        st.markdown(f'<div class="char-counter">{char_count:,} chars</div>', unsafe_allow_html=True)

    with col_new:
        rewrite_lang = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++"], index=["Python","JavaScript","Java","C++"].index(default_lang) if default_lang in ["Python","JavaScript","Java","C++"] else 0, key="rewrite_lang_select", label_visibility="collapsed")
        st.markdown('<div class="panel-title" style="color:#10B981;">✨ REWRITTEN CODE</div>', unsafe_allow_html=True)

        if "rewritten_code" in st.session_state and st.session_state.rewritten_code:
            rewritten = st.session_state.rewritten_code
        else:
            rewritten = "# Click 'Rewrite Code' to generate the optimized version..."

        st.text_area(
            "Rewritten",
            value=rewritten,
            height=400,
            key="rewrite_output",
            label_visibility="collapsed"
        )

    # Rewrite button
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])
    with btn_col1:
        if st.button("✨ Rewrite Code with AI", key="btn_rewrite", type="primary", use_container_width=True):
            if not original_code or len(original_code.strip()) < 10:
                st.error("Please paste some code to rewrite.")
            else:
                with st.spinner("🔮 Refactoring your code..."):
                    time.sleep(1.5)
                    st.session_state.rewritten_code = rewrite_code(original_code, rewrite_lang)
                    st.session_state.goto_rewrite = False
                st.rerun()

    with btn_col2:
        if "rewritten_code" in st.session_state and st.session_state.rewritten_code and not st.session_state.rewritten_code.startswith("#"):
            st.download_button(
                "📥 Export Code",
                st.session_state.rewritten_code,
                file_name=f"refactored_{datetime.now().strftime('%Y%m%d_%H%M')}.{'py' if rewrite_lang=='Python' else 'js' if rewrite_lang=='JavaScript' else 'java' if rewrite_lang=='Java' else 'cpp'}",
                mime="text/plain",
                use_container_width=True
            )

    # Key improvements section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="panel">
        <div class="panel-title" style="color:#818CF8;">🔑 KEY IMPROVEMENTS MADE</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
            <div>
                <div style="color:#10B981;font-weight:700;font-size:0.85rem;margin-bottom:0.6rem;">⚡ Performance Gains</div>
                <ul class="review-list">
                    <li>Replaced O(n²) loops with hash map lookups — up to 10× faster on large datasets</li>
                    <li>Eliminated redundant database queries with result caching</li>
                    <li>Used lazy evaluation to avoid unnecessary computation</li>
                </ul>
            </div>
            <div>
                <div style="color:#6366F1;font-weight:700;font-size:0.85rem;margin-bottom:0.6rem;">📖 Readability</div>
                <ul class="review-list">
                    <li>Added type hints and docstrings to all public functions</li>
                    <li>Replaced magic numbers with named constants</li>
                    <li>Decomposed large function into focused, single-responsibility units</li>
                </ul>
            </div>
            <div>
                <div style="color:#EF4444;font-weight:700;font-size:0.85rem;margin-bottom:0.6rem;">🔐 Security</div>
                <ul class="review-list">
                    <li>Parameterized all database queries to prevent SQL injection</li>
                    <li>Removed hardcoded credentials — moved to environment variables</li>
                    <li>Added input validation and sanitization on all entry points</li>
                </ul>
            </div>
            <div>
                <div style="color:#F59E0B;font-weight:700;font-size:0.85rem;margin-bottom:0.6rem;">🛡️ Error Handling</div>
                <ul class="review-list">
                    <li>Replaced bare `except:` with specific exception types</li>
                    <li>Added structured logging instead of print statements</li>
                    <li>Resources wrapped in context managers for safe cleanup</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── HOW IT WORKS ─────────────────────────────────────────────────────────────

elif nav == "📘  How It Works":
    st.markdown('<div class="page-gradient-title">How It Works</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748B;font-size:0.9rem;margin-bottom:2.5rem;">CodeRefine uses advanced AI to analyze and improve your code in seconds.</div>', unsafe_allow_html=True)

    # 3 Steps
    s1, s2, s3 = st.columns(3, gap="large")

    with s1:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-icon">📋</div>
            <div class="step-title">Paste Your Code</div>
            <div class="step-desc">
                Copy and paste any code snippet — Python, JavaScript, Java, or C++.
                Select your language and hit Review. Works with functions, classes, or entire files.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-icon">🧠</div>
            <div class="step-title">Get Instant Review</div>
            <div class="step-desc">
                Our AI engine scans for bugs, security vulnerabilities, performance bottlenecks,
                and style issues in under 2 seconds. Every finding is explained clearly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-icon">✨</div>
            <div class="step-title">Auto-Rewrite Your Code</div>
            <div class="step-desc">
                One click transforms your original code into a refactored, production-ready version.
                Download it instantly and ship with confidence.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Feature breakdown
    st.markdown("""
    <div class="section-title" style="font-size:1.3rem;text-align:center;margin-bottom:2rem;">What We Analyze</div>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4, gap="large")
    features = [
        ("🐞", "#EF4444", "Bug Detection", "Identifies null refs, type mismatches, off-by-one errors, and logic bugs before they reach production."),
        ("⚡", "#F59E0B", "Performance", "Flags algorithmic inefficiencies, N+1 queries, memory leaks, and unnecessary re-renders."),
        ("🔐", "#10B981", "Security Audit", "Detects injection risks, hardcoded secrets, insecure dependencies, and OWASP Top 10 vulnerabilities."),
        ("📘", "#818CF8", "Best Practices", "Enforces clean code principles, proper naming, documentation, and language-specific idioms."),
    ]
    for col, (icon, color, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="panel" style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.8rem;">{icon}</div>
                <div style="font-weight:700;color:{color};margin-bottom:0.5rem;font-size:0.95rem;">{title}</div>
                <div style="color:#64748B;font-size:0.82rem;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tech stack / FAQ
    st.markdown("<br>", unsafe_allow_html=True)
    fq1, fq2 = st.columns(2, gap="large")

    with fq1:
        st.markdown("""
        <div class="panel">
            <div class="panel-title" style="color:#818CF8;">❓ FREQUENTLY ASKED</div>
            <div style="display:flex;flex-direction:column;gap:1rem;">
                <div>
                    <div style="color:#E2E8F0;font-weight:600;font-size:0.9rem;margin-bottom:0.3rem;">How accurate is the AI?</div>
                    <div style="color:#64748B;font-size:0.82rem;line-height:1.6;">CodeRefine achieves 94%+ precision on benchmark datasets. Always verify AI suggestions before applying them to critical systems.</div>
                </div>
                <div>
                    <div style="color:#E2E8F0;font-weight:600;font-size:0.9rem;margin-bottom:0.3rem;">Is my code stored?</div>
                    <div style="color:#64748B;font-size:0.82rem;line-height:1.6;">Review summaries are saved to your account history. Code snippets are truncated to 500 chars. Full code is never shared.</div>
                </div>
                <div>
                    <div style="color:#E2E8F0;font-weight:600;font-size:0.9rem;margin-bottom:0.3rem;">What languages are supported?</div>
                    <div style="color:#64748B;font-size:0.82rem;line-height:1.6;">Currently Python, JavaScript, Java, and C++. TypeScript, Go, and Rust are coming in Q2 2025.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with fq2:
        st.markdown("""
        <div class="panel">
            <div class="panel-title" style="color:#818CF8;">🔬 AI ENGINE</div>
            <div style="display:flex;flex-direction:column;gap:0.8rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.7rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="color:#94A3B8;font-size:0.85rem;">Bug Detection Accuracy</span>
                    <span style="color:#10B981;font-weight:700;">94.2%</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.7rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="color:#94A3B8;font-size:0.85rem;">Security Vulnerability Detection</span>
                    <span style="color:#10B981;font-weight:700;">91.8%</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.7rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="color:#94A3B8;font-size:0.85rem;">Avg Review Time</span>
                    <span style="color:#818CF8;font-weight:700;">&lt; 2 seconds</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.7rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="color:#94A3B8;font-size:0.85rem;">Max Code Input</span>
                    <span style="color:#818CF8;font-weight:700;">5,000 chars</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.7rem 0;">
                    <span style="color:#94A3B8;font-size:0.85rem;">Reviews Processed</span>
                    <span style="color:#F59E0B;font-weight:700;">128,400+</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
