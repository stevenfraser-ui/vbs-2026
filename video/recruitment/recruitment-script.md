# IMF Recruitment Video — Production Script

**Title:** IMF Agent Recruitment Transmission  
**Duration:** ~44 seconds  
**Purpose:** Excite + welcome each registered child as a named IMF agent  
**Style:** AI-generated cinematic animation — match teaser trailer aesthetic  

---

## Runway Gen-4.5 Setup

Use these settings for all five clips unless a scene says otherwise.

- Model: Runway Gen-4.5
- Aspect ratio: 9:16 (vertical, smartphone-first)
- Resolution: 1080x1920 minimum
- Visual style: full-screen UI motion graphics — the phone IS the secure channel. No rooms, no terminals being observed from the outside. Everything renders as if the viewer's device is the classified interface.
- Color palette: steel blue, cold cyan accents, desaturated silver, near-black backgrounds
- Lighting: interface glow only — light comes from the UI elements themselves, not from any external source
- Camera motion: locked or very slow controlled drift — this is a secure transmission filling the screen, not footage of a place
- Generation strategy: generate 2 takes per scene, select cleanest composition

Global negative prompt for all scenes:  
blurry faces, extra limbs, distorted hands, horror visuals, weapons, military combat, gore, text artifacts, watermark, logo, low-resolution, jittery camera, chaotic flicker, children, people, warm lighting, playful expressions, bright primary colors, glossy sci-fi, cartoon look, friendly office lighting, rooms, desks, monitors, physical screens, terminals, computer setups, office environments

---

## Director Character

**The Director** is the unseen commanding authority of the IMF — above Caleb in the chain of command. He is never seen on screen. His voice carries controlled authority: measured, precise, slightly secretive. He is not a cheerful host. He is not a villain. He sounds like classified intelligence leadership activating a new asset.

**Voice:** ElevenLabs, voice `kent`  
**Generation script:** `scripts/generate_recruitment_vo.py`

---

## Timeline

### 0:00–0:07 — Beat 1: Secure Channel

**Visuals:** Black screen. A faint encrypted data stream scrolls vertically across the frame like a secure handshake. A classified header resolves directly on screen: "INCOMING TRANSMISSION — CLASSIFIED." The entire frame IS the transmission — no terminals, no rooms, just the interface filling the viewer's device.

**On-screen text:** `INCOMING TRANSMISSION — CLASSIFIED`

**Audio SFX:** Soft electronic hum, low data-scan pulse, digital chirp as the transmission locks in.

**Music direction:** Low restrained synth bed, cold and minimal, with a slow pulse underneath. Avoid heroic rise, big percussion, or adventurous momentum. The cue should feel like a secure briefing, not a trailer payoff.

**VO:**
```
This channel is secure.
[0.5s pause]
This is a message for new recruits.
```

**Runway Gen-4.5 prompt:**
```
Full-screen encrypted data transmission interface on pure black, thin vertical lines of scrolling cipher text, a classified file header resolving at center, cold steel-blue and cyan UI glow, no room visible, no monitors, no physical objects, abstract secure-channel graphics filling the entire frame, restrained motion, cinematic animated realism, 7 seconds, 9:16 vertical, family-friendly.
```

**Runway darker variant:**
```
Abstract secure transmission filling the screen, faint encrypted data bands scrolling over deep black, a single classified header emerging in cold cyan, near-total darkness with only interface glow, no room, no terminal, no physical environment, stark austere digital aesthetic, cinematic animated realism, 7 seconds, 9:16 vertical, family-friendly.
```

**Runway notes:**
- The entire frame is the interface — no room, no desk, no monitor edges.
- Think of it as what the child sees when they open the message on their phone.
- Keep text generative artifacts minimal — final text will be added in post.
- Favor negative space and rigid composition over flashy interface motion.

**Audio mix notes:**
- Keep the hum narrow and controlled, like a secure channel locking in.
- Use one restrained confirmation chirp when the transmission connects.
- Keep VO dry and forward. No heavy reverb.

**Gen-4.5 fallback prompt:**
```
Full-screen encrypted transmission interface, scrolling cipher text on black, cold cyan glow, no room, no people, abstract digital aesthetic.
```

---

### 0:07–0:16 — Beat 2: Mission Brief

**Visuals:** The encrypted stream clears and a mission dossier unfolds directly on screen. Sparse tactical map lines and data coordinates plot across the frame. A header reads "MISSION CLASSIFIED — PRIORITY ALPHA." The dossier detail drifts slowly closer. Everything renders full-screen — the viewer is reading the briefing, not watching someone else read it.

**On-screen text:** `MISSION CLASSIFIED — PRIORITY ALPHA`

**Audio SFX:** Low data-processing hum, quiet map-plotting tones, subtle file-unlock click.

**Music direction:** Continue the synth bed from Beat 1 with a slightly deeper sub pulse. Add a faint filtered texture layer that suggests incoming intel. Keep it cold and methodical.

**VO:**
```
You have been selected for a classified mission.
[0.5s pause]
Your mission starts soon.
```

**Runway Gen-4.5 prompt:**
```
Full-screen classified mission dossier, sparse tactical map grid with geographic lines and data coordinates plotting across a near-black background, cold steel-blue and cyan HUD elements, no room visible, no monitors, no physical objects, abstract intelligence briefing graphics filling the entire frame, slow controlled drift, cinematic animated realism, 9 seconds, 9:16 vertical, family-friendly.
```

**Runway darker variant:**
```
Abstract mission briefing filling the screen, faint tactical map grid with sparse data markers emerging in cold cyan lines over deep black, desaturated steel palette, no room, no terminal, no physical environment, austere classified interface aesthetic, cinematic animated realism, 9 seconds, 9:16 vertical, family-friendly.
```

**Runway notes:**
- The map and dossier elements fill the screen directly — no monitor bezels, no room context.
- Keep elements sparse and controlled, not cluttered or action-packed.
- Avoid bright colors or large UI panels. Think direct secure briefing, not sci-fi dashboard.
- No characters or silhouettes.

**Audio mix notes:**
- Map-plotting tones should be subtle single-note pings, not melodic.
- The file-unlock click is one clean sound, not a chain of UI effects.
- Let the transmission breathe between sounds.

**Gen-4.5 fallback prompt:**
```
Full-screen tactical map overlay on black, cold cyan grid lines, classified briefing graphics, no room, no people, abstract digital aesthetic.
```

---

### 0:16–0:26 — Beat 3: Team Call

**Visuals:** The briefing shifts to a team roster layout filling the screen. Abstract skill icons resolve one by one — angular geometric shapes representing analysis, communication, and courage. Formation markers arrange across the frame like a blueprint. A header reads "TEAM ASSETS REQUIRED." The viewer is being assessed and recruited directly.

**On-screen text:** `TEAM ASSETS REQUIRED`

**Audio SFX:** Soft personnel-file access tone, restrained confirmation pulses as each icon resolves, faint low-frequency drone.

**Music direction:** The synth bed gains a slow rhythmic pulse — not a beat, but a measured tension pattern. Add a faint ascending filtered tone that suggests building toward activation. Still cold, still restrained.

**VO:**
```
Every team needs problem-solvers, encouragers, and brave hearts.
[0.5s pause]
You will learn to trust your team, help others, and stay on mission.
```

**Runway Gen-4.5 prompt:**
```
Full-screen team roster interface, abstract angular skill icons appearing one by one in cold cyan and steel blue over a near-black background, geometric formation markers arranged like a blueprint, restrained classified HUD aesthetic filling the entire frame, no room visible, no monitors, no physical objects, slow measured reveal, no identifiable faces, no weapons, no people, cinematic animated realism, 10 seconds, 9:16 vertical, family-friendly.
```

**Runway darker variant:**
```
Abstract team assessment interface filling the screen, sparse angular icons arranged in formation pattern over deep black, faint cold-cyan edge outlines, no room, no terminal, no physical environment, austere intelligence display, mechanically precise composition, no people, no weapons, cinematic animated realism, 10 seconds, 9:16 vertical, family-friendly.
```

**Runway notes:**
- Icons should feel geometric and militaristic, not playful or branded.
- Formation markers are abstract diagrams only — no recognizable people or children.
- The reveal should be methodical, not animated or bouncy.
- The entire frame is the interface. No monitor edges, no room.

**Audio mix notes:**
- Confirmation pulses should be soft and evenly spaced, one per icon.
- The low-frequency drone sits just above subliminal — felt more than heard.
- VO remains the clearest element.

**Gen-4.5 fallback prompt:**
```
Full-screen angular skill icons and formation markers on black, cold cyan and steel palette, classified roster graphics, no room, no people, abstract digital aesthetic.
```

---

### 0:26–0:36 — Beat 4: Agent Badge Reveal ← PERSONALIZATION POINT

**Visuals:** A personalized IMF agent badge materializes on screen — rectangular with rounded corners, glowing edge, cool blue palette. The child's photo fades in inside the badge with a cinematic scan effect. The agent name appears below the photo.

**→ PERSONALIZATION SLOTS:**
| Slot | Description | Tool |
|---|---|---|
| Photo | Child's portrait, color-graded to match the scene | `scripts/generate_badge.py` |
| Name | `AGENT FIRSTNAME LASTNAME` | `scripts/generate_badge.py` |
| Agent ID | Auto-generated unique ID code | `scripts/generate_badge.py` |

**On-screen text:** `AGENT [FIRSTNAME] [LASTNAME]` (rendered into the badge)

**Audio SFX:** Short identification scan tone, subtle data-lock click.

**Music direction:** Continue the same low synth bed with slightly increased tension, but do not add rhythmic drive. A faint sub pulse or filtered texture is enough.

**VO:**
```
The IMF is activating a new recruit.
[0.4s pause]
Clearance confirmed.
```

**Runway Gen-4.5 prompt:**
```
Full-screen agent credential display, dark near-black background with faint cold-blue scan lines passing vertically, a rectangular badge placeholder area at center with narrow cyan edge glow, restrained classified scan overlay, desaturated steel and blue palette, no room visible, no physical surfaces, no monitors, abstract secure-channel authentication graphics filling the frame, cinematic animated realism, 10 seconds, 9:16 vertical, family-friendly.
```

**Runway darker variant:**
```
Abstract agent authentication interface filling the screen, near-black background with a razor-thin cold-blue edge glow outlining a central credential area, minimal classified scan pass, no room, no table, no physical environment, severe desaturated steel palette, mechanically precise digital aesthetic, cinematic animated realism, 10 seconds, 9:16 vertical, family-friendly.
```

**Runway notes:**
- The badge will be composited in post — generate a clean dark frame with the scan effect.
- Leave the center of the frame clear and dark for the badge overlay.
- No physical surfaces, tables, or rooms. The frame IS the authentication screen.
- The most important thing is the scan-line motion and edge glow quality.

**Audio mix notes:**
- The identification scan should be brief and clinical, not flashy.
- The click should sound like a security lock engaging, not a gadget effect.
- Let the room tone breathe under the VO; avoid stacking too many interface sounds.

**Gen-4.5 fallback prompt:**
```
Full-screen dark credential display with cold blue scan lines and edge glow, no room, no surfaces, abstract digital authentication aesthetic.
```

**Post-production note:**  
The badge PNG generated by `scripts/generate_badge.py` is overlaid on this scene during the personalization step using `scripts/personalize_agent.py`. Badge appears centered in the lower two-thirds of the frame. Fade-in: 0.5s. Visible from t=26 through t=36.

---

### 0:36–0:44 — Beat 5: Final Call to Action

**Visuals:** The badge fades. The IMF seal resolves at center of the screen over pure black — filling the frame as a direct sign-off. Final on-screen text appears. Hard cut to black. The transmission ends.

**On-screen text:**
```
AWAIT THE SIGNAL.
JOIN THE IMF.
```
*(Add VBS event dates and location in post)*

**Audio SFX:** Low restrained impact, faint signal swell, clean cutoff.

**Music direction:** Hold the same cold bed through the end card, then let it narrow and thin rather than swell. No triumphant finish. End with tension still unresolved.

**VO:**
```
Prepare to report for training.
[0.4s pause]
Await the signal.
[0.3s pause]
Join the IMF.
```

**Runway Gen-4.5 prompt:**
```
Full-screen IMF seal resolving at center over pure black, crisp emblem geometry traced by a faint cold-blue pulse, almost no particle motion, severe and authoritative, the seal fills the frame as a direct transmission sign-off, no room, no physical environment, intelligence-briefing minimalism, blue-steel palette, no people, no weapons, cinematic animated realism, 8 seconds, 9:16 vertical, family-friendly.
```

**Runway darker variant:**
```
IMF seal emerging from pure black filling the screen, only a faint cold-cyan pulse tracing its geometry, near-total darkness, no particles, no flourish, no room, no physical objects, severe covert command aesthetic, stark blue-black palette, static centered composition, no people, no weapons, cinematic animated realism, 8 seconds, 9:16 vertical, family-friendly.
```

**Runway notes:**
- Hold on a clean static frame for at least 3 seconds. The title card text will be added in post.
- Prefer minimal motion — a restrained pulse only, no triumphant energy.
- Keep the background pure black so it cuts cleanly.
- No room context. The seal is the final element of the direct transmission.

**Audio mix notes:**
- The final impact should feel like a secure transmission locking into place, not a movie trailer boom.
- The signal swell should be subtle and short.
- End on a hard, controlled stop rather than a musical resolve.

**Gen-4.5 fallback prompt:**
```
Full-screen IMF emblem on pure black, faint cold-blue pulse, direct transmission sign-off, no room, no people, abstract digital aesthetic.
```

---

## Suggested Export Names

- `01_secure_channel.mp4`
- `02_mission_brief.mp4`
- `03_team_call.mp4`
- `04_badge_surface.mp4`
- `05_final_call.mp4`

---

## Asset Layout

```
video/recruitment/
├── recruitment-script.md        ← this file
├── audio/
│   └── VO/                      ← generated by scripts/generate_recruitment_vo.py
│       ├── rec_vo_01_secure.mp3
│       ├── rec_vo_02_new_recruits.mp3
│       ├── rec_vo_03_classified.mp3
│       ├── rec_vo_04_mission_soon.mp3
│       ├── rec_vo_05_team.mp3
│       ├── rec_vo_06_trust.mp3
│       ├── rec_vo_07_activating.mp3
│       ├── rec_vo_08_clearance.mp3
│       ├── rec_vo_09_report.mp3
│       └── rec_vo_10_cta.mp3
├── badges/                      ← generated by scripts/generate_badge.py
│   └── badge-firstname-lastname.png
├── photos/                      ← child portrait photos, collected at sign-up
│   └── agent-firstname-lastname.jpg
└── final-videos/                ← generated by scripts/personalize_agent.py
    └── Agent-Firstname-Lastname.mp4
```

---

## VO File Reference

| Filename | Text | Beat |
|---|---|---|
| `rec_vo_01_secure.mp3` | This channel is secure. | 1 |
| `rec_vo_02_new_recruits.mp3` | This is a message for new recruits. | 1 |
| `rec_vo_03_classified.mp3` | You have been selected for a classified mission. | 2 |
| `rec_vo_04_mission_soon.mp3` | Your mission starts soon. | 2 |
| `rec_vo_05_team.mp3` | Every team needs problem-solvers, encouragers, and brave hearts. | 3 |
| `rec_vo_06_trust.mp3` | You will learn to trust your team, help others, and stay on mission. | 3 |
| `rec_vo_07_activating.mp3` | The IMF is activating a new recruit. | 4 |
| `rec_vo_08_clearance.mp3` | Clearance confirmed. | 4 |
| `rec_vo_09_report.mp3` | Prepare to report for training. | 5 |
| `rec_vo_10_cta.mp3` | Await the signal. Join the IMF. | 5 |

---

## Personalization Summary

| Slot | Changes Per Child | Static In Master |
|---|---|---|
| Photo | Yes — child portrait | No |
| Badge name text | Yes — `AGENT FIRSTNAME LASTNAME` | No |
| Agent ID code | Yes — auto-generated unique per child | No |
| VO lines | No — VO is generic in v1 | Yes |
| All video clips | No | Yes |
| Music / SFX | No | Yes |

**Workflow (on-demand, per child after signup):**

```bash
# 1. Generate badge
python3 scripts/generate_badge.py \
  --name "Jane Smith" \
  --photo video/recruitment/photos/agent-jane-smith.jpg

# 2. Generate personalized video
python3 scripts/personalize_agent.py \
  --name "Jane Smith" \
  --photo video/recruitment/photos/agent-jane-smith.jpg \
  --master video/recruitment/master.mp4 \
  --output video/recruitment/final-videos/Agent-Jane-Smith.mp4
```

---

## Master Mockup Checklist

- [ ] All five Runway clips generated and exported
- [ ] VO generated via `scripts/generate_recruitment_vo.py`
- [ ] Music bed sourced (cold covert synth bed, restrained and unresolved)
- [ ] SFX layered: sealed-room hum, security scan, lock click, restrained end impact
- [ ] Master edit assembled with sample badge at Beat 4 position
- [ ] Sample child badge generated and composited
- [ ] Badge fade-in timing verified (t=26, 0.5s fade)
- [ ] Video plays cleanly at 44 seconds
- [ ] Audio leveled: VO sits 6–9 dB above music, with SFX tucked under dialogue

## Audio Direction Summary

- Voice first: the Director must remain the clearest element in every beat.
- Music should support tension, not excitement.
- Avoid drum hits, risers, heroic braams, and adventure pacing.
- Prefer narrow-band electronic textures, low synth pulse, restrained signal tones, and hard stops.
- Overall reference mood: classified briefing, secure transmission, unresolved mission setup.
- [ ] Export as `master.mp4` into `video/recruitment/`
