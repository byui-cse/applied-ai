# Lab · Phase 1 Week 7 (Calendar week 7)
## Brownfield capstone: cross-subsystem integration in Canvas LMS

**Codebase:** [Canvas LMS](https://github.com/instructure/canvas-lms) · [`../../brownfield-project.md`](../../brownfield-project.md)

### Goal
Deliver a **Canvas LMS integration & refactor plan** (AI-generated, human-verified) for an instructor-approved slice (feature or bug).

### Steps

1. AI drafts a map across relevant **Canvas** areas (e.g. `app/`, `ui/`, `packages/`, `gems/`): dependencies, build order, runtime touchpoints.
2. Identify top 5 failure modes for *your* slice; add **verification** steps per mode.
3. Propose a phased rollout with **rollback** triggers.
4. Optional: use MCP + worktrees together for evidence gathering on your clone.

### Definition of done
Plan readable by a tech lead in 10 minutes; includes unknowns and next actions; grounded in paths under [instructure/canvas-lms](https://github.com/instructure/canvas-lms).
