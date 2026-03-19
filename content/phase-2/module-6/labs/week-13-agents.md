# Week 13 Lab: Agents (Role Design + Conflict Resolution)

## Agent workflow
1. Planner role
   - Creates a task plan and assumptions
2. Implementer role
   - Proposes changes and a diff summary
3. Verifier role
   - Checks correctness and safety using verifiable artifacts
4. Arbitration when agents disagree
   - Verifier collects evidence and either resolves or requests human review

## Iteration protocol
1. Iteration 1 (conservative)
   - Draft roles and handoff artifacts
   - Define an arbitration policy that triggers on conflicts
2. Iteration 2 (refine + reduce context)
   - Make evidence requirements stricter
   - Use artifacts to avoid re-sending large context buffers
   - Improve trace logging for auditability

## Submission checklist
- `week-13-context-management.md`
- `week-13-markdown-memory.md`
- arbitration policy (embedded section or separate)
- trace log template

## Reflection
- What made disagreements detectable rather than silent?
- Where did you reduce context by passing artifacts instead of raw text?

