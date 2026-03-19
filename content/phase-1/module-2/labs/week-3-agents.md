# Week 3 Lab: Agents (Memory-First Two Iterations)

## Agent protocol
Use your memory artifacts as the interface:

1. Confirm understanding of the new task using only a short task brief.
2. Generate your answer using ONLY:
   - your small task brief
   - the memory artifacts:
     - `architecture-summary.md`
     - `key-decisions.md`
     - `known-risks.md`
   - (optional) the minimum evidence required by `update-policy.md`
3. If required information is missing, ask clarification questions before proceeding.
4. After you finish the task, decide what changed and update memory using `update-policy.md`.

## Iteration protocol (two runs)
1. Iteration 1: use existing memory artifacts
   - Produce an answer using the current memory artifacts
   - Record your assumptions and any uncertainties
2. Iteration 2: update memory with evidence
   - Identify what facts changed or were wrong
   - Update `architecture-summary`, `key-decisions`, `known-risks` using evidence rules
   - Note what context tokens you would save vs re-including raw files

## Submission checklist
- `architecture-summary.md`
- `key-decisions.md`
- `known-risks.md`
- `update-policy.md`

## Reflection
- What information should never be regenerated from scratch?
- What update rule will you enforce to prevent stale memory?

