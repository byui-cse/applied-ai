# Week 10 Lab: Context Management (Plugin Contract Boundaries)

Plugin contracts work when you describe them like an interface: inputs, outputs, errors, guarantees, and safety constraints. Your context budget should include only what is required to define those boundaries.

## Context budget goals
- Include enough detail to specify schemas and error modes
- Exclude anything that would cause unsafe behavior or ambiguous guarantees
- Keep versioning and fallback explicit so workflows can degrade safely

## What to include
- The chosen capability and its purpose
- Input schema (what arguments it accepts)
- Output schema (what structured result it returns)
- Error modes and how the agent should respond
- Safety constraints (what it must never do)
- Versioning policy (how breaking changes are introduced)
- Fallback behavior (what happens when it fails)

## What to exclude
- Vague “best effort” promises without explicit safety constraints
- Context unrelated to the plugin’s purpose

## Iteration protocol
1. Iteration 1 (conservative)
   - Draft the core contract: name/purpose, input/output schemas, error modes, and fallback
2. Iteration 2 (tighten)
   - Strengthen safety constraints and make them testable
   - Add/clarify versioning policy boundaries
   - Remove contract fields that don’t help reliability or safety

## Reflection
- What would you treat as “non-negotiable” plugin guarantees?
- How will you test plugin correctness in your workflow?

