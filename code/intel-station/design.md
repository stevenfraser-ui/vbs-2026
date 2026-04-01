

The SKILL.md 'description' should inform the agent that they are strictly only to use this skill when the user asks a question containing very specific key words.

When a phase is completed, we should clear the agent context, and instead only include a summary of what was learned in the completed Phases.

All agent responses should be returned as structured output to clearly mark what information has been uncovered and to offer directions for the user to go.
Each skill should specifically mention the intel that is being unlocked and displayed in the "Data Viewer"

Initial Agent prompt should be extremely bare bones. 
Add a Phase 0 prompt for the Agent which tells it that it knows almost nothing about the Light until we dive into intel.
Responses from the agent must be extremely short. 


For younger kids, we won't even show a chat box. The agent will always respond with 3 leading options for the user to ask about and they will just select which one they want to do. Example response:
> If you'd like I can: 
> 1. Review field reports for mentions of the Light.
> 2. Review surveillance documentation
> 3. Check intercepted communications for anything relevant.

For older kids, keep it more open ended allowing the kid to ask the next question.

New skills/kb structure:
phase1-skills/
- codenames/
  - SKILL.md
  - references/
    - codename_registry_decrypted.md
    - codename_registry_partial.md
- field-reports/
  - SKILL.md
  - etc...
phase2-skills/
phase3-skills/

Each category of intel becomes a skill. This skill "guards" the intel docs with specific requirements that need to be met before it will release each document to the user. Once the document is released, it should be available in the "Data Viewer".