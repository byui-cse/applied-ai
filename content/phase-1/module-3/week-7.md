# Week 7: Brownfield Studio - From Code Map to Verified Patch

## Learning objectives
- Orchestrate a full brownfield workflow: map -> plan -> propose -> verify -> record
- Maintain context efficiency across multiple iterations
- Produce a handoff artifact that a teammate can execute without the original prompt trail

## Key ideas
- End-to-end quality comes from verification discipline
- Recording architectural state prevents rework
- The best "AI output" is a set of bounded, test-backed changes

## Lab: Studio capstone (brownfield refactor workflow)
1. Create `lab/week-7/brownfield-studio.md` with the following sections:
   - System map (what you believe the architecture is)
   - Task plan (what changes you will attempt)
   - Tool plan (how you will navigate and verify evidence)
   - Risk plan (what might break and how you will detect it)
2. Write a "propose changes" step that explicitly references:
   - your context budget
   - your architectural memory artifacts
   - your caching/debt workflow
3. Add a verification section that lists:
   - required tests/checks
   - what "success" looks like
   - what you do if verification fails
4. Finish with a handoff note:
   - what to run
   - what files changed (high level)
   - what remaining debt (if any) you recommend next

## Submission checklist
- `brownfield-studio.md`
- A short reflection: one insight and one thing to improve next time

## Reflection questions
- At what point did you spend the most tokens, and how will you reduce it later?
- What verification step gave you the most confidence?

