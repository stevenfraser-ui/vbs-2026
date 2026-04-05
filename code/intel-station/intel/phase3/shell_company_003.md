---
id: "shell_company_003"
type: "shell_company"
title: "Midnight Sun Security AB"
classification: "SECRET"
reference: "SC-MSS-001"
phase: 3
critical: false
summary: "Swedish shell company — linked to Prometheus Dynamics through personnel connections"
metadata:
  source: "Swedish Companies Registration Office"
  confidence: "HIGH"
---
# CORPORATE REGISTRY EXTRACT — MIDNIGHT SUN SECURITY AB

**SOURCE:** Swedish Companies Registration Office (Bolagsverket)
**RETRIEVED BY:** IMF Corporate Intelligence Unit
**DATE OF RETRIEVAL:** 2025-01-22
**CONFIDENCE:** HIGH

---

## COMPANY DETAILS

| Field | Value |
|-------|-------|
| **Company Name** | Midnight Sun Security AB |
| **Registration No.** | SE-559432-8817 |
| **Registered:** | 2024-01-25 |
| **Jurisdiction:** | Stockholm, Sweden |
| **Status:** | Active |
| **Stated Purpose:** | "Cryptographic access management and dynamic authentication systems" |

## DIRECTORS & OFFICERS

| Name | Role | Notes |
|------|------|-------|
| Astrid Lindmark | Managing Director | **Cross-reference match:** Former cryptography specialist at PROMETHEUS DYNAMICS R&D division (Zürich, 2020-2023). Published papers on "rotating cryptographic seed patterns for physical access control." |
| Johan Ekström | Lead Engineer | Specialist in secure terminal design and hardware authentication modules. Previously employed by Swedish defense contractor Saab Dynamics — legitimate hire, but recruited specifically for this project. |

## KNOWN CONTRACTS

- **APS-PO-2024-B** (2024-06-15): $14.8M contract from Arctic Procurement Services AG
  - Scope: "Dynamic pathway authentication system — Site S-7"
  - Deliverables:
    - Cryptographic pathway pattern generation engine
    - Timed rotation protocol — safe path changes on configurable intervals
    - Secure display terminals for authorized personnel to view current safe path
    - Integration interface with kinetic detection hardware (provided by separate vendor)
  - Specification: "System must generate unique traversal patterns using rotating cryptographic seed. Pattern must change at intervals no greater than [REDACTED] minutes. Display terminals must show current valid path to authorized users only."
  - Status: Completed 2024-11-30

## IMF ANALYST NOTE

Midnight Sun Security designed **the system that determines which path across the floor is safe.** The path isn't fixed — it changes on a timer using cryptographic algorithms, essentially making it a **password that keeps changing.**

This is the critical link between the pressure-sensitive floor (installed by a different contractor) and the ability to actually cross it safely. Without knowing the current safe path pattern, even knowing about the floor grid is useless.

The secure display terminals suggest that authorized PROMETHEUS personnel check a screen before crossing the floor to see the current pattern. **If we can access that terminal or crack the rotation algorithm, we'd know which squares are safe.**

---

*IMF Corporate Intelligence — Shell Company Identification Program*
