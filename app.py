"""
CodeRefine - AI-Powered Code Review & Rewriting Assistant
Main entry point - redirects to login or dashboard based on session state.
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from database import init_db

# Page configuration
st.set_page_config(
    page_title="CodeRefine — Smarter Code. Cleaner Future.",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database
init_db()

# Global CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Syne:wght@400;600;800&display=swap');

* {
    font-family: 'Syne', sans-serif !important;
}
code, pre, .stTextArea textarea {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stSidebarNav"] { display: none; }

body, .stApp {
    background: #080B14 !important;
    color: #E2E8F0 !important;
}
</style>
""", unsafe_allow_html=True)

# Redirect logic
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("pages/1_Login.py")
else:
    st.switch_page("pages/3_Dashboard.py")
