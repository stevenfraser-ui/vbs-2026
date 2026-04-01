# LEAKED TECHNICAL SPECIFICATION — MIDNIGHT SUN SECURITY

**DOCUMENT ID:** MSS-SPEC-DPP-v2.1
**PROJECT:** Dynamic Pathway Protocol v2.1
**CLIENT:** Arctic Procurement Services AG (Contract APS-PO-2024-B)
**CLASSIFICATION:** CONTRACTOR CONFIDENTIAL
**RECOVERED BY:** IMF Cyber Operations — exfiltrated from Midnight Sun Security cloud backup

---

## 1. SYSTEM OVERVIEW

The Dynamic Pathway Protocol (DPP) is a cryptographic access management system that generates and rotates authorized traversal patterns for a physical access corridor. The system determines which squares in a grid are safe to cross and **changes the safe path on a timed interval.**

## 2. PATTERN GENERATION

| Parameter | Value |
|-----------|-------|
| **Grid Size** | 8×8 (configuration provided by integration partner) |
| **Algorithm** | AES-256 rotating cryptographic seed |
| **Rotation Interval** | Configurable — client requested every [REDACTED] minutes |
| **Patterns per Cycle** | Unique — no pattern repeats within a 30-day window |
| **Safe Squares per Pattern** | Variable — minimum 8, maximum 14 per pattern |
| **Path Constraint** | At least one valid traversal route must exist from Row 1 to Row 8 |

## 3. HOW IT WORKS

1. A **master cryptographic seed** is stored in a hardware security module (HSM)
2. Every [REDACTED] minutes, the seed generates a new **pathway pattern**
3. The pattern specifies which grid squares are **SAFE** (can be stepped on) and which are **ARMED** (trigger alert)
4. The pattern is pushed to the flooring system (separate vendor) and displayed on **secure terminals**
5. Authorized personnel check the secure terminal before crossing to see the current safe path
6. When the timer expires, a new pattern is generated and the old path becomes invalid

## 4. SECURE DISPLAY TERMINALS

- **Location:** Mounted at corridor entrance (Site S-7, Level B3)
- **Access:** Biometric authentication required (fingerprint + retinal scan)
- **Display:** Real-time 8×8 grid showing current safe squares highlighted in green
- **Timeout:** Display auto-blanks after 10 seconds
- **Logging:** All terminal access events logged with user ID, timestamp, biometric data

## 5. IMPORTANT DESIGN NOTE

**FROM MIDNIGHT SUN ENGINEERING TEAM:**

We designed this system to work with "an 8×8 sensor grid installed by another vendor." We were never given details about what the sensors actually do — only that our pathway configuration must be transmitted to them in real time. We assume it's some form of access control, but the exact mechanism is unknown to us.

We were also told a "third vendor" handles "response protocols" if an unauthorized traversal occurs. We have no visibility into what that response entails.

## 6. VULNERABILITY ASSESSMENT

The DPP has no known vulnerabilities when operating as designed. However:
- If the HSM is compromised, all future patterns can be predicted
- If a secure terminal is accessed by an unauthorized user, the current (but not future) pattern is exposed
- The system has no awareness of whether its patterns are being followed — it only generates and displays them

---

*Midnight Sun Security AB — Cryptographic Access Management*
