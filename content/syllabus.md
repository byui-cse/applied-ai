# Applied AI for Software Engineering

**Credits:** 2 · **Format:** Two meetings per week · **Duration:** 14 weeks  
**Audience:** Juniors and seniors in computing-related programs  

## Course premise

Students **do not hand-author implementation code**. All design, exploration, refactoring, scaffolding, testing ideas, and documentation are produced **through collaboration with AI tools** (IDE assistants, chat interfaces, agents, MCP-connected tools, etc.). The course trains *judgment*: scoping work, verifying outputs, managing context, and shipping outcomes safely on brownfield and greenfield systems.

## Learning outcomes

By the end of the term, students should be able to:

1. **Budget and shape context** for large existing codebases using markdown artifacts, concise prompts, and selective file inclusion—aiming to keep high-signal context **under roughly 20%** of available window where practical.
2. **Describe architectural and debt state** to an AI partner using structured notes, caches, and repeatable “state refresh” rituals.
3. **Use extended tooling** (e.g., MCP, worktrees, multi-root workspaces) to navigate, compare, and refactor **Canvas LMS** without losing track of changes.
4. **Stand up greenfield projects** that are *AI-ready*: clear boundaries, conventions, skills/rules, and extension points—generated and iterated via AI, not typed line-by-line.
5. **Extend LLM behavior** with plugins/tools and **orchestrate agents** (single- and multi-agent) for specialized dev tasks.
6. **Integrate workflows** that combine multiple agents and MCP capabilities toward a **production-minded greenfield MVP** (definition of done, risks, and demo).

## Phase overview

| Phase | Weeks (calendar) | Theme | Modules |
|------|------------------|--------|---------|
| **Phase 1** | 1–7 | Brownfield — [Canvas LMS](https://github.com/instructure/canvas-lms) | 1–3 |
| **Phase 2** | 8–14 | Greenfield (new systems) | 4–7 |

### Module map

| Module | Focus |
|--------|--------|
| **1 — Context & efficiency** | Markdown systems, staying under ~20% context, token optimization for large codebases |
| **2 — Architectural state** | “Memory” for the project, caching strategies, technical debt management with AI |
| **3 — Extended tools** | MCP, worktrees, cross-subsystem navigation in Canvas (e.g. `app/`, `ui/`, `packages/`, `gems/`) and refactor planning |
| **4 — Foundations & skills** | Core AI software engineering habits; clean, AI-ready architecture from scratch |
| **5 — Extensibility** | Plugins and integrations that extend LLM capabilities in a new application |
| **6 — Autonomous agents** | Single- and multi-agent designs for specialized development work |
| **7 — Advanced workflows** | Orchestration, complex MCP usage, MVP hardening and demo |

## Weekly index

Content paths use **phase-local week numbers** (`phase-1/week-1` … `phase-2/week-7`). Calendar mapping:

| Calendar week | Phase | Folder | Module |
|---------------|-------|--------|--------|
| 1 | 1 | `phase-1/week-1` | 1 |
| 2 | 1 | `phase-1/week-2` | 1 |
| 3 | 1 | `phase-1/week-3` | 2 |
| 4 | 1 | `phase-1/week-4` | 2 |
| 5 | 1 | `phase-1/week-5` | 3 |
| 6 | 1 | `phase-1/week-6` | 3 |
| 7 | 1 | `phase-1/week-7` | 3 (capstone) |
| 8 | 2 | `phase-2/week-1` | 4 |
| 9 | 2 | `phase-2/week-2` | 4 |
| 10 | 2 | `phase-2/week-3` | 5 |
| 11 | 2 | `phase-2/week-4` | 5 |
| 12 | 2 | `phase-2/week-5` | 6 |
| 13 | 2 | `phase-2/week-6` | 6 |
| 14 | 2 | `phase-2/week-7` | 7 (integration) |

## Grading (suggested)

| Component | Weight (example) | Notes |
|-----------|------------------|--------|
| Phase 1 portfolio | 35% | **Canvas LMS** ([instructure/canvas-lms](https://github.com/instructure/canvas-lms)): context pack, debt/state artifacts, refactor or integration *plan* + AI transcript log |
| Phase 2 MVP | 40% | Greenfield: AI-generated codebase + README for humans/AI + demo |
| Participation & peer review | 15% | Constructive review of others’ prompts/plans (no code authorship requirement) |
| Reflections | 10% | Short weeklies on failure modes, verification habits, and context discipline |

Adjust weights to match your department template.

## Academic integrity & safety

- **Cite AI use** as required by your institution; retain prompts and major outputs when submitting work.
- **Verify** AI-proposed commands, dependency changes, and refactors before they touch shared systems.
- **Secrets:** Never paste keys, tokens, or student PII into models; use redacted examples.

## Folder layout (this repository)

```text
content/
  syllabus.md                 ← this file
  phase-1/
    brownfield-project.md     ← Canvas LMS (official brownfield repo)
    week-N/
      day-1.md                ← first class meeting (Session 1)
      day-2.md                ← second class meeting (Session 2)
      week-overview.md        ← week overview (activities + learning outcomes)
      labs/
        README.md             ← lab brief for the week
  phase-2/
    week-N/
      day-1.md
      day-2.md
      week-overview.md
      labs/
        README.md
```

## Required tools (typical)

- AI-assisted IDE (e.g., Cursor, Copilot, or equivalent) with **project rules** / skills where supported  
- Access to an **MCP-capable** environment for Phase 1 module 3 and Phase 2 later modules  
- Git (worktrees emphasized in Phase 1)  
- **Phase 1 brownfield:** clone **[Canvas LMS](https://github.com/instructure/canvas-lms)** — see [`phase-1/brownfield-project.md`](phase-1/brownfield-project.md)  
- **Phase 2 greenfield:** a **greenfield** product idea approved by week 8  

## Phase 1 brownfield

All work in weeks 1–7 uses **Canvas LMS** as the shared legacy codebase. Students contribute **AI-assisted** plans, documentation, and (where your course allows) **verified** changes toward scoped issues or features—see [instructure/canvas-lms](https://github.com/instructure/canvas-lms) and the [project wiki](https://github.com/instructure/canvas-lms/wiki) for installation and contribution norms.

---

*Syllabus version aligned to 14-week, twice-weekly schedule. Edit dates, policies, and grading to match your catalog.*
