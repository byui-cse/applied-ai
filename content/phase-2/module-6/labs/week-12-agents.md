# Week 12 Lab: Agents (Tool Loop with Guardrails)

## Agent workflow
1. Plan
   - Create an initial plan
2. Act
   - Make allowed tool call(s)
3. Observe
   - Collect evidence from observations
4. Decide
   - Continue or stop based on evidence sufficiency and guardrails
5. Output (schema-shaped)
   - Produce structured output that includes plan, evidence, diff_summary, verification_steps, risk_notes

## Iteration protocol
1. Iteration 1 (conservative)
   - Draft loop with max steps/tool calls
   - Draft schema and ensure every field has a purpose
   - Create a minimal “success transcript”
2. Iteration 2 (tighten safety)
   - Make evidence-insufficient behavior explicit
   - Refine schema fields so they can be validated without reading everything manually

## Submission checklist
- `week-12-context-management.md`
- `week-12-markdown-memory.md`
- One sample "success transcript"

## Reflection
- Which guardrail is most important for safety vs quality?
- How will you detect infinite loops early?

