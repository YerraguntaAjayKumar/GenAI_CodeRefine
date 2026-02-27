"""
CodeRefine - Login Page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database import authenticate_user, init_db

st.set_page_config(
    page_title="Login — CodeRefine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

init_db()

# Redirect if already logged in
if "user" in st.session_state and st.session_state.user:
    st.switch_page("pages/3_Dashboard.py")

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Syne:wght@400;600;800&display=swap');

* { font-family: 'Syne', sans-serif !important; margin: 0; padding: 0; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }
.stDeployButton { display: none; }

html, body, .stApp {
    background: #080B14 !important;
    color: #E2E8F0 !important;
    min-height: 100vh;
}

/* Animated background grid */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        linear-gradient(rgba(99, 102, 241, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99, 102, 241, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

.brand-header {
    text-align: center;
    padding: 3rem 0 2rem;
}

.brand-logo {
    font-family: 'Syne', sans-serif !important;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #06B6D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -2px;
    display: block;
}

.brand-tagline {
    color: #64748B;
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.auth-card {
    background: linear-gradient(145deg, #0F1629 0%, #111827 100%);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(99, 102, 241, 0.05),
                inset 0 1px 0 rgba(255,255,255,0.05);
    margin: 0 auto;
    position: relative;
    overflow: hidden;
}

.auth-card::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
    pointer-events: none;
}

.auth-card::after {
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(6, 182, 212, 0.06) 0%, transparent 70%);
    pointer-events: none;
}

.auth-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 0.3rem;
}

.auth-subtitle {
    color: #64748B;
    font-size: 0.85rem;
    margin-bottom: 2rem;
}

/* Input styling */
.stTextInput input {
    background: rgba(15, 22, 41, 0.8) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Syne', sans-serif !important;
    transition: all 0.2s !important;
}
.stTextInput input:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}
.stTextInput label {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

.divider {
    display: flex;
    align-items: center;
    margin: 1.5rem 0;
    color: #334155;
    font-size: 0.8rem;
}
.divider::before, .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(99, 102, 241, 0.1);
}
.divider::before { margin-right: 1rem; }
.divider::after { margin-left: 1rem; }

.nav-link {
    text-align: center;
    color: #64748B;
    font-size: 0.85rem;
    margin-top: 1rem;
}
.nav-link a {
    color: #6366F1;
    text-decoration: none;
    font-weight: 600;
}

.success-msg {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #10B981;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}
.error-msg {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #EF4444;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

.feature-pills {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.5rem 0 2.5rem;
}
.pill {
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.75rem;
    color: #8B5CF6;
    letter-spacing: 0.5px;
}

[data-testid="stVerticalBlock"] { gap: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# Brand header
st.markdown("""
<div class="brand-header">
    <span class="brand-logo">⚡ CodeRefine</span>
    <p class="brand-tagline">Smarter Code. Cleaner Future.</p>
</div>
<div class="feature-pills">
    <span class="pill">🐞 Bug Detection</span>
    <span class="pill">⚡ Performance Analysis</span>
    <span class="pill">🔐 Security Audit</span>
    <span class="pill">✨ Auto-Rewrite</span>
</div>
""", unsafe_allow_html=True)

# Auth card
st.markdown('<div class="auth-card">', unsafe_allow_html=True)
st.markdown('<div class="auth-title">Welcome back</div>', unsafe_allow_html=True)
st.markdown('<div class="auth-subtitle">Sign in to continue to your workspace</div>', unsafe_allow_html=True)

# Show messages
if "signup_success" in st.session_state and st.session_state.signup_success:
    st.markdown('<div class="success-msg">✓ Account created! Please sign in.</div>', unsafe_allow_html=True)
    st.session_state.signup_success = False

if "login_error" in st.session_state and st.session_state.login_error:
    st.markdown(f'<div class="error-msg">✗ {st.session_state.login_error}</div>', unsafe_allow_html=True)
    st.session_state.login_error = None

# Form
username = st.text_input("Username", placeholder="Enter your username", key="login_username")
password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Sign In →", key="login_btn"):
    if not username or not password:
        st.session_state.login_error = "Please fill in all fields."
        st.rerun()
    else:
        user = authenticate_user(username, password)
        if user:
            st.session_state.user = user
            st.session_state.login_error = None
            st.switch_page("pages/3_Dashboard.py")
        else:
            st.session_state.login_error = "Invalid username or password."
            st.rerun()

st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
st.markdown('<div class="nav-link">Don\'t have an account? <a href="/2_Signup" target="_self">Create one free →</a></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
