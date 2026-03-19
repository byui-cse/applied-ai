# Week 2 Lab: Markdown Memory (Chunk Map + Evaluation)

Fill in the templates below so they can be reused in later prompts.

## Chunk map (template)
Use one section per chunk.

```markdown
## <Chunk name>
- Where it lives: <path(s) / module(s)>
- Inclusion rules: <what this chunk should be used for>
- "Do not use for" rules: <when to exclude>
- Notes: <edge cases / boundaries / assumptions>
```

## Retrieval queries (template)
Write queries in natural language. For each query, also note what chunks must be returned.

```markdown
## Query 1: Bugfix
- Query text: <...>
- Expected chunks: <...>
- Why: <...>

## Query 2: Refactor
- Query text: <...>
- Expected chunks: <...>
- Why: <...>

## Query 3: New feature
- Query text: <...>
- Expected chunks: <...>
- Why: <...>
```

## Dry-run evaluation (template)
For each query, do a “dry run” listing expected chunks and why they are sufficient.

```markdown
## Evaluation: <Query name>
- Expected chunks:
  - <chunk name 1>
  - <chunk name 2>
- Why sufficient:
  - <bullet per expected chunk>
- Failure modes to watch:
  - <what would indicate retrieval is returning too much/too little>
```

## Evaluation rubric (template)
Keep it short and actionable.

```markdown
## Rubric criteria (3-5)
1. Correctness
   - What “good” looks like:
2. Minimal changes
   - What “good” looks like:
3. Clarity of assumptions
   - What “good” looks like:
4. Test impact
   - What “good” looks like:
```

## Deliverables (filled in by you)
- Chunk map (filled)
- Retrieval queries (3 queries)
- Dry-run evaluation + evaluation rubric

