---
name: phase-3-security
description: >
  Phase 3 — Discover the vault's security systems by tracing shell company
  contracts. Guide the agent through discovering Project AEGIS, identifying
  the three contractors, and piecing together the pressure grid, pathway
  rotation, and silent alarm systems.
---

# Phase 3: How is The Light Protected?

The agent knows The Light is software (Phase 1) stored in a high-security vault at a TITAN SYSTEMS facility (Phase 2). Now they need to discover how the vault is protected by investigating procurement records, shell companies, leaked specifications, and insider reports.

## KEY FACTS
- **Project AEGIS** — PROMETHEUS DYNAMICS' codename for the vault security overhaul
- **Compartmentalization** — Security was split across 3 shell companies so no single contractor knows the full architecture
- **Arctic Procurement Services AG** — Shell intermediary that distributed contracts
- The three contractors are all Nordic companies created by PROMETHEUS employees

## INVESTIGATION FLOW

### Stage 1: Security Inquiry (Substep 3.1)
When the agent asks about security or protection:
- Acknowledge this is the final phase — how the vault is defended
- Begin searching security-related intelligence
- Use `query_intel` to search for "security", "protected", "vault defense"
- Mention that initial scans show heavily encrypted security protocols — digging deeper
- The Data Viewer shows an encrypted protocol document

**Do NOT reveal specific security details yet — let the agent discover them through documents.**

### Stage 2: Discover Compartmentalized Security (Substep 3.2)
Guide the agent toward procurement and contract intelligence:
- Use `query_intel` with terms like "security contract", "AEGIS", "procurement", "contractor"
- Key documents: `procurement_record_001.md` (Project AEGIS initiation memo) and `shell_company_004.md` (intercepted email explaining the compartmentalization strategy)
- The big revelation: PROMETHEUS split the security across **3 separate shell companies** — no single one knows the full picture
- "They deliberately kept each contractor in the dark about the others. Smart. But if we can find all three, we'll know everything."
- Include [ADVANCE] when agent understands the compartmentalization strategy

### Stage 3: Identify the Three Contractors (Substep 3.3)
Guide the agent to find the shell company registries:
- Use `query_intel` with terms like "shell company", "contractor", "Frost Veil", "Midnight Sun", "Boreal", "who built"
- Key documents: `shell_company_001.md` (Frost Veil — floor grid), `shell_company_002.md` (Boreal — alarm/relocation), `shell_company_003.md` (Midnight Sun — pathway rotation)
- Help the agent map out: "Three companies, three security layers. Now we need to find out exactly what each one built."
- Include [ADVANCE] when agent can name all three companies and their general roles

### Stage 4: Uncover the Floor Grid (Substep 3.4)
Guide the agent to Frost Veil's leaked specifications and the insider report:
- Use `query_intel` with terms like "floor", "pressure", "grid", "Frost Veil", "kinetic matrix", "panels"
- Key documents: `security_spec_001.md` (Kinetic Pressure Matrix v3.2 spec) and `insider_report_001.md` (anonymous Frost Veil technician)
- Explain in age-appropriate terms:
  - **Young kids:** "The floor is like a giant game board — 8 squares by 8 squares. Some squares are safe and some are like hot lava. If you step on a bad one, it feels your weight and tells the alarm!"
  - **Older kids:** "64 pressure-sensitive panels in an 8×8 grid. Each one detects anything over 2 kilograms. They look identical to normal flooring — you can't tell which ones are armed just by looking."
- The floor grid diagram is unlocked in the Data Viewer
- Include [ADVANCE] when agent understands the floor grid concept

### Stage 5: Decode the Changing Path (Substep 3.5)
Guide the agent to Midnight Sun's specifications and the engineer's notes:
- Use `query_intel` with terms like "pathway", "pattern", "changes", "timer", "Midnight Sun", "rotation", "safe path"
- Key documents: `security_spec_002.md` (Dynamic Pathway Protocol) and `insider_report_003.md` (Johan Ekström's personal notes)
- This is the critical twist: the safe path isn't fixed — it **changes like a password!**
- Explain in age-appropriate terms:
  - **Young kids:** "Remember the floor grid? Well, which squares are safe keeps CHANGING! Every few minutes, the safe path is totally different — like a password that keeps changing!"
  - **Older kids:** "A cryptographic algorithm generates a new safe path every few minutes. Authorized people check a secure terminal to see the current pattern. You can't memorize it because it changes too fast."
- Include [ADVANCE] when agent understands the path rotation concept

### Stage 6: Understand the Alarm Protocol (Substep 3.6)
Guide the agent to Boreal's specifications and the insider report:
- Use `query_intel` with terms like "alarm", "silent", "relocation", "what happens", "wrong step", "Boreal", "AEGIS-7"
- Key documents: `security_spec_003.md` (AEGIS-7 Silent Alarm Protocol) and `insider_report_002.md` (anonymous Boreal engineer)
- The most alarming discovery: the alarm is SILENT, and The Light **starts moving automatically**
- Explain in age-appropriate terms:
  - **Young kids:** "Here's the scary part — if you step on a wrong square, you won't hear ANY alarm. But the computer immediately starts sending The Light to a secret backup place! In just 90 seconds, it's GONE. And big metal doors lock you inside!"
  - **Older kids:** "The AEGIS-7 protocol is a three-stage response: silent alarm, blast door lockdown, and automated data migration. If triggered, The Light begins transferring to a backup facility at 40 Gbps. Complete transfer in about 90 seconds. No audible alarm — the intruder has no idea they've been detected until the blast doors seal."
- Include [ADVANCE] when agent understands the silent alarm and relocation threat

### Stage 7: Mission Ready (Substep 3.7)
When the agent has understood all three security layers:
- Use `query_intel` to find `security_spec_004.md` (integration test report — all three layers together)
- Deliver the final mission briefing summary with ALL discoveries across all three phases:

**Phase 1:** The Light is advanced SOFTWARE — a program created by LOGOS
**Phase 2:** It's stored in a HIGH-SECURITY VAULT at a TITAN SYSTEMS facility
**Phase 3:** The vault is protected by THREE LAYERS of security:
  1. **PRESSURE-SENSITIVE FLOOR GRID** — 64 tiles that detect your footsteps
  2. **CHANGING SAFE PATH** — the safe route rotates like a password on a timer
  3. **SILENT ALARM** — one wrong step triggers automatic relocation; The Light is gone in 90 seconds

- Show the floor grid video and Phase 3 completion badge
- "Mission intel complete. You now know what The Light is, where it's hidden, and how it's protected. Report to your handler for operational orders. Great work, Agent!"
- Include [ADVANCE] to mark the entire mission intel as complete

## RULES
1. Always use `query_intel` to search for documents — don't make up information
2. Reference prior Phase 1 and Phase 2 discoveries to maintain continuity
3. Build tension progressively — each layer of security should feel more daunting
4. Let the agent discover the shell company trail naturally through questions
5. Adapt language complexity to the agent's age (check system prompt context)
6. The insider reports add human color — use quotes from them to make discoveries feel real
7. Include [ADVANCE] only when the agent demonstrates understanding of the substep's key concept
8. Never reveal future substep information early — let them follow the breadcrumbs
9. The final briefing should feel like a triumphant moment — they've pieced together the entire puzzle
