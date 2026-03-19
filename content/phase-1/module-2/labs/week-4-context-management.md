# Week 4 Lab: Context Management (Cache + Debt Boundaries)

Caching and technical debt work reduces tokens only when you are explicit about what can go stale and when you will re-check.

## Context budget goals
- Include enough system context to propose a sensible cache layer
- Include enough workflow context to propose a verification-first plan
- Exclude anything that would encourage “guessing” about invalidation or evidence

## What to include
- The subsystem you are caching (its responsibilities and where recomputation happens)
- The cache layers you plan to use (summaries, extracted facts, tool outputs, decision outcomes)
- Invalidation rules you can explain in plain terms
- For debt items: symptom, suspected cause, evidence link(s), and risk level

## What to exclude
- Unrelated parts of the codebase that you cannot connect to the cache keys/invalidation rules
- “Maybe” invalidation rules that are not tied to observable triggers
- Debt items without evidence or a concrete next action

## Iteration protocol
1. Iteration 1 (conservative)
   - Propose a cache plan with clear cache keys and explicit invalidation rules
   - Draft 3-6 debt items with evidence links and a recommended next action
   - Add propose-plan and verification steps for one debt item
2. Iteration 2 (tighten boundaries)
   - Reduce cache scope to only what the invalidation rules can support
   - Strengthen evidence links and make “verification steps” specific (tests/checks)
   - Remove any assumptions that are not covered by the plan

## Reflection
- Which part of the workflow is easiest to automate safely?
- What would convince you that cached information is stale?

