# Week 8 Lab: Context Management (AI-Ready Docs + Tests)

This lab saves tokens by turning “what good looks like” into repository structure: docs, examples, tests, and stable interfaces.

## Context budget goals
- Include only the information needed to write an AI-ready handbook and acceptance criteria
- Exclude vague future details; prefer concrete conventions you can test
- Keep prompt work grounded in the repo structure you just created

## What to include
- Project overview (what it does)
- Architecture map (components and boundaries)
- How-to-run instructions (commands + env placeholders)
- Feature checklist for “how to add a feature”
- Acceptance criteria for a small future feature
- Expected tests/checks
- A prompt contract that references the handbook

## What to exclude
- Unimplemented features not covered by acceptance criteria
- Large code dumps; summarize boundaries instead
- Prompt contracts that do not reference verification (tests/checks)

## Iteration protocol
1. Iteration 1 (conservative)
   - Draft handbook + acceptance criteria + test plan at a basic level
   - Draft a prompt contract that references those docs
2. Iteration 2 (tighten)
   - Make commands and env placeholders specific
   - Ensure acceptance criteria are testable and listed in the test plan
   - Simplify prompt contract to only what future AI work must follow

## Reflection
- What documentation would have saved you time last week in brownfield work?
- Which conventions will you keep stable as the project grows?

