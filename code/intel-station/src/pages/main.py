"""Main interface — split-screen Chat Terminal + Data Viewer."""

import streamlit as st

from src.config.phases import PHASES, TOTAL_SUBSTEPS
from src.services import database_service as db
from src.services import progress_service
from src.services import asset_service
from src.services.agent_service import get_agent_response
from src.tools.query_intel import get_document, CATEGORY_LABELS
from src.utils.audio import play_unlock_chime, play_phase_complete


def render_main():
    """Render the main split-screen interface."""
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.session_state.page = "login"
        st.rerun()
        return

    user = db.get_user_by_id(user_id)
    if not user:
        st.session_state.page = "login"
        st.rerun()
        return

    # Initialize session state
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0

    # Get progress info
    progress = progress_service.get_progress_info(user)

    # Top bar
    _render_top_bar(user, progress)

    # Check for mission complete
    if progress["mission_complete"]:
        _render_mission_complete(user, progress)
        return

    # Split-screen layout
    chat_col, viewer_col = st.columns([4, 6], gap="medium")

    with chat_col:
        _render_chat_terminal(user, progress)

    with viewer_col:
        _render_data_viewer(progress)


def _render_top_bar(user, progress):
    """Render the top status bar."""
    cols = st.columns([1, 3, 1])

    with cols[0]:
        st.image("assets/imf_logo.svg", width=60)

    with cols[1]:
        st.markdown(
            f"<div style='font-family:monospace; color:#00d4ff;'>"
            f"<b>AGENT {user.name.upper()}</b> &nbsp;|&nbsp; "
            f"Phase {progress['current_phase']}: {progress['phase_title']}"
            f"</div>",
            unsafe_allow_html=True,
        )
        # Progress bar
        st.progress(
            progress["progress_pct"],
            text=f"Intel gathered: {progress['steps_completed']}/{progress['total_steps']}",
        )

    with cols[2]:
        if st.button("Logout", key="logout_btn"):
            for key in ["user_id", "failed_attempts"]:
                st.session_state.pop(key, None)
            st.session_state.page = "login"
            st.rerun()


def _render_chat_terminal(user, progress):
    """Render the left panel — chat interface."""
    st.markdown(
        "<div style='font-family:monospace; color:#00d4ff; font-size:14px; "
        "border-bottom:1px solid #1a3a4a; padding-bottom:8px; "
        "margin-bottom:12px;'>"
        "CHAT TERMINAL</div>",
        unsafe_allow_html=True,
    )

    # Load chat history from DB
    chat_history = db.get_chat_history(user.id)

    # Display chat messages in a container with fixed height
    chat_container = st.container(height=400)
    with chat_container:
        if not chat_history:
            # Welcome message
            st.markdown(
                "<div style='color:#667; font-family:monospace; "
                "text-align:center; padding:20px;'>"
                "IMF Central AI online.<br>"
                f"Welcome, Agent {user.name}.<br>"
                "What would you like to investigate?"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            for msg in chat_history:
                if msg.role == "user":
                    with st.chat_message("user", avatar="🕵️"):
                        st.write(msg.message)
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(msg.message)

    # Input area
    user_input = st.chat_input(
        "Ask IMF Central AI...",
        key="chat_input",
    )

    if user_input:
        _handle_user_message(user, user_input, chat_history)


def _handle_user_message(user, message, chat_history):
    """Process a user's message through the AI agent."""
    # Save user message
    db.add_chat_message(
        user_id=user.id,
        role="user",
        message=message,
        phase=user.current_phase,
        substep=user.current_substep,
    )

    # Build history for context
    history_dicts = [
        {"role": m.role, "message": m.message}
        for m in chat_history[-6:]
    ]

    # Get AI response
    with st.spinner("Scanning classified channels..."):
        response = get_agent_response(
            user=user,
            user_message=message,
            chat_history=history_dicts,
            failed_attempts=st.session_state.failed_attempts,
        )

    # Save AI response
    db.add_chat_message(
        user_id=user.id,
        role="assistant",
        message=response.chat_text,
        phase=user.current_phase,
        substep=user.current_substep,
    )

    # Handle advancement
    if response.should_advance:
        result = progress_service.advance_user(user)

        if result.advanced:
            st.session_state.failed_attempts = 0
            if result.newly_unlocked_assets:
                play_unlock_chime()
            if result.phase_completed:
                play_phase_complete()
        # If blocked (missing docs), the AI said [ADVANCE] but docs aren't
        # met yet — don't count as failed attempt, just continue
    else:
        st.session_state.failed_attempts += 1

    st.rerun()


def _render_data_viewer(progress):
    """Render the right panel — data viewer with KB documents and assets."""
    st.markdown(
        "<div style='font-family:monospace; color:#ff6b35; font-size:14px; "
        "border-bottom:1px solid #3a2a1a; padding-bottom:8px; "
        "margin-bottom:12px;'>"
        "DATA VIEWER</div>",
        unsafe_allow_html=True,
    )

    accessed_docs = progress.get("accessed_docs", [])
    unlocked_asset_keys = progress["unlocked_asset_keys"]

    # Get traditional assets for phases 2/3
    all_assets = asset_service.get_assets_for_display(unlocked_asset_keys)
    unlocked_assets = [a for a in all_assets if a["unlocked"]]

    has_kb_docs = len(accessed_docs) > 0
    has_assets = len(unlocked_assets) > 0

    if not has_kb_docs and not has_assets:
        st.markdown(
            "<div style='color:#334; font-family:monospace; text-align:center; "
            "padding:60px 20px;'>"
            "NO INTEL RECOVERED YET<br><br>"
            "<span style='font-size:48px;'>🔒</span><br><br>"
            "Ask IMF Central AI to begin scanning."
            "</div>",
            unsafe_allow_html=True,
        )
        return

    # Build tab list based on what's available
    tab_names = []
    tab_keys = []

    # Always show Intelligence Database tab if we have KB docs
    if has_kb_docs:
        tab_names.append("🗂️ Intelligence Database")
        tab_keys.append("kb")

    # Show phase tabs for traditional assets (P2/P3)
    for phase_num in sorted(PHASES.keys()):
        phase_unlocked = [a for a in unlocked_assets if a["phase"] == phase_num]
        if phase_unlocked:
            tab_names.append(f"Phase {phase_num}: {PHASES[phase_num]['title']}")
            tab_keys.append(f"phase_{phase_num}")

    if len(tab_names) == 0:
        return

    tabs = st.tabs(tab_names)

    for idx, key in enumerate(tab_keys):
        with tabs[idx]:
            if key == "kb":
                _render_kb_documents(accessed_docs)
            else:
                phase_num = int(key.split("_")[1])
                phase_assets = [a for a in unlocked_assets if a["phase"] == phase_num]
                for asset_data in phase_assets:
                    _render_asset(asset_data)


# Category icons for visual distinction
_CATEGORY_ICONS = {
    "field_reports": "📋",
    "intercepted_comms": "📡",
    "informant_tips": "🕵️",
    "surveillance": "🛰️",
    "hostile_orgs": "⚠️",
    "tech_analysis": "🔬",
    "codenames": "🔑",
    "transfer_logs": "🚚",
    "facility_reports": "🏢",
    "corporate_intel": "🏛️",
    "energy_analysis": "⚡",
    "procurement_records": "📦",
    "shell_companies": "🏗️",
    "security_specs": "🔐",
    "insider_reports": "🕶️",
}


def _render_kb_documents(accessed_docs: list[dict]):
    """Render accessed KB documents organized by category."""
    # Group by category
    by_category = {}
    for doc in accessed_docs:
        cat = doc["category"]
        by_category.setdefault(cat, []).append(doc)

    # Render each category
    for category, cat_docs in by_category.items():
        icon = _CATEGORY_ICONS.get(category, "📄")
        label = CATEGORY_LABELS.get(category, category)

        st.markdown(
            f"<div style='font-family:monospace; color:#00d4ff; font-size:13px; "
            f"margin-top:16px; margin-bottom:8px; padding:6px 10px; "
            f"background:#0a1a2a; border-left:3px solid #00d4ff; "
            f"border-radius:4px;'>"
            f"{icon} {label} ({len(cat_docs)} file{'s' if len(cat_docs) != 1 else ''})"
            f"</div>",
            unsafe_allow_html=True,
        )

        for doc in cat_docs:
            doc_data = get_document(doc["doc_filename"])
            if doc_data:
                with st.expander(
                    f"{icon} {doc['doc_filename']}",
                    expanded=False,
                ):
                    st.markdown(doc_data["content"])


def _render_asset(asset_data: dict):
    """Render a single unlocked asset in the Data Viewer."""
    asset_key = asset_data["key"]
    asset_type = asset_data["type"]
    label = asset_data["label"]

    with st.expander(f"📄 {label}", expanded=True):
        if asset_type == "text":
            content = asset_service.read_text_asset(asset_key)
            if content:
                st.code(content, language="markdown")
            else:
                st.warning("File contents unavailable.")

        elif asset_type == "image":
            path = asset_data.get("path")
            if path and path.exists() and path.stat().st_size > 0:
                st.image(str(path), caption=label)
            else:
                # Placeholder for empty image files
                st.markdown(
                    f"<div style='background:#1a2a3a; border:2px dashed #334; "
                    f"border-radius:8px; padding:40px; text-align:center; "
                    f"color:#556; font-family:monospace;'>"
                    f"[IMAGE PLACEHOLDER]<br>{label}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        elif asset_type == "video":
            path = asset_data.get("path")
            if path and path.exists() and path.stat().st_size > 0:
                st.video(str(path))
            else:
                st.markdown(
                    f"<div style='background:#1a2a3a; border:2px dashed #334; "
                    f"border-radius:8px; padding:40px; text-align:center; "
                    f"color:#556; font-family:monospace;'>"
                    f"[VIDEO PLACEHOLDER]<br>{label}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        elif asset_type == "audio":
            path = asset_data.get("path")
            if path and path.exists() and path.stat().st_size > 0:
                st.audio(str(path))
            else:
                st.markdown(
                    f"<div style='background:#1a2a3a; border:2px dashed #334; "
                    f"border-radius:8px; padding:40px; text-align:center; "
                    f"color:#556; font-family:monospace;'>"
                    f"[AUDIO PLACEHOLDER]<br>{label}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        else:
            st.info(f"Asset type '{asset_type}' — display not implemented.")


def _render_mission_complete(user, progress):
    """Render the mission complete summary screen."""
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(
            "<div style='text-align:center; padding:30px;'>"
            "<h1 style='color:#00ff88; font-family:monospace;'>"
            "MISSION INTEL COMPLETE</h1>"
            "<p style='color:#00d4ff; font-family:monospace; font-size:18px;'>"
            f"Outstanding work, Agent {user.name}!</p>"
            "</div>",
            unsafe_allow_html=True,
        )

        # Summary of discoveries
        st.markdown(
            "<div style='font-family:monospace; color:#aaa; font-size:16px; "
            "padding:20px; border:1px solid #1a3a4a; border-radius:10px; "
            "background:#0a1a2a;'>",
            unsafe_allow_html=True,
        )

        st.markdown("### Intelligence Summary")
        st.markdown(
            "**1. The Light** is advanced **SOFTWARE** — "
            "a powerful digital program created by **LOGOS** (The Architect)."
        )
        st.markdown(
            "**2. Location:** Stored in a **HIGH-SECURITY SERVER VAULT** — "
            "a heavily armored facility housing massive computer systems."
        )
        st.markdown(
            "**3. Protection:** The vault uses a **PRESSURE-SENSITIVE FLOOR GRID** — "
            "one wrong step triggers a silent alarm that relocates The Light."
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            "<p style='text-align:center; color:#ff6b35; "
            "font-family:monospace; font-size:20px; padding-top:30px;'>"
            "Report to your handler for operational orders."
            "</p>",
            unsafe_allow_html=True,
        )

    # Still show full data viewer below
    st.markdown("---")
    st.markdown(
        "<h3 style='font-family:monospace; color:#ff6b35;'>"
        "RECOVERED INTEL ARCHIVE</h3>",
        unsafe_allow_html=True,
    )
    _render_data_viewer(progress)
