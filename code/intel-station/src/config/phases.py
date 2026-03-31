"""
Phase and substep definitions for the Intel Station progression.

All three phases are exploration-driven — the agent queries the knowledge base
and discovers documents naturally through conversation.  Substep advancement is
triggered when the AI detects understanding ([ADVANCE] marker) AND the agent
has accessed the required documents for that substep.

AI guidance for each phase lives in the corresponding SKILL.md files under
skills/phase-{N}-*/SKILL.md.
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
        "description": "Locate where The Light software is stored by tracing its relocation trail.",
        "substeps": {
            1: {
                "description": "Initial location search — investigate where software this massive could be stored",
                "hint_concepts": [
                    "where", "location", "stored", "hidden",
                    "kept", "find it", "server", "computer",
                    "logos", "lab", "worked",
                ],
                "assets_to_unlock": [],
                "required_documents": [],
            },
            2: {
                "description": "Discover The Light has been relocated — it outgrew its first home",
                "hint_concepts": [
                    "moved", "relocated", "transfer", "too big",
                    "outgrew", "lab", "power", "capacity",
                    "where did it start", "first",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "transfer_log_001.md",
                    "facility_report_001.md",
                ],
            },
            3: {
                "description": "Trace the full relocation trail — exponential growth overwhelmed every facility",
                "hint_concepts": [
                    "growth", "exponential", "bigger", "more power",
                    "iron crest", "government", "next",
                    "where did it go", "military", "moved again",
                ],
                "assets_to_unlock": [
                    "phase2/world_map_scan.png",
                ],
                "required_documents": [
                    "facility_report_003.md",
                    "transfer_log_002.md",
                ],
            },
            4: {
                "description": "A private corporation was contracted — identify TITAN SYSTEMS",
                "hint_concepts": [
                    "corporation", "company", "contract", "private",
                    "titan", "who", "permanent", "housing",
                    "corporate", "built",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "intercepted_comm_006.md",
                    "corporate_intel_001.md",
                ],
            },
            5: {
                "description": "TITAN has many facilities — energy analysis reveals the classified one: The Vault",
                "hint_concepts": [
                    "which facility", "energy", "power", "classified",
                    "anomaly", "vault", "200 megawatts", "site",
                    "data center", "which one",
                ],
                "assets_to_unlock": [
                    "phase2/satellite_image.png",
                ],
                "required_documents": [
                    "corporate_intel_002.md",
                    "energy_analysis_002.md",
                ],
            },
            6: {
                "description": "The Vault confirmed — The Light is in the Server Core",
                "hint_concepts": [
                    "inside", "blueprint", "layout", "server core",
                    "confirmed", "vault", "found it",
                    "what is in there", "building",
                ],
                "assets_to_unlock": [
                    "phase2/vault_blueprint.png",
                    "phase2/phase2_complete.png",
                ],
                "required_documents": [
                    "facility_report_004.md",
                ],
            },
        },
    },
    3: {
        "title": "How is it protected?",
        "description": "Discover the vault's security systems by tracing shell company contracts.",
        "substeps": {
            1: {
                "description": "Begin security analysis — investigate how the vault is protected",
                "hint_concepts": [
                    "security", "protected", "guards", "alarm",
                    "defense", "how do we get in", "locked",
                    "safe", "traps", "get past",
                ],
                "assets_to_unlock": [
                    "phase3/encrypted_protocol.png",
                ],
                "required_documents": [],
            },
            2: {
                "description": "Discover compartmentalized security — Project AEGIS and shell companies",
                "hint_concepts": [
                    "aegis", "compartment", "contractor", "contract",
                    "who built", "shell company", "procurement",
                    "split", "secret", "separate",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "procurement_record_001.md",
                    "shell_company_004.md",
                ],
            },
            3: {
                "description": "Identify the three shell companies and their roles",
                "hint_concepts": [
                    "frost veil", "midnight sun", "boreal",
                    "three companies", "who are they", "contractors",
                    "reykjavik", "stockholm", "oslo", "floor",
                    "pathway", "alarm", "which companies",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "shell_company_001.md",
                    "shell_company_002.md",
                    "shell_company_003.md",
                ],
            },
            4: {
                "description": "Uncover the pressure-sensitive floor grid",
                "hint_concepts": [
                    "floor", "pressure", "grid", "tiles", "panels",
                    "step", "weight", "sensor", "frost veil",
                    "kinetic", "matrix", "8 by 8",
                ],
                "assets_to_unlock": [
                    "phase3/floor_grid_diagram.png",
                ],
                "required_documents": [
                    "security_spec_001.md",
                    "insider_report_001.md",
                ],
            },
            5: {
                "description": "Decode the changing pathway — safe path rotates on a timer",
                "hint_concepts": [
                    "path", "pattern", "changes", "timer", "rotate",
                    "password", "safe squares", "cryptographic",
                    "midnight sun", "terminal", "which tiles",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "security_spec_002.md",
                    "insider_report_003.md",
                ],
            },
            6: {
                "description": "Understand the silent alarm and relocation protocol",
                "hint_concepts": [
                    "alarm", "silent", "what happens", "wrong step",
                    "trigger", "relocate", "move", "transfer",
                    "boreal", "blast doors", "90 seconds",
                ],
                "assets_to_unlock": [],
                "required_documents": [
                    "security_spec_003.md",
                    "insider_report_002.md",
                ],
            },
            7: {
                "description": "All intel gathered — Mission Ready",
                "hint_concepts": [
                    "ready", "got it", "understand", "mission",
                    "go", "next", "plan", "summary", "what now",
                    "let's do this", "all three", "beat it",
                ],
                "assets_to_unlock": [
                    "phase3/floor_grid_video.mp4",
                    "phase3/phase3_complete.png",
                ],
                "required_documents": [
                    "security_spec_004.md",
                ],
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
