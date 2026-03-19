# Week 8 Lab: Markdown Memory (AI Handbook + Prompt Contract)

## `ai-handbook.md` template
```markdown
# AI Handbook

## Project overview
<what it does>

## Architecture map
<components and boundaries>

## How to run
### Requirements
- <...>

### Commands
<command examples>

### Env vars (placeholders)
- <ENV_VAR_NAME>=<value>

## How to add a feature
Checklist:
1. <clarify feature scope / acceptance criteria>
2. <find the relevant components/boundaries>
3. <add/adjust tests>
4. <update docs/examples>
5. <verify with the acceptance checks>
```

## `acceptance-criteria.md` template
```markdown
# Acceptance Criteria: <Feature name>

## Requirements
- <bullet list>

## What must be true (testable)
- <criterion 1>
- <criterion 2>
- <criterion 3>
```

## Test plan section (template)
```markdown
# Test Plan

## Unit tests
- <what you expect to cover>

## Integration checks
- <what you will run>
```

## Prompt contract for future AI work (template)
```markdown
[Prompt Contract: <future feature task>]

## Inputs I will provide
- Handbook excerpts:
- Relevant files:
- Acceptance criteria:

## Output format (must include)
1. Changes summary
2. Tests to run + expected results
3. Notes on assumptions and follow-ups

## Required verification
- Must reference the Test Plan
- Must align with acceptance criteria
```

## Deliverables
- `ai-handbook.md`
- `acceptance-criteria.md`
- Prompt contract (short, reusable)

