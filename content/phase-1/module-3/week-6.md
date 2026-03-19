# Week 6: Extended Tools - Worktrees for Safe Parallel Refactors

## Learning objectives
- Use git worktrees to isolate refactors and keep rollbacks safe
- Maintain a clean workflow for multi-step AI-assisted edits
- Reduce the risk of "accidental context creep" by controlling diffs

## Key ideas
- Worktrees let you run parallel experiment branches without losing your mainline
- AI changes should be reviewable: small diffs + clear intent
- Rollback discipline is part of engineering, not just version control

## Lab: Parallel refactor plan with worktrees
1. Pick a refactor goal that can be tested (examples: extract a module, rename types, reduce coupling, introduce an adapter)
2. Write `lab/week-6/worktree-plan.md` with:
   - main branch strategy (what stays stable)
   - worktree branch strategy (what experiments are isolated)
   - verification checklist (tests/linters/builds you will run)
3. In your lab plan, include the exact git workflow you will follow (commands as text), e.g. create worktree, make changes, run tests, record result
4. Produce a "diff summary" section: how you will describe changes without pasting large code blocks into prompts

## Submission checklist
- `worktree-plan.md` (with commands + verification checklist)
- Diff summary template (2-3 paragraphs)

## Reflection questions
- What failure mode did worktrees prevent for you?
- How will you keep AI edits reviewable and bounded?

