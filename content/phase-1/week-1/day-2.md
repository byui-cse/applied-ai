# Introduction - Day 2
## Your First Agent

> **Markdown Review:** review the [Markdown Cheatsheet](https://www.markdownguide.org/basic-syntax/) for tips and tricks on how to create markdown.

## Definitions

The following are definitions in context to LLMs, AI, and software engineering for this section.

### Agents

An AI agent is a system that perceives its environment, processes information, and acts autonomously to achieve specific goals. These agents can adapt their actions based on data, feedback, and changes in their surroundings. AI agents are commonly found in applications like virtual assistants, robotics, and automated systems.  
[Source: IBM — AI Agents](https://www.ibm.com/think/topics/ai-agents)

### Markdown

Markdown is a lightweight markup language used to format text with simple symbols, making documents easy to read and write. In the AI and LLM context, markdown enables you to organize prompts, responses, and documentation with clear structure and emphasis. It's widely supported by LLM interfaces, making collaboration and knowledge sharing more effective.

<% quiz assessments/phase-1/week-1/agents-and-markdown.json %>

## Practice

<% editor markdown-with-preview assessments/phase-1/week-1/markdown-practice.json %>

---

## Lab 2 — Repository analysis agent

**Lab instructions:** [`labs/lab-2.md`](labs/lab-2.md) — you will define an LLM agent that scans a repository (what it reads, how it chunks work, and how it records findings). In your fork, create an `agents` folder and add a markdown file named `analyze-repo.md` that documents your agent: how it behaves, what tools or scripts it relies on, and how you keep context use efficient. **Minimum requirements** (your spec must cover all of these): **(1)** create or maintain **index files** so the agent can navigate the repo quickly without re-reading everything; **(2)** follow **context-management** practices so the agent targets **40% or less** of the available context budget for typical runs; **(3)** provide **agent scripts** for steps that should run **outside** the LLM (shell, search, indexing, etc.). The lab does **not** include a ready-made prompt—you decide the wording while meeting those requirements.
