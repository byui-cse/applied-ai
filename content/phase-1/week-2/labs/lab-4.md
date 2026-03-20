# Lab 4 — Plan Creation & MCP 

You will **connect** the official [GitHub MCP Server](https://github.com/github/github-mcp-server) to your AI tooling and author an agent that turns your Lab 3 requirements package into a **real GitHub Project** on the **correct repository**, populated with **user stories** (and supporting work items) derived from your research—not from guesswork.

**Prerequisites:** Complete [`lab-1.md`](../../week-1/labs/lab-1.md) (fork, EC2, Remote SSH), [`lab-2.md`](../../week-1/labs/lab-2.md) (`agents/analyze-repo.md`), and [`lab-3.md`](lab-3.md) (`agents/tasks/feature-1/implementation-research.md` with a clear **Lab 4 handoff** section). Complete the PAT preparation in [`day-2.md`](../day-2.md).

---

## Goal

By the end of this lab:

1. **GitHub MCP** is configured and working in **Cursor**, **Claude Code**, and **GitHub Copilot** (per the instructions below—use the paths that match your installed versions).
2. You have **`agents/project-creation.md`**: an agent specification that tells an LLM how to use the MCP **together with** your Lab 3 artifacts to create and populate a project plan.
3. You can **demonstrate** that an AI session, following that agent, created the **entire** GitHub Project structure for your feature on the **intended** fork/repository—including **all necessary stories** (and clearly labeled tasks or milestones where your handoff calls for them).

---

## Repository layout (required)

In your **fork** of the course repository, add or extend:

| Path | Purpose |
|------|--------|
| `agents/project-creation.md` | Agent spec: role, inputs (paths to Lab 3 files), outputs, step-by-step use of GitHub MCP tools, guardrails, and how you verify success. |

You may add a short **`docs/`** or **`agents/`** note listing which MCP host you used for the graded demo (optional but helpful for grading).

---

## Part A — GitHub Personal Access Token (PAT)

The GitHub MCP Server acts on your behalf. Create a **fine-grained** or **classic** PAT with the **minimum** scopes needed for this lab.

**Typical needs for this lab**

| Capability | Why |
|------------|-----|
| Repository contents & issues | Create **issues** that represent **user stories** and link them to your project. |
| Projects | Create and update a **GitHub Project** (board) and add items. |

Follow GitHub’s guide: [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). **Do not commit** the token. Prefer environment variables or your host’s secret inputs.

**Official server reference:** [github/github-mcp-server](https://github.com/github/github-mcp-server) (installation, remote vs local, toolsets, read-only mode).

---

## Part B — Enable the `projects` toolset (recommended)

The GitHub MCP Server groups tools into **toolsets**. For GitHub Projects, ensure the **`projects`** toolset is available (plus whatever you need for issues and repos—see the server README for defaults and the `GITHUB_TOOLSETS` environment variable).

If your host lets you pass environment variables to a local server, you can start with:

```bash
GITHUB_TOOLSETS="default,projects"
```

Adjust if your instructor asks for a stricter allow-list. When in doubt, read the **Toolsets** section of the [GitHub MCP Server README](https://github.com/github/github-mcp-server).

---

## Part C — Configure the GitHub MCP Server in each environment

Use **one** of the deployment models from the official repo:

- **Remote (hosted)** — simplest if your app supports HTTP MCP and GitHub’s remote endpoint (OAuth or PAT). See **“Remote GitHub MCP Server”** in the [README](https://github.com/github/github-mcp-server).
- **Local (Docker)** — runs `ghcr.io/github/github-mcp-server` with `GITHUB_PERSONAL_ACCESS_TOKEN`. See **“Local GitHub MCP Server”** in the [README](https://github.com/github/github-mcp-server).

Complete **one of the three** host setups below so you can work the same workflow in different tools.

### 1. Cursor

1. Open Cursor’s **MCP** settings (location varies by version; search the UI for “MCP” or “Model Context Protocol”).
2. Add a server entry for GitHub using either the **remote URL** pattern or the **Docker/stdio** pattern from the [GitHub MCP Server README — “Install in Other MCP Hosts” / Cursor](https://github.com/github/github-mcp-server).
3. Supply the PAT via your host’s supported mechanism (prompt, env var, or header—**never** paste into tracked project files).
4. Restart or reload MCP if required, then confirm GitHub tools appear in the agent/tool panel.

Optional: workspace file **`.vscode/mcp.json`** is a common way to share the same shape of config with other tools—see the upstream examples in the README.

### 2. Claude Code

1. Follow Anthropic’s current documentation for **adding an MCP server** to Claude Code (config file or CLI—whichever your version supports).
2. Point the configuration at the same GitHub MCP deployment you used for Cursor (remote HTTP or local Docker/stdio).
3. Ensure `GITHUB_PERSONAL_ACCESS_TOKEN` (or equivalent) is available to the process **without** storing it in the repo.

### 3. GitHub Copilot (VS Code / Copilot Chat)

1. Use a **recent** VS Code build that supports MCP and, if using the remote server, the OAuth/PAT flow described in the [README](https://github.com/github/github-mcp-server) under **“Remote GitHub MCP Server”** and **“Install in VS Code”**.
2. Add the GitHub MCP server entry to your Copilot/MCP configuration as directed in the same README section.
3. Toggle **Agent** mode (or your product’s equivalent) so tool use is permitted, then verify GitHub tools load.

If your campus blocks remote endpoints, prefer the **Docker**-based local server from the README.

---

## Minimum requirements

Your **`agents/project-creation.md`** must show how you satisfy **all** of the following.

### 1. Inputs and source of truth

- **Primary input:** `agents/tasks/feature-1/implementation-research.md` from Lab 3 (especially the **Lab 4 handoff** section: milestones, tasks, dependencies, definition of done).
- **Secondary context:** `agents/tasks/feature-1/feature-1.md` for the one-line problem framing, if needed.
- **Repository targeting:** Explicit instructions for **owner**, **repo name**, and **branch/default ref** the project belongs to (your **course fork** unless your instructor specifies otherwise). The agent must **not** create projects against random repositories.

### 2. Orchestration with GitHub MCP

Describe **which categories of MCP tools** the model should use (names may vary by server version—refer to your connected tool list), for example:

- Create or select a **GitHub Project** tied to the right owner/repo context.
- Create **issues** that represent **user stories** (title + body with acceptance hints).
- Add those issues (or drafts) to the project and set **priority / status / iteration** fields *if* your project template uses them.

You are not graded on quoting exact tool names from memory—**you are** graded on a **repeatable procedure** that matches what appears when MCP is connected.

### 3. Integration with Lab 2 (analyze-repo)

Include at least **one** concrete instruction that ties a **story** or milestone to **evidence** from your Lab 2 workflow (for example: “for each major subsystem identified in `implementation-research.md` § Codebase analysis, ensure there is a story or sub-task that references that subsystem”). This connects planning to the brownfield reality you already captured.

### 4. Completeness and “necessary stories”

The agent spec must require the AI to derive **all** stories needed to deliver the feature **as scoped in Lab 3**:

- Cover **in-scope** functional requirements (group or split into stories as appropriate).
- Reflect **testing and verification** work as explicit stories or acceptance subtasks (so “done” is provable).
- Represent **dependencies** between stories or phases when your handoff calls for them (GitHub issue linking, project dependencies, or labels—pick one approach and document it).

### 5. Verification

Document how **you** (the human) confirm success without trusting the model blindly:

- Links to the **Project** and **Issues** in the target repo.
- A short checklist that the set of stories **maps** to the Lab 3 functional requirements (traceability).

---

## What you turn in

- **`agents/project-creation.md`** meeting the minimum requirements above.
- **Evidence** of a successful run: URL(s) or screenshots your instructor allows, showing the created **GitHub Project** on the **correct** repository and the **story/issue** set. Redact tokens and secrets.

---

## Template (optional)

You may start from this outline and replace the placeholders.

<% editor markdown "# Role\n\n# Inputs (paths)\n\n# Target repository\n\n# Constraints (no wrong repo, no secrets in files)\n\n# Steps — GitHub MCP\n\n## Create or attach Project\n\n## Create user stories (Issues)\n\n## Link to Lab 3 requirements\n\n## Tie to Lab 2 / codebase findings\n\n# Verification checklist\n\n# Example session notes (no secrets)" %>

---

## What we intentionally omit

There is **no** requirement to implement your Canvas feature in this lab—only to **materialize the plan** in GitHub using MCP-backed automation. You also do **not** need to write a custom MCP server; use the **official** [GitHub MCP Server](https://github.com/github/github-mcp-server).

## Rubric

## Grading Rubric

| Criteria                                                                                                                    | Points |
|-----------------------------------------------------------------------------------------------------------------------------|--------|
| **1. `agents/project-creation.md` specifies a clear agent role, input paths, and correct target repository**                |   4    |
| **2. Constraints section prevents wrong repo modifications and exclusion of secrets in files**                              |   4    |
| **3. Explicit, repeatable steps for using GitHub MCP tools (project creation, issue/user story generation, assignment)**    |   5    |
| **4. Clear procedure for mapping Lab 3 functional requirements to user stories/issues in the GitHub Project**               |   5    |
| **5. Includes at least one link between Lab 2 codebase findings and stories/milestones (codebase analysis traceability)**   |   4    |
| **6. Explicit handling of story dependencies, testing/verification tasks, and acceptance criteria mapping ("done" = provable)|   4    |
| **7. Concrete verification procedure/checklist so a human can confirm correct Project/Issues and criterion mapping**         |   2    |
| **8. Evidence of a successful run included (screenshots, URLs) per instructions, with no secrets exposed**                  |   2    |

**Total:** 30 points

#### Evaluation Notes:
- Partial credit may be awarded for incomplete or partial fulfillment within each rubric item.
- Maximum credit requires documentation that follows all minimum requirements, links to Lab 2 and Lab 3 work, and alignment of project artifacts/outputs to the course objectives.
- No implementation code or Canvas feature delivery is required in this lab; focus is on agent spec and project/issue setup and documentation.


<% checklist
GitHub MCP configured in Cursor, Claude Code, and GitHub Copilot (per README); PAT scopes minimized and token not committed
`projects` (and related) toolsets understood; GitHub tools visible in the host
`agents/project-creation.md` specifies inputs from Lab 3, correct repo targeting, MCP orchestration, Lab 2 traceability, and verification
Demonstrated run: GitHub Project on the intended repo with all necessary user stories / work items aligned to Lab 3 scope
No secrets in the repository; evidence submitted per instructor instructions
%>

<% links
[Lab 3](lab-3.md)
[Day 2 — MCP & definitions](../day-2.md)
[GitHub MCP Server](https://github.com/github/github-mcp-server)
[Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
%>
