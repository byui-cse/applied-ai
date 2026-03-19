# Week 2: Token Optimization for Large Existing Codebases

## Learning objectives
- Chunk a legacy codebase into retrieval-friendly units
- Design search/query strategies that minimize irrelevant context
- Create a simple evaluation rubric for "good enough" AI outputs

## Key ideas
- Retrieval should be task-oriented (what you need), not file-oriented (what you found)
- Good chunk boundaries reduce both tokens and ambiguity
- Evaluation is a workflow step, not a final grade

## Lab: Chunk + retrieve + evaluate
1. Choose a subsystem (10-30 files is enough for the lab) and create `lab/week-2/chunk-map.md`
2. Propose 6-12 chunks with: name, where it lives, inclusion rules, and "do not use for" rules
3. Write 3 retrieval queries (in natural language) that would fetch the chunks needed for: bugfix, refactor, and new feature
4. Perform one "dry run" evaluation: for each query, list the expected chunks and explain why those chunks are sufficient
5. Define an evaluation rubric with 3-5 criteria (examples: correctness, minimal changes, clarity of assumptions, test impact)

## Submission checklist
- `chunk-map.md`
- Retrieval queries (in the same file or linked)
- Evaluation rubric (short and actionable)

## Reflection questions
- Which chunk boundary was hardest to define, and why?
- How will you know when retrieval is failing (before the model fails)?

