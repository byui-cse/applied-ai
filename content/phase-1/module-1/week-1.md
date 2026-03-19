# Week 1: Context & Efficiency - Prompt Contracts and Context Budgets

## Learning objectives
- Design a repeatable prompt contract for development tasks
- Stay under a strict context budget by choosing what to include and what to exclude
- Turn "LLM instructions" into engineering artifacts you can reuse

## Key ideas
- A context budget is a constraint you design for, not a limitation you react to
- Markdown is your "structured memory layer" for requirements, plans, and diffs
- Token optimization is mostly about scope control (not clever wording)

## Lab: Build a context budget + prompt contract
1. Pick one realistic brownfield task (examples: "rename a symbol safely", "add a new feature flag", "fix a bug in a small subsystem")
2. Create `lab/week-1/context-budget.md` with these sections: Task Summary, Relevant Files (initial guess), Required Outputs, Exclusions
3. Write a prompt contract template in `lab/week-1/prompt-contract.md` that includes: inputs you will provide, the exact output format you want, and how the model should ask for missing info
4. Run 2 prompt iterations: first with a conservative subset of context, then with a slightly expanded subset; record which parts mattered
5. Update the budget: remove anything that did not change the output quality

## Submission checklist
- `context-budget.md` (final, after iteration 2)
- `prompt-contract.md` (versioned or clearly updated)
- A short note: "What I would include next time, and why"

## Reflection questions
- Where did you accidentally include "too much" context?
- What instruction or output format improved consistency the most?

