#!/usr/bin/env python3
"""Create unpublished wiki page 'Instructor Notes (Do NOT Publish)' as first module item."""
from __future__ import annotations

import json
import ssl
import urllib.request
from pathlib import Path

CANVAS_DIR = Path(__file__).resolve().parent
REPO = CANVAS_DIR.parent
COURSE_ID = 406352
MODULE_ID = 4542815

PAGE_TITLE = "Instructor Notes (Do NOT Publish)"

# Matches course newspaper shell (inline styles only); staff-only banner at top.
PAGE_BODY = """<div style="margin:0;padding:0;font-family:Georgia,'Times New Roman',Times,serif;font-size:16px;line-height:1.65;color:#0f0e0d;background-color:#ebe6dc;padding:clamp(12px,3vw,22px);">
<div style="max-width:52rem;margin:0 auto;">
<div style="background-color:#faf6ef;border:1px solid rgba(15,14,13,0.12);border-radius:3px;padding:clamp(18px,3vw,28px);">
<p style="margin:0 0 1em 0;padding:0.6rem 0.75rem;background:rgba(107,20,20,0.08);border-left:3px solid #6b1414;font-size:0.95rem;"><strong>Staff only.</strong> Keep this page <strong>unpublished</strong> so students cannot read these notes.</p>
<h1 style="font-family:Georgia,serif;font-size:1.45rem;margin:0 0 0.75rem 0;color:#0f0e0d;">Week 1 — Brownfield · Instructor briefing (~20 min)</h1>
<p style="margin:0 0 1.25em 0;color:#3d3832;">Quick prep for <strong>face-to-face</strong> and <strong>online</strong> sections. Week 1 introduces the brownfield codebase (<strong>Canvas LMS</strong>), context discipline, agents/markdown, and two scaffolded labs.</p>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Course frame</h2>
<ul style="margin:0 0 1.1em 0;padding-left:1.35em;">
<li style="margin:0.35em 0;">Juniors/seniors; <strong>applied AI for software engineering</strong>—students work <strong>through</strong> AI for the workflow, not hand-authored production code.</li>
<li style="margin:0.35em 0;"><strong>Phase 1 (weeks 1–7):</strong> brownfield; upstream example: <a href="https://github.com/instructure/canvas-lms" style="color:#6b1414;">instructure/canvas-lms</a>.</li>
<li style="margin:0.35em 0;"><strong>Gradebook:</strong> Prepare 20% · Class Work 20% · Labs 60%.</li>
</ul>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Module flow (Brownfield — Week 1)</h2>
<ol style="margin:0 0 1.1em 0;padding-left:1.35em;">
<li style="margin:0.35em 0;"><strong>Day 1:</strong> Prepare 1.1 → Instruction 1.1: Context → Lab 1.1: Setup Canvas (fork, EC2, Remote SSH, clone on instance).</li>
<li style="margin:0.35em 0;"><strong>Day 2:</strong> Instruction 1.2: Agents (wiki) → Prepare 1.2 → Lab 1.2: Analysis Agent (<code style="font-size:0.9em;">agents/analyze-repo.md</code>, indexes, context budget, scripts).</li>
</ol>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Teaching moves</h2>
<ul style="margin:0 0 1.1em 0;padding-left:1.35em;">
<li style="margin:0.35em 0;"><strong>F2F:</strong> Short intro on greenfield vs brownfield and why a “map” beats a whole-repo paste; demo finding <code>README</code>/<code>doc/</code> without loading everything. Budget time for <strong>AWS Learner Lab + SSH</strong>—the main Lab 1.1 bottleneck.</li>
<li style="margin:0.35em 0;"><strong>Online:</strong> Async “ready to go” checklist (AWS lab access, GitHub). Route PEM/security-group/Remote SSH questions to announcements or OH; use live time for concepts and Lab 1.2 rubric alignment.</li>
<li style="margin:0.35em 0;"><strong>Both:</strong> <strong>Prepare</strong> = vocabulary; <strong>Instruction</strong> = reflection/prompts; <strong>Labs</strong> = evidence + rubrics in SpeedGrader.</li>
</ul>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Where students stall</h2>
<ul style="margin:0 0 1.1em 0;padding-left:1.35em;">
<li style="margin:0.35em 0;"><strong>Lab 1.1:</strong> EC2 SG, <code>chmod 400</code>, SSH config—offer one anonymized “good” config pattern (never share private keys).</li>
<li style="margin:0.35em 0;"><strong>Vocabulary:</strong> context <em>window</em> vs <em>management</em>—tie back to Instruction 1.1 and Prepare quizzes.</li>
<li style="margin:0.35em 0;"><strong>Lab 1.2:</strong> Vague specs—point to rubric (indexes, ≤40% context, scripts out-of-LLM) and the lab’s template spine.</li>
</ul>

<h2 style="font-family:Georgia,serif;font-size:1.15rem;margin:1.5rem 0 0.5rem 0;border-bottom:1px solid rgba(15,14,13,0.15);padding-bottom:0.25rem;">Logistics</h2>
<ul style="margin:0 0 0;padding-left:1.35em;">
<li style="margin:0.35em 0;">Align due dates with your section policy.</li>
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
    syncs.insert(
        0,
        {
            "kind": "wiki_page",
            "name": PAGE_TITLE,
            "source": ".canvas/create_instructor_notes_week1.py",
            "canvas_page_slug": str(slug),
            "canvas_module_item_id": mid,
            "published": False,
            "audience": "instructors_only",
            "note": "Unpublished page; first item in Brownfield - Week 1 module",
        },
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
