# Labs · Phase 1 Week 2 (Calendar week 2)

- **[Lab 3 — Implementation research & requirements](lab-3.md)** (feature analysis, requirements, testing plan)

---

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

<% checklist
Verbose baseline prompt captured for one real Canvas question
AI audit classified essential vs nice-to-have content
Bulk pastes replaced with path + line range + question pointers
Compared verbose vs optimized runs; noted which answer was more actionable
Before/after write-up ties choices to your context budget
%>

