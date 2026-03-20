# Week 7 · Phase 1 (Calendar week 7) — Module 3
## Brownfield capstone: cross-subsystem integration in Canvas LMS

> **Course rule:** Students do not hand-author implementation code. You may type prompts, edit markdown, run approved commands, and critique outputs.

## Preparation
Identify the **Canvas LMS** areas your feature or fix touches (e.g. Rails `app/` vs `ui/` vs `packages/` vs `gems/`). Skim [instructure/canvas-lms](https://github.com/instructure/canvas-lms) docs for any external integration your story needs (LTI, plugins, APIs). See [`../brownfield-project.md`](../brownfield-project.md).

## Session 1 — Monorepo-scale realities (Canvas)

- Boundaries inside one repo: server vs client packages, shared gems, build pipelines
- Using AI to draft a **subsystem map** (who calls whom; data and build order)
- Contracts: REST/GraphQL, events, plugin APIs—where upstream documents truth ([wiki](https://github.com/instructure/canvas-lms/wiki), `doc/`)

---

**Next class:** [`day-2.md`](day-2.md) — Session 2 (refactor or migration plan without hand-coding).

<% checklist
Canvas areas touched by your story identified (app, ui, packages, gems, …)
Subsystem map or integration sketch started with AI
Contract truth located (docs/wiki/code) for APIs or integrations you need
%>
