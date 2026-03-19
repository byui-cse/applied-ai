# Week 1 Lab: Markdown Memory (Prompt Contracts)

Markdown is your "structured memory layer" for requirements, plans, and diffs.

## Goal
Turn your informal instructions into an engineering artifact you can reuse: a prompt contract.

## Step-by-step
1. Turn your context budget into markdown
   - Copy `Task Summary`, `Relevant Files`, `Required Outputs`, and `Exclusions` into markdown headings.
2. Write a prompt contract template that contains:
   - Inputs you will provide (exact list)
   - The exact output format you want
   - Missing-info protocol (how the model should ask questions before proceeding)
3. Run iteration 1 using only the markdown artifacts from steps 1-2.
4. Record:
   - Which parts of the contract improved consistency
   - What the model misunderstood (and which contract field would prevent it next time)

## Prompt contract template
```markdown
[Prompt Contract: <task name>]

## Inputs I will provide
- [Context: files/snippets you include]
- [Constraints / requirements]
- [Acceptance criteria]

## Context I am intentionally not providing
- [Exclusions]

## Output format (must match exactly)
1. Assumptions
   - ...
2. Plan
   - ...
3. Changes / Answer
   - ...
4. Verification
   - ...

## If you are missing required information
Ask numbered clarification questions only.
For each question, state:
- Why it matters for correctness
- What specific format/choice you need from me
Then wait for my answers before producing the final output.
```

## Deliverables
- A filled-in prompt contract (based on your chosen task)

## Reflection
- What instruction or output format improved consistency the most?
