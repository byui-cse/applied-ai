# Week 5 Lab: Context Management (Tool-First Evidence)

The point of tool-first workflows is to avoid speculation. Your context budget should be “evidence-shaped”: include the minimal inputs the tool contracts require, and exclude everything that encourages guessing.

## Context budget goals
- Keep tool calls grounded in explicit contracts (inputs/outputs/error modes)
- Include enough evidence to justify each proposed change
- Reduce prompt bloat by recording tool outputs in a trace log instead of re-sending raw data

## What to include
- A chosen refactor task brief (the intent)
- Tool contracts you will rely on (2-4 contracts)
- For each tool call in your workflow:
  - what inputs you passed
  - the expected output shape
  - the actual returned evidence (summarized into the trace log)
- Verification steps (tests/checks you will run)

## What to exclude
- Large raw logs or full file dumps that you do not actually use as evidence
- Proposed changes before evidence is collected
- Vague error handling (always specify how the workflow reacts to failures)

## Iteration protocol
1. Iteration 1 (conservative)
   - Use fewer tool contracts
   - Produce a trace log that clearly maps: intention -> evidence -> change -> verification
2. Iteration 2 (improved reliability)
   - Refine one tool contract’s inputs/outputs/error modes
   - Improve how you summarize tool output into trace-log evidence (less irrelevant text)

## Reflection
- Where did you previously allow the model to speculate?
- How should tool outputs be summarized to stay context-efficient?

