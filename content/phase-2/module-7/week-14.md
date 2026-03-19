# Week 14: Advanced Workflows - Production-Ready Greenfield MVP Capstone

## Learning objectives
- Orchestrate multiple agents and complex tool integrations end-to-end
- Combine MCP-style navigation with plugin/tool contracts and verification
- Produce workflow artifacts suitable for handoff to a developer team

## Key ideas
- Capstone success is measured by verification and traceability, not by clever prompts
- Advanced workflows are compositional: tools + agents + memory artifacts + evaluation
- A production workflow includes rollback/contingency plans

## Lab: Capstone workflow plan (end-to-end)
1. Choose a Greenfield MVP feature set (3-5 user stories) aligned to your Week 8 acceptance criteria
2. Write `lab/week-14/capstone-workflow.md` with these sections:
   - Agent roster (roles and responsibilities)
   - MCP/tool plan (what tools each agent uses and why)
   - Plugin integration plan (contracts + versions + fallback behavior)
   - Memory/state plan (what artifacts are carried forward)
   - Verification plan (tests/checks, success criteria, failure handling)
3. Add a traceability section:
   - how you record evidence
   - how you summarize diffs without flooding context
4. End with a "handoff packet" checklist:
   - what someone needs to run and review your changes
   - what documentation you generated during the workflow

## Submission checklist
- `capstone-workflow.md` (complete, with verification and handoff packet)
- A short reflection (what you would refine for reliability next run)

## Reflection questions
- Which workflow component reduced risk the most (memory, caching, tools, plugins, or arbitration)?
- Where did you still need human judgment, and why?

