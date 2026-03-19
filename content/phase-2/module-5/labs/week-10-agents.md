# Week 10 Lab: Agents (Contract Draft + Sanity Check)

## Agent workflow
1. Pick a new capability and its purpose
2. Draft the plugin contract as an interface:
   - input schema
   - output schema
   - error modes
   - safety constraints
   - versioning policy
   - fallback behavior
3. Sanity-check:
   - Is every guarantee explicit and safe?
   - Are fallback behavior and error handling coherent?

## Iteration protocol
1. Iteration 1 (conservative)
   - Draft a minimal contract with the required sections
   - Make fallback behavior clear
2. Iteration 2 (tighten)
   - Make safety constraints more concrete and testable
   - Add boundaries for version compatibility and breaking changes

## Submission checklist
- `week-10-context-management.md`
- `week-10-markdown-memory.md`
- One paragraph describing how this plugin reduces tokens or improves reliability

## Reflection
- What would you treat as "non-negotiable" plugin guarantees?
- How will you test plugin correctness in your workflow?

