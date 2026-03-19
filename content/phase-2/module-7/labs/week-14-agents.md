# Week 14 Lab: Agents (Capstone Workflow Protocol)

## Agent workflow (planning + compositional execution)
1. Choose an MVP feature set aligned to your acceptance criteria
2. Define the agent roster and responsibilities
3. Define MCP/tool plan: which tools each agent uses and why
4. Define plugin integration plan: contracts + versions + fallback
5. Define memory/state plan: what artifacts are carried forward
6. Define verification plan: tests/checks, success criteria, failure handling
7. Add traceability: record evidence and summarize diffs
8. Finish with a handoff packet checklist

## Iteration protocol (two runs)
1. Iteration 1 (conservative)
   - Draft all sections with clear boundaries
   - Ensure fallback plans and verification gates exist
2. Iteration 2 (production-ready)
   - Improve reliability: tighten evidence requirements
   - Reduce any redundant artifact fields that add context but not value
   - Ensure handoff packet is complete enough for another developer

## Submission checklist
- `week-14-context-management.md`
- `week-14-markdown-memory.md`
- A short reflection (what you would refine for reliability next run)

## Reflection
- Which workflow component reduced risk the most (memory, caching, tools, plugins, or arbitration)?
- Where did you still need human judgment, and why?

