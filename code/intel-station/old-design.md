

We need to rebuild/restructure how this app works.
Eliminate the `query_intel` tool entirely and the idea of a knowledge base. 
The agent should not be instructed to guide the user. Instead, the agent should be limited on what knowledge it actually possesses. This will keep context to a minimum and make sure it doesn't reveal too much too soon.


When a phase is completed, we should clear the agent context, and instead only include a summary of what was learned in the completed Phases.

All agent responses should be returned as structured output to clearly mark what information has been uncovered and to offer directions for the user to go.
Here is what needs to be included in each response:
- summary of the intel retrieved
- list of paths to intel files that were unlocked
- list of 2 or 3 suggestions for the user to proceed with further investigation


Initial Agent prompt should be extremely bare bones. 
Add a Phase 0 prompt for the Agent which tells it that it knows almost nothing about the Light until we dive into intel.
Responses from the agent must be extremely short. 


For younger kids, we won't even show a chat box. The agent will always respond with 3 leading options for the user to ask about and they will just select which one they want to do. Example response:
> If you'd like I can: 
> 1. Review field reports for mentions of the Light.
> 2. Review surveillance documentation
> 3. Check intercepted communications for anything relevant.

For older kids, keep it more open ended allowing the kid to ask the next question.
