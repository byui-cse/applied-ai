# Week 4 Lab: Agents (Propose -> Verify -> Record)

Treat your agent workflow like an engineered pipeline:
- propose a plan
- verify it with evidence
- record outcomes so future work is traceable

## Agent protocol
1. Propose
   - Draft the cache plan (cache keys + invalidation rules)
   - Draft a debt tracker with evidence and risk level
2. Verify
   - For the selected debt item, list tests/checks you will run
   - Specify what success looks like
3. Record
   - Capture what changed and why
   - Note any follow-up debt items that remain

## Iteration protocol
1. Iteration 1 (conservative)
   - Keep cache scope tight
   - Verification steps should be generic but present
2. Iteration 2 (improved boundaries)
   - Make invalidation rules and verification steps more concrete
   - Remove assumptions not backed by evidence you can verify

## Submission checklist
- `week-4-context-management.md`
- `week-4-markdown-memory.md`
- A short note: "What I would include next time, and why"

## Reflection
- Which part of the workflow is easiest to automate safely?
- What would convince you that cached information is stale?

