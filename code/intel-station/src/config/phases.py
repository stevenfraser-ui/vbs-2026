"""Phase configuration for the Intel Station app.

Progression is now phase-only, gated by
critical intel collection (see game_graph.py for CRITICAL_INTEL).
"""

PHASE_CONFIG = {
    1: {
        "title": "Investigation",
        "description": "Discover what The Light is and who created it.",
        "conclusion": "The Light isn't a thing at all. It's Software!",
    },
    2: {
        "title": "Location",
        "description": "Locate where The Light is stored.",
        "conclusion": "The Light is stored in a secret facility called The Vault!",
    },
    3: {
        "title": "Security",
        "description": "Discover The Vault's security measures.",
        "conclusion": "The Vault is protected by a rotating password pressure-sensitive floor grid and silent alarm!",
    },
}


def get_phase_title(phase: int) -> str:
    """Return the title for a phase, or empty string if unknown."""
    return PHASE_CONFIG.get(phase, {}).get("title", "")


def get_phase_description(phase: int) -> str:
    """Return the description for a phase, or empty string if unknown."""
    return PHASE_CONFIG.get(phase, {}).get("description", "")


def get_phase_conclusion(phase: int) -> str:
    """Return the conclusion text for a phase."""
    return PHASE_CONFIG.get(phase, {}).get("conclusion", "")


def get_total_phases() -> int:
    """Return the total number of phases."""
    return len(PHASE_CONFIG)
