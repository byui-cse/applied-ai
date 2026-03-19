# Week 2 Lab: Agents (Two-Iteration Protocol)

Even without tools enabled, you can treat retrieval + evaluation like an agent workflow by running two iterations against your own interfaces.

## Agent protocol
1. Start from your `chunk map` as “long-term retrieval memory”.
2. For each retrieval query:
   - Predict which chunks should be returned
   - Compare against your inclusion rules and your dry-run plan
3. Produce evaluation outputs in the exact structure from your memory file:
   - Expected chunks
   - Why those chunks are sufficient
   - Rubric scores (or at least rubric-aligned notes)

## Iteration protocol (two runs)
1. Iteration 1 (conservative)
   - Use your initial chunk boundaries
   - Use only your first set of query wording
   - Record what retrieval would bring back (as your dry-run expected chunks)
2. Iteration 2 (refined)
   - Adjust chunk boundaries and/or query wording
   - Keep changes tied to output quality (fewer irrelevant chunks, clearer assumptions, better rubric fit)

## Submission checklist
- `week-2-context-management.md` (final context budget + what you refined)
- `week-2-markdown-memory.md` (filled: chunk map, retrieval queries, dry-run evaluation, rubric)
- A short note: "What I would include next time, and why"

## Reflection
- Which chunk boundary was hardest to define, and why?
- How will you know when retrieval is failing (before the model fails)?

