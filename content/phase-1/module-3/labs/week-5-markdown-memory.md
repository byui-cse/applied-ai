# Week 5 Lab: Markdown Memory (Tool Contracts + Trace Log)

## `tool-contracts.md` template
Write 2-4 tool contracts.

```markdown
## Tool: <name> (example: "search symbol")
- Purpose:

## Inputs
- <field name>: <type / meaning>

## Outputs
- <field name>: <type / meaning>

## Error modes
- <what errors can occur>

## Failure behavior (how the LLM/agent should react)
- <what to do next>
```

## `trace-log.md` template
Use one section per step in your chosen refactor.

```markdown
# Intent
<what you wanted to change and why>

# Evidence collected
## Step: <tool name>
- Inputs passed:
- Returned evidence (summarized):
- What this evidence proves:

# Proposed change summary
<high-level summary of the change>

# Verification steps
- Tests/checks to run:
- What success looks like:
```

## Traceable prompt template
```markdown
You may only propose changes after collecting evidence using the tool contracts.
If evidence is missing or insufficient, ask for what you need or stop.
Output the plan in this structure:
1) Evidence collected
2) Proposed change summary
3) Verification steps
```

## Deliverables
- `tool-contracts.md` (filled)
- `trace-log.md` (filled)
- Traceable prompt (1)

