# Week 12 Lab: Context Management (Guardrails for Tool Loops)

Structured, bounded agent loops prevent runaway actions and make results verifiable.

## Context budget goals
- Include only what the agent needs to plan, act, observe, and decide
- Exclude open-ended instructions that encourage indefinite exploration
- Keep guardrails and schemas in-context so outputs remain checkable

## What to include
- Initial planning step input
- Tool call steps you allow
- Observation/feedback steps
- Decision step: when to stop or continue
- Guardrails:
  - max steps
  - max tool calls
  - what to do when evidence is insufficient
- Structured output schema the agent must follow

## What to exclude
- Unbounded loops (“keep going until you feel done”)
- Tool calls without a corresponding observation/verification step

## Iteration protocol
1. Iteration 1 (conservative)
   - Draft the loop and include max-step / max-tool guardrails
   - Define a schema with the required fields
2. Iteration 2 (tighten safety + checkability)
   - Make “evidence insufficient” behavior explicit
   - Refine schema fields so they support verification (evidence, verification_steps, risk_notes)

## Reflection
- Which guardrail is most important for safety vs quality?
- How will you detect infinite loops early?

