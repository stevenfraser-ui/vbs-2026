"""AI Agent service using Strands Agents SDK with Ollama.

Integrates:
- AgentSkills plugin for phase-gated SKILL.md instructions
- query_intel custom tool for knowledge-base searches
- Document access tracking for progression
"""

import logging
import re
from dataclasses import dataclass, field

from strands import Agent
from strands.models.ollama import OllamaModel
from strands import AgentSkills, Skill

from src.config.settings import OLLAMA_URL, OLLAMA_MODEL, SKILLS_PATH
from src.config.phases import (
    PHASES, TOTAL_SUBSTEPS, compute_progress,
)
from src.config.system_prompt import build_system_prompt
from src.services import database_service as db
from src.tools.query_intel import query_intel, get_document, CATEGORY_LABELS
from src.models.user import User

logger = logging.getLogger(__name__)

ADVANCE_MARKER = "[ADVANCE]"

# --- Skill loading ---

_SKILLS_CACHE: dict[str, Skill] = {}


def _load_skills() -> dict[str, Skill]:
    """Load phase skills from the skills/ directory. Cached."""
    global _SKILLS_CACHE
    if _SKILLS_CACHE:
        return _SKILLS_CACHE

    skill_dirs = {
        1: "phase-1-investigation",
        2: "phase-2-location",
        3: "phase-3-security",
    }

    for phase_num, dir_name in skill_dirs.items():
        skill_dir = SKILLS_PATH / dir_name
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            skill = Skill.from_file(str(skill_dir))
            _SKILLS_CACHE[phase_num] = skill
            logger.info("Loaded skill for phase %d from %s", phase_num, skill_dir)
        else:
            logger.warning("Skill file not found: %s", skill_md)

    return _SKILLS_CACHE


def _get_skills_for_phase(phase: int) -> list[Skill]:
    """Get the skills that should be active for the given phase.

    Returns the current phase skill. Previous phase skills are NOT included
    to keep context focused.
    """
    all_skills = _load_skills()
    active = []
    if phase in all_skills:
        active.append(all_skills[phase])
    return active


# --- Document tracking wrapper ---

def _make_tracking_query_intel(user_id: int, phase: int, substep: int):
    """Create a wrapper around query_intel that tracks document access.

    We wrap the tool so that every time the AI calls query_intel, we parse
    the returned document filenames and record them as accessed.
    """
    original_fn = query_intel.tool_func if hasattr(query_intel, 'tool_func') else None

    def _extract_doc_filenames(result_text: str) -> list[str]:
        """Extract document filenames from query_intel results."""
        # Pattern matches "Document: filename.md" lines in the output
        return re.findall(r"Document:\s*(\S+\.md)", result_text)

    # We use query_intel directly — the agent will call it as a tool.
    # After the agent response, we parse which docs were referenced.
    # The tracking happens in get_agent_response after the agent call.
    return query_intel


# --- Agent creation ---

@dataclass
class AgentResponse:
    """Parsed response from the AI agent."""
    chat_text: str
    should_advance: bool
    accessed_docs: list[str] = field(default_factory=list)


def _build_discovered_summary(phase: int, substep: int) -> str:
    """Build a summary of what the agent has discovered so far."""
    lines = []
    for p_num in sorted(PHASES.keys()):
        p_data = PHASES[p_num]
        for s_num in sorted(p_data["substeps"].keys()):
            if p_num < phase or (p_num == phase and s_num < substep):
                lines.append(
                    f"- Phase {p_num} Step {s_num}: {p_data['substeps'][s_num]['description']}"
                )
    return "\n".join(lines) if lines else "Nothing discovered yet — this is the start of the mission."


def _build_accessed_docs_summary(user_id: int) -> str:
    """Build a summary of which KB documents this agent has accessed."""
    docs = db.get_accessed_documents(user_id)
    if not docs:
        return "No intelligence documents accessed yet."

    by_category = {}
    for doc in docs:
        cat = doc["category"]
        label = CATEGORY_LABELS.get(cat, cat)
        by_category.setdefault(label, []).append(doc["doc_filename"])

    lines = []
    for cat_label, filenames in by_category.items():
        lines.append(f"- {cat_label}: {', '.join(filenames)}")
    return "\n".join(lines)


def _create_model() -> OllamaModel:
    """Create a configured Ollama model instance."""
    return OllamaModel(
        host=OLLAMA_URL,
        model_id=OLLAMA_MODEL,
        temperature=0.4,
        max_tokens=300,
    )


def _create_agent(user: User, failed_attempts: int = 0) -> Agent:
    """Create a Strands Agent with Skills, tools, and system prompt."""
    phase_data = PHASES.get(user.current_phase, {})

    system_prompt = build_system_prompt(
        agent_name=user.name,
        agent_age=user.age,
        current_phase=user.current_phase,
        phase_title=phase_data.get("title", "Unknown"),
        progress_completed=compute_progress(user.current_phase, user.current_substep),
        total_substeps=TOTAL_SUBSTEPS,
        discovered_summary=_build_discovered_summary(
            user.current_phase, user.current_substep
        ),
        accessed_docs_summary=_build_accessed_docs_summary(user.id),
        failed_attempts=failed_attempts,
    )

    # Load skills for current phase
    phase_skills = _get_skills_for_phase(user.current_phase)

    model = _create_model()

    # Build tools list — query_intel is always available
    tools = [query_intel]

    # Add skills plugin if we have skills
    if phase_skills:
        skills_plugin = AgentSkills(skills=phase_skills)
        return Agent(
            model=model,
            system_prompt=system_prompt,
            tools=tools,
            plugins=[skills_plugin],
            callback_handler=None,
        )

    return Agent(
        model=model,
        system_prompt=system_prompt,
        tools=tools,
        callback_handler=None,
    )


def _build_chat_context(chat_history: list[dict]) -> str:
    """Build recent chat context to include with the user message."""
    if not chat_history:
        return ""
    recent = chat_history[-6:]
    lines = []
    for msg in recent:
        role = "Agent" if msg["role"] == "user" else "IMF Central AI"
        lines.append(f"{role}: {msg['message']}")
    return "\n".join(lines)


def _extract_accessed_docs(raw_text: str) -> list[str]:
    """Extract document filenames referenced in the agent response or tool output."""
    # Matches filenames like field_report_001.md, intercepted_comm_002.md, etc.
    pattern = r'\b([a-z][a-z0-9_]+\.md)\b'
    filenames = re.findall(pattern, raw_text, re.IGNORECASE)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for fn in filenames:
        fn_lower = fn.lower()
        if fn_lower not in seen:
            seen.add(fn_lower)
            unique.append(fn)
    return unique


def _record_doc_access(user_id: int, filenames: list[str],
                       phase: int, substep: int) -> None:
    """Record accessed documents in the database."""
    for fn in filenames:
        doc = get_document(fn)
        if doc:
            db.record_document_access(
                user_id=user_id,
                doc_filename=fn,
                category=doc["category"],
                phase=phase,
                substep=substep,
            )


def parse_response(raw_text: str) -> AgentResponse:
    """Parse the AI response, extracting the advance marker and doc references."""
    should_advance = ADVANCE_MARKER in raw_text
    chat_text = raw_text.replace(ADVANCE_MARKER, "").strip()
    accessed_docs = _extract_accessed_docs(raw_text)
    return AgentResponse(
        chat_text=chat_text,
        should_advance=should_advance,
        accessed_docs=accessed_docs,
    )


def get_agent_response(
    user: User,
    user_message: str,
    chat_history: list[dict],
    failed_attempts: int = 0,
) -> AgentResponse:
    """
    Send a message to the AI agent and get a parsed response.

    Handles:
    - Building the agent with current phase skill + query_intel tool
    - Parsing the response for [ADVANCE] markers
    - Extracting and recording KB document accesses
    """
    agent = _create_agent(user, failed_attempts)

    # Build the full message with context
    context = _build_chat_context(chat_history)
    if context:
        full_message = (
            f"Previous conversation:\n{context}\n\n"
            f"Agent's new message: {user_message}"
        )
    else:
        full_message = user_message

    try:
        result = agent(full_message)
        raw_text = str(result)
        response = parse_response(raw_text)

        # Record document accesses
        if response.accessed_docs:
            _record_doc_access(
                user_id=user.id,
                filenames=response.accessed_docs,
                phase=user.current_phase,
                substep=user.current_substep,
            )

        return response
    except Exception as e:
        logger.error("Agent call failed: %s", e)
        return AgentResponse(
            chat_text=(
                "Systems experiencing interference, Agent. "
                "Try your question again."
            ),
            should_advance=False,
        )
