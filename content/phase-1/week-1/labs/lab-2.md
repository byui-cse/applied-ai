# Lab 2 — Repository Analysis Agent

You will design an **LLM agent** that helps someone understand a codebase by scanning and summarizing a repository. This lab does **not** give you a copy-paste system prompt. You write your own agent specification and supporting artifacts.

**Prerequisite:** Complete the setup in [`lab-1.md`](lab-1.md) (fork the course repo, EC2, Remote SSH) so you have a GitHub fork and a place to run commands.

---

## Goal

Produce an AI agent so that a user (or an automation) can point the agent at a repository and get structured, repeatable analysis, without blowing the context window on every run.

---

## Repository layout (required)

In your **fork** of the course repository, add:

| Path | Purpose |
|------|--------|
| `agents/analyze-repo.md` | Single markdown file that describes your repository-scanning agent: role, inputs, outputs, constraints, and how index files and scripts fit together. |

You may add other files under `agents/` or elsewhere if your design needs them (for example, script entrypoints referenced from `analyze-repo.md`).

---

## Minimum requirements

Your `agents/analyze-repo.md` (and any files it points to) must show how you satisfy **all** of the following.

### 1. Index files for fast lookup

The agent should not rely on reading the entire tree every time. Specify **index files** you create or update (for example, a manifest of directories, a symbol map, a list of key files, or generated summaries per folder). Explain **when** they are built or refreshed and **how** the agent uses them to decide what to open next.

### 2. Context management — 40% or less budget

Describe **context management** explicitly: how you chunk work, what gets summarized vs. quoted, and how you avoid loading redundant text. State a target of **40% or less** of your model’s **usable context budget** for a typical analysis pass (define what “typical” means in your doc, e.g. “first pass on a repo under N files”). If you measure tokens, say how; if you estimate, say how you estimate.

### 3. Agent scripts for out-of-LLM processes

Identify work that should **not** be done inside the LLM (search, listing, hashing, building indexes, formatting output files). Provide **scripts** (shell, Python, or similar—your choice) that perform those steps, and explain in `analyze-repo.md` how the agent is supposed to invoke or assume those scripts. The LLM plans and interprets; scripts do deterministic heavy lifting.

---

## What you turn in

- **`agents/analyze-repo.md`** meeting the minimum requirements above.  
- **Scripts** you reference, committed in the repo with short comments or a “how to run” section in the markdown.  
- Optional: a short note in the same file on **limitations** (what the agent is not designed to do).

Your instructor may ask for a demo or PR against your fork; follow their submission steps.

---

## Template Agent

Utilizing the task markdown file, you can start with a strong structure for your agents.

<% editor markdown "# Role\n\n# Task\n\n# Steps\n\n# Analysis\n\n# Examples" %>

---

## What we intentionally omit

There is **no** official prompt text in this lab. You must author the instructions your agent follows while satisfying indexing, context limits, and scripted preprocessing/postprocessing yourself.

## Rubric

### Lab 2 Grading Rubric (30 points)

| Criteria                                                                                           | Points |
|----------------------------------------------------------------------------------------------------|--------|
| **1. `agents/analyze-repo.md` exists and includes agent's role, inputs, outputs, and constraints** |   6    |
| **2. Index files (or equivalent) are specified: when built/refreshed and how the agent uses them** |   6    |
| **3. Context management section: explicit, targets ≤ 40% usable context for a defined “typical” run** |   6    |
| **4. Scripts for deterministic/automation steps are referenced, documented, and included**          |   6    |
| **5. Supporting files/limitations (if any) match description in analyze-repo.md**                   |   3    |
| **6. Overall clarity, organization, and completeness of agent docs and scripts**                    |   3    |

**Total:** 30 points

#### Evaluation Notes:
- Points may be partially awarded per item at instructor’s discretion.
- Rubric aligns with minimum requirements and checklist above; full credit requires meeting all requirements with clear evidence in files, docs, and scripts referenced from `agents/analyze-repo.md`.




<% checklist
`agents/analyze-repo.md` committed in your fork with role, I/O, and constraints
Index files (or equivalent) specified: when built, how refreshed, how the agent uses them
Context management section targets **40% or less** of usable context for a defined “typical” run
Scripts for deterministic steps referenced and documented (how to invoke or assume them)
Supporting files and limitations (if any) match what you describe in the spec
%>

<% links
 [Lab 1](labs/lab-1.md)
%>