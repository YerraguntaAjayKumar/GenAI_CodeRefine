"""
CodeRefine - Signup Page
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database import create_user, init_db
import re

st.set_page_config(
    page_title="Sign Up — CodeRefine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

init_db()

if "user" in st.session_state and st.session_state.user:
    st.switch_page("pages/3_Dashboard.py")

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

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        linear-gradient(rgba(139, 92, 246, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(139, 92, 246, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}

.brand-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}

.brand-logo {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.5rem;
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
    font-size: 0.85rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

.auth-card {
    background: linear-gradient(145deg, #0F1629 0%, #111827 100%);
    border: 1px solid rgba(139, 92, 246, 0.15);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(139, 92, 246, 0.05),
                inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
}

.auth-card::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.07) 0%, transparent 70%);
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

.stTextInput input {
    background: rgba(15, 22, 41, 0.8) !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Syne', sans-serif !important;
    transition: all 0.2s !important;
}
.stTextInput input:focus {
    border-color: #8B5CF6 !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
}
.stTextInput label {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

.stButton > button {
    background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
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
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
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
    background: rgba(139, 92, 246, 0.1);
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
    color: #8B5CF6;
    text-decoration: none;
    font-weight: 600;
}

.perks {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin: 1rem 0 2rem;
}
.perk {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #64748B;
}
.perk-icon { font-size: 1rem; }

[data-testid="stVerticalBlock"] { gap: 0.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brand-header">
    <span class="brand-logo">⚡ CodeRefine</span>
    <p class="brand-tagline">Smarter Code. Cleaner Future.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="auth-card">
    <div class="auth-title">Create your account</div>
    <div class="auth-subtitle">Join thousands of developers shipping better code</div>
    <div class="perks">
        <div class="perk"><span class="perk-icon">🐞</span> Bug Detection</div>
        <div class="perk"><span class="perk-icon">⚡</span> Performance Analysis</div>
        <div class="perk"><span class="perk-icon">🔐</span> Security Audit</div>
        <div class="perk"><span class="perk-icon">✨</span> Auto Code Rewrite</div>
        <div class="perk"><span class="perk-icon">📊</span> Review History</div>
        <div class="perk"><span class="perk-icon">📥</span> Export Reports</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Show error from session
if "signup_error" in st.session_state and st.session_state.signup_error:
    st.markdown(f'<div class="error-msg">✗ {st.session_state.signup_error}</div>', unsafe_allow_html=True)
    st.session_state.signup_error = None

username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
email = st.text_input("Email Address", placeholder="your@email.com", key="signup_email")
password = st.text_input("Password", placeholder="Min. 8 characters", type="password", key="signup_password")
confirm = st.text_input("Confirm Password", placeholder="Repeat your password", type="password", key="signup_confirm")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Create Account →", key="signup_btn"):
    error = None
    if not all([username, email, password, confirm]):
        error = "Please fill in all fields."
    elif len(username) < 3:
        error = "Username must be at least 3 characters."
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        error = "Please enter a valid email address."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."
    elif password != confirm:
        error = "Passwords do not match."

    if error:
        st.session_state.signup_error = error
        st.rerun()
    else:
        success, msg = create_user(username, email, password)
        if success:
            st.session_state.signup_success = True
            st.switch_page("pages/1_Login.py")
        else:
            st.session_state.signup_error = msg
            st.rerun()

st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
st.markdown('<div class="nav-link">Already have an account? <a href="/1_Login" target="_self">Sign in →</a></div>', unsafe_allow_html=True)
