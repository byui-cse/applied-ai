# Brownfield codebase: Canvas LMS

**Repository:** [instructure/canvas-lms](https://github.com/instructure/canvas-lms)  
**Upstream:** Open-source learning management system (LMS) by Instructure, Inc.  
**License:** [AGPL-3.0](https://github.com/instructure/canvas-lms/blob/master/LICENSE) — review obligations before redistributing modified versions.

## Why this project

Canvas LMS is a **large, real-world brownfield** codebase: Ruby and Rails–backed server code, substantial JavaScript/TypeScript front-end (`ui/`, `packages/`), vendored gems, and rich domain concepts (courses, assignments, grading, integrations). It is an authentic setting for **context budgeting**, AI-assisted navigation, and scoped features or bug fixes **without students hand-authoring implementation** in this course—AI proposes changes; students verify, steer, and document.

## What students should do

- **Clone** the repo early in Phase 1 and keep a **local fork or branch** per your course policy.
- **Scope** work to issues or features your instructor approves (labels, difficulty, area of the tree).
- **Use** upstream docs (e.g. [`README.md`](https://github.com/instructure/canvas-lms/blob/master/README.md), [project wiki](https://github.com/instructure/canvas-lms/wiki), [`CONTRIBUTING.md`](https://github.com/instructure/canvas-lms/blob/master/CONTRIBUTING.md)) for setup expectations—installation is non-trivial; time-box local runs as your syllabus allows.
- **Respect** institutional security: no production secrets; no scraping private instances; use public issue descriptions and local/dev data only.

## Pointers for AI-assisted work

- The repo includes **AI-oriented guidance** at the root (e.g. `AGENTS.md`, `CLAUDE.md`—filenames may evolve); treat these as **starting prompts**, not ground truth.
- **High-level layout** (indicative, not exhaustive): `app/` (Rails), `config/`, `ui/` and `packages/` (front-end), `gems/`, `gems/plugins/`, `spec/`, `doc/`, Docker and tooling under `docker-compose/`, `bin/`, etc.
- **Boundaries** matter: pick a **vertical slice** (e.g. one feature area, one package) for context packs and labs so prompts stay under your context budget.

## Relationship to course content

All Phase 1 weekly plans (`phase-1/week-*`) and labs assume this repository unless otherwise noted. Greenfield work in Phase 2 is **separate** from Canvas unless you explicitly tie them for a portfolio.
