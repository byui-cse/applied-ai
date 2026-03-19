# Week 4: Architectural State - Caching and Technical Debt Workflows

## Learning objectives
- Plan caching strategies that reduce repeated work and repeated token usage
- Use AI to assist with technical debt while keeping ownership and validation human
- Create a workflow for "propose -> verify -> record" so changes are traceable

## Key ideas
- Cache at the right layer: summaries, extracted facts, and decision outcomes
- Caching only helps if invalidation is explicit (what changes should bust cache)
- Debt tracking is a management tool: it should include evidence and impact

## Lab: Create a debt + cache playbook
1. Create `lab/week-4/cache-plan.md` with:
   - What you cache (summaries, facts, tool outputs)
   - Cache keys (file hash, query signature, or time windows)
   - Invalidation rules (what forces regeneration)
2. Create `lab/week-4/debt-tracker.md` with 3-6 debt items:
   - Symptom, suspected cause, evidence link, risk level, recommended next action
3. For 1 debt item, write a "propose plan" section that an AI could generate
4. Add a "verification section" listing what tests or checks you will run before accepting changes

## Submission checklist
- `cache-plan.md`
- `debt-tracker.md`
- Debt item propose + verification sections (embedded or separate)

## Reflection questions
- Which part of the workflow is easiest to automate safely?
- What would convince you that cached information is stale?

