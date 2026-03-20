# Lab · Phase 1 Week 2 (Calendar week 2)
## Token optimization & the ~20% context rule

**Codebase:** [Canvas LMS](https://github.com/instructure/canvas-lms) · [`../../brownfield-project.md`](../../brownfield-project.md)

### Goal
Cut a bloated prompt + attachment set by ~80% without losing task clarity.

### Steps

1. Start with an intentionally verbose prompt for a real **Canvas** question (e.g., “where is user/session authentication handled?” with pointers into `app/` or `config/`).
2. Use AI to **audit** your own prompt: classify sentences as essential vs nice-to-have.
3. Replace bulk pastes with **pointers**: path + line range + question.
4. Compare two runs: verbose vs optimized; record which produced the more actionable answer.

### Definition of done
Written before/after with a short rationale tied to token/context budget.

