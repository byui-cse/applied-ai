# Week 5 Lab: Agents (Tool Contracts as Interfaces)

Treat each tool contract like an interface that constrains the agent.

## Agent workflow
1. Start with intent
   - Define what you want to change (intent)
2. Collect evidence via tool contracts
   - For each required piece of info, call the relevant tool contract
   - Summarize results into `trace-log.md`
3. Propose changes only after evidence
   - Use the traceable prompt logic: no evidence, no proposals
4. Verify before accepting
   - List tests/checks and record what happens

## Iteration protocol
1. Iteration 1 (conservative)
   - Use 2 tool contracts
   - Produce a trace log and a traceable prompt that enforces evidence-first behavior
2. Iteration 2 (expanded reliability)
   - Add 1-2 more tool contracts as needed
   - Improve error-mode handling and evidence summarization

## Submission checklist
- `week-5-context-management.md`
- `week-5-markdown-memory.md`
- A short "before vs after" note: what changed in your workflow

## Reflection
- Where did you previously allow the model to speculate?
- How should tool outputs be summarized to stay context-efficient?

