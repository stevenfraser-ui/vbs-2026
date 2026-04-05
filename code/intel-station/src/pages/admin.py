"""Admin page — user management and progress reset."""

import logging
import sqlite3

import streamlit as st

from src.config.settings import ADMIN_PASSWORD
from src.config.phases import get_phase_title
from src.services import database_service as db

logger = logging.getLogger(__name__)


def render_admin():
    """Render the admin panel."""
    # Password gate
    if not st.session_state.get("admin_authenticated"):
        _render_password_gate()
        return

    st.markdown(
        "<h2 style='font-family:monospace; color:#ff6b35;'>"
        "IMF ADMIN CONSOLE</h2>",
        unsafe_allow_html=True,
    )

    tab_users, tab_bulk, tab_reset = st.tabs([
        "User Management", "Bulk Create", "Reset Controls",
    ])

    with tab_users:
        _render_user_management()

    with tab_bulk:
        _render_bulk_create()

    with tab_reset:
        _render_reset_controls()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()
    with col2:
        if st.button("Logout Admin"):
            st.session_state.admin_authenticated = False
            st.session_state.page = "login"
            st.rerun()


def _render_password_gate():
    """Simple password prompt for admin access."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h2 style='text-align:center; font-family:monospace; "
            "color:#ff6b35;'>ADMIN ACCESS</h2>",
            unsafe_allow_html=True,
        )
        password = st.text_input(
            "Enter admin password",
            type="password",
            key="admin_pwd_input",
        )
        if st.button("Authenticate", type="primary", use_container_width=True):
            if password == ADMIN_PASSWORD:
                logger.info("Admin authenticated")
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                logger.warning("Admin authentication failed")
                st.error("Access denied.")

        st.markdown("---")
        if st.button("Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()


def _render_user_management():
    """List, create, edit, and delete users."""
    st.subheader("All Agents")

    users = db.get_all_users()

    if not users:
        st.info("No agents registered. Create some below or use Bulk Create.")
    else:
        for user in users:
            phase_title = get_phase_title(user.current_phase)
            status = "COMPLETE" if user.completed else (
                f"Phase {user.current_phase}: {phase_title}"
            )

            with st.expander(
                f"Agent {user.name} — Code: {user.code} — {status}"
            ):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Phase", f"{user.current_phase}")
                with col2:
                    st.metric("Age", user.age)
                with col3:
                    st.metric("Code", user.code)

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(
                        "Reset Progress",
                        key=f"reset_{user.id}",
                        use_container_width=True,
                    ):
                        db.reset_user_progress(user.id)
                        logger.info("Admin reset progress for user_id=%d name=%r", user.id, user.name)
                        st.success(f"Progress reset for {user.name}.")
                        st.rerun()
                with col_b:
                    if st.button(
                        "Delete Agent",
                        key=f"delete_{user.id}",
                        use_container_width=True,
                    ):
                        logger.info("Admin deleted user_id=%d name=%r", user.id, user.name)
                        db.delete_user(user.id)
                        st.success(f"Agent {user.name} removed.")
                        st.rerun()

    # Create new user form
    st.markdown("---")
    st.subheader("Register New Agent")
    with st.form("create_user_form"):
        name = st.text_input("Agent Name")
        code = st.text_input("4-Digit Code", max_chars=4)
        age = st.number_input("Age", min_value=4, max_value=15, value=8)
        submitted = st.form_submit_button("Create Agent", type="primary")

        if submitted:
            if not name or not code:
                st.error("Name and code are required.")
            elif len(code) != 4 or not code.isdigit():
                st.error("Code must be exactly 4 digits.")
            else:
                try:
                    db.create_user(name=name, code=code, age=age)
                    st.success(f"Agent {name} registered with code {code}.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Code {code} is already taken.")


def _render_bulk_create():
    """Bulk create users from a text area (one per line: name,code,age)."""
    st.subheader("Bulk Agent Registration")
    st.markdown(
        "Enter one agent per line in the format: `name,code,age`\n\n"
        "Example:\n```\nSarah,1234,7\nJames,5678,10\nEmma,9012,5\n```"
    )

    bulk_input = st.text_area(
        "Agents (name,code,age — one per line)",
        height=200,
        key="bulk_input",
    )

    if st.button("Create All Agents", type="primary"):
        if not bulk_input.strip():
            st.error("Enter at least one agent.")
            return

        lines = bulk_input.strip().split("\n")
        created = 0
        errors = []

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                errors.append(f"Line {i}: Expected name,code,age — got '{line}'")
                continue

            name, code, age_str = parts
            if len(code) != 4 or not code.isdigit():
                errors.append(f"Line {i}: Code must be 4 digits — got '{code}'")
                continue

            try:
                age = int(age_str)
            except ValueError:
                errors.append(f"Line {i}: Age must be a number — got '{age_str}'")
                continue

            if age < 4 or age > 15:
                errors.append(f"Line {i}: Age must be 4-15 — got {age}")
                continue

            try:
                db.create_user(name=name, code=code, age=age)
                created += 1
            except sqlite3.IntegrityError:
                errors.append(f"Line {i}: Code {code} already exists")

        if created:
            st.success(f"Created {created} agent(s).")
        if errors:
            for err in errors:
                st.error(err)
        if created:
            st.rerun()


def _render_reset_controls():
    """Global reset controls."""
    st.subheader("Reset Controls")

    st.warning(
        "These actions affect ALL agents. Use with caution."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Reset all progress** — keeps agents but clears their "
                     "progress, chat history, and unlocked assets.")
        if st.button("Reset All Progress", type="primary"):
            st.session_state.confirm_reset_all = True

        if st.session_state.get("confirm_reset_all"):
            st.error("Are you sure? This cannot be undone.")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Yes, Reset All"):
                    db.reset_all_progress()
                    logger.info("Admin reset all progress")
                    st.session_state.confirm_reset_all = False
                    st.success("All progress has been reset.")
                    st.rerun()
            with col_b:
                if st.button("Cancel"):
                    st.session_state.confirm_reset_all = False
                    st.rerun()
