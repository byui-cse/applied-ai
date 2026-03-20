# Introduction - Day 1
## Getting Started with the Course

> **Course goal:** Students **do not** write the implementation code by hand. You may type prompts, edit markdown, run approved commands, and critique outputs, but not the code.

## Preparation

1. Clone **[Canvas LMS](https://github.com/instructure/canvas-lms)** locally
2. Install your favorite IDE or CLI tool. I would recommend one of the following:
    - Github Copilot with [VS Code](https://code.visualstudio.com/)
    - [Claude Code](https://code.claude.com/docs/en/quickstart)
    - [Cursor](https://cursor.com/download) (IDE or `cursor agents`)

## Definitions

Please review the following definitions

### What is Brownfield?

Brownfield projects refer to working with existing systems, software, or codebases that are already in use—often large, complex, and built over many years. Instead of starting from scratch (a "greenfield" project), brownfield work means improving, extending, or integrating with what’s already there. This usually involves navigating legacy code, understanding prior design decisions, and finding ways to evolve or modernize the system without breaking what’s already working.

### What is Greenfield?

Greenfield development refers to starting a project from scratch, without any constraints imposed by existing code, systems, or architecture. In a greenfield project, you have the freedom to design and build new solutions using the latest technologies, best practices, and modern patterns—without the need to account for legacy decisions or technical debt. This approach allows for more creativity and flexibility, but often means you need to establish everything from the ground up, such as infrastructure, workflows, and conventions.

<% quiz assessments/phase-1/week-1/green-brown.json %>

### Context Window

**Context window** (in the context of large language models, or LLMs) refers to the maximum amount of text—measured in tokens or words—that the model can "see," process, and use at one time during a conversation or task. Everything within this window (such as recent messages, code snippets, or document content) is available for the model to consider when generating its response. Information outside the context window is forgotten or ignored by the model, meaning it cannot influence responses unless it is reintroduced. The size of the context window determines how much background, history, or detail an LLM can reason about at once.

### Context Management

**Context management** refers to the practice of carefully controlling how much information is kept "in view" for an AI system at any given time—typically aiming to use less than 40% of the available context window. This ensures that only the most relevant, necessary details are present, avoiding information overload. Good context management helps AI models remain focused, efficient, and accurate by preventing important details from being drowned out by excessive or outdated information. In practical terms, this means thoughtfully selecting, summarizing, or archiving content to maintain clarity and performance within the model's limits.

<% quiz assessments/phase-1/week-1/context.json %>

---

## Lab 1 - Set up Canvas-LMS

**Lab Instructions:** [`labs/lab-1.md`](labs/lab-1.md) — fork the course repo, AWS Academy EC2, and Remote SSH. Session 2 (markdown systems for teams): [`day-2.md`](day-2.md).
