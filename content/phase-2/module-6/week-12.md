# Week 12: Autonomous Agents - Single-Agent Tool Loops with Guardrails

## Learning objectives
- Design an agent loop that uses tools safely and predictably
- Force structured outputs so results can be verified
- Add guardrails to prevent runaway actions

## Key ideas
- An agent is an orchestration pattern: plan -> act -> observe -> refine
- Guardrails should be engineered constraints (limits, schemas, verification steps)
- Structured outputs let you validate without reading everything manually

## Lab: Agent loop + structured output schema
1. Write `lab/week-12/agent-loop.md` describing:
   - initial planning step
   - tool call step(s)
   - observation step(s)
   - decision step (continue/stop)
2. Add guardrails:
   - max steps
   - max tool calls
   - what to do when evidence is insufficient
3. Define a structured output schema for the agent (examples: `plan`, `evidence`, `diff_summary`, `verification_steps`, `risk_notes`)
4. Write one sample agent run transcript (short) showing how the schema would look after success

## Submission checklist
- `agent-loop.md`
- Structured output schema (embedded or separate)
- One sample "success transcript"

## Reflection questions
- Which guardrail is most important for safety vs quality?
- How will you detect infinite loops early?

