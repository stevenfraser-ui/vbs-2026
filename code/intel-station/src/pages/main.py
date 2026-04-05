"""Main interface — split-screen Chat Terminal + Data Viewer."""

import random
import time

import streamlit as st

from src.config.phases import get_phase_title, get_total_phases
from src.services import database_service as db
from src.services import game_service
from src.services import progress_service
from src.services.intel_service import load_intel


# ── Session state defaults ────────────────────────────────────────────

def _init_session_state(user):
    """Initialize game session state, reconstructing from DB if needed."""
    if "visited_nodes" not in st.session_state:
        visited = game_service.reconstruct_visited_nodes(user.id)
        st.session_state["visited_nodes"] = visited

        if visited:
            current = game_service.reconstruct_current_node(visited)
            if current:
                node = game_service.get_node(current)
                st.session_state["current_node"] = current
                st.session_state["current_response"] = node.get("response", "")
                st.session_state["current_questions"] = game_service.get_available_questions(
                    current, visited
                )
            else:
                st.session_state["current_node"] = None
                st.session_state["current_response"] = None
                st.session_state["current_questions"] = game_service.get_start_questions()
        else:
            st.session_state["current_node"] = None
            st.session_state["current_response"] = None
            st.session_state["current_questions"] = game_service.get_start_questions()

    if "animating" not in st.session_state:
        st.session_state["animating"] = False
    if "parent_node" not in st.session_state:
        st.session_state["parent_node"] = None


# ── Main render ───────────────────────────────────────────────────────

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

    _init_session_state(user)
    progress = progress_service.get_progress_info(user)

    _render_top_bar(user, progress)

    if progress["mission_complete"]:
        _render_mission_complete(user, progress)
        return

    chat_col, viewer_col = st.columns([4, 6], gap="medium")

    with chat_col:
        _render_chat_terminal(user, progress)

    with viewer_col:
        _render_data_viewer(user)


# ── Top Bar ───────────────────────────────────────────────────────────

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
        st.progress(
            progress["progress_pct"],
            text=f"Phase {progress['current_phase']} of {progress['total_phases']}",
        )

    with cols[2]:
        if st.button("Logout", key="logout_btn", type="tertiary"):
            # Clear game state on logout
            for key in ["visited_nodes", "current_node", "current_response",
                        "current_questions", "animating", "parent_node"]:
                st.session_state.pop(key, None)
            st.session_state.pop("user_id", None)
            st.session_state.page = "login"
            st.rerun()


# ── Chat Terminal ─────────────────────────────────────────────────────

def _render_chat_terminal(user, progress):
    """Render the left panel — question-driven chat terminal."""
    st.markdown(
        "<div style='font-family:monospace; color:#00d4ff; font-size:14px; "
        "border-bottom:1px solid #1a3a4a; padding-bottom:8px; "
        "margin-bottom:12px;'>"
        "CHAT TERMINAL</div>",
        unsafe_allow_html=True,
    )

    # Response display area
    response_area = st.container(height=400)
    with response_area:
        if st.session_state.get("animating"):
            _run_typewriter_animation()
        elif st.session_state.get("current_response"):
            # Show the last response (static, post-animation)
            node = game_service.get_node(st.session_state["current_node"])
            _render_static_response(st.session_state["current_response"], node)
        else:
            # Welcome state — no response yet
            st.markdown(
                "<div style='color:#667; font-family:monospace; "
                "text-align:center; padding:40px 20px;'>"
                "IMF Central AI online.<br>"
                f"Welcome, Agent {user.name}.<br><br>"
                "Select a prompt below to begin your investigation."
                "</div>",
                unsafe_allow_html=True,
            )

    # Question buttons
    if not st.session_state.get("animating"):
        _render_question_buttons(user, progress)


def _run_typewriter_animation():
    """Run character-by-character typewriter animation."""
    text = st.session_state.get("animation_text", "")
    placeholder = st.empty()

    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(
            f"<div style='font-family:monospace; color:#e0e0e0; "
            f"font-size:14px; padding:20px; line-height:1.6;'>"
            f"{displayed}<span style='color:#00d4ff;'>█</span></div>",
            unsafe_allow_html=True,
        )
        time.sleep(random.uniform(0.015, 0.050))

    # Final render without cursor
    placeholder.markdown(
        f"<div style='font-family:monospace; color:#e0e0e0; "
        f"font-size:14px; padding:20px; line-height:1.6;'>"
        f"{displayed}</div>",
        unsafe_allow_html=True,
    )

    # Check for dead-end message
    node = game_service.get_node(st.session_state.get("current_node", ""))
    if node and node.get("dead_end") and node.get("dead_end_message"):
        time.sleep(0.5)
        dead_end_placeholder = st.empty()
        de_text = f"\n⚠ {node['dead_end_message']}"
        de_displayed = ""
        for char in de_text:
            de_displayed += char
            dead_end_placeholder.markdown(
                f"<div style='font-family:monospace; color:#ff6b35; "
                f"font-size:13px; padding:10px 20px; "
                f"border-left:3px solid #ff6b35;'>"
                f"{de_displayed}<span style='color:#ff6b35;'>█</span></div>",
                unsafe_allow_html=True,
            )
            time.sleep(random.uniform(0.015, 0.050))
        dead_end_placeholder.markdown(
            f"<div style='font-family:monospace; color:#ff6b35; "
            f"font-size:13px; padding:10px 20px; "
            f"border-left:3px solid #ff6b35;'>"
            f"{de_displayed}</div>",
            unsafe_allow_html=True,
        )

    # Animation done
    st.session_state["animating"] = False
    time.sleep(0.3)
    st.rerun()


def _render_static_response(response_text, node=None):
    """Render the response text without animation (post-animation or reload)."""
    st.markdown(
        f"<div style='font-family:monospace; color:#e0e0e0; "
        f"font-size:14px; padding:20px; line-height:1.6;'>"
        f"{response_text}</div>",
        unsafe_allow_html=True,
    )

    if node and node.get("dead_end") and node.get("dead_end_message"):
        st.markdown(
            f"<div style='font-family:monospace; color:#ff6b35; "
            f"font-size:13px; padding:10px 20px; "
            f"border-left:3px solid #ff6b35;'>"
            f"⚠ {node['dead_end_message']}</div>",
            unsafe_allow_html=True,
        )


def _render_question_buttons(user, progress):
    """Render the clickable question prompts."""
    questions = st.session_state.get("current_questions", [])
    current_node = st.session_state.get("current_node")

    # For dead-end nodes, show parent's unvisited questions
    if current_node:
        node = game_service.get_node(current_node)
        if node and node.get("dead_end"):
            questions = game_service.get_parent_unvisited_questions(
                current_node, st.session_state.get("visited_nodes", set())
            )

    # Check if phase conclusion should be injected
    conclusion_id = progress.get("phase_conclusion_available")
    if conclusion_id and conclusion_id not in st.session_state.get("visited_nodes", set()):
        # Add conclusion as a special button if not already in the list
        if conclusion_id not in questions:
            questions = list(questions) + [conclusion_id]

    if not questions:
        st.markdown(
            "<div style='font-family:monospace; color:#667; font-size:12px; "
            "text-align:center; padding:8px;'>"
            "Analyzing available intelligence streams...</div>",
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        "<div style='font-family:monospace; color:#667; font-size:11px; "
        "margin-top:8px;'>AVAILABLE INQUIRIES:</div>",
        unsafe_allow_html=True,
    )

    for q_id in questions:
        q_node = game_service.get_node(q_id)
        if not q_node:
            continue

        is_conclusion = q_node.get("phase_complete") is not None
        btn_type = "primary" if is_conclusion else "secondary"

        if st.button(
            q_node["label"],
            key=f"q_{q_id}",
            use_container_width=True,
            type=btn_type,
        ):
            _handle_question_click(user, q_id)


def _handle_question_click(user, node_id: str):
    """Process a question click — record intel, update state, trigger animation."""
    node = game_service.process_question(user.id, node_id, user.current_phase)
    if not node:
        return

    visited = st.session_state.get("visited_nodes", set())
    parent = st.session_state.get("current_node")
    visited.add(node_id)

    # Handle phase completion
    if node.get("phase_complete"):
        progress_service.advance_phase(user)

    # Update session state
    st.session_state["visited_nodes"] = visited
    st.session_state["parent_node"] = parent
    st.session_state["current_node"] = node_id
    st.session_state["current_response"] = node.get("response", "")
    st.session_state["current_questions"] = game_service.get_available_questions(
        node_id, visited
    )
    st.session_state["animation_text"] = node.get("response", "")
    st.session_state["animating"] = True
    st.rerun()


# ── Data Viewer ───────────────────────────────────────────────────────

_TYPE_ICONS = {
    "field_report": "📋",
    "intercepted_comm": "📡",
    "informant_tip": "🕵️",
    "surveillance": "🛰️",
    "hostile_org": "⚠️",
    "tech_analysis": "🔬",
    "codename_registry": "🔑",
    "transfer_log": "🔄",
    "facility_report": "🏗️",
    "energy_analysis": "⚡",
    "corporate_intel": "🏢",
    "shell_company": "🪆",
    "insider_report": "🤫",
    "procurement_record": "💰",
    "security_spec": "🛡️",
}

_TYPE_LABELS = {
    "field_report": "Field Reports",
    "intercepted_comm": "Intercepted Communications",
    "informant_tip": "Informant Tips",
    "surveillance": "Surveillance Reports",
    "hostile_org": "Hostile Organizations",
    "tech_analysis": "Technical Analysis",
    "codename_registry": "Code-Name Registry",
    "transfer_log": "Transfer Logs",
    "facility_report": "Facility Reports",
    "energy_analysis": "Energy Analysis",
    "corporate_intel": "Corporate Intelligence",
    "shell_company": "Shell Companies",
    "insider_report": "Insider Reports",
    "procurement_record": "Procurement Records",
    "security_spec": "Security Specifications",
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
            "Select a prompt to begin scanning."
            "</div>",
            unsafe_allow_html=True,
        )
        return

    # Group by phase, then by type
    by_phase: dict[int, list[dict]] = {}
    for doc in accessed_docs:
        phase = doc["phase"]
        by_phase.setdefault(phase, []).append(doc)

    total_phases = get_total_phases()
    for phase_num in range(1, total_phases + 1):
        if phase_num > user.current_phase:
            break

        phase_docs = by_phase.get(phase_num, [])
        phase_title = get_phase_title(phase_num)
        is_current = phase_num == user.current_phase
        is_completed = phase_num < user.current_phase

        header_suffix = ""
        if is_completed:
            header_suffix = " ✓"

        with st.expander(
            f"Phase {phase_num}: {phase_title}{header_suffix} ({len(phase_docs)} files)",
            expanded=is_current,
        ):
            if not phase_docs:
                st.markdown(
                    "<div style='color:#445; font-family:monospace; padding:20px; "
                    "text-align:center;'>No intel recovered for this phase yet.</div>",
                    unsafe_allow_html=True,
                )
                continue

            _render_phase_documents(phase_docs)


def _render_phase_documents(docs: list[dict]):
    """Render documents for a single phase, grouped by type."""
    by_type: dict[str, list[dict]] = {}
    for doc in docs:
        cat = doc["category"]
        by_type.setdefault(cat, []).append(doc)

    for doc_type, type_docs in by_type.items():
        icon = _TYPE_ICONS.get(doc_type, "📄")
        label = _TYPE_LABELS.get(doc_type, doc_type.replace("_", " ").title())

        st.markdown(
            f"<div style='font-family:monospace; color:#00d4ff; font-size:13px; "
            f"margin-top:12px; margin-bottom:6px; padding:4px 8px; "
            f"background:#0a1a2a; border-left:3px solid #00d4ff; "
            f"border-radius:4px;'>"
            f"{icon} {label} ({len(type_docs)})"
            f"</div>",
            unsafe_allow_html=True,
        )

        for doc in type_docs:
            _render_intel_document(doc)


def _render_intel_document(doc: dict):
    """Render a single intel document with its content."""
    filename = doc["doc_filename"]
    phase = doc["phase"]
    intel_path = f"intel/phase{phase}/{filename}"

    intel_data = load_intel(intel_path)

    if intel_data:
        fm = intel_data["frontmatter"]
        body = intel_data["body"]
        display_title = fm.get("title", filename)
        classification = fm.get("classification", "")
        reference = fm.get("reference", "")

        header = f"{display_title}"
        if classification:
            header += f" [{classification}]"
        if reference:
            header += f" — {reference}"
    else:
        display_title = filename.replace("_", " ").replace("-", " ").replace(".md", "").title()
        header = display_title
        body = "*Intel file unavailable — data may have been relocated.*"

    with st.expander(header, expanded=False):
        if intel_data:
            fm = intel_data["frontmatter"]
            _render_classification_badge(fm.get("classification", ""))
            if fm.get("summary"):
                st.markdown(
                    f"<div style='font-family:monospace; color:#aaa; "
                    f"font-size:12px; padding:4px 0 8px 0; "
                    f"border-bottom:1px solid #1a3a4a; margin-bottom:8px;'>"
                    f"📎 {fm['summary']}</div>",
                    unsafe_allow_html=True,
                )
        st.markdown(body)


def _render_classification_badge(classification: str):
    """Render a colored classification badge."""
    colors = {
        "TOP SECRET": ("#ff4444", "#3a1111"),
        "TOP SECRET — EYES ONLY": ("#ff2222", "#4a0a0a"),
        "SECRET": ("#ff8800", "#3a2200"),
        "CONFIDENTIAL": ("#ffcc00", "#3a3300"),
    }
    fg, bg = colors.get(classification, ("#888888", "#222222"))
    st.markdown(
        f"<span style='font-family:monospace; font-size:11px; "
        f"color:{fg}; background:{bg}; padding:2px 8px; "
        f"border-radius:3px; border:1px solid {fg};'>"
        f"🔒 {classification}</span>",
        unsafe_allow_html=True,
    )


# ── Mission Complete ──────────────────────────────────────────────────

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

    st.markdown("---")
    st.markdown(
        "<h3 style='font-family:monospace; color:#ff6b35;'>"
        "RECOVERED INTEL ARCHIVE</h3>",
        unsafe_allow_html=True,
    )
    _render_data_viewer(user)
