"""Intel Station — Streamlit entry point."""

import streamlit as st

from src.config.settings import LOG_LEVEL
from src.config.logging_config import setup_logging

# Configure logging before any other app imports
setup_logging(log_level=LOG_LEVEL)

from src.services.database_service import init_db
from src.pages.login import render_login
from src.pages.main import render_main
from src.pages.admin import render_admin

# --- Page Config ---
st.set_page_config(
    page_title="IMF Intelligence Terminal",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Hide Streamlit default elements for full-screen feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Dark spy HQ theme */
    .stApp {
        background-color: #0a0e17;
        color: #c0c8d8;
        font-family: 'Courier New', monospace;
    }

    /* Chat input styling */
    .stChatInput > div {
        background-color: #0d1520 !important;
        border: 1px solid #1a3a4a !important;
    }

    /* Chat messages */
    .stChatMessage {
        background-color: #0d1520 !important;
        border: 1px solid #1a2a3a !important;
        border-radius: 8px !important;
    }

    /* Buttons */
    .stButton > button {
        font-family: 'Courier New', monospace;
        font-weight: bold;
        border: 1px solid #1a3a4a;
        background-color: #0d1520;
        color: #00d4ff;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 18px;
    }

    .stButton > button:hover {
        background-color: #1a2a3a;
        border-color: #00d4ff;
        color: #ffffff;
    }

    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background-color: #00d4ff;
        color: #0a0e17;
        border: none;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #00a8cc;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #00d4ff;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #0d1520 !important;
        border: 1px solid #1a3a4a !important;
        color: #00d4ff !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #0d1520;
        border: 1px solid #1a3a4a;
        border-radius: 4px 4px 0 0;
        color: #667;
        font-family: 'Courier New', monospace;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1a2a3a !important;
        color: #00d4ff !important;
        border-color: #00d4ff !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00d4ff;
        font-family: 'Courier New', monospace;
    }

    /* Containers / columns */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    /* Text input */
    .stTextInput > div > div > input {
        background-color: #0d1520 !important;
        color: #00d4ff !important;
        border: 1px solid #1a3a4a !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Number input */
    .stNumberInput > div > div > input {
        background-color: #0d1520 !important;
        color: #00d4ff !important;
        border: 1px solid #1a3a4a !important;
    }

    /* Text area */
    .stTextArea > div > div > textarea {
        background-color: #0d1520 !important;
        color: #00d4ff !important;
        border: 1px solid #1a3a4a !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Code blocks */
    .stCodeBlock {
        background-color: #0d1520 !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0e17;
    }
    ::-webkit-scrollbar-thumb {
        background: #1a3a4a;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Database ---
init_db()

# --- Session State Defaults ---
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- Routing ---
page = st.session_state.page

# Allow URL query param for admin access
query_params = st.query_params
if query_params.get("page") == "admin" and page == "login":
    st.session_state.page = "admin"
    page = "admin"

if page == "login":
    render_login()
elif page == "main":
    render_main()
elif page == "admin":
    render_admin()
else:
    st.session_state.page = "login"
    render_login()
