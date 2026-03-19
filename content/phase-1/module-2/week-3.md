# Week 3: Architectural State - Memory Management

## Learning objectives
- Separate short-term context from long-term architectural knowledge
- Create "AI memory artifacts" that teams can read and update
- Use structured summaries to reduce repeated reasoning

## Key ideas
- Memory is not just text: it is a contract, a format, and an update policy
- Long-term artifacts should be stable, versionable, and tied to code facts
- Architectural state reduces rework when tasks repeat across weeks

## Lab: Design AI memory artifacts for a brownfield refactor
1. Create `lab/week-3/ai-memory/` with:
   - `architecture-summary.md` (what the system is and how major pieces connect)
   - `key-decisions.md` (decision log with dates and "why")
   - `known-risks.md` (risk register: what breaks easily and why)
2. Write update rules in `lab/week-3/update-policy.md` (examples: when to add a decision, how to revise a summary, what evidence is required)
3. Take a new task prompt and answer it using ONLY:
   - a small task brief
   - the memory artifacts above
4. Compare: how many context tokens would you save vs re-including raw files?

## Submission checklist
- `architecture-summary.md`
- `key-decisions.md`
- `known-risks.md`
- `update-policy.md`

## Reflection questions
- What information should never be regenerated from scratch?
- What update rule will you enforce to prevent stale memory?

