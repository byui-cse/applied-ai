# Week 5: Extended Tools - MCP-First Navigation and Traceable Refactors

## Learning objectives
- Understand how Model Context Protocol (MCP) can provide structured tool access
- Design a tool-first task plan that produces traceable edits
- Reduce "guessing" by requiring tool outputs to back up changes

## Key ideas
- MCP helps standardize tool interfaces and expected data formats
- A traceable refactor ties: intention -> evidence -> change -> verification
- Tools are more reliable when you specify contracts and boundaries

## Lab: Tool contracts + trace log
1. Write `lab/week-5/tool-contracts.md` with 2-4 tool contracts (examples: "search symbol", "read file range", "run tests", "create diff/patch plan")
2. For one tool contract, specify: inputs, outputs, error modes, and how you want the LLM to react to failure
3. Create `lab/week-5/trace-log.md` for a chosen refactor task with sections:
   - Intent
   - Evidence collected (what tools were called and what they returned)
   - Proposed change summary
   - Verification steps
4. Write 1 "traceable prompt" that tells the model to only propose changes after collecting evidence via the contracts

## Submission checklist
- `tool-contracts.md`
- `trace-log.md`
- A short "before vs after" note: what changed in your workflow when tools became first-class

## Reflection questions
- Where did you previously allow the model to speculate?
- How should tool outputs be summarized to stay context-efficient?

