My 'code/intel-station/' app is not working this way. I have decided there is no reason to use an LLM at all. I want a more deterministic approach. Make a plan to remove the LLM approach altogether and replace it with a graph tree of questions that lead to unlocked intel.

Build a comprehensive plan for this new design:

## The Chat Terminal

I want to convert this to a more conventional game structure, but with a simulated chat-like experience. Instead of a chat history that keeps track of messages and an open-ended chat box, update the chat input to just be the area where the questions appear. We will still start with the same 2 questions to start the game, but each question will direct to a very specific piece of intel and a set of 3 new questions. More on that in the "Game Progression" section. In the area that is currently a list of messages, I want the answer to the message to appear in the center of the section much like the empty chat history message shows now. However, make this message appear a few characters at a time and after a very short delay as if it were the response from a complicated search through terabytes of data - to simulate an AI response.

## The Data Viewer

The data viewer continues to function like it does now. As intel is uncovered, it should become available for the user to select and view in the data viewer section.
However, here is where one of the major changes to the project is needed. All of the '.md' files in the phase1-skills, phase2-skills, and phase3-skills directories need to be formatted into structured data. They already have some form of structure, but it needs to be locked in so that we can have code that parses the file into a cool UI design for each of the different categories of intel. 

You will need to create a render function for each type of intel as noted by its prefix. When the intel is selected in the Data Viewer, it must use the appropriate render function based on the intel type.

I also want the Data Viewer to separate intel into the different phases so that when phase 1 is complete, those intel categories are collapsed out of view to simplify the view, and the conclusion that the player came to (see "Completing "Phases"" section below) should appear for that phase.

The new phase should only appear after a phase is complete. The phases should be collapsible in an accordion style UI in the Data Viewer section.

## Game Progression

The new game progression will be entirely deterministic. We will need some kind of graph or database structure that defines which question leads to which intel. Here is an example of what this means:
First 2 questions:
1. What is the Light?
2. Who is the Architect?

Clicking question 1 connects to 1 or 2 pieces of intel, a summary of the intel, and 3 pre-determined questions that flow naturally based on that intel. Each of those 3 questions then leads to more intel and more questions. Some of the questions should eventually lead to dead ends, where the "AI" responds with something like "I'm sorry, I cannot find any more information on that subject." and then returns the other questions the agent hasn't clicked yet.

All of this becomes completely deterministic and laid out in some sort of structured data that I can easily update as needed to fix the flow of the game whenever I need to.

I think we can also remove the idea of having phases broken up into stages. It might be simple enough to have specific intel marked as critical so that when the player has unlocked all critical intel for a phase, they move on to the next phase and when they have completed all phases, they have won the game.

## Completing "Phases"

When the player gathers all critical intel for a phase, one of the "recommended prompts" should have something like, "The Light isn't a thing at all. It's Software!" so that when the player selects it, they are confirming they understand that phase's intention. Then the next "recommended prompts" begin the next phase.