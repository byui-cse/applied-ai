# Week 12 Lab: Markdown Memory (Agent Loop + Structured Output)

## `agent-loop.md` template
```markdown
# Agent Loop

## 1) Initial planning
- Input:
- Planned actions:

## 2) Tool call step(s)
- Allowed tool calls:
- Tool input rules:

## 3) Observation step(s)
- What evidence you collect:
- How you decide what to do next:

## 4) Decision step (continue/stop)
- Stop conditions:
- Continue conditions:

## Guardrails
- Max steps:
- Max tool calls:
- Evidence insufficient behavior:
```

## Structured output schema (template)
```markdown
{
  "plan": "<string or structured object>",
  "evidence": [
    {
      "tool": "<tool name>",
      "inputs": "<summary>",
      "result": "<summary>",
      "what_it_proves": "<...>"
    }
  ],
  "diff_summary": "<string>",
  "verification_steps": ["<step 1>", "<step 2>"],
  "risk_notes": ["<risk 1>", "<risk 2>"]
}
```

## Sample success transcript (short)
Fill this with a brief “after success” example showing schema-shaped output.

## Deliverables
- `agent-loop.md`
- Structured output schema
- One sample success transcript

