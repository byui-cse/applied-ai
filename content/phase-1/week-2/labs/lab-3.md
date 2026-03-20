# Lab 3 — Feature Specifications

You will **research** how to implement the Canvas feature you selected in [`day-1.md`](../day-1.md). This lab is about analysis, requirements, and verification planning—**not** writing production code.

**Prerequisites:** Complete [`lab-1.md`](../../week-1/labs/lab-1.md) (fork, EC2, Remote SSH) and [`lab-2.md`](../../week-1/labs/lab-2.md) (repository analysis agent in `agents/analyze-repo.md`). Your feature brief should live under `agents/tasks/feature-1/` as described on day 1.

---

## Goal

Produce a **research and requirements package** that ties your feature idea to the real Canvas LMS codebase: what must be true for the feature to succeed (functionally and non-functionally), how the system should behave at boundaries, and how you will **prove** the work later—without implementing the feature yet.

---

## Repository layout (required)

In your **fork** of the course repository, add or extend:

| Path | Purpose |
|------|--------|
| `agents/tasks/feature-1/implementation-research.md` | Single markdown file containing all sections below (design, functional and non-functional requirements, codebase findings, testing plan). |

You may reference `agents/tasks/feature-1/feature-1.md` for scope and problem statement; **do not duplicate** the pitch—link or summarize in one short paragraph, then focus on research.

---

## Minimum requirements

Your `implementation-research.md` must show how you satisfy **all** of the following. You are welcome to use AI to assist with the research, **however** I want you to have complete control and knowledge about all the decisions that you are committing to.

### 1. Design considerations

Document **design** choices and tradeoffs as if you were aligning engineering and product: user flows, data that crosses boundaries (APIs, jobs, permissions), UX risks, and how this feature interacts with existing Canvas concepts (courses, users, roles, etc.).

> Note: in **Lab 4** you will implement an **MCP** that connects to **GitHub Projects** to keep the **project plan** in sync with your work. You do **not** build that integration in this lab—only capture **what** you will want the plan to track (milestones, tasks, dependencies, definition of done) so Lab 4 can automate it sensibly.

### 2. Functional requirements

List **functional requirements** in testable form (given/when/then or numbered “the system shall…” statements). Tie each requirement to **user-visible or system-visible behavior**, not to a specific file or framework.

Include **in scope** vs **out of scope** boundaries so scope creep is visible early.

### 3. Non-functional requirements

Cover what matters for this feature beyond “it works once”: performance expectations, security and privacy (FERPA-adjacent thinking for education data), accessibility, observability (logging/metrics), reliability, and compatibility with Canvas deployment assumptions you can infer or cite.

### 4. Codebase analysis using your Lab 2 agent

Use the **repository analysis agent** you specified in Lab 2 (`agents/analyze-repo.md`; see [`lab-2.md`](../../week-1/labs/lab-2.md)) against **Canvas LMS** (your fork clone).

In `implementation-research.md`, record:

- **Hypotheses** about where change will land (areas of the repo: engines, APIs, React bundles, jobs, etc.).
- **Concrete findings** from agent-assisted exploration: representative paths, subsystems, extension points, or patterns Canvas already uses that you will follow.
- **Open questions** that still need a spike or stakeholder input—clearly labeled.

The goal is to show **traceability** from requirements to likely code locations and unknowns, not exhaustive line-by-line reading.

### 5. Testing and verification plan

Build a **solid** plan for how you will know the feature is correct and safe **before** you write implementation code. Include:

- **Unit-level** expectations (what logic deserves isolated tests).
- **Integration** points (API, DB, external services if any).
- **Manual / exploratory** checks (roles, edge cases, regression of nearby flows).
- **Acceptance criteria** mapped back to your functional requirements.

If automated testing is impractical for some areas, say why and what you will do instead (checklists, feature flags, staged rollout—at the planning level).

---

## What you turn in

- **`agents/tasks/feature-1/implementation-research.md`** meeting the minimum requirements above.
- Evidence that you **used** your Lab 2 workflow (for example, short excerpts of index output or script logs you are willing to share, or a “session notes” subsection—no secrets).

---

## Template (optional)

You may start from this outline and replace the placeholders.

<% editor markdown "# Feature (one-line)\n\n# Link to feature brief\n\n# Design considerations\n\n## Lab 4 handoff (GitHub Projects / MCP)\n\n# Functional requirements\n\n## In scope\n\n## Out of scope\n\n# Non-functional requirements\n\n# Codebase analysis (Lab 2 agent)\n\n## Hypotheses\n\n## Findings\n\n## Open questions\n\n# Testing and verification plan\n\n## Unit\n\n## Integration\n\n## Manual / exploratory\n\n## Acceptance criteria map" %>

---

## What we intentionally omit

There is **no** implementation of the Canvas feature or the Lab 4 MCP in this lab. You are producing the **research and requirements** package that makes implementation and automated planning tractable later.

<% checklist
`implementation-research.md` exists with design considerations and Lab 4 planning handoff (GitHub Projects / MCP) noted
Functional requirements are testable; in/out of scope is explicit
Non-functional requirements cover security, performance, a11y, and operability as relevant
Lab 2 `analyze-repo` agent used against Canvas; hypotheses, findings, and open questions documented
Testing and verification plan ties unit, integration, manual, and acceptance criteria to requirements
No production feature code in this lab—research and planning only
%>

<% links
[Lab 1](../../week-1/labs/lab-1.md)
[Lab 2](../../week-1/labs/lab-2.md)
[Lab 4](labs/lab-4.md)
[Day 1 — feature selection](../day-1.md)
%>
