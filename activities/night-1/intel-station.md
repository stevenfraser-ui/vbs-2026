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

### To Be Filled in Later

- The specifics of the fictional information the AI will unlock.
- Images, audio and video bytes to display as they progress. (For now, just generate an 'assets/' directory the code refers to)
