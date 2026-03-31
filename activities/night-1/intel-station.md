Below are the specific details for the "Intel Station" activity web app.

### Tech Stack

**Web App (Optimized for Tablets or Laptops)**
- Docker
- Python 3
- A Streamlit web app running in full-screen mode on a tablet or laptop.
- Use Strands Agents SDK connecting to Ollama [ref docs](https://strandsagents.com/docs/user-guide/concepts/model-providers/ollama/)
- It will connect to my Ollama server running at 192.168.4.104:11434. [ollama api docs](https://docs.ollama.com/api/chat)
  - Model: llama3.1
- Store users and user progress in Sqlite database

### Technical Details

- Project structure
  - Create this as a new application in the 'code/intel-station/' directory
  - Put python source code in a new 'code/intel-station/src/' directory
  - Put requirements.txt in 'code/intel-station/'
- Follow SOLID programming principles
- Must handle multiple users interacting at the same time. Each user will sign in with a 4-digit code. We must keep track of each user's progress individually.
- User information must at least include "name", "code", "age", "progress"

### User Interface Concepts

A split-screen terminal. 
- **The Left Panel ("Chat Terminal"):** A chat interface where kids communicate with the "IMF Central AI". Responses from the AI will be short and simple, providing status updates mostly, whereas most of the actual information is revealed in the "Data Viewer".
- **The Right Panel ("Data Viewer"):** A dynamic display area where unlocked intercepted images, audio files, videos, or blueprints appear. As the users unlock more and more information, the data should be revealed in the "Data Viewer" and selectable so they can go back and forth through the data they have uncovered.
- The IMF logo (currently stored at 'code/keypad/assets/imf.svg') must be shown in the "Chat Terminal" panel.
- See images of mockups in 'activities/night-1/intel-station-mockups/'

### The AI Mechanic

The AI agent must be given a strict system prompt. It acts as a "Gatekeeper." It is told the current state of the kids' knowledge based on the Briefing and will only release the next piece of intel if the kids ask a question containing a specific keyword or concept they just learned. This forces them to read, comprehend, and ask logical follow-up questions.
The agent must be told to respond with structured data that the app will use to keep track of the kids' progress through the game.
The AI prompt will also be instructed to explain things according to the user's age.

#### Safety/guardrails

Since kids are chatting with a model, the app should:
- reject unrelated open-ended conversations
- keep all answers short
- avoid theological improvisation outside the scripted game
- avoid revealing future-phase intel early
- avoid asking kids for personal info

### Main App Interaction

The kids will ask questions and talk to the AI. Prompts closely matching specific pre-scripted questions will reveal pre-scripted data, videos, etc.. in the "Data Viewer". Based on this data, the kids should deduce logical next step questions to ask the agent.

### Prompt Progression Flow

There will be 3 main phases (or logic gates) the kids must get through to learn everything they need to learn to complete "the game".
Each phase should require multiple back and forth question and answers for the kids to pull all of the necessary information from the AI.
The application must keep track of how much information they have unlocked to show their progress.
Even though there are 3 main phases, there will be far more than only 3 progress points.

**Phase 1: What is The Light?**
- *Action:* Kids must ask the AI questions about "The Light" based on the briefing.
- *AI Response:* The AI pulls up intercepted messages from "The Architect." The messages talk about "compiling code" and "digital perfection."
- *Discovery:* The AI helps explain that The Light isn't a magical glowing rock; it's **software** (a powerful computer program or secret digital recipe). 

**Phase 2: Where is it?**
- *Action:* Since it's software, the kids must ask where it is stored. 
- *AI Response:* The AI searches for massive energy signatures needed to hold such software and unlocks a blueprint of a building.
- *Discovery:* It's held in a **High-Security Server Vault**. (The AI explains a server vault is like a massive, highly armored library for computers instead of books).

**Phase 3: How is it protected?**
- *Action:* The kids ask about security, defenses, or alarms at the vault.
- *AI Response:* The AI decrypts the final security protocol file. A video or flashing diagram appears in the Data Viewer.
- *Discovery:* The vault has a **Pressure-Sensitive Floor Grid**. Anyone entering must step only on pre-designated safe squares, or an alarm will trigger.

### Operational Parameters

- **Devices:** 3-5 tablets/laptops running simultaneously against one server
- **Time per group:** 13-15 minutes per rotation
- **Device usage:** Mix — some kids share a device in pairs, some work individually
- **Completion:** It's okay if some groups don't finish all 3 phases
- **Facilitation:** Light adult facilitation — adult nearby but kids lead the interaction
- **Sign-in:** Hybrid — leaders pre-create accounts (name, age, code) via admin page; kids enter 4-digit code to log in
- **Group rotation:** Individual login with 4-digit code + leader can reset stations between groups
- **Briefing context:** Kids only know what they learned from Act 1 (no physical handout)
- **Progress persistence:** Night 1 only (ephemeral — reset between events)

### UI Style & Features

- **Visual style:** Sleek spy HQ — dark UI with blue/orange accents, modern dashboard feel
- **AI personality:** Friendly but businesslike ("Good question, Agent! I've found something in our database.")
- **Keyword triggering:** Semantic understanding — the AI judges whether the kid demonstrates comprehension, not exact keyword matching
- **Data Viewer content:** Mixed media — images, text documents, audio, video
- **Streaming:** AI responses appear with a typewriter/streaming effect
- **Sound effects:** UI sounds on key events (message beep, unlock chime, scan sweep, phase complete fanfare)
- **Post-completion:** Summary screen showing all 3 discoveries, "MISSION INTEL COMPLETE — Report to your handler"

### Detailed Phase Progression (10 sub-steps)

**Phase 1: What is The Light? (4 sub-steps)**

1. **1.1 — Initial Query:** Kid asks about "The Light." AI acknowledges and begins searching classified database. Data Viewer shows: "SCANNING ARCHIVES..." animation.
2. **1.2 — Intercepted Messages:** AI finds intercepted transmissions from "The Architect." Data Viewer displays 3 decoded text messages referencing "compiling code," "the blueprint is digital," and "perfection through programming."
3. **1.3 — Analysis Request:** Kid asks follow-up about what "compiling code" means or what the messages suggest. AI explains the terminology in age-appropriate language. Data Viewer shows: a decoded document with highlighted keywords.
4. **1.4 — Discovery Confirmation:** Kid demonstrates understanding that The Light is software/a program. AI confirms: "Intel verified. The Light is advanced software — a powerful digital program created by The Architect." Data Viewer shows: Phase 1 COMPLETE badge + summary.

**Phase 2: Where is it? (3 sub-steps)**

5. **2.1 — Location Query:** Kid asks where the software is stored/located. AI initiates energy signature scan — software this powerful needs massive electricity. Data Viewer shows: world map with heat signatures.
6. **2.2 — Energy Signature Identified:** AI narrows location to a massive power draw. Data Viewer shows: zoomed-in satellite image of a building complex.
7. **2.3 — Blueprint Unlocked:** AI decrypts building schematic. Data Viewer shows: building blueprint with labeled rooms, highlighting "SERVER VAULT" in the center. AI explains: "A server vault is like a massive, heavily armored library for computers." Phase 2 COMPLETE.

**Phase 3: How is it protected? (3 sub-steps)**

8. **3.1 — Security Query:** Kid asks about the vault's security/defenses/alarms. AI begins decrypting security protocol files. Data Viewer shows: partially decrypted document with redacted sections.
9. **3.2 — Protocol Decrypted:** AI fully decrypts the security file. Data Viewer shows: animated diagram of a floor grid with safe/danger zones highlighted + short video/animation of the pressure-sensitive floor.
10. **3.3 — Mission Ready:** All intel gathered. AI delivers final briefing summary. Data Viewer shows: complete mission summary with all 3 discoveries listed, "MISSION INTEL COMPLETE" status.

### AI System Prompt Design

- **Role:** "IMF Central AI" — classified intelligence analysis system
- **Personality:** Friendly but professional. Uses spy/mission terminology. Addresses kids as "Agent [name]."
- **Dynamic context injection:** User's name, age, current phase/substep injected into system prompt per request
- **Age adaptation:**
  - Ages 4-7: Very simple words, short sentences, fun comparisons ("a recipe for computers")
  - Ages 8-9: Simple but slightly more detailed, briefly explains technical terms
  - Ages 10-12: More sophisticated language, can handle technical terms directly
- **Response format:** 1-3 sentences max. Includes `[ADVANCE]` marker when the kid demonstrates understanding to progress.
- **Hint escalation:** After 2-3 failed attempts without progress, AI gives increasingly direct hints
- **Safety guardrails (in system prompt):**
  - Stay in character at all times
  - Reject off-topic conversation: "That's outside my operational parameters, Agent."
  - Never reveal future-phase intel
  - Keep all responses under 3 sentences
  - No theological improvisation — stick strictly to mission narrative
  - Never ask for personal information
  - Never generate violent, scary, or inappropriate content

### Database Schema

```
users:          id, name, code (unique 4-digit), age, current_phase, current_substep, completed, timestamps
chat_history:   id, user_id (FK), role, message, phase, substep, timestamp
unlocked_assets: id, user_id (FK), asset_key, phase, substep, unlocked_at
```

SQLite with WAL mode enabled for concurrent multi-user access.

### UI Layout

**Login Screen:**
- IMF logo centered, "AGENT LOGIN" header
- 4-digit code keypad (large touch-friendly buttons)
- On valid code: transition to main interface
- On invalid code: "Agent not recognized. Contact your handler."

**Main Interface (Split-Screen):**
- **Left Panel — Chat Terminal (40%):** IMF logo, agent name, progress bar, scrollable chat bubbles, streaming AI responses, large chat input
- **Right Panel — Data Viewer (60%):** Phase tabs, asset gallery (thumbnails), main display area (image/text/audio/video), locked assets shown as grayed placeholders with lock icons, glow animation on new unlocks

**Summary/Completion Screen:**
- Overlays when all 10 sub-steps complete
- Shows all 3 discoveries with unlocked assets
- "MISSION INTEL COMPLETE — Report to your handler for next orders"
- Full data viewer still accessible below

**Admin Page (/?page=admin):**
- Password-protected (default: imf2026)
- User CRUD (create, edit, delete agents)
- Bulk user creation (paste CSV: name,code,age per line)
- Reset individual or all progress
- View all agents and their current status

### Asset Manifest

```
assets/
  phase1/
    intercepted_msg_01.md    # "Compiling code... Version 7.4.1..."
    intercepted_msg_02.md    # "They'll never find it... it's something you RUN"
    intercepted_msg_03.md    # "Perfection through programming... source code complete"
    decoded_document.png     # Analysis document with highlighted keywords
    phase1_complete.png      # Phase 1 completion badge
  phase2/
    world_map_scan.png       # World map with energy heat signatures
    satellite_image.png      # Zoomed-in building complex
    vault_blueprint.png      # Server vault blueprint with labeled rooms
    phase2_complete.png      # Phase 2 completion badge
  phase3/
    encrypted_protocol.png   # Partially decrypted security document
    floor_grid_diagram.png   # Pressure-sensitive floor grid layout
    floor_grid_video.mp4     # Short walkthrough animation of floor grid
    phase3_complete.png      # Phase 3 completion badge
  sounds/
    message_beep.mp3         # New message notification
    unlock_chime.mp3         # Intel unlocked sound
    scan_sweep.mp3           # Scanning/processing sound
    phase_complete.mp3       # Phase completion fanfare
    typing_click.mp3         # Typewriter keystroke sound
  imf_logo.svg               # IMF logo (copied from keypad app)
```

**Note:** Image/audio/video assets are currently placeholder files. Replace with production assets before the event.

### App Architecture

```
code/intel-station/
  Dockerfile
  docker-compose.yml
  requirements.txt
  .env / .env.example
  src/
    app.py                    # Streamlit entry point, routing, CSS theming
    pages/
      login.py                # Keypad login screen
      main.py                 # Split-screen chat + data viewer
      admin.py                # Admin panel
    services/
      agent_service.py        # Strands Agent + Ollama integration
      database_service.py     # SQLite CRUD (WAL mode for concurrency)
      progress_service.py     # Phase advancement logic
      asset_service.py        # Asset manifest and media serving
    models/
      user.py, chat.py, asset.py  # Dataclass models
    config/
      settings.py             # App config (env vars)
      phases.py               # Phase/substep definitions with asset mappings
      system_prompt.py        # AI system prompt template
    utils/
      audio.py                # Sound effect helpers (HTML/JS injection)
  assets/                     # All media assets
  data/                       # SQLite DB (created at runtime)
```

### Docker Deployment

- Ollama runs externally at 192.168.4.104:11434 — the app container just connects to it
- `docker-compose up` starts the Streamlit app on port 8501
- Volumes mount `assets/` and `data/` for persistence
- Access the app at `http://<host>:8501`
- Access admin at `http://<host>:8501/?page=admin`
