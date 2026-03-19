# Week 1 Lab: Agents (Two-Iteration Protocol)

Even if you are not using tools yet, "agents" show up as a workflow: repeat attempts with a defined interface and measurable constraints.

## What this lab is
- Use the prompt contract + context budget as the interface between you and the model/agent
- Run two agent-style iterations:
  1. conservative context
  2. slightly expanded context
- Update the budget based on what changed output quality

## Step-by-step
1. Define the agent protocol (use this checklist every time)
   - First, confirm you understand the task summary
   - If required information is missing, ask clarification questions using the missing-info protocol from your prompt contract
   - Produce output that matches the exact output format
2. Iteration 1 (agent run with conservative context)
   - Provide only your conservative `Relevant Files`
   - Keep `Exclusions` enforced
   - Record what the agent produced and what assumptions it had to make
3. Iteration 2 (agent run with expanded context)
   - Add a small amount of additional relevant context
   - Keep `Required Outputs` unchanged
   - Record differences versus iteration 1:
     - Did quality improve?
     - Did the agent make fewer assumptions?
     - Did the output align better with your expected format?
4. Update the context budget
   - Remove any context that did not change output quality
   - Add any new context that proved necessary

## Submission checklist
- `week-1-context-management.md` (final context budget after iteration 2)
- `week-1-markdown-memory.md` (updated prompt contract)
- A short note: "What I would include next time, and why"

## Reflection questions
- Where did you accidentally include "too much" context?
- What instruction or output format improved consistency the most?
