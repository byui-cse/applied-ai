# Week 9: Foundations & Skills - Prompt Suites and Engineering Evaluation

## Learning objectives
- Turn prompts into a testable suite (inputs + expected properties)
- Define acceptance checks so AI outputs can be validated automatically
- Build a lightweight regression workflow for agent-assisted changes

## Key ideas
- Evaluation is the bridge between "LLM looks right" and "engineering is correct"
- A prompt suite should capture: intent, constraints, and expected behavior
- Regression tests protect you from context drift and prompt overfitting

## Lab: Create a prompt suite + evaluation rubric
1. Choose 3 representative tasks related to your Week 8 acceptance criteria
2. For each task, write:
   - `task brief` (one paragraph)
   - `inputs you will provide` (files, config snippets, constraints)
   - `output format` (what the model must produce)
   - `acceptance properties` (what must be true)
3. Create `lab/week-9/evaluation-rubric.md` with 4-6 criteria and how you will check each one
4. Run one "dry evaluation": score one hypothetical model response against your rubric

## Submission checklist
- `prompt-suite.md` (or separate files)
- `evaluation-rubric.md`
- 1-2 sentences on how you will run regression checks later

## Reflection questions
- What acceptance properties are easiest to validate automatically?
- Where do humans still need to confirm correctness?

