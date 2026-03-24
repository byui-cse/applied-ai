#!/usr/bin/env python3
"""Create unpublished wiki page for Week 2 instructor notes as first item in Brownfield - Week 2 module."""
from __future__ import annotations

import json
import ssl
import urllib.request
from pathlib import Path

CANVAS_DIR = Path(__file__).resolve().parent
REPO = CANVAS_DIR.parent
COURSE_ID = 406352
MODULE_ID = 4543209  # Brownfield - Week 2

PAGE_TITLE = "Instructor Notes — Week 2 (Do NOT Publish)"

# Matches course newspaper shell (inline styles only); staff-only banner at top.
PAGE_BODY = """<div style="margin:0;padding:0;font-family:Georgia,'Times New Roman',Times,serif;font-size:16px;line-height:1.65;color:#0f0e0d;background-color:#ebe6dc;padding:clamp(12px,3vw,22px);">
<div style="max-width:52rem;margin:0 auto;">
<div style="background-color:#faf6ef;border:1px solid rgba(15,14,13,0.12);border-radius:3px;padding:clamp(18px,3vw,28px);">
<p style="margin:0 0 1em 0;padding:0.6rem 0.75rem;background:rgba(107,20,20,0.08);border-left:3px solid #6b1414;font-size:0.95rem;"><strong>Staff only.</strong> Keep this page <strong>unpublished</strong> so students cannot read these notes.</p>
<h1 style="font-family:Georgia,serif;font-size:1.45rem;margin:0 0 0.75rem 0;color:#0f0e0d;">Week 2 — Brownfield · Instructor briefing (~20 min)</h1>
<p style="margin:0 0 1.25em 0;color:#3d3832;">Quick prep for <strong>face-to-face</strong> and <strong>online</strong> sections. Week 2 moves from repository analysis to <strong>feature selection</strong>, <strong>requirements and research</strong> (<code style="font-size:0.9em;">implementation-research.md</code>), <strong>MCP</strong> + <strong>GitHub Projects</strong>, and a <strong>table pitch</strong> with peer feedback.</p>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Course frame</h2>
<ul style="margin:0 0 1.1em 0;padding-left:1.35em;">
<li style="margin:0.35em 0;">Same brownfield spine: <strong>Canvas LMS</strong> fork; students still work <strong>through</strong> AI for workflow, not shipping production Canvas code in these labs.</li>
<li style="margin:0.35em 0;"><strong>Gradebook:</strong> Prepare 20% · Class Work 20% · Labs 60%.</li>
<li style="margin:0.35em 0;"><strong>Module lock:</strong> Confirm <strong>unlock</strong> dates if you stagger sections; Week 2 content assumes Lab 1.x groundwork is done.</li>
</ul>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Module flow (Brownfield — Week 2)</h2>
<ol style="margin:0 0 1.1em 0;padding-left:1.35em;">
<li style="margin:0.35em 0;"><strong>Day 3 — Feature Planning:</strong> Instruction 2.1 (wiki) → Prepare 2.1 → Lab 2.1: Feature Agent (<code style="font-size:0.9em;">implementation-research.md</code>, Lab 2 agent, requirements/testing plan).</li>
<li style="margin:0.35em 0;"><strong>Day 4 — Project Planning:</strong> Prepare 2.2 (MCP/vocabulary) → Instruction 2.2 (table pitch + submit peer feedback) → Lab 2.2: Project Planning (<code style="font-size:0.9em;">agents/project-creation.md</code>, GitHub MCP, Projects).</li>
</ol>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Teaching moves</h2>
<ul style="margin:0 0 1.1em 0;padding-left:1.35em;">
<li style="margin:0.35em 0;"><strong>F2F:</strong> Short connect from Week 1 analysis agent to “what we build.” Use Lab 2.1 to enforce <strong>traceability</strong> (reqs → codebase hypotheses → verification). For Lab 2.2, budget time for <strong>PAT scope</strong>, <strong>MCP host config</strong> (Cursor / Claude Code / Copilot), and “wrong repo” guardrails.</li>
<li style="margin:0.35em 0;"><strong>Online:</strong> Table pitch for Instruction 2.2 may need <strong>async alternative</strong> (partner feedback in discussion or short video)—spell that in announcements if needed.</li>
<li style="margin:0.35em 0;"><strong>Both:</strong> <strong>Prepare</strong> = definitions; <strong>Instruction 2.2</strong> = participation/feedback capture; <strong>Labs</strong> = rubric-graded artifacts and URLs (redact secrets in submissions).</li>
</ul>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Where students stall</h2>
<ul style="margin:0 0 1.1em 0;padding-left:1.35em;">
<li style="margin:0.35em 0;"><strong>Lab 2.1:</strong> Scope creep vs. “research only”—point to rubric rows and explicit in/out of scope; ensure Lab 2 agent usage is evidenced, not asserted.</li>
<li style="margin:0.35em 0;"><strong>Prepare 2.2 / MCP:</strong> Confusing MCP with “the model” or with Git alone—tie back to day-2 definitions.</li>
<li style="margin:0.35em 0;"><strong>Lab 2.2:</strong> Projects created on the <strong>wrong repo</strong>, PATs in commits, or empty GitHub Project—rubric rewards explicit targeting, verification checklist, and evidence URLs.</li>
</ul>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Logistics</h2>
<ul style="margin:0 0 0;padding-left:1.35em;">
<li style="margin:0.35em 0;">Align due dates with your section policy (defaults in repo index use <strong>America/Boise</strong>).</li>
<li style="margin:0.35em 0;">Labs use native Canvas rubrics—partial credit at your discretion.</li>
<li style="margin:0.35em 0;">Course markdown lives in Git; Canvas is delivery—resync after content edits.</li>
</ul>
</div>
</div>
</div>"""


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, _, v = line.partition("=")
            out[k.strip()] = v.strip()
    return out


def api_request(method: str, url: str, token: str, *, body: dict | None = None) -> dict | list | str:
    data = json.dumps(body).encode() if body is not None else None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx) as r:
        raw = r.read().decode()
        if r.status == 204 or not raw:
            return ""
        return json.loads(raw)


def main() -> None:
    env = load_env(REPO / "available_tools/.env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    created = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/pages",
        token,
        body={
            "wiki_page": {
                "title": PAGE_TITLE,
                "body": PAGE_BODY,
                "published": False,
                "editing_roles": "teachers",
            }
        },
    )
    if not isinstance(created, dict):
        raise RuntimeError("unexpected pages response")
    slug = created.get("url")
    if not slug:
        raise RuntimeError("no url slug in response")
    print("Created page slug:", slug)

    mod = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "Page",
                "page_url": str(slug),
                "position": 1,
                "title": PAGE_TITLE,
                "published": False,
            }
        },
    )
    mid = None
    if isinstance(mod, dict):
        mid = mod.get("id")
    print("Module item:", mod)

    idx_path = CANVAS_DIR / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    syncs = idx.setdefault("syncs", [])
    insert_at = 0
    for i, s in enumerate(syncs):
        if s.get("kind") == "module_subheader" and s.get("title") == "Day 3 - Feature Planning":
            insert_at = i
            break
    syncs.insert(
        insert_at,
        {
            "kind": "wiki_page",
            "name": PAGE_TITLE,
            "source": ".canvas/create_instructor_notes_week2.py",
            "canvas_page_slug": str(slug),
            "canvas_module_item_id": mid,
            "published": False,
            "audience": "instructors_only",
            "canvas_module_id": MODULE_ID,
            "note": "Unpublished page; first item in Brownfield - Week 2 module",
        },
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
