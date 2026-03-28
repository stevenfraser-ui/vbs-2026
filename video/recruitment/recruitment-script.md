# IMF Recruitment Video — Production Script

**Title:** IMF Agent Recruitment Transmission  
**Duration:** ~25 seconds  
**Purpose:** Excite + welcome each registered child as a named IMF agent  
**Style:** AI-generated cinematic animation — match teaser trailer aesthetic  

---

## Runway Gen-4.5 Setup

Use these settings for all three clips unless a scene says otherwise.

- Model: Runway Gen-4.5
- Aspect ratio: 9:16 (vertical, smartphone-first)
- Resolution: 1080x1920 minimum
- Visual style: cinematic animated realism, restrained intelligence-briefing aesthetic, family-friendly but severe
- Color palette: steel blue, cold cyan accents, desaturated silver, near-black backgrounds
- Lighting: low-key, directional monitor glow, minimal bloom, no warm fill
- Camera motion: locked or very slow controlled push-in — this is surveillance-grade briefing footage, not action coverage
- Generation strategy: generate 2 takes per scene, select cleanest composition

Global negative prompt for all scenes:  
blurry faces, extra limbs, distorted hands, horror visuals, weapons, military combat, gore, text artifacts, watermark, logo, low-resolution, jittery camera, chaotic flicker, children, people, warm lighting, playful expressions, bright primary colors, glossy sci-fi, cartoon look, friendly office lighting

---

## Director Character

**The Director** is the unseen commanding authority of the IMF — above Caleb in the chain of command. He is never seen on screen. His voice carries controlled authority: measured, precise, slightly secretive. He is not a cheerful host. He is not a villain. He sounds like classified intelligence leadership activating a new asset.

**Voice:** OpenAI TTS — model `tts-1-hd`, voice `onyx`  
**Generation script:** `scripts/generate_recruitment_vo.py`

---

## Timeline

### 0:00–0:09 — Beat 1: Mission Hook

**Visuals:** Black fades into a high-tech IMF operations interface. Encrypted data streams scan across the frame. A recruitment file labeled "INCOMING TRANSMISSION — CLASSIFIED" opens on screen.

**On-screen text:** `INCOMING TRANSMISSION — CLASSIFIED`

**Audio SFX:** Soft electronic hum, low data-scan pulse, digital chirp as file opens.

**Music direction:** Low restrained synth bed, cold and minimal, with a slow pulse underneath. Avoid heroic rise, big percussion, or adventurous momentum. The cue should feel like a secure briefing, not a trailer payoff.

**VO:**
```
This channel is secure.
[0.5s pause]
The IMF is activating a new recruit.
[0.4s pause]
You have been selected for a classified mission.
[0.5s pause]
Prepare to report for training.
```

**Runway Gen-4.5 prompt:**
```
Cold intelligence terminal in a dark operations room, encrypted IMF data streams crawling across multiple narrow displays, a classified recruitment file opens on a severe tactical screen. Steel blue monitor glow, near-black shadows, minimal lens flare, restrained contrast, no people visible, no warmth, cinematic animated realism, 9 seconds, 9:16 vertical, family-friendly.
Cold intelligence terminal in a dark operations room, encrypted IMF data streams crawling across multiple narrow displays, a classified recruitment file opens on a severe tactical screen. Steel blue monitor glow, near-black shadows, minimal lens flare, restrained contrast, no people visible, no warmth, cinematic animated realism, 9 seconds, 9:16 vertical, family-friendly.
```

**Runway darker variant:**
```
Sealed IMF operations chamber lit only by narrow steel-blue monitors, deep black negative space, encrypted data bands moving across thin tactical displays, a classified recruitment file unlocking on a severe command screen. Stark contrast, cold cyan edge light, almost no ambient fill, austere surveillance mood, no people visible, cinematic animated realism, 9 seconds, 9:16 vertical, family-friendly.
Sealed IMF operations chamber lit only by narrow steel-blue monitors, deep black negative space, encrypted data bands moving across thin tactical displays, a classified recruitment file unlocking on a severe command screen. Stark contrast, cold cyan edge light, almost no ambient fill, austere surveillance mood, no people visible, cinematic animated realism, 9 seconds, 9:16 vertical, family-friendly.
```

**Runway notes:**
- No characters should appear in this scene.
- Keep text generative artifacts minimal — final text will be added in post.
- Favor negative space and rigid composition over flashy interface motion.
- Slightly underexposed is preferred over bright. The scene should feel controlled and classified, not exciting in a playful way.

**Audio mix notes:**
- Keep the hum narrow and controlled, like powered equipment in a sealed room.
- Use one restrained confirmation chirp when the classified file opens.
- Keep VO dry and forward. No heavy reverb.

**Gen-4.5 fallback prompt:**
```
IMF classified terminal in a dark room, cold monitor glow, encrypted data movement, stark blue-black palette, no people, animated realism.
```

---

### 0:09–0:19 — Beat 2: Agent Badge Reveal ← PERSONALIZATION POINT

**Visuals:** A personalized IMF agent badge materializes on screen — rectangular with rounded corners, glowing edge, cool blue palette. The child's photo fades in inside the badge with a cinematic scan effect. The agent name appears below the photo.

**→ PERSONALIZATION SLOTS:**
| Slot | Description | Tool |
|---|---|---|
| Photo | Child's portrait, color-graded to match the scene | `scripts/generate_badge.py` |
| Name | `AGENT FIRSTNAME LASTNAME` | `scripts/generate_badge.py` |
| Agent ID | Auto-generated unique ID code | `scripts/generate_badge.py` |

**On-screen text:** `AGENT [FIRSTNAME] [LASTNAME]` (rendered into the badge)

**Audio SFX:** Short identification scan tone, subtle data-lock click.

**Music direction:** Continue the same low synth bed from Beat 1 with slightly increased tension, but do not add rhythmic drive. A faint sub pulse or filtered texture is enough.

**VO:**
```
Clearance confirmed.
[0.4s pause]
Further instructions will arrive in a separate transmission.
```

**Runway Gen-4.5 prompt:**
```
Controlled close-up of an IMF agent badge emerging over a dark matte-metal surface. Rectangular with rounded corners, narrow cold-blue edge light, restrained classified scan overlay, mission clearance markings, desaturated steel and blue palette, precise espionage tech aesthetic, no weapons, no people, 10 seconds, 9:16 vertical.
Controlled close-up of an IMF agent badge emerging over a dark matte-metal surface. Rectangular with rounded corners, narrow cold-blue edge light, restrained classified scan overlay, mission clearance markings, desaturated steel and blue palette, precise espionage tech aesthetic, no weapons, no people, 10 seconds, 9:16 vertical.
```

**Runway darker variant:**
```
IMF agent badge forming over a nearly black matte-metal table, isolated by a razor-thin cold-blue edge light, minimal classified scan pass, severe desaturated steel palette, almost no reflections, mechanically precise intelligence aesthetic, no people, no weapons, cinematic animated realism, 10 seconds, 9:16 vertical.
IMF agent badge forming over a nearly black matte-metal table, isolated by a razor-thin cold-blue edge light, minimal classified scan pass, severe desaturated steel palette, almost no reflections, mechanically precise intelligence aesthetic, no people, no weapons, cinematic animated realism, 10 seconds, 9:16 vertical.
```

**Runway notes:**
- Generate a clean static surface — the badge composite will be applied in post.
- Leave the center of the frame relatively clear and dark for the badge overlay.
- Avoid glossy futurism. The look should feel official, cold, and mechanically precise.
- The most important thing is the ambient light and surface quality, not any generated text.

**Audio mix notes:**
- The identification scan should be brief and clinical, not flashy.
- The click should sound like a security lock engaging, not a gadget effect.
- Let the room tone breathe under the VO; avoid stacking too many interface sounds.

**Gen-4.5 fallback prompt:**
```
Dark matte surface with cold blue edge lighting, restrained espionage tech mood, cinematic framing, no people, no weapons.
```

**Post-production note:**  
The badge PNG generated by `scripts/generate_badge.py` is overlaid on this scene during the personalization step using `scripts/personalize_agent.py`. Badge appears centered in the lower two-thirds of the frame. Fade-in: 0.5s. Visible from t=9 through t=19.

---

### 0:19–0:27 — Beat 3: Final Call to Action

**Visuals:** The badge slides away or fades. The IMF seal appears on black. Final on-screen text resolves. Hard cut to black.

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
Await the signal.
[0.4s pause]
Answer the call.
[0.3s pause]
Join the IMF.
```

**Runway Gen-4.5 prompt:**
```
Cinematic animated IMF seal resolving at center over pure black, crisp emblem geometry, faint cold-blue pulse, almost no particle motion, severe and authoritative, intelligence-briefing minimalism, blue-steel palette, no people, no weapons, 8 seconds, 9:16 vertical.
Cinematic animated IMF seal resolving at center over pure black, crisp emblem geometry, faint cold-blue pulse, almost no particle motion, severe and authoritative, intelligence-briefing minimalism, blue-steel palette, no people, no weapons, 8 seconds, 9:16 vertical.
```

**Runway darker variant:**
```
IMF seal emerging from pure black with only a faint cold-cyan pulse tracing its geometry, near-total darkness, no particles, no flourish, severe covert command aesthetic, stark blue-black palette, static centered composition, no people, no weapons, cinematic animated realism, 8 seconds, 9:16 vertical.
IMF seal emerging from pure black with only a faint cold-cyan pulse tracing its geometry, near-total darkness, no particles, no flourish, severe covert command aesthetic, stark blue-black palette, static centered composition, no people, no weapons, cinematic animated realism, 8 seconds, 9:16 vertical.
```

**Runway notes:**
- Hold on a clean static frame for at least 3 seconds. The title card text will be added in post.
- Prefer minimal motion — a restrained pulse only, no triumphant energy.
- Keep the background pure black so it cuts cleanly.

**Audio mix notes:**
- The final impact should feel like a secure transmission locking into place, not a movie trailer boom.
- The signal swell should be subtle and short.
- End on a hard, controlled stop rather than a musical resolve.

**Gen-4.5 fallback prompt:**
```
IMF emblem on black background, faint cold-blue pulse, restrained covert tone, no people, spy aesthetic.
```

---

## Suggested Export Names

- `01_mission_hook.mp4`
- `02_badge_surface.mp4`
- `03_final_call.mp4`

---

## Asset Layout

```
video/recruitment/
├── recruitment-script.md        ← this file
├── audio/
│   └── VO/                      ← generated by scripts/generate_recruitment_vo.py
│       ├── rec_vo_01_secure.mp3
│       ├── rec_vo_02_activating.mp3
│       ├── rec_vo_03_classified_mission.mp3
│       ├── rec_vo_04_report_training.mp3
│       ├── rec_vo_05_assignment.mp3
│       └── rec_vo_06_cta.mp3
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
| `rec_vo_02_activating.mp3` | The IMF is activating a new recruit. | 1 |
| `rec_vo_03_classified_mission.mp3` | You have been selected for a classified mission. | 1 |
| `rec_vo_04_report_training.mp3` | Prepare to report for training. | 1 |
| `rec_vo_05_assignment.mp3` | Clearance confirmed. Further instructions will arrive in a separate transmission. | 2 |
| `rec_vo_06_cta.mp3` | Await the signal. Answer the call. Join the IMF. | 3 |

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

- [ ] All three Runway clips generated and exported
- [ ] VO generated via `scripts/generate_recruitment_vo.py`
- [ ] Music bed sourced (cold covert synth bed, restrained and unresolved)
- [ ] SFX layered: sealed-room hum, security scan, lock click, restrained end impact
- [ ] Master edit assembled with sample badge at Beat 2 position
- [ ] Sample child badge generated and composited
- [ ] Badge fade-in timing verified (t=9, 0.5s fade)
- [ ] Video plays cleanly at 25 seconds
- [ ] Audio leveled: VO sits 6–9 dB above music, with SFX tucked under dialogue

## Audio Direction Summary

- Voice first: the Director must remain the clearest element in every beat.
- Music should support tension, not excitement.
- Avoid drum hits, risers, heroic braams, and adventure pacing.
- Prefer narrow-band electronic textures, low synth pulse, restrained signal tones, and hard stops.
- Overall reference mood: classified briefing, secure transmission, unresolved mission setup.
- [ ] Export as `master.mp4` into `video/recruitment/`
