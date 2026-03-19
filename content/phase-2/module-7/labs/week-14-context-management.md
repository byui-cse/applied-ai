# Week 14 Lab: Context Management (End-to-End Workflow Context)

Capstones succeed when you pass artifacts forward instead of re-sending raw context. Your context budget should specify what is carried in the handoff packet and how verification gates decisions.

## Context budget goals
- Include only the workflow components needed to run end-to-end reliably
- Exclude speculative details not covered by verification or contracts
- Keep traceability: every key decision should tie back to evidence you collected

## What to include
- Agent roster (roles and responsibilities)
- MCP/tool plan (what tools each agent uses and why)
- Plugin integration plan (contracts + versions + fallback behavior)
- Memory/state plan (what artifacts are carried forward)
- Verification plan (tests/checks, success criteria, failure handling)
- Traceability section (how you record evidence and summarize diffs)
- Handoff packet checklist (what someone needs to run and review your changes)

## What to exclude
- Large raw conversation history
- Unverified assumptions that are not covered by the verification plan

## Iteration protocol
1. Iteration 1 (conservative)
   - Draft each component section with clear boundaries and verification gates
   - Create a handoff packet checklist based on your plan
2. Iteration 2 (tighten for production)
   - Make fallback behavior explicit and safe
   - Improve traceability and diff summarization to avoid context flooding
   - Reduce any redundant artifact fields that do not improve reliability

## Reflection
- Which workflow component reduced risk the most (memory, caching, tools, plugins, or arbitration)?
- Where did you still need human judgment, and why?

