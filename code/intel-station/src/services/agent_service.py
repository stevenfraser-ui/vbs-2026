"""AI Agent service using Strands Agents SDK with Ollama.

Integrates:
- AgentSkills plugin for phase-gated SKILL.md instructions
- query_intel custom tool for knowledge-base searches
- Document access tracking for progression
"""

import logging
import re
import time
from dataclasses import dataclass, field

from strands import Agent
from strands.models.ollama import OllamaModel
from strands import AgentSkills, Skill

from src.config.settings import OLLAMA_URL, OLLAMA_MODEL, SKILLS_DIR
from src.config.system_prompt import build_system_prompt
from src.models.user import User
from src.services import database_service as db

logger = logging.getLogger(__name__)


# --- Agent creation ---

@dataclass
class AgentResponse:
    """Parsed response from the AI agent."""
    intel_summary: str
    stage_completed: bool
    intel_uncovered: list[str]
    recommended_prompts: list[str]


def _create_model() -> OllamaModel:
    """Create a configured Ollama model instance."""
    return OllamaModel(
        host=OLLAMA_URL,
        model_id=OLLAMA_MODEL,
        temperature=0.4,
        max_tokens=300,
    )

def _get_skills_dir_for_phase(phase: int) -> str:
    """Get the skills directory path string for a given phase number."""
    skills_dir = SKILLS_DIR.with_name(f"phase{phase}-skills")
    if skills_dir.exists() and skills_dir.is_dir():
        return str(skills_dir)
    else:
        logger.warning("Skills directory not found for phase %d: %s", phase, skills_dir)
        return None

def _create_agent(user: User) -> Agent:
    """Create a Strands Agent with Skills, tools, and system prompt."""

    system_prompt = build_system_prompt(
        agent_name=user.name,
        agent_age=user.age,
        current_phase=user.current_phase,
        current_stage=user.current_stage,
    )

    # Load skills for current phase
    phase_skills = _get_skills_dir_for_phase(user.current_phase)

    model = _create_model()

    # Add skills plugin if we have skills
    if phase_skills:
        skills_plugin = AgentSkills(skills=phase_skills)
        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            plugins=[skills_plugin],
            callback_handler=None,
        )
    else:
        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            callback_handler=None,
        )

    logger.info(
        "Agent created for user_id=%d phase=%d stage=%d model=%s skills=%d",
        user.id, user.current_phase, user.current_stage,
        OLLAMA_MODEL, len(phase_skills),
    )
    return agent


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
    logger.info(
        "Agent response requested: user_id=%d phase=%d stage=%d "
        "msg_len=%d failed_attempts=%d",
        user.id, user.current_phase, user.current_stage,
        len(user_message), failed_attempts,
    )

    agent = _create_agent(user)

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
        t0 = time.monotonic()
        result = agent(full_message)
        elapsed = time.monotonic() - t0
        raw_text = str(result)
        response = parse_response(raw_text)

        logger.info(
            "Agent response received: user_id=%d elapsed=%.2fs "
            "resp_len=%d stage_completed=%s docs_accessed=%d",
            user.id, elapsed, len(response.intel_summary),
            response.stage_completed, len(response.intel_uncovered),
        )
        logger.debug(
            "Agent raw response (user_id=%d): should_advance=%s docs=%s",
            user.id, response.should_advance, response.accessed_docs,
        )

        # Record document accesses
        if response.accessed_docs:
            _record_doc_access(
                user_id=user.id,
                filenames=response.accessed_docs,
                phase=user.current_phase,
                stage=user.current_stage,
            )

        return response
    except Exception as e:
        logger.error(
            "Agent call failed: user_id=%d phase=%d — %s",
            user.id, user.current_phase, e,
            exc_info=True,
        )
        return AgentResponse(
            chat_text=(
                "Systems experiencing interference, Agent. "
                "Try your question again."
            ),
            stage_completed=False,
        )
    finally:
        clear_user_context()
        logger.debug("User context cleared: user_id=%d", user.id)
