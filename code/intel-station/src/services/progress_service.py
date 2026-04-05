"""Progress service — handles phase advancement based on critical intel."""

import logging

from src.config.phases import get_phase_title, get_total_phases
from src.services import database_service as db
from src.services import game_service
from src.models.user import User

logger = logging.getLogger(__name__)


def advance_phase(user: User) -> User | None:
    """Advance the user to the next phase, or mark mission complete."""
    total = get_total_phases()

    if user.current_phase < total:
        new_phase = user.current_phase + 1
        updated = db.update_user(user.id, current_phase=new_phase)
        logger.info("Phase advanced: user_id=%d -> phase=%d", user.id, new_phase)
    else:
        updated = db.update_user(user.id, completed=True)
        logger.info("Mission complete: user_id=%d", user.id)

    return updated


def get_progress_info(user: User) -> dict:
    """Get a summary dict of the user's progress for display."""
    total_phases = get_total_phases()
    accessed_docs = db.get_accessed_documents(user.id)
    completion_node = game_service.check_phase_completion_available(
        user.id, user.current_phase
    )

    return {
        "current_phase": user.current_phase,
        "phase_title": get_phase_title(user.current_phase),
        "total_phases": total_phases,
        "progress_pct": (user.current_phase - 1) / total_phases if total_phases > 0 else 0,
        "mission_complete": user.completed,
        "accessed_docs": accessed_docs,
        "phase_conclusion_available": completion_node,
    }
