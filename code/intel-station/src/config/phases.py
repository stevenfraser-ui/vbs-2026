"""
Phase and substep definitions for the Intel Station progression.

Phase 1 is exploration-driven — the agent queries the knowledge base and
discovers documents naturally through conversation.  Substep advancement is
triggered when the AI detects understanding ([ADVANCE] marker) AND the agent
has accessed the required documents for that substep.

Phases 2 and 3 use traditional static assets and AI guidance lives in the
corresponding SKILL.md files (not here).
"""

PHASES = {
    1: {
        "title": "What is The Light?",
        "description": "Discover the true nature of The Light by investigating the intelligence knowledge base.",
        "substeps": {
            1: {
                "description": "Initial inquiry — explore field reports and rumors about The Light",
                "hint_concepts": [
                    "the light", "what is it", "mission", "device",
                    "what are we looking for", "briefing", "tell me",
                ],
                "assets_to_unlock": [],
                "required_documents": [],
            },
            2: {
                "description": "Red herrings encountered — conflicting intel about weapon/gemstone theories",
                "hint_concepts": [
                    "weapon", "gemstone", "rumors", "informant",
                    "what people say", "dangerous", "different stories",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "field_report_001.md",
                    "field_report_002.md",
                ],
            },
            3: {
                "description": "Who created The Light? Discover 'the designer'",
                "hint_concepts": [
                    "who made it", "who created", "designer", "creator",
                    "architect", "who built", "genius", "ghost",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "informant_tip_003.md",
                ],
            },
            4: {
                "description": "Code name discovery — LOGOS identified",
                "hint_concepts": [
                    "code name", "name", "logos", "unknown-7",
                    "identity", "who is", "registry",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "tech_analysis_003.md",
                    "codename_registry_decrypted.md",
                ],
            },
            5: {
                "description": "LOGOS intercepted messages found — key clues about digital nature",
                "hint_concepts": [
                    "logos messages", "intercepted", "communications",
                    "what did logos say", "transmissions",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "intercepted_comm_002.md",
                    "intercepted_comm_004.md",
                ],
            },
            6: {
                "description": "Analyzing LOGOS messages — understanding 'compiling', 'code', 'RUN'",
                "hint_concepts": [
                    "compiling", "code", "digital", "run",
                    "what does it mean", "programming", "source code",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "intercepted_comm_005.md",
                ],
            },
            7: {
                "description": "Contradicting the red herrings — weapon/gemstone theories debunked",
                "hint_concepts": [
                    "not a weapon", "cobalt was wrong", "not a gemstone",
                    "digital", "not physical", "debunked", "wrong",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "informant_tip_004.md",
                ],
            },
            8: {
                "description": "Discovery confirmed: The Light is software",
                "hint_concepts": [
                    "software", "program", "computer program",
                    "app", "digital", "not physical", "not a device",
                    "it runs", "you run it", "code",
                ],
                "assets_to_unlock": [
                    "phase1/phase1_complete.png",
                ],
                "required_documents": [],
            },
        },
    },
    2: {
        "title": "Where is it?",
        "description": "Locate where The Light software is stored.",
        "substeps": {
            1: {
                "description": "Location query initiated",
                "hint_concepts": [
                    "where", "location", "stored", "hidden",
                    "kept", "find it", "server", "computer",
                ],
                "assets_to_unlock": [
                    "phase2/world_map_scan.png",
                ],
                "required_documents": [],
            },
            2: {
                "description": "Energy signature narrowed to building",
                "hint_concepts": [
                    "energy", "signature", "power", "building",
                    "what is that", "zoom in", "where exactly",
                    "that spot", "big",
                ],
                "assets_to_unlock": [
                    "phase2/satellite_image.png",
                ],
                "required_documents": [],
            },
            3: {
                "description": "Blueprint unlocked — Server Vault discovered",
                "hint_concepts": [
                    "inside", "building", "blueprint", "layout",
                    "closer", "what is in there", "vault",
                    "map", "rooms",
                ],
                "assets_to_unlock": [
                    "phase2/vault_blueprint.png",
                    "phase2/phase2_complete.png",
                ],
                "required_documents": [],
            },
        },
    },
    3: {
        "title": "How is it protected?",
        "description": "Discover the vault's security systems.",
        "substeps": {
            1: {
                "description": "Security inquiry initiated",
                "hint_concepts": [
                    "security", "protected", "guards", "alarm",
                    "defense", "how do we get in", "locked",
                    "safe", "traps",
                ],
                "assets_to_unlock": [
                    "phase3/encrypted_protocol.png",
                ],
                "required_documents": [],
            },
            2: {
                "description": "Security protocol fully decrypted",
                "hint_concepts": [
                    "decrypt", "floor", "pressure", "grid",
                    "how does it work", "what kind of security",
                    "keep going", "more", "finish",
                ],
                "assets_to_unlock": [
                    "phase3/floor_grid_diagram.png",
                    "phase3/floor_grid_video.mp4",
                ],
                "required_documents": [],
            },
            3: {
                "description": "All intel gathered — Mission Ready",
                "hint_concepts": [
                    "ready", "got it", "understand", "mission",
                    "go", "next", "plan", "summary", "what now",
                    "let's do this",
                ],
                "assets_to_unlock": [
                    "phase3/phase3_complete.png",
                ],
                "required_documents": [],
            },
        },
    },
}

# Total number of substeps across all phases
TOTAL_SUBSTEPS = sum(
    len(phase["substeps"]) for phase in PHASES.values()
)


def get_substep(phase: int, substep: int) -> dict | None:
    """Get a specific substep definition."""
    phase_data = PHASES.get(phase)
    if not phase_data:
        return None
    return phase_data["substeps"].get(substep)


def get_phase_substep_count(phase: int) -> int:
    """Get the number of substeps in a phase."""
    phase_data = PHASES.get(phase)
    if not phase_data:
        return 0
    return len(phase_data["substeps"])


def get_all_asset_keys() -> list[str]:
    """Get a flat list of all asset keys across all phases."""
    assets = []
    for phase in PHASES.values():
        for substep in phase["substeps"].values():
            assets.extend(substep["assets_to_unlock"])
    return assets


def compute_progress(phase: int, substep: int) -> int:
    """Compute the total number of substeps completed (0-indexed from start)."""
    completed = 0
    for p_num in sorted(PHASES.keys()):
        if p_num < phase:
            completed += len(PHASES[p_num]["substeps"])
        elif p_num == phase:
            completed += substep - 1
            break
    return completed
