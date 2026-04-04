"""Progress service — handles phase/stage advancement.

Primary advancement: the LLM returns stage_completed=true.
Fallback: if the agent has accessed all required key documents for the
current stage, advance even if the LLM didn't flag completion.
"""

import logging
from dataclasses import dataclass

from src.config.phases import (
    PHASE_CONFIG,
    get_stage_count,
    get_total_stages,
    get_phase_title,
    get_required_documents,
    compute_progress,
)
from src.services import database_service as db
from src.models.user import User

logger = logging.getLogger(__name__)


@dataclass
class AdvanceResult:
    """Result of attempting to advance the user's progress."""
    advanced: bool
    new_phase: int
    new_stage: int
    phase_completed: bool
    mission_complete: bool
    user: User


def check_required_documents(user: User) -> bool:
    """Check if the user has accessed all required documents for their current stage.

    Returns True if all required documents have been accessed (or if there
    are no requirements for this stage).
    """
    required = get_required_documents(user.current_phase, user.current_stage)
    if not required:
        return False  # No requirements defined means we can't auto-advance

    accessed = db.get_accessed_doc_filenames(user.id)
    missing = [doc for doc in required if doc not in accessed]
    if missing:
        logger.debug(
            "Required docs check: user_id=%d phase=%d stage=%d missing=%s",
            user.id, user.current_phase, user.current_stage, missing,
        )
        return False
    return True


def advance_user(user: User) -> AdvanceResult:
    """Advance the user to the next stage.

    Increments the stage. If the stage exceeds the current phase's count,
    moves to the next phase. If all phases are done, marks the mission
    as complete.
    """
    current_phase = user.current_phase
    current_stage = user.current_stage
    stage_count = get_stage_count(current_phase)

    phase_completed = False
    mission_complete = False

    if current_stage < stage_count:
        new_phase = current_phase
        new_stage = current_stage + 1
    elif current_phase < max(PHASE_CONFIG.keys()):
        new_phase = current_phase + 1
        new_stage = 1
        phase_completed = True
    else:
        # All phases done
        new_phase = current_phase
        new_stage = current_stage
        phase_completed = True
        mission_complete = True

    updated_user = db.update_user(
        user.id,
        current_phase=new_phase,
        current_stage=new_stage,
        completed=mission_complete,
    )

    if mission_complete:
        logger.info("Mission complete: user_id=%d", user.id)
    elif phase_completed:
        logger.info(
            "Phase completed: user_id=%d phase=%d -> phase=%d stage=%d",
            user.id, current_phase, new_phase, new_stage,
        )
    else:
        logger.info(
            "Stage advanced: user_id=%d phase=%d stage=%d -> stage=%d",
            user.id, new_phase, current_stage, new_stage,
        )

    return AdvanceResult(
        advanced=True,
        new_phase=new_phase,
        new_stage=new_stage,
        phase_completed=phase_completed,
        mission_complete=mission_complete,
        user=updated_user,
    )


def get_progress_info(user: User) -> dict:
    """Get a summary dict of the user's progress for display."""
    completed = compute_progress(user.current_phase, user.current_stage)
    total = get_total_stages()
    accessed_docs = db.get_accessed_documents(user.id)

    return {
        "current_phase": user.current_phase,
        "current_stage": user.current_stage,
        "phase_title": get_phase_title(user.current_phase),
        "stages_completed": completed,
        "total_stages": total,
        "progress_pct": completed / total if total > 0 else 0,
        "mission_complete": user.completed,
        "accessed_docs": accessed_docs,
    }
