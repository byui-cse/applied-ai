# Week 9 Lab: Context Management (Prompt Suites + Regression)

Evaluation bridges “LLM looks right” and “engineering is correct”. Your context budget should make acceptance checks explicit so outputs can be validated (not just reviewed).

## Context budget goals
- Include only the tasks and acceptance criteria needed to build a prompt suite
- Exclude extra context that does not affect the properties being tested
- Make regression steps repeatable: the same suite should be re-runnable later

## What to include
- 3 representative tasks related to your Week 8 acceptance criteria
- For each task:
  - task brief (what success means)
  - inputs you will provide
  - output format the model must follow
  - acceptance properties (what must be true)
- A short evaluation rubric and how you will check it

## What to exclude
- Context drift: do not rely on unstated assumptions
- Long raw context; prefer structured inputs and acceptance properties

## Iteration protocol
1. Iteration 1 (conservative)
   - Choose the 3 tasks and write the prompt suite structure + rubric
   - Run one dry evaluation against your own hypothetical responses
2. Iteration 2 (tighten regression)
   - Refine acceptance properties to be more checkable
   - Improve rubric clarity so scoring is consistent
   - Remove any prompt fields that don’t improve evaluation quality

## Reflection
- What acceptance properties are easiest to validate automatically?
- Where do humans still need to confirm correctness?

