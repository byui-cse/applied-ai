# Week 10: Extensibility - Plugin Contracts for LLM Tools

## Learning objectives
- Define plugin/tool contracts so new capabilities are predictable
- Manage versions and compatibility boundaries
- Add safety constraints so plugins cannot perform unsafe actions

## Key ideas
- A plugin contract is an interface: inputs, outputs, errors, and guarantees
- Versioning is how you keep an ecosystem stable as prompts evolve
- Safety boundaries should be explicit, testable, and enforced in workflow

## Lab: Design a plugin (tool) contract
1. Pick one new capability you want (examples: "code search adapter", "schema validator", "test runner wrapper", "diff summarizer")
2. Write `lab/week-10/plugin-contract.md` with:
   - plugin name and purpose
   - input schema (what arguments it accepts)
   - output schema (what structured result it returns)
   - error modes and how the agent should respond
   - safety constraints (what it must never do)
3. Add a "versioning policy" section: how breaking changes are introduced
4. Define one "fallback behavior" when the plugin fails (what the agent does next)

## Submission checklist
- `plugin-contract.md`
- One paragraph describing how this plugin reduces tokens or improves reliability

## Reflection questions
- What would you treat as "non-negotiable" plugin guarantees?
- How will you test plugin correctness in your workflow?

