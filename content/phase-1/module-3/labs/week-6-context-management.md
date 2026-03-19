# Week 6 Lab: Context Management (Bounded Diffs with Worktrees)

Worktrees help you avoid context creep by separating experiments into isolated branches. Your context budget should still be explicit: include only what’s needed to make the refactor plan and verification steps correct.

## Context budget goals
- Keep each iteration bounded to the intended refactor scope
- Include only the information needed to plan changes and run verification
- Exclude unrelated diffs and large raw outputs; summarize results into the plan

## What to include
- The chosen refactor goal (what success means)
- The workflow rules:
  - what stays stable on main
  - what experiments live on worktrees
- A verification checklist you can run to confirm the refactor goal
- A “diff summary” description of changes without dumping large blocks into prompts

## What to exclude
- Large code blocks you do not need for planning
- Any command sequence that is not part of your recorded workflow
- Unverified assumptions about how changes affect tests/linters/build

## Iteration protocol
1. Iteration 1 (conservative)
   - Keep the worktree experiment small
   - Use a minimal verification checklist that still proves your refactor goal
2. Iteration 2 (tighten boundaries)
   - Reduce scope if verification is too expensive
   - Make your diff summary more precise so review is easier

## Reflection
- What failure mode did worktrees prevent for you?
- How will you keep AI edits reviewable and bounded?

