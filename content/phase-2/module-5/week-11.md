# Week 11: Extensibility - Integrate Plugins into Real Workflows

## Learning objectives
- Orchestrate plugin usage inside a development flow
- Add measurement so plugins can be evaluated and improved
- Design safe fallback and graceful degradation

## Key ideas
- A plugin is useful only when it is integrated into a workflow with verification
- "Fallback behavior" prevents cascading failures in agent systems
- Measurement turns subjective quality into actionable signals

## Lab: Workflow integration + fallback
1. Choose a workflow step that your plugin will support (examples: "locate relevant code", "validate a proposed diff", "run a focused test")
2. Write `lab/week-11/plugin-workflow.md` with:
   - where the plugin is called
   - required preconditions (what must be true before call)
   - postconditions (what must be verified after call)
   - what happens on failure (fallback plan)
3. Add a simple measurement plan: what signals you will record (latency, pass/fail, success rate, token usage)
4. Write one "operator note" for humans: how to interpret plugin outputs and when to override them

## Submission checklist
- `plugin-workflow.md`
- measurement plan (embedded or separate)

## Reflection questions
- What plugin failures are recoverable vs not?
- What would you automate next to reduce human overhead?

