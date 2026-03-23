# Applied AI for Software Engineering

**Credits:** 2 · **Format:** Two meetings per week · **Duration:** 14 weeks  

## Course premise

Students **will not implement code by hand**. All design, exploration, refactoring, scaffolding, testing ideas, and documentation are produced **through collaboration with AI tools** (IDE assistants, chat interfaces, agents, MCP-connected tools, etc.). The course trains *judgment*: scoping work, verifying outputs, managing context, and shipping outcomes safely on brownfield and greenfield systems.

## Learning outcomes

By the end of the term, students should be able to:

1. **Budget and shape context** for large existing codebases using markdown artifacts, concise prompts, and selective file inclusion—aiming to keep high-signal context **under roughly 40%** of available window where practical.
2. **Describe architectural and debt state** to an AI tool using structured notes, caches, and repeatable “state refresh” rituals.
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

## Grading

| Component | Weight (example) | Notes |
|-----------|------------------|--------|
| Phase 1 portfolio | 35% | **Canvas LMS** ([instructure/canvas-lms](https://github.com/instructure/canvas-lms)): context pack, debt/state artifacts, refactor or integration *plan* + AI transcript log |
| Phase 2 MVP | 40% | Greenfield: AI-generated codebase + README for humans/AI + demo |
| Participation & peer review | 15% | Constructive review of others’ prompts/plans (no code authorship requirement) |
| Reflections | 10% | Short weeklies on failure modes, verification habits, and context discipline |

Adjust weights to match your department template.

## Late Policy

Late work will only be accepted with prior consent from the instructor or teaching assistant.

## Student Support

Support is available in many ways including via other class members, tutoring, and instructor student hours. In addition, help is available through [the university's academic support center](http://www.byui.edu/academic-support-centers).

# Dress and Grooming

You are expected to follow the university's [Dress and Grooming Standards](http://www.byui.edu/student-honor-office/ces-honor-code/dress-and-grooming)

This includes any [current university requirements and/or guidelines](https://www.byui.edu/covid-19-updates) related to wearing masks and/or social distancing.

# Preventing Sexual Misconduct

BYU-Idaho prohibits sex discrimination by its employees and students in all of its education programs or activities. This includes all forms of sexual harassment, such as sexual assault, dating violence, domestic violence, stalking, conditioning a grade or job on participation in sexual conduct, and other forms of unwelcome sexual conduct.

As an instructor, one of my responsibilities is to help create a safe learning environment for my students and for the campus as a whole. University policy requires deans and department chairs, and encourages all faculty, to report every incident of sexual harassment that comes to their attention. If you encounter or experience sexual harassment, please contact the Title IX Coordinator at titleix@byui.edu or 208-496-9209. Additional information about sex discrimination, sexual harassment, and available resources can be found at [www.byui.edu/titleix](https://byui-cse.github.io/itm310-course/course/www.byui.edu/titleix)

# Disability Services

BYU-Idaho does not discriminate against persons with disabilities in providing its educational and administrative services and programs and follows applicable federal and state law. This policy extends to the University’s electronic and information technologies (EIT).

Students with qualifying disabilities should contact the Disability Services Office at disabilityservices@byui.edu or 208-496-9210. Additional information about Disability Services resources can be found at [http://www.byui.edu/disabilities](http://www.byui.edu/disabilities).

# Academic Honesty

Academic Honesty means students do their own work. This also means their instructors will evaluate that work. Students should not be dishonest—this includes all types of work in their courses. The complete Academic Honesty Policy can be found at [http://www.byui.edu/student-honor-office/ces-honor-code/academic-honesty](http://www.byui.edu/student-honor-office/ces-honor-code/academic-honesty).

# Academic Grievances

Students are encouraged to contact their instructors regarding course-related concerns. If concerns cannot be resolved in this way, students may contact the [BYU-Idaho Support Center](http://www.byui.edu/contact-us). to formally register a concern or grievance. [The Student Grievance Policy](https://content.byui.edu/integ/gen/d42e66fd-6e72-448f-a4c2-4d88a4ed26d2/0/Final%20Student%20Grievance%20Policy%20-%20catalog%20version.docx). can be found here.

# Changes to Schedule and Assignments

Schedules, assignments, and policies are subject to change. You will be notified of any changes on I-learn.

# Generative AI Policy

The "Generative AI Usage Policy" for the Computer Science and Engineering (CSE) Department provides guidelines for the ethical and practical use of generative AI in education and software development. It encourages students to utilize AI tools for enhancing learning, creativity, and productivity while requiring them to disclose AI assistance in their work. This policy aims to integrate generative AI into the curriculum, fostering a balanced and innovative learning environment. [The CSE Generative AI Policy](https://byui-cse.github.io/department/student-resources/generative-ai/generative-ai-policy.html) can be found here.

---

*Syllabus version aligned to 14-week, twice-weekly schedule. Edit dates, policies, and grading to match your catalog.*

<% checklist
Understand the course premise (AI collaboration, not hand-authored implementation)
Located the weekly index and know how calendar weeks map to `phase-1/week-*` and `phase-2/week-*`
Phase 1: Canvas LMS clone and brownfield expectations are clear
Phase 2: greenfield product direction approved by the stated milestone (e.g. week 8)
Will cite AI use and verify commands/changes per academic integrity and safety notes
%>
