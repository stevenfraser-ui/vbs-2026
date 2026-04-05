"""Deterministic question→intel graph for the Intel Station game.

GAME_GRAPH defines every question node, its response text, the intel it
unlocks, and which follow-up questions it leads to.

CRITICAL_INTEL lists the intel files per phase that must ALL be unlocked
before the phase-conclusion prompt appears.
"""

# Phase 1 critical intel — the 6 key revelations that prove The Light is software
CRITICAL_INTEL = {
    1: [
        "intel/phase1/field_report_004-meridian.md",
        "intel/phase1/intercepted_comm_002.md",
        "intel/phase1/intercepted_comm_005.md",
        "intel/phase1/surveillance_003.md",
        "intel/phase1/tech_analysis_003.md",
        "intel/phase1/codename_registry_decrypted.md",
    ],
    # Phase 2 & 3: TBD when those graphs are authored
    2: [],
    3: [],
}

# Phase conclusion node IDs — mapped by phase number
PHASE_CONCLUSIONS = {
    1: "q_phase1_conclusion",
    2: "q_phase2_conclusion",
    3: "q_phase3_conclusion",
}

GAME_GRAPH = {
    # ── Start ──────────────────────────────────────────────────────────
    "start": {
        "questions": ["q_what_is_light", "q_who_is_architect"],
    },

    # ── Branch A: "What is the Light?" ─────────────────────────────────
    "q_what_is_light": {
        "label": "What is the Light?",
        "phase": 1,
        "response": (
            "Searching classified databases... Multiple field reports "
            "reference an asset code-named 'The Light.' Initial intelligence "
            "suggests it may be the most dangerous weapon ever created — but "
            "field operatives report conflicting evidence. A convoy intercepted "
            "during Operation SANDSTORM carried nothing but encrypted hard "
            "drives. No physical weapon was recovered."
        ),
        "intel": [
            "intel/phase1/field_report_001-sandstorm.md",
            "intel/phase1/informant_tip_001-cobalt.md",
        ],
        "questions": ["q_is_it_weapon", "q_convoy_contents", "q_who_wants_it"],
        "dead_end": False,
    },

    "q_is_it_weapon": {
        "label": "Could the Light be some kind of weapon?",
        "phase": 1,
        "response": (
            "Scanning weapons trafficking databases... A black market contact "
            "code-named VIPER insisted it's a weapon, but a tech broker who "
            "examined the evidence laughed at the suggestion. Meanwhile, the "
            "MERIDIAN GROUP — an arms brokering network — is actively hunting "
            "for a physical object. They seem confident they can find it, sell "
            "it, and ship it."
        ),
        "intel": [
            "intel/phase1/field_report_002-glacier.md",
            "intel/phase1/hostile_org_001-meridian.md",
        ],
        "questions": ["q_sparrow_lead", "q_meridian_plans", "q_arms_network"],
        "dead_end": False,
    },

    "q_convoy_contents": {
        "label": "Why were there only hard drives in the convoy?",
        "phase": 1,
        "response": (
            "Re-analyzing Operation SANDSTORM seizure manifest... The convoy "
            "carried encrypted hard drives and server components — no physical "
            "weapon, no prototype casing, no delivery system. A separate arms "
            "dealer contact stated plainly: 'It's not something you can hold. "
            "I don't know what it is, but everyone's looking in the wrong place.'"
        ),
        "intel": [
            "intel/phase1/field_report_003-dustline.md",
        ],
        "questions": ["q_cobalt_update", "q_facility_raid", "q_find_creator"],
        "dead_end": False,
    },

    "q_who_wants_it": {
        "label": "Who else is searching for the Light?",
        "phase": 1,
        "response": (
            "Pulling counter-intelligence profiles... Two additional hostile "
            "organizations are pursuing The Light. SHADOW COLLECTIVE — a "
            "network of elite hackers — appears to understand it's digital in "
            "nature. They're probing servers worldwide. And IRON VEIL — a "
            "state-sponsored operation — has been monitoring encrypted signals "
            "from someone they refer to only as 'the designer.'"
        ),
        "intel": [
            "intel/phase1/hostile_org_002-shadow.md",
            "intel/phase1/hostile_org_003-iron-veil.md",
        ],
        "questions": ["q_shadow_approach", "q_hostile_meeting", "q_find_creator"],
        "dead_end": False,
    },

    # ── Dead Ends ──────────────────────────────────────────────────────

    "q_sparrow_lead": {
        "label": "What about the glowing gemstone report?",
        "phase": 1,
        "response": (
            "Investigating SPARROW's claim of a glowing blue gemstone in "
            "South America... After extensive cross-referencing, this report "
            "has zero corroboration from any other source. SPARROW's "
            "reliability rating is LOW. Physical evidence, informant networks, "
            "and signal intelligence all contradict the existence of any such "
            "object. This lead is cold."
        ),
        "intel": [
            "intel/phase1/informant_tip_002-sparrow.md",
        ],
        "questions": [],
        "dead_end": True,
        "dead_end_message": (
            "SPARROW's gemstone claim is a dead end. No corroborating "
            "evidence found in any database."
        ),
    },

    "q_arms_network": {
        "label": "Do any arms dealers have real information?",
        "phase": 1,
        "response": (
            "Querying arms trafficking networks globally... Every weapons "
            "dealer and broker in our database is confused. None of them have "
            "seen anything matching The Light in any physical form. Multiple "
            "contacts independently confirmed: 'Everyone's chasing something, "
            "but nobody's holding anything.' The weapons trafficking community "
            "is chasing a ghost."
        ),
        "intel": [],
        "questions": [],
        "dead_end": True,
        "dead_end_message": (
            "Arms trafficking networks have no actionable leads. The Light "
            "doesn't appear in any weapons database."
        ),
    },

    "q_meridian_wrong": {
        "label": "Why can't MERIDIAN find the Light?",
        "phase": 1,
        "response": (
            "Analyzing MERIDIAN GROUP failures... Every physical recovery "
            "operation they've attempted has come up empty. Their auction "
            "plans, transportation logistics, and storage preparations are "
            "all built on a fundamental misunderstanding. They are searching "
            "for something that does not exist in the form they imagine. "
            "MERIDIAN will never find The Light this way."
        ),
        "intel": [],
        "questions": [],
        "dead_end": True,
        "dead_end_message": (
            "MERIDIAN's search is based on a false assumption. They will "
            "never find a physical object."
        ),
    },

    "q_shadow_approach": {
        "label": "How is SHADOW COLLECTIVE searching?",
        "phase": 1,
        "response": (
            "Monitoring SHADOW COLLECTIVE hacking operations... Their digital "
            "probing is scattered across hundreds of servers worldwide. While "
            "they correctly suspect The Light is digital, they have no idea "
            "where to look. Their attacks are broad, unfocused, and haven't "
            "gotten close to anything significant. They're as lost as the rest."
        ),
        "intel": [],
        "questions": [],
        "dead_end": True,
        "dead_end_message": (
            "SHADOW COLLECTIVE is searching blindly across global networks. "
            "No actionable intelligence from their operations."
        ),
    },

    "q_logos_dead_end": {
        "label": "Can we search other databases for LOGOS?",
        "phase": 1,
        "response": (
            "Running broad search across all allied intelligence databases, "
            "public records, and dark web archives... The code name LOGOS does "
            "not appear anywhere outside our own encrypted registry. It was "
            "deliberately chosen to avoid any existing records. Without "
            "decrypting our own registry, we cannot confirm the identity "
            "behind LOGOS."
        ),
        "intel": [],
        "questions": [],
        "dead_end": True,
        "dead_end_message": (
            "No external records found for code name LOGOS. Internal registry "
            "decryption is the only remaining path."
        ),
    },

    # ── Continuing Investigation ───────────────────────────────────────

    "q_meridian_plans": {
        "label": "What is MERIDIAN planning to do with the Light?",
        "phase": 1,
        "response": (
            "Intercepting MERIDIAN GROUP communications... They're organizing "
            "an auction for The Light. Their messages reference plans to "
            "'ship it, fly it, drive it out of the country.' They clearly "
            "believe The Light is a physical object that can be transported "
            "and sold to the highest bidder."
        ),
        "intel": [
            "intel/phase1/intercepted_comm_003.md",
        ],
        "questions": ["q_meridian_wrong", "q_cobalt_update", "q_facility_raid"],
        "dead_end": False,
    },

    "q_cobalt_update": {
        "label": "Has COBALT provided any corrections?",
        "phase": 1,
        "response": (
            "Checking informant network for updates... COBALT has sent an "
            "urgent correction to their earlier assessment. Direct quote: "
            "'I was wrong about the weapon part. I've been asking around more "
            "carefully. Whatever this thing is — it's never been in a box, "
            "never been on a shelf. It lives somewhere else entirely.' "
            "COBALT's reliability remains HIGH."
        ),
        "intel": [
            "intel/phase1/informant_tip_004-cobalt-2.md",
        ],
        "questions": ["q_digital_theory", "q_facility_raid", "q_find_creator"],
        "dead_end": False,
    },

    "q_facility_raid": {
        "label": "Have any facilities been connected to the Light?",
        "phase": 1,
        "response": (
            "Accessing Operation MERIDIAN raid report... A raid on a "
            "MERIDIAN-linked facility discovered something unexpected. No "
            "weapons — only rows of high-powered servers, fiber-optic cables, "
            "industrial cooling systems, and a terminal flashing 'TRANSFER "
            "COMPLETE.' Thermal satellite scans of three suspect sites show "
            "Site Gamma with a 47-megawatt energy anomaly consistent with "
            "massive computing infrastructure."
        ),
        "intel": [
            "intel/phase1/field_report_004-meridian.md",
            "intel/phase1/surveillance_001.md",
        ],
        "questions": ["q_digital_theory", "q_energy_signature", "q_intercepted_transmissions"],
        "dead_end": False,
    },

    "q_find_creator": {
        "label": "Can we find whoever created the Light?",
        "phase": 1,
        "response": (
            "Reviewing high-value source debriefings... A trusted contact "
            "from Operation CANOPY delivered this assessment: 'You're asking "
            "the wrong question. Stop asking what it is — find the person who "
            "made it, and everything else falls into place. People have been "
            "looking in the wrong direction from the start.'"
        ),
        "intel": [
            "intel/phase1/field_report_005-canopy.md",
        ],
        "questions": ["q_architect_signals", "q_hostile_meeting", "q_digital_theory"],
        "dead_end": False,
    },

    # ── Branch B: "Who is the Architect?" ──────────────────────────────

    "q_who_is_architect": {
        "label": "Who is the Architect?",
        "phase": 1,
        "response": (
            "Cross-referencing intelligence networks... We've intercepted a "
            "transmission from an unidentified source discussing a recently "
            "completed prototype. The message confirms testing is finished and "
            "the asset needs protection. Separately, an informant describes a "
            "ghost-like figure known only as 'The Architect' — someone "
            "brilliant enough to have built The Light from scratch. No "
            "confirmed identity."
        ),
        "intel": [
            "intel/phase1/intercepted_comm_001.md",
            "intel/phase1/informant_tip_003-ridge.md",
        ],
        "questions": ["q_architect_signals", "q_hostile_meeting", "q_find_creator"],
        "dead_end": False,
    },

    # ── Converging Investigation ───────────────────────────────────────

    "q_digital_theory": {
        "label": "Could the Light be something digital?",
        "phase": 1,
        "response": (
            "Analyzing intercepted transmissions from the signal source "
            "designated UNKNOWN-7... Two decoded message fragments are "
            "unmistakable. First: 'The blueprint is digital. It compiles. It "
            "runs. It thinks.' Second transmission, weeks later: 'It's "
            "something you RUN, not something you HOLD.' The source appears "
            "to be openly mocking those searching for a physical object."
        ),
        "intel": [
            "intel/phase1/intercepted_comm_002.md",
            "intel/phase1/intercepted_comm_004.md",
        ],
        "questions": ["q_source_code", "q_signal_analysis", "q_who_is_unknown7"],
        "dead_end": False,
    },

    "q_intercepted_transmissions": {
        "label": "What else have we intercepted?",
        "phase": 1,
        "response": (
            "Decoding latest UNKNOWN-7 transmission... This message uses "
            "explicit software terminology — 'source code,' 'programming,' "
            "'server deployment.' It states The Light is complete and ready "
            "for deployment but requires a specific type of server "
            "infrastructure to run. UNKNOWN-7 refers to needing 'the right "
            "server — nothing else will do.'"
        ),
        "intel": [
            "intel/phase1/intercepted_comm_005.md",
        ],
        "questions": ["q_signal_analysis", "q_who_is_unknown7", "q_energy_signature"],
        "dead_end": False,
    },

    "q_source_code": {
        "label": "The transmissions mention source code?",
        "phase": 1,
        "response": (
            "Decoding additional UNKNOWN-7 transmission... Confirmed — the "
            "latest intercept explicitly references 'source code,' "
            "'programming language,' and 'server deployment.' The Light is "
            "described as complete, compiled, and waiting to be deployed on "
            "sufficiently powerful hardware. This is software. Advanced, "
            "unprecedented software."
        ),
        "intel": [
            "intel/phase1/intercepted_comm_005.md",
        ],
        "questions": ["q_energy_signature", "q_who_is_unknown7", "q_hostile_meeting"],
        "dead_end": False,
    },

    "q_signal_analysis": {
        "label": "Can we trace UNKNOWN-7's signal?",
        "phase": 1,
        "response": (
            "Running signal traffic analysis... UNKNOWN-7 has transmitted 47 "
            "encrypted bursts over the monitoring period, with increasing "
            "frequency. The pattern is consistent with pre-deployment "
            "communications — someone preparing to launch an operation. Signal "
            "fingerprint analysis confirms this is a single individual, highly "
            "sophisticated, using custom encryption."
        ),
        "intel": [
            "intel/phase1/surveillance_002.md",
        ],
        "questions": ["q_who_is_unknown7", "q_energy_signature", "q_hostile_meeting"],
        "dead_end": False,
    },

    "q_architect_signals": {
        "label": "Can we trace the Architect's communications?",
        "phase": 1,
        "response": (
            "Correlating signal intelligence with UNKNOWN-7 designation... "
            "47 encrypted transmission bursts detected with increasing "
            "frequency — a pre-deployment pattern. Cross-referencing signal "
            "profiles with identity analysis: the transmission signature of "
            "UNKNOWN-7 matches the individual various assets call 'the "
            "designer.' They are the same person."
        ),
        "intel": [
            "intel/phase1/surveillance_002.md",
            "intel/phase1/tech_analysis_003.md",
        ],
        "questions": ["q_who_is_unknown7", "q_hostile_meeting", "q_energy_signature"],
        "dead_end": False,
    },

    "q_energy_signature": {
        "label": "What does the energy analysis tell us?",
        "phase": 1,
        "response": (
            "Running technical analysis on recovered energy data... The "
            "47-megawatt power signature is consistent with a massive "
            "computing operation — NOT weapons manufacturing or storage. "
            "Cooling infrastructure matches server farm requirements. "
            "Additionally, cryptographic analysis of intercepted data shows "
            "custom AES-variant encryption designed specifically for software "
            "deployment pipelines, not weapons systems."
        ),
        "intel": [
            "intel/phase1/tech_analysis_001.md",
            "intel/phase1/tech_analysis_002.md",
        ],
        "questions": ["q_who_is_unknown7", "q_who_is_logos", "q_source_code"],
        "dead_end": False,
    },

    "q_who_is_unknown7": {
        "label": "Who is UNKNOWN-7?",
        "phase": 1,
        "response": (
            "Cross-referencing all available intelligence on UNKNOWN-7... "
            "Running signal pattern matching, voice analysis, encryption "
            "fingerprinting, and transmission location data against all known "
            "profiles. Result: UNKNOWN-7 is confirmed to be the same "
            "individual IRON VEIL calls 'the designer.' Signal patterns, "
            "encryption methods, and behavioral profile are a verified match."
        ),
        "intel": [
            "intel/phase1/tech_analysis_003.md",
        ],
        "questions": ["q_who_is_logos", "q_hostile_meeting", "q_energy_signature"],
        "dead_end": False,
    },

    "q_hostile_meeting": {
        "label": "Have the hostile groups communicated with each other?",
        "phase": 1,
        "response": (
            "Accessing surveillance report... An observation team documented "
            "a clandestine meeting between representatives of MERIDIAN GROUP, "
            "SHADOW COLLECTIVE, and IRON VEIL. During the exchange, they "
            "referenced a code name none of our assets had encountered "
            "before: LOGOS. All three organizations believe LOGOS is the "
            "creator of The Light."
        ),
        "intel": [
            "intel/phase1/surveillance_003.md",
        ],
        "questions": ["q_who_is_logos", "q_who_is_unknown7", "q_source_code"],
        "dead_end": False,
    },

    "q_who_is_logos": {
        "label": "Who or what is LOGOS?",
        "phase": 1,
        "response": (
            "Searching IMF code-name registry... Partial records show known "
            "operatives and their identities, but several registry entries "
            "remain encrypted at Level 5 clearance. The name LOGOS appears in "
            "one of the locked entries. We do not yet have confirmation of who "
            "LOGOS is — but our cryptography division thinks they can break it."
        ),
        "intel": [
            "intel/phase1/codename_registry_partial.md",
        ],
        "questions": ["q_decrypt_registry", "q_logos_dead_end"],
        "dead_end": False,
    },

    "q_decrypt_registry": {
        "label": "Decrypt the registry entry for LOGOS",
        "phase": 1,
        "response": (
            "Applying Level 5 decryption protocols to locked registry "
            "entries.......... Decryption complete. CONFIRMED: LOGOS = "
            "UNKNOWN-7 = 'The Designer' = 'The Architect.' One individual. "
            "Creator of The Light. Identity verified across all signal, "
            "informant, and surveillance intelligence streams. The Architect "
            "has been positively identified."
        ),
        "intel": [
            "intel/phase1/codename_registry_decrypted.md",
        ],
        "questions": [],
        "dead_end": False,
    },

    # ── Phase 1 Conclusion ────────────────────────────────────────────
    "q_phase1_conclusion": {
        "label": "The Light isn't a thing at all. It's Software!",
        "phase": 1,
        "response": (
            "PHASE 1 ANALYSIS CONFIRMED. All intelligence converges on a "
            "single conclusion: The Light is not a physical object. It is "
            "advanced software — a powerful, unprecedented digital program "
            "created by an individual code-named LOGOS, also known as The "
            "Architect. The Light compiles, runs, and thinks. It requires "
            "massive computing infrastructure to operate. MERIDIAN, SHADOW, "
            "and IRON VEIL are all searching — but now we know what they're "
            "really after. New mission priority: Locate where The Light is "
            "being stored."
        ),
        "intel": [],
        "questions": [],  # Phase 2 starting questions — TBD
        "dead_end": False,
        "phase_complete": 1,
    },

    # ── Phase 2 & 3 placeholders ──────────────────────────────────────
    "q_phase2_conclusion": {
        "label": "The Light is stored in a secret facility called The Vault!",
        "phase": 2,
        "response": "PHASE 2 ANALYSIS CONFIRMED. [Placeholder — Phase 2 graph TBD]",
        "intel": [],
        "questions": [],
        "dead_end": False,
        "phase_complete": 2,
    },

    "q_phase3_conclusion": {
        "label": "The Vault is protected by a pressure grid, rotating pathway, and silent alarm!",
        "phase": 3,
        "response": "PHASE 3 ANALYSIS CONFIRMED. [Placeholder — Phase 3 graph TBD]",
        "intel": [],
        "questions": [],
        "dead_end": False,
        "phase_complete": 3,
    },
}
