"""Main interface — split-screen Chat Terminal + Data Viewer."""

from pathlib import Path

import streamlit as st

from src.config.settings import PROJECT_ROOT
from src.config.phases import get_total_stages
from src.services import database_service as db
from src.services import progress_service
from src.services.agent_service import get_agent_response


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
        _render_data_viewer(user)


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
        total = get_total_stages()
        st.progress(
            progress["progress_pct"],
            text=f"Intel gathered: {progress['stages_completed']}/{total}",
        )

    with cols[2]:
        if st.button("Logout", key="logout_btn"):
            st.session_state.pop("user_id", None)
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
            st.markdown(
                "<div style='color:#667; font-family:monospace; "
                "text-align:center; padding:20px;'>"
                "IMF Central AI online.<br>"
                f"Welcome, Agent {user.name}.<br>"
                "Select a prompt below to begin your investigation."
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

            # Show recommended prompts from the last assistant message
            _render_recommended_prompts(user, chat_history)

    # Initial prompt buttons OR normal chat input
    is_initial = (
        not chat_history
        and user.current_phase == 1
        and user.current_stage == 1
    )

    if is_initial:
        _render_initial_prompts(user, chat_history)
    else:
        user_input = st.chat_input(
            "Ask IMF Central AI...",
            key="chat_input",
        )
        if user_input:
            _handle_user_message(user, user_input, chat_history)


def _render_initial_prompts(user, chat_history):
    """Show starter prompt buttons for brand-new agents."""
    st.markdown(
        "<div style='font-family:monospace; color:#667; font-size:13px; "
        "text-align:center; padding:8px 0;'>"
        "Choose your first inquiry:</div>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "What is the Light?",
            key="init_prompt_1",
            use_container_width=True,
            type="primary",
        ):
            _handle_user_message(user, "What is the Light?", chat_history)
    with col2:
        if st.button(
            "Who is the Architect?",
            key="init_prompt_2",
            use_container_width=True,
            type="primary",
        ):
            _handle_user_message(user, "Who is the Architect?", chat_history)


def _render_recommended_prompts(user, chat_history):
    """Show recommended prompts from the last assistant response as clickable buttons."""
    if not chat_history:
        return

    # Check session state for stored recommended prompts
    prompts = st.session_state.get("recommended_prompts", [])
    if not prompts:
        return

    st.markdown(
        "<div style='font-family:monospace; color:#667; font-size:11px; "
        "margin-top:8px;'>SUGGESTED INQUIRIES:</div>",
        unsafe_allow_html=True,
    )
    for i, prompt_text in enumerate(prompts[:3]):
        if st.button(
            prompt_text,
            key=f"rec_prompt_{i}",
            use_container_width=True,
        ):
            _handle_user_message(user, prompt_text, chat_history)


def _handle_user_message(user, message, chat_history):
    """Process a user's message through the AI agent."""
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
        )

    # Only persist messages if the agent succeeded
    db.add_chat_message(
        user_id=user.id,
        role="user",
        message=message,
        phase=user.current_phase,
        stage=user.current_stage,
    )

    # Save AI response
    db.add_chat_message(
        user_id=user.id,
        role="assistant",
        message=response.intel_summary,
        phase=user.current_phase,
        stage=user.current_stage,
    )

    # Store recommended prompts for UI display
    st.session_state["recommended_prompts"] = response.recommended_prompts

    # Handle advancement: primary check (LLM) or fallback (required docs)
    should_advance = response.stage_completed
    if not should_advance:
        # Fallback: check if required documents have all been accessed
        should_advance = progress_service.check_required_documents(user)

    if should_advance:
        progress_service.advance_user(user)

    st.rerun()


# --- Data Viewer ---

# Category display labels
_CATEGORY_LABELS = {
    "field_reports": "Field Reports",
    "intercepted_comms": "Intercepted Communications",
    "informant_tips": "Informant Tips",
    "surveillance": "Surveillance Reports",
    "hostile_orgs": "Hostile Organizations",
    "tech_analysis": "Technical Analysis",
    "codenames": "Code-Name Registry",
    "other": "Other Intel",
}

# Category icons for visual distinction
_CATEGORY_ICONS = {
    "field_reports": "📋",
    "intercepted_comms": "📡",
    "informant_tips": "🕵️",
    "surveillance": "🛰️",
    "hostile_orgs": "⚠️",
    "tech_analysis": "🔬",
    "codenames": "🔑",
    "other": "📄",
}


def _render_data_viewer(user):
    """Render the right panel — data viewer with uncovered intel documents."""
    st.markdown(
        "<div style='font-family:monospace; color:#ff6b35; font-size:14px; "
        "border-bottom:1px solid #3a2a1a; padding-bottom:8px; "
        "margin-bottom:12px;'>"
        "DATA VIEWER</div>",
        unsafe_allow_html=True,
    )

    accessed_docs = db.get_accessed_documents(user.id)

    if not accessed_docs:
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

    # Group documents by category
    by_category: dict[str, list[dict]] = {}
    for doc in accessed_docs:
        cat = doc["category"]
        by_category.setdefault(cat, []).append(doc)

    # Render each category
    for category, cat_docs in by_category.items():
        icon = _CATEGORY_ICONS.get(category, "📄")
        label = _CATEGORY_LABELS.get(category, category.replace("_", " ").title())

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
            doc_filename = doc["doc_filename"]
            display_name = Path(doc_filename).stem.replace("_", " ").replace("-", " ").title()

            # Read the actual markdown file from disk
            file_path = PROJECT_ROOT / doc_filename
            if file_path.exists():
                content = file_path.read_text(encoding="utf-8")
            else:
                content = "*Intel file unavailable — data may have been relocated.*"

            with st.expander(f"{icon} {display_name}", expanded=False):
                st.markdown(content)


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
    _render_data_viewer(user)
