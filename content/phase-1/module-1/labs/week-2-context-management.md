# Week 2 Lab: Context Management (Context Budgets)

Token savings here come from retrieval discipline: you include only the small set of code chunks that are relevant to the task, and you exclude the rest.

## Context budget goals
- Pick a subsystem small enough to reason about (10-30 files is enough)
- Define chunk boundaries so retrieval is task-oriented (what you need), not file-oriented (what you happened to find)
- Use a short, explicit evaluation loop so you can detect retrieval failing early

## What to include
- A chosen subsystem description (what you consider the scope)
- A `chunk map` that defines each chunk’s:
  - inclusion rules
  - “do not use for” rules
- Three natural-language retrieval queries you will test:
  - bugfix query
  - refactor query
  - new feature query
- A “dry run” plan for each query:
  - expected chunks
  - why those chunks are sufficient
- An evaluation rubric (3-5 criteria) so you can judge results consistently

## What to exclude
- The full legacy codebase (or large unrelated directories)
- Chunks that are ambiguous boundaries (e.g., content that applies to multiple unrelated tasks)
- “Just in case” context that isn’t supported by your inclusion rules

## Iteration protocol
1. Iteration 1 (conservative context)
   - Use your initial chunk map boundaries and your first set of retrieval queries.
   - For each query, list expected chunks and explain why they are sufficient.
2. Iteration 2 (refined boundaries)
   - Adjust chunk boundaries and/or the query wording when your expected retrieval set becomes unstable.
   - Keep what changed tied to output quality (did you get fewer irrelevant chunks, clearer assumptions, better rubric scores?)

## Reflection
- Which chunk boundary was hardest to define, and why?
- How will you know when retrieval is failing (before the model fails)?

