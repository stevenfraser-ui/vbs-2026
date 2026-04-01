"""Login page — 4-digit code keypad for agent authentication."""

import logging

import streamlit as st

from src.services import database_service as db

logger = logging.getLogger(__name__)


def render_login():
    """Render the agent login screen with a keypad interface."""

    # Center content
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        # IMF Logo
        st.image("assets/imf_logo.svg", width=200)
        st.markdown(
            "<h1 style='text-align:center; color:#00d4ff; "
            "font-family: monospace;'>AGENT LOGIN</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center; color:#667; "
            "font-family: monospace;'>Enter your 4-digit agent code</p>",
            unsafe_allow_html=True,
        )

        # Code input display
        if "login_code" not in st.session_state:
            st.session_state.login_code = ""
        if "login_error" not in st.session_state:
            st.session_state.login_error = ""

        code = st.session_state.login_code
        display_code = code.ljust(4, "·")
        st.markdown(
            f"<div style='text-align:center; font-size:48px; "
            f"letter-spacing:20px; font-family:monospace; color:#00d4ff; "
            f"padding:20px; border:2px solid #1a3a4a; border-radius:10px; "
            f"background:#0a1a2a;'>{display_code}</div>",
            unsafe_allow_html=True,
        )

        if st.session_state.login_error:
            st.error(st.session_state.login_error)

        # Keypad buttons
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # Number rows
        for row in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
            cols = st.columns(3)
            for i, num in enumerate(row):
                with cols[i]:
                    if st.button(
                        str(num),
                        key=f"key_{num}",
                        use_container_width=True,
                    ):
                        if len(st.session_state.login_code) < 4:
                            st.session_state.login_code += str(num)
                            st.session_state.login_error = ""
                            st.rerun()

        # Bottom row: Clear, 0, Enter
        cols = st.columns(3)
        with cols[0]:
            if st.button("CLR", key="key_clear", use_container_width=True):
                st.session_state.login_code = ""
                st.session_state.login_error = ""
                st.rerun()
        with cols[1]:
            if st.button("0", key="key_0", use_container_width=True):
                if len(st.session_state.login_code) < 4:
                    st.session_state.login_code += "0"
                    st.session_state.login_error = ""
                    st.rerun()
        with cols[2]:
            if st.button(
                "GO",
                key="key_enter",
                use_container_width=True,
                type="primary",
            ):
                _attempt_login()


def _attempt_login():
    """Validate the entered code and log in."""
    code = st.session_state.login_code

    if len(code) != 4:
        st.session_state.login_error = "Enter a full 4-digit code, Agent."
        st.rerun()
        return

    user = db.get_user_by_code(code)
    if user is None:
        logger.warning("Login failed: unknown agent code entered (len=%d)", len(code))
        st.session_state.login_error = (
            "Agent not recognized. Contact your handler."
        )
        st.session_state.login_code = ""
        st.rerun()
        return

    # Successful login
    logger.info("Login successful: user_id=%d name=%r age=%d", user.id, user.name, user.age)
    st.session_state.user_id = user.id
    st.session_state.page = "main"
    st.session_state.login_code = ""
    st.session_state.login_error = ""
    st.rerun()
