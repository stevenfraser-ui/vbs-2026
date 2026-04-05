"""AI Agent service using Strands Agents SDK with Ollama.

Integrates:
- AgentSkills plugin for phase-gated SKILL.md instructions
- Document access tracking for progression
"""

import json
import logging
import re
import time
from pathlib import Path
from pydantic import BaseModel, Field

from strands import Agent
from strands.models.ollama import OllamaModel
from strands.models import BedrockModel
from strands import AgentSkills

from src.config.settings import OLLAMA_URL, OLLAMA_MODEL, PROJECT_ROOT
from src.config.system_prompt import build_system_prompt
from src.models.user import User
from src.services import database_service as db

logger = logging.getLogger(__name__)


# --- Data classes ---

class AgentResponse(BaseModel):
    """Parsed response from the AI agent."""
    intel_summary: str
    stage_completed: bool
    intel_uncovered: list[str] = Field(default_factory=list)
    recommended_prompts: list[str] = Field(default_factory=list)


# --- Category mapping ---

_CATEGORY_PREFIXES = {
    "intercepted_comm": "intercepted_comms",
    "field_report": "field_reports",
    "informant_tip": "informant_tips",
    "surveillance": "surveillance",
    "hostile_org": "hostile_orgs",
    "tech_analysis": "tech_analysis",
    "codename_registry": "codenames",
}


def _derive_category(filename: str) -> str:
    """Derive a category from a document filename prefix."""
    basename = Path(filename).stem  # e.g. "intercepted_comm_001"
    for prefix, category in _CATEGORY_PREFIXES.items():
        if basename.startswith(prefix):
            return category
    return "other"


# --- Agent creation ---

def _create_model() -> OllamaModel:
    """Create a configured Ollama model instance."""
    return OllamaModel(
        host=OLLAMA_URL,
        model_id=OLLAMA_MODEL,
        temperature=0,
        max_tokens=300,
    )

def _create_bedrock_model() -> BedrockModel:
    """Create a configured Bedrock model instance."""
    return BedrockModel(
        model_id='minimax.minimax-m2.5',
        temperature=0.8,
        max_tokens=300,
    )

def _get_skills_dir_for_phase(phase: int) -> str | None:
    """Get the skills directory path string for a given phase number."""
    skills_dir = PROJECT_ROOT / f"phase{phase}-skills/"
    if skills_dir.exists() and skills_dir.is_dir():
        return str(skills_dir)
    logger.warning("Skills directory not found for phase %d: %s", phase, skills_dir)
    return None


def _create_agent(user: User) -> Agent:
    """Create a Strands Agent with Skills and system prompt."""
    system_prompt = build_system_prompt(
        agent_name=user.name,
        agent_age=user.age,
        current_phase=user.current_phase,
        current_stage=user.current_stage,
    )

    phase_skills = _get_skills_dir_for_phase(user.current_phase)
    model = _create_model()
    #model = _create_bedrock_model()

    skills_plugin = AgentSkills(skills=phase_skills)
    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        plugins=[skills_plugin],
        #callback_handler=None,
        structured_output_model=AgentResponse,
    )

    logger.info(
        "Agent created for user_id=%d phase=%d stage=%d skills_dir=%s",
        user.id, user.current_phase, user.current_stage, phase_skills,
    )
    return agent


# --- Response parsing ---

_JSON_RETRY_PROMPT = (
    "Your previous response was not valid JSON. "
    "Please respond again using ONLY the exact JSON format specified "
    "in your instructions. No text outside the JSON block."
)


def _extract_json(raw_text: str) -> dict | None:
    """Try to extract a JSON object from raw LLM text.

    Handles markdown code fences and bare JSON.
    """
    # Try to find JSON inside ```json ... ``` or ``` ... ``` fences
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if fence_match:
        try:
            return json.loads(fence_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find a bare JSON object
    brace_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def _json_to_agent_response(data: dict) -> AgentResponse:
    """Convert a parsed JSON dict to an AgentResponse."""
    return AgentResponse(
        intel_summary=str(data.get("intel_summary", "")),
        stage_completed=bool(data.get("stage_completed", False)),
        intel_uncovered=list(data.get("intel_uncovered", [])),
        recommended_prompts=list(data.get("recommended_prompts", [])),
    )


def parse_response(raw_text: str, agent: Agent) -> AgentResponse:
    """Parse the LLM response JSON, retrying once on failure.

    1. Attempt to extract JSON from raw_text.
    2. If that fails, re-prompt the agent once asking for proper JSON.
    3. If the retry also fails, fall back to raw text as intel_summary.
    """
    # First attempt
    logger.info("parsing agent response, first attempt")
    data = _extract_json(raw_text)
    if data is not None:
        return _json_to_agent_response(data)

    logger.warning("First JSON parse failed, retrying with correction prompt")

    # Retry: re-prompt the agent
    try:
        retry_result = agent(_JSON_RETRY_PROMPT)
        retry_text = str(retry_result)
        data = _extract_json(retry_text)
        if data is not None:
            return _json_to_agent_response(data)
    except Exception as e:
        logger.warning("JSON retry agent call failed: %s", e)

    # Fallback: treat raw text as the summary
    logger.warning("Both JSON parse attempts failed, falling back to raw text")
    return AgentResponse(
        intel_summary=raw_text.strip(),
        stage_completed=False,
    )


# --- Document access recording ---

def _record_doc_access(
    user_id: int,
    filenames: list[str],
    phase: int,
    stage: int,
) -> None:
    """Record document accesses from intel_uncovered paths."""
    for filepath in filenames:
        category = _derive_category(filepath)
        db.record_document_access(
            user_id=user_id,
            doc_filename=filepath,
            category=category,
            phase=phase,
            stage=stage,
        )


# --- Chat context ---

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


# --- Main entry point ---

def get_agent_response(
    user: User,
    user_message: str,
    chat_history: list[dict],
) -> AgentResponse:
    """Send a message to the AI agent and get a parsed response."""
    logger.info(
        "Agent response requested: user_id=%d phase=%d stage=%d msg_len=%d",
        user.id, user.current_phase, user.current_stage, len(user_message),
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
        
        response = result.structured_output
        #response = parse_response(str(result), agent)

        logger.info(
            "Agent response received: user_id=%d elapsed=%.2fs "
            "resp_len=%d stage_completed=%s docs_accessed=%d",
            user.id, elapsed, len(response.intel_summary),
            response.stage_completed, len(response.intel_uncovered),
        )

        # Record document accesses
        if response.intel_uncovered:
            _record_doc_access(
                user_id=user.id,
                filenames=response.intel_uncovered,
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
            intel_summary=(
                "Systems experiencing interference, Agent. "
                "Try your question again."
            ),
            stage_completed=False,
        )
