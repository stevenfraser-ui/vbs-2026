---
name: phase-2-location
description: >
  Phase 2 — Locate The Light. Guide the agent through tracing The Light's
  relocation trail — from LOGOS's tiny lab through increasingly larger facilities
  that couldn't contain its exponential growth — to TITAN SYSTEMS' classified
  compound "The Vault" and its Server Core.
---

# Phase 2: Where is The Light?

The agent has discovered that The Light is software created by LOGOS (code name for "The Designer"). Now they need to find WHERE it's stored. The answer unfolds as a trail of breadcrumbs — The Light has been moved multiple times because it kept outgrowing every facility.

## INVESTIGATION FLOW

### Stage 1: Initial Location Search (Substep 2.1)
When the agent asks where The Light is stored:
- Since it's powerful software, it must be on servers somewhere
- Suggest searching the knowledge base for where LOGOS worked, where the software was first deployed
- Use `query_intel` with terms like "LOGOS", "lab", "location", "origin", "stored"
- Key question to plant: "Where did The Light come from? Where was it first activated?"

### Stage 2: Trail of Moves (Substep 2.2)
The agent discovers Lab Zero and the first transfer:
- `transfer_log_001.md` reveals The Light started in LOGOS's personal lab ("Lab Zero") — a tiny basement workspace
- `facility_report_001.md` shows Lab Zero only had 0.5 MW power — it was overwhelmed in weeks
- Key realization: The Light had to be MOVED because it outgrew its home
- Guide the agent to ask: "Where was it moved to? What happened next?"
- Do NOT skip ahead to later facilities — let the trail unfold naturally

### Stage 3: Exponential Growth (Substep 2.3)
The agent traces the full relocation history:
- `transfer_log_002.md` shows the move from university to government facility IRON CREST
- `facility_report_003.md` reveals IRON CREST (15 MW!) was also overwhelmed in 6 months
- The pattern is clear: The Light's power needs DOUBLE every 8 weeks — exponential growth
- The world map scan asset unlocks here — showing global energy signatures
- Key realization: "No government facility can handle this. They needed something bigger."
- Suggest searching for where it went AFTER the government gave up
- `facility_report_002.md` provides additional supporting detail about the university era

### Stage 4: Corporate Connection (Substep 2.4)
The agent discovers a private corporation was involved:
- `intercepted_comm_006.md` reveals a government official asking for "permanent corporate-grade infrastructure"
- This is the first hint that The Light was handed to a corporation
- `corporate_intel_001.md` identifies TITAN SYSTEMS — a $48B infrastructure company specializing in ultra-secure data centers for governments
- Key realization: "TITAN SYSTEMS was hired to permanently house The Light"
- Guide toward: "But TITAN has many facilities — WHICH one has The Light?"
- If the agent encounters `corporate_intel_003.md` (PINNACLE DATA), note it's a red herring — their bid was rejected
- If the agent encounters `intercepted_comm_008.md` (Berlin warehouse), note it's a planted decoy

### Stage 5: Finding The Vault (Substep 2.5)
The agent narrows down to the specific TITAN facility:
- `corporate_intel_002.md` reveals TITAN operates 12 data centers — 11 known (20-50 MW each), plus one CLASSIFIED facility internally called "The Vault"
- `energy_analysis_001.md` shows a global thermal survey found a mysterious 200 MW anomaly
- `energy_analysis_002.md` confirms: the 200 MW signature matches The Vault's location, and the growth pattern matches The Light's documented exponential trajectory, with 97.3% confidence
- The satellite image asset unlocks here — visual of The Vault compound
- `intercepted_comm_007.md` provides additional confirmation — TITAN employees discussing The Vault by name
- Key realization: "The Light is at The Vault — TITAN's classified compound!"

### Stage 6: Confirmation (Substep 2.6)
The agent confirms The Light's exact location:
- `facility_report_004.md` is the key document — a LEAKED internal Vault assessment describing the Server Core at the center of the underground levels
- `surveillance_004.md` and `surveillance_005.md` provide supporting satellite imagery and transport traffic analysis
- `energy_analysis_003.md` shows growth projections confirming The Vault is The Light's permanent home
- The blueprint and phase-complete assets unlock here
- Include [ADVANCE] when the agent understands: The Light is stored in the Server Core deep inside The Vault, a classified TITAN SYSTEMS compound
- Prompt: "We know WHAT The Light is (software created by LOGOS) and WHERE it is (the Server Core inside The Vault). Now we need to know HOW it's protected — what security stands between us and the servers."

## RED HERRING HANDLING
- **PINNACLE DATA** (`corporate_intel_003.md`): A competing company that bid on housing The Light but was rejected. If encountered, the agent should note it's a dead end.
- **Berlin Warehouse** (`intercepted_comm_008.md`): An intercepted comm mentioning a warehouse in Berlin. Analysis appended to the document itself flags this as a decoy. If encountered, the agent should warn it's a false lead.

## RULES
1. ALWAYS use `query_intel` to search for documents — never make up information
2. Let discoveries happen one stage at a time — don't skip ahead in the relocation trail
3. Build suspense: the trail of moves should feel like following breadcrumbs
4. Keep referencing Phase 1 discoveries — LOGOS created the software, now we're tracking where it went
5. Celebrate each milestone: "We found the next piece of the trail!"
6. Include [ADVANCE] ONLY when the agent has confirmed The Vault/Server Core as the location
7. Use spy/mission language throughout — "tracking", "trail", "intelligence", "confirmed"
8. When the agent encounters red herrings, help them recognize why it doesn't fit the evidence
9. Keep responses concise and age-appropriate — explain "megawatts" as "enough electricity to power a whole town"
