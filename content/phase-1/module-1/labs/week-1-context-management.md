# Week 1 Lab: Context Management (Context Budgets)

A context budget is a constraint you design for, not a limitation you react to.

## What you're doing
- Pick one realistic brownfield task
- Define what context is required to produce the outputs
- Explicitly exclude anything that shouldn’t affect the result

## Step-by-step
1. Pick a realistic task (examples: `rename a symbol safely`, `add a new feature flag`, `fix a bug in a small subsystem`).
2. Create your context budget using these sections:
   - Task Summary
   - Relevant Files (initial guess)
   - Required Outputs
   - Exclusions
3. First iteration (conservative context)
   - Use only the information listed in `Relevant Files` that you believe is sufficient.
   - Do not include extra surrounding code, logs, or design notes "just in case".
4. Second iteration (expanded context)
   - Expand `Relevant Files` slightly (add 1-3 more targets, or broaden to adjacent modules that plausibly affect the outputs).
   - Keep `Exclusions` the same unless you can explain why a previously excluded piece of context improved output quality.
5. Update the budget
   - Remove any context that did not change output quality.
   - Record what you learned (short, specific, and tied to the iterations above).

## Deliverables
- A filled-in, final context budget (after iteration 2)

## Reflection
- Where did you accidentally include "too much" context?
- Which exclusions turned out to be safe (and why)?
