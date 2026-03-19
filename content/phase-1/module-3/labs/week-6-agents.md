# Week 6 Lab: Agents (Plan Across Worktrees)

## Agent workflow
1. Plan the worktree strategy
   - main branch strategy (what stays stable)
   - worktree branch strategy (isolated experiments)
2. Record verification steps
   - tests/linters/builds you will run
3. Produce a diff summary
   - describe changes without pasting large code blocks

## Iteration protocol
1. Iteration 1 (conservative)
   - Choose a refactor goal that you can verify confidently
   - Draft a verification checklist and an initial diff summary approach
2. Iteration 2 (refine boundaries)
   - Tighten commands so they are reproducible
   - Make the verification steps more specific to what could break
   - Update the diff summary template to fit your refactor style

## Submission checklist
- `week-6-context-management.md`
- `week-6-markdown-memory.md`
- Diff summary template (embedded or separate)

## Reflection
- What failure mode did worktrees prevent for you?
- How will you keep AI edits reviewable and bounded?

