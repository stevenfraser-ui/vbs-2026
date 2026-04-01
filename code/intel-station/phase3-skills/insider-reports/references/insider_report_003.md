# IMF INTELLIGENCE REPORT — RECOVERED PERSONAL NOTES

**REPORT ID:** IMF-HUM-2025-0045
**SOURCE:** Recovered notebook — Johan Ekström, Lead Engineer, Midnight Sun Security AB
**RECOVERED BY:** IMF field team during authorized search of Ekström's Stockholm residence (subject cooperating)
**DATE:** 2025-02-08
**RELIABILITY:** A-1 (Completely reliable, confirmed by multiple sources)

---

## RECOVERED NOTES — TRANSCRIPTION

*The following entries are transcribed from a personal engineering notebook recovered with the subject's consent. Entries are dated and appear to be working notes made during the Midnight Sun Security contract.*

---

**2024-07-01 — Project Kickoff**

New contract. Biggest one yet. We're designing a "dynamic pathway authentication system" for some Arctic facility. The client (through a procurement company I've never heard of) wants a system that controls which squares on an 8×8 grid are safe to walk on. The safe path **changes like a password** — on a timer.

Sounds like something out of a spy movie.

**2024-08-15 — Algorithm Design**

The rotation algorithm is elegant. AES-256 seed generates a new pattern every few minutes. Each pattern guarantees at least one valid route from one side of the grid to the other. Authorized people check a secure terminal before crossing — it shows them the current safe squares in green.

**Think of it like this:** imagine a chessboard where some squares are "hot lava." Every few minutes, the hot lava squares change. You need to check the screen to see which squares are safe RIGHT NOW. Step on the wrong one and... well, I don't actually know what happens. They won't tell us.

**2024-09-20 — Integration Questions**

Asked the project manager what happens when someone steps on a wrong square. He said "that's handled by a different system." I pushed and he shut me down hard. "You design the pattern. Someone else handles the response. That's all you need to know."

Fair enough. But I can't shake the feeling that "the response" is something extreme.

**2024-11-28 — Final Testing**

System is live. Patterns rotate perfectly. Terminals display correctly. Every few minutes, a completely new safe path appears. You literally cannot memorize it — by the time you've studied the pattern, it's about to change.

**The only way across is to check the terminal right before you cross, and move fast.**

I still don't know what they're protecting. I still don't know what happens if you step wrong. And after this project, I'm not sure I want to know.

---

## IMF ANALYST NOTE

Ekström's notes provide a human perspective on the Dynamic Pathway Protocol. Key operational intelligence:

1. **The safe path changes every few minutes** — like a constantly rotating password
2. **There's always at least one valid route** from one side to the other
3. **Authorized users check a secure terminal** to see the current pattern before crossing
4. **The pattern can't be memorized** — it changes too quickly
5. **Ekström himself didn't know** what happens if you step wrong (compartmentalization in action)

This confirms: to cross the floor safely, **we need access to the secure terminal or the ability to crack the rotation algorithm.** Brute-forcing the path is not an option — with 64 tiles and only 8-14 safe ones, the odds of guessing correctly are essentially zero.

---

*IMF HUMINT Division — Recovered Materials*
