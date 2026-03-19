# Week 11 Lab: Agents (Integrate + Fail Gracefully)

## Agent workflow
1. Identify the workflow step the plugin supports
2. Integrate the plugin call with:
   - required preconditions
   - postconditions you will verify
   - failure behavior (fallback plan)
3. Add measurement so you can evaluate and improve the plugin integration
4. Produce an operator note so humans know when to override outputs

## Iteration protocol
1. Iteration 1 (conservative)
   - Basic integration: preconditions, postconditions, fallback
   - Measurement signals present but minimal
2. Iteration 2 (graceful degradation + measurement)
   - Improve what happens on failure (fallback is actionable)
   - Make postconditions clearer and easier to verify
   - Refine measurement so it matches your reality

## Submission checklist
- `week-11-context-management.md`
- `week-11-markdown-memory.md`
- measurement plan (embedded or separate)

## Reflection
- What plugin failures are recoverable vs not?
- What would you automate next to reduce human overhead?

