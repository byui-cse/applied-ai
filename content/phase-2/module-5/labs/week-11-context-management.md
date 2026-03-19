# Week 11 Lab: Context Management (Workflow Integration + Fallback)

A plugin only reduces tokens if it fits into a verified workflow. Your context budget should include the preconditions/postconditions and a fallback plan so failures do not cascade.

## Context budget goals
- Include only the workflow step context needed to call the plugin safely
- Exclude surrounding logic you are not using for pre/postconditions
- Make measurement and fallback plans explicit

## What to include
- The workflow step the plugin supports
- Where the plugin is called in the workflow
- Required preconditions
- What must be verified after the call (postconditions)
- Fallback plan on failure
- Measurement signals to record (latency, pass/fail, success rate, token usage)
- Operator notes (when humans override)

## What to exclude
- Plugin calls without clear preconditions
- Postconditions that cannot be verified
- Error handling that does not specify fallback behavior

## Iteration protocol
1. Iteration 1 (conservative)
   - Write the workflow integration with basic pre/postconditions and a fallback
   - Draft a minimal measurement plan
2. Iteration 2 (tighten + improve safety)
   - Improve preconditions/postconditions so they are checkable
   - Make fallback behavior more concrete and less ambiguous
   - Refine measurement signals to match what you can record reliably

## Reflection
- What plugin failures are recoverable vs not?
- What would you automate next to reduce human overhead?

