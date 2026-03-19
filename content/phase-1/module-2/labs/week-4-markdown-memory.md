# Week 4 Lab: Markdown Memory (Cache Plan + Debt Tracker)

## `cache-plan.md` template
```markdown
# Cache Plan

## What you cache
- <summaries | extracted facts | tool outputs | decision outcomes>

## Cache keys
- <file hash, query signature, time windows, etc.>

## Invalidation rules
1. <rule name>
   - What changes should bust it:
   - Why it is sufficient:
2. <rule name>
   - ...

## Notes
- How you will validate correctness after cache refresh
```

## `debt-tracker.md` template
Create 3-6 debt items.

```markdown
# Debt Tracker

## <Debt item title>
- Symptom:
- Suspected cause:
- Evidence link(s):
- Risk level:
- Recommended next action:

### Proposed plan (for one debt item)
- Proposal:
- Why this approach:

### Verification steps
- Tests/checks to run:
- What success looks like:
- What to do if verification fails:
```

## `propose plan` + verification section checklist
- Include an actionable “next action”
- Include what you will verify before accepting changes

## Deliverables
- `cache-plan.md`
- `debt-tracker.md`
- Propose + verification sections for at least one debt item

