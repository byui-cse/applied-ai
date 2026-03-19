# Week 13: Autonomous Agents - Multi-Agent Coordination and Arbitration

## Learning objectives
- Split work across specialized roles (planner, implementer, verifier)
- Design handoffs so state is preserved without large context re-sends
- Add arbitration rules when agents disagree

## Key ideas
- Multi-agent systems require interface discipline: what each agent receives and produces
- Handoffs should carry "just enough state" plus verifiable artifacts
- Arbitration prevents hidden conflicts from compounding

## Lab: Role design + conflict resolution
1. Write `lab/week-13/multi-agent-design.md` with roles:
   - Planner (creates task plan)
   - Implementer (proposes changes)
   - Verifier (checks correctness and safety)
2. Define handoff artifacts between roles (examples: `plan.md`, `diff_summary.md`, `verification_report.md`)
3. Create an arbitration policy for disagreements:
   - what evidence the verifier must collect
   - when to request human review
4. Add a trace log template so you can audit decisions later

## Submission checklist
- `multi-agent-design.md`
- arbitration policy (embedded section or separate)
- trace log template

## Reflection questions
- What made disagreements detectable rather than silent?
- Where did you reduce context by passing artifacts instead of raw text?

