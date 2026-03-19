# Week 3 Lab: Context Management (Architectural Memory)

This week is about reducing repeated reasoning by separating:
- short-term context (the current task)
- long-term architectural knowledge (memory artifacts you update over time)

## Context budget goals
- Include only a small task brief for each new request
- Bring in stable memory artifacts that teams can reuse
- Avoid re-sending raw files unless your memory artifacts explicitly call for evidence refresh

## What to include
- A small task brief (what you are asked to do)
- The long-term memory artifacts from your memory file:
  - `architecture-summary` (what the system is and how pieces connect)
  - `key-decisions` (decision log with why)
  - `known-risks` (risk register and why)
- When needed: the minimum evidence required to update memory (per your update policy)

## What to exclude
- Large raw file dumps that duplicate what is already in memory
- Speculation that contradicts what your memory artifacts state
- Decisions that require new evidence but are not supported by it

## Iteration protocol
1. Iteration 1 (answer with existing memory)
   - Use only the small task brief + your memory artifacts
   - Produce an answer using structured summaries, not repeated derivations
2. Iteration 2 (update memory with evidence)
   - After completing the task, decide what changed
   - Update memory artifacts according to your update-policy rules
   - Add evidence-backed revisions while keeping stable facts stable

## Reflection
- What information should never be regenerated from scratch?
- What update rule will you enforce to prevent stale memory?

