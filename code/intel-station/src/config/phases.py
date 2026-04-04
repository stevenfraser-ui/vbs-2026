"""Phase and stage configuration for the Intel Station app.

Each phase has a title and a dict of stages. Each stage lists the
required_documents that must be accessed before the stage is considered
complete (used as a fallback when the LLM does not return
stage_completed=true).
"""

PHASE_CONFIG = {
    1: {
        "title": "Investigation",
        "description": "Discover what The Light is and who created it.",
        "stages": {
            1: {
                "required_documents": [
                    "phase1-skills/stage-1/references/field_report_003-dustline.md",
                    "phase1-skills/stage-1/references/hostile_org_001-meridian.md",
                ],
            },
            2: {
                "required_documents": [
                    "phase1-skills/stage-2/references/field_report_004-meridian.md",
                    "phase1-skills/stage-2/references/surveillance_001.md",
                ],
            },
            3: {
                "required_documents": [
                    "phase1-skills/stage-3/references/intercepted_comm_005.md",
                    "phase1-skills/stage-3/references/surveillance_003.md",
                ],
            },
            4: {
                "required_documents": [
                    "phase1-skills/stage-4/references/tech_analysis_003.md",
                    "phase1-skills/stage-4/references/codename_registry_decrypted.md",
                ],
            },
        },
    },
    2: {
        "title": "Location",
        "description": "Locate where The Light is stored.",
        "stages": {},  # placeholder — not yet built
    },
    3: {
        "title": "Security",
        "description": "Discover The Vault's security measures.",
        "stages": {},  # placeholder — not yet built
    },
}


def get_phase_title(phase: int) -> str:
    """Return the title for a phase, or empty string if unknown."""
    return PHASE_CONFIG.get(phase, {}).get("title", "")


def get_phase_description(phase: int) -> str:
    """Return the description for a phase, or empty string if unknown."""
    return PHASE_CONFIG.get(phase, {}).get("description", "")


def get_stage_count(phase: int) -> int:
    """Return the number of stages in a phase."""
    phase_data = PHASE_CONFIG.get(phase)
    if not phase_data:
        return 0
    return len(phase_data["stages"])


def get_stage_data(phase: int, stage: int) -> dict | None:
    """Return the stage dict for a given phase/stage, or None."""
    phase_data = PHASE_CONFIG.get(phase)
    if not phase_data:
        return None
    return phase_data["stages"].get(stage)


def get_required_documents(phase: int, stage: int) -> list[str]:
    """Return the list of required document paths for a phase/stage."""
    stage_data = get_stage_data(phase, stage)
    if not stage_data:
        return []
    return stage_data.get("required_documents", [])


def get_total_stages() -> int:
    """Return the total number of stages across all phases."""
    return sum(len(p["stages"]) for p in PHASE_CONFIG.values())


def compute_progress(current_phase: int, current_stage: int) -> int:
    """Return the number of stages completed so far (0-based).

    Stages in earlier phases are counted in full.  The current stage is
    not counted because it is still in progress.
    """
    completed = 0
    for phase_num in sorted(PHASE_CONFIG.keys()):
        if phase_num < current_phase:
            completed += len(PHASE_CONFIG[phase_num]["stages"])
        elif phase_num == current_phase:
            completed += current_stage - 1
            break
    return completed
