"""Progress service — handles phase/substep advancement and asset unlocking.

Advancement requires BOTH:
1. The AI including [ADVANCE] in its response
2. The agent having accessed all required_documents for the current substep
"""

import logging
from dataclasses import dataclass

from src.config.phases import (
    PHASES, get_substep, get_phase_substep_count, compute_progress, TOTAL_SUBSTEPS,
)
from src.services import database_service as db
from src.models.user import User

logger = logging.getLogger(__name__)


@dataclass
class AdvanceResult:
    """Result of attempting to advance the user's progress."""
    advanced: bool
    new_phase: int
    new_substep: int
    newly_unlocked_assets: list[str]
    phase_completed: bool
    mission_complete: bool
    user: User
    blocked_reason: str = ""


def check_required_documents(user: User) -> tuple[bool, list[str]]:
    """Check if the user has accessed all required documents for their current substep.

    Returns (all_met, missing_docs).
    """
    substep_data = get_substep(user.current_phase, user.current_substep)
    if not substep_data:
        return True, []

    required = substep_data.get("required_documents", [])
    if not required:
        return True, []

    accessed = db.get_accessed_doc_filenames(user.id)
    missing = [doc for doc in required if doc not in accessed]
    if missing:
        logger.debug(
            "Doc requirement check: user_id=%d phase=%d substep=%d missing=%s",
            user.id, user.current_phase, user.current_substep, missing,
        )
    return len(missing) == 0, missing


def advance_user(user: User) -> AdvanceResult:
    """
    Advance the user to the next substep, unlocking any associated assets.

    Checks required_documents before allowing advancement. If docs are
    missing, advancement is blocked and the reason is returned.
    """
    current_substep_data = get_substep(user.current_phase, user.current_substep)
    if not current_substep_data:
        return AdvanceResult(
            advanced=False,
            new_phase=user.current_phase,
            new_substep=user.current_substep,
            newly_unlocked_assets=[],
            phase_completed=False,
            mission_complete=user.completed,
            user=user,
        )

    # Check required documents
    docs_met, missing_docs = check_required_documents(user)
    if not docs_met:
        logger.info(
            "Advancement blocked: user_id=%d phase=%d substep=%d missing=%s",
            user.id, user.current_phase, user.current_substep, missing_docs,
        )
        return AdvanceResult(
            advanced=False,
            new_phase=user.current_phase,
            new_substep=user.current_substep,
            newly_unlocked_assets=[],
            phase_completed=False,
            mission_complete=user.completed,
            user=user,
            blocked_reason=f"Missing required documents: {', '.join(missing_docs)}",
        )

    # Unlock assets for the current substep
    newly_unlocked = []
    for asset_key in current_substep_data.get("assets_to_unlock", []):
        db.unlock_asset(
            user_id=user.id,
            asset_key=asset_key,
            phase=user.current_phase,
            substep=user.current_substep,
        )
        newly_unlocked.append(asset_key)
        logger.info(
            "Asset unlocked: user_id=%d asset=%r phase=%d substep=%d",
            user.id, asset_key, user.current_phase, user.current_substep,
        )

    # Determine next position
    phase_count = get_phase_substep_count(user.current_phase)
    phase_completed = False
    mission_complete = False

    if user.current_substep < phase_count:
        # Move to next substep within the same phase
        new_phase = user.current_phase
        new_substep = user.current_substep + 1
    elif user.current_phase < max(PHASES.keys()):
        # Move to the first substep of the next phase
        new_phase = user.current_phase + 1
        new_substep = 1
        phase_completed = True
    else:
        # Mission complete
        new_phase = user.current_phase
        new_substep = user.current_substep
        phase_completed = True
        mission_complete = True

    # Update the database
    updated_user = db.update_user(
        user.id,
        current_phase=new_phase,
        current_substep=new_substep,
        completed=mission_complete,
    )

    if mission_complete:
        logger.info("Mission complete: user_id=%d", user.id)
    elif phase_completed:
        logger.info(
            "Phase completed: user_id=%d completed_phase=%d -> phase=%d substep=%d",
            user.id, user.current_phase, new_phase, new_substep,
        )
    else:
        logger.info(
            "Substep advanced: user_id=%d phase=%d substep=%d -> substep=%d",
            user.id, new_phase, user.current_substep, new_substep,
        )

    return AdvanceResult(
        advanced=True,
        new_phase=new_phase,
        new_substep=new_substep,
        newly_unlocked_assets=newly_unlocked,
        phase_completed=phase_completed,
        mission_complete=mission_complete,
        user=updated_user,
    )


def get_progress_info(user: User) -> dict:
    """Get a summary dict of the user's progress for display."""
    completed = compute_progress(user.current_phase, user.current_substep)
    phase_data = PHASES.get(user.current_phase, {})
    unlocked = db.get_unlocked_assets(user.id)
    unlocked_keys = [a.asset_key for a in unlocked]
    accessed_docs = db.get_accessed_documents(user.id)

    return {
        "current_phase": user.current_phase,
        "current_substep": user.current_substep,
        "phase_title": phase_data.get("title", ""),
        "phase_description": phase_data.get("description", ""),
        "steps_completed": completed,
        "total_steps": TOTAL_SUBSTEPS,
        "progress_pct": completed / TOTAL_SUBSTEPS if TOTAL_SUBSTEPS > 0 else 0,
        "mission_complete": user.completed,
        "unlocked_asset_keys": unlocked_keys,
        "accessed_docs": accessed_docs,
    }
