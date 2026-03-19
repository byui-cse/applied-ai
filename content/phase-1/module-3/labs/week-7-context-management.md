# Week 7 Lab: Context Management (Brownfield Studio Boundaries)

End-to-end brownfield success comes from bounded workflow steps. Your context budget should focus on the minimum artifacts needed to map, plan, verify, and record outcomes.

## Context budget goals
- Keep your workflow explainable: each step should consume a small, named artifact
- Prevent “context creep” by excluding raw dumps once you have maps/plans
- Use verification as a forcing function (evidence before you record success)

## What to include
- System map (your best current belief about architecture)
- Task plan (what changes you will attempt)
- Tool plan (how you will gather evidence and verify it)
- Risk plan (what might break and how you will detect it)
- A context budget reference:
  - what you included
  - what you excluded

## What to exclude
- Large amounts of raw code that you do not need after the map/plan exists
- Assumptions without a verification step
- Risks you cannot test or observe

## Iteration protocol
1. Iteration 1 (conservative workflow)
   - Make minimal, verifiable changes
   - Keep tool plan simple and evidence-oriented
2. Iteration 2 (tighter boundaries + better verification)
   - Refine the risk plan and verification steps
   - Record learnings so later tasks reuse the “studio” artifacts

## Reflection
- At what point did you spend the most tokens, and how will you reduce it later?
- What verification step gave you the most confidence?

