# Week 11 Lab: Markdown Memory (Plugin Workflow + Operator Notes)

## `plugin-workflow.md` template
```markdown
# Plugin Workflow Integration

## Where the plugin is called
<step name / description>

## Required preconditions
- <what must be true before call>

## Postconditions (what you must verify)
- <what must be true after call>
- <how you verify it>

## What happens on failure (fallback plan)
- If plugin fails:
  - <fallback action>
- What must still be preserved:
  - <safety / correctness invariants>
```

## Measurement plan template
```markdown
# Measurement Plan

## Signals
- Latency:
- Pass/fail outcome:
- Success rate:
- Token usage:

## How you record it
- <where/how you log>
```

## Operator note template
```markdown
# Operator Note (Human Interpretation)

## How to interpret plugin outputs
- <what output means>

## When humans should override
- <conditions where human judgment is required>
```

## Deliverables
- `plugin-workflow.md` (filled)
- measurement plan (embedded or separate)
- operator note (embedded or separate)

