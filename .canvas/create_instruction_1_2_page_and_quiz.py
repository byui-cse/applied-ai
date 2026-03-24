#!/usr/bin/env python3
"""Publish wiki page Instruction 1.2: Agents + classic quiz Prepare: 1.2 - Agents and Markdown."""
from __future__ import annotations

import html
import json
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CANVAS_DIR = Path(__file__).resolve().parent
REPO = CANVAS_DIR.parent
sys.path.insert(0, str(CANVAS_DIR))
from build_canvas_content import build_from_markdown  # noqa: E402

COURSE_ID = 406352
MODULE_ID = 4542815
PREPARE_GROUP_ID = 2320233
TOTAL_POINTS = 10.0
DUE = datetime(2026, 4, 23, 10, 15, tzinfo=ZoneInfo("America/Boise"))

# Fourth distractor for each agents-and-markdown MC question
EXTRA_AGENTS = [
    "A passive document that cannot interact with tools or external systems",
    "A static README file checked into version control only",
    "A single-turn chat reply with no memory of prior messages",
    "A proprietary file format used only inside one IDE vendor",
]

# Wrong markdown options for practice challenges (3 each; correct is expectedMarkdown)
MD1_WRONG = [
    "# Quick start",
    "### Quick start",
    "Quick start",
]
MD2_WRONG = [
    "This is *important* for the team.",
    "This is important for the team.",
    "This uses the word important but without emphasis markers.",
]
MD3_WRONG = [
    "1. First item\n2. Second item",
    "* First item\n* Second item",
    "+ First item\n+ Second item",
]


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


def api_request(
    method: str,
    url: str,
    token: str,
    *,
    body: dict | None = None,
) -> dict | list | str:
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


def build_quiz_description_html(canvas_base_url: str, page_slug: str) -> str:
    page_url = f"{canvas_base_url}/courses/{COURSE_ID}/pages/{page_slug}"
    return f"""<div style="margin:0;padding:0;font-family:Georgia,'Times New Roman',Times,serif;font-size:17px;line-height:1.68;color:#0f0e0d;background-color:#ebe6dc;padding:clamp(12px,3vw,22px);">
<div style="max-width:52rem;margin:0 auto;">
<div style="background-color:#faf6ef;border:1px solid rgba(15,14,13,0.12);border-radius:3px;box-shadow:0 1px 0 rgba(255,255,255,0.55) inset,0 10px 28px rgba(15,12,8,0.05);padding:clamp(20px,3vw,32px);">
<ul style="margin:0;padding-left:1.35em;">
<li style="margin:0.4em 0;">Review <a href="{page_url}" style="color:#6b1414;text-decoration:underline;text-underline-offset:0.2em;">Instruction 1.2: Agents</a> before you begin.</li>
<li style="margin:0.4em 0;"><strong>Unlimited attempts.</strong> Your <strong>highest</strong> score is kept.</li>
</ul>
</div>
</div>
</div>"""


def load_agents_mc() -> list[dict]:
    data = json.loads(
        (REPO / "assessments/phase-1/week-1/agents-and-markdown.json").read_text(encoding="utf-8")
    )
    out: list[dict] = []
    for i, q in enumerate(data["questions"]):
        choices = list(q["choices"]) + [EXTRA_AGENTS[i]]
        ci = int(q["correctIndex"])
        out.append(
            {
                "prompt": q["prompt"],
                "choices": choices,
                "correct_index": ci,
                "correct_comments": data.get("feedbackCorrect", ""),
                "incorrect_comments": data.get("feedbackIncorrect", ""),
            }
        )
    return out


def load_markdown_practice_mc() -> list[dict]:
    data = json.loads(
        (REPO / "assessments/phase-1/week-1/markdown-practice.json").read_text(encoding="utf-8")
    )
    challenges = data["challenges"]
    wrong_sets = [MD1_WRONG, MD2_WRONG, MD3_WRONG]
    out: list[dict] = []
    for ch, wrongs in zip(challenges, wrong_sets, strict=True):
        correct = ch["expectedMarkdown"]
        choices = [correct] + list(wrongs)
        # Correct is always index 0 before shuffle; we'll shuffle indices when posting
        out.append(
            {
                "prompt": ch["prompt"],
                "choices": choices,
                "correct_index": 0,
                "correct_comments": "Matches the reference markdown.",
                "incorrect_comments": "Compare your answer to the syntax in the Instruction page and Markdown cheatsheet.",
            }
        )
    return out


def points_split(n: int, total: float) -> list[float]:
    base = round(total / n, 2)
    pts = [base] * n
    pts[-1] = round(pts[-1] + (total - sum(pts)), 2)
    return pts


def main() -> None:
    env = load_env(REPO / "available_tools/.env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    page_html = build_from_markdown(
        REPO / "content/phase-1/week-1/day-2.md",
        masthead="Applied AI · Instruction 1.2",
        strip_reader_sections=True,
    )

    page_created = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/pages",
        token,
        body={
            "wiki_page": {
                "title": "Instruction 1.2: Agents",
                "body": page_html,
                "published": True,
                "editing_roles": "teachers",
            }
        },
    )
    if not isinstance(page_created, dict):
        raise RuntimeError("unexpected wiki_page response")
    page_slug = page_created.get("url") or page_created.get("page_id")
    if not page_slug:
        raise RuntimeError(f"no slug in page response: {page_created.keys()}")
    print("Wiki page created:", page_slug, page_created.get("html_url"))

    desc_html = build_quiz_description_html(base, str(page_slug))

    quiz_body = {
        "quiz": {
            "title": "Prepare: 1.2 - Agents and Markdown",
            "description": desc_html,
            "quiz_type": "assignment",
            "published": True,
            "shuffle_answers": True,
            "allowed_attempts": -1,
            "scoring_policy": "keep_highest",
            "show_correct_answers": True,
            "due_at": DUE.isoformat(),
        }
    }
    created = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/quizzes",
        token,
        body=quiz_body,
    )
    if not isinstance(created, dict):
        raise RuntimeError("unexpected quiz response")
    quiz_id = created["id"]
    assignment_id = created.get("assignment_id")
    print("Quiz id:", quiz_id, "assignment_id:", assignment_id)

    mc_agents = load_agents_mc()
    mc_md = load_markdown_practice_mc()
    questions = mc_agents + mc_md
    n = len(questions)
    point_list = points_split(n, TOTAL_POINTS)

    for pos, (q, pts) in enumerate(zip(questions, point_list, strict=True), start=1):
        choices = q["choices"]
        correct_idx = int(q["correct_index"])
        answers = []
        for j, text in enumerate(choices):
            weight = 100 if j == correct_idx else 0
            answers.append({"answer_text": text, "answer_weight": weight})
        qbody = {
            "question": {
                "question_name": f"Q{pos}",
                "question_type": "multiple_choice_question",
                "question_text": f"<p>{html.escape(q['prompt'])}</p>",
                "points_possible": pts,
                "position": pos,
                "correct_comments": q["correct_comments"],
                "incorrect_comments": q["incorrect_comments"],
                "answers": answers,
            }
        }
        api_request(
            "POST",
            f"{base}/api/v1/courses/{COURSE_ID}/quizzes/{quiz_id}/questions",
            token,
            body=qbody,
        )
        print("  Question", pos, "/", n)

    api_request(
        "PUT",
        f"{base}/api/v1/courses/{COURSE_ID}/quizzes/{quiz_id}",
        token,
        body={"quiz": {"points_possible": TOTAL_POINTS}},
    )
    print("Quiz points_possible set to", TOTAL_POINTS)

    if assignment_id:
        api_request(
            "PUT",
            f"{base}/api/v1/courses/{COURSE_ID}/assignments/{assignment_id}",
            token,
            body={
                "assignment": {
                    "due_at": DUE.isoformat(),
                    "assignment_group_id": PREPARE_GROUP_ID,
                }
            },
        )
        print("Updated assignment due_at + Prepare group")

    # Module: Page then Quiz after existing items (positions 6 and 7)
    api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "Page",
                "page_url": str(page_slug),
                "position": 6,
                "title": "Instruction 1.2: Agents",
            }
        },
    )
    print("Module item: Page @ 6")

    api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "Quiz",
                "content_id": str(quiz_id),
                "position": 7,
                "title": "Prepare: 1.2 - Agents and Markdown",
            }
        },
    )
    print("Module item: Quiz @ 7")

    idx_path = CANVAS_DIR / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    syncs = idx.setdefault("syncs", [])
    syncs.append(
        {
            "kind": "wiki_page",
            "name": "Instruction 1.2: Agents",
            "source": "content/phase-1/week-1/day-2.md",
            "canvas_page_slug": str(page_slug),
        }
    )
    syncs.append(
        {
            "kind": "quiz",
            "name": "Prepare: 1.2 - Agents and Markdown",
            "canvas_quiz_id": quiz_id,
            "canvas_assignment_id": assignment_id,
            "points_total": int(TOTAL_POINTS),
            "due_at": "2026-04-23T10:15:00 America/Boise",
            "attempts": "unlimited",
            "scoring_policy": "keep_highest",
            "sources": [
                "assessments/phase-1/week-1/agents-and-markdown.json",
                "assessments/phase-1/week-1/markdown-practice.json",
            ],
        }
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
