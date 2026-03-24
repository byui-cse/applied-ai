#!/usr/bin/env python3
"""Create classic Canvas quiz 'Prepare: 1.1 - Green, Brown, Context' via REST API.

New Quizzes are not created through this endpoint; Instructure exposes classic
quizzes at POST /api/v1/courses/:id/quizzes. Use this or build in UI for NQ.
"""
from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
COURSE_ID = 406352
MODULE_ID = 4542815  # Brownfield - Week 1
# Assignment for "Instruction 1.1: Context" (review before quiz)
INSTRUCTION_ASSIGNMENT_ID = 16666079
TOTAL_QUIZ_POINTS = 10.0


def build_quiz_description_html(canvas_base_url: str, instruction_assignment_id: int) -> str:
    """Short Canvas quiz intro: link to instruction + attempts policy (inline styles, matches course shell)."""
    assignment_url = f"{canvas_base_url}/courses/{COURSE_ID}/assignments/{instruction_assignment_id}"
    return f"""<div style="margin:0;padding:0;font-family:Georgia,'Times New Roman',Times,serif;font-size:17px;line-height:1.68;color:#0f0e0d;background-color:#ebe6dc;padding:clamp(12px,3vw,22px);">
<div style="max-width:52rem;margin:0 auto;">
<div style="background-color:#faf6ef;border:1px solid rgba(15,14,13,0.12);border-radius:3px;box-shadow:0 1px 0 rgba(255,255,255,0.55) inset,0 10px 28px rgba(15,12,8,0.05);padding:clamp(20px,3vw,32px);">
<ul style="margin:0;padding-left:1.35em;">
<li style="margin:0.4em 0;">Review <a href="{assignment_url}" style="color:#6b1414;text-decoration:underline;text-underline-offset:0.2em;">Instruction 1.1: Context</a> before you begin.</li>
<li style="margin:0.4em 0;"><strong>Unlimited attempts.</strong> Your <strong>highest</strong> score is kept.</li>
</ul>
</div>
</div>
</div>"""


# Fourth distractor per question (JSON assessments have 3 choices each)
EXTRA_GREEN = [
    "A project limited to changing only marketing copy, with no engineering work",
    "You are required to keep every legacy module even if you replace behavior",
    "Having no production traffic or users to worry about",
    "You must postpone choosing a stack until after the first release",
]

EXTRA_CONTEXT = [
    "The fixed pixel height of the IDE chat panel",
    "It is merged automatically into long-term vector memory without loss",
    "Between 95% and 100% so the model uses the entire window every time",
    "To paste the full repository into each prompt for completeness",
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
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            raw = r.read().decode()
            if r.status == 204 or not raw:
                return ""
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        raise RuntimeError(f"HTTP {e.code}: {err[:2000]}") from e


def build_questions() -> list[dict]:
    gb = json.loads(
        (REPO / "assessments/phase-1/week-1/green-brown.json").read_text(encoding="utf-8")
    )
    cx = json.loads(
        (REPO / "assessments/phase-1/week-1/context.json").read_text(encoding="utf-8")
    )
    out: list[dict] = []
    for i, q in enumerate(gb["questions"]):
        choices = list(q["choices"]) + [EXTRA_GREEN[i]]
        ci = int(q["correctIndex"])
        out.append(
            {
                "group": "green-brown",
                "prompt": q["prompt"],
                "choices": choices,
                "correct_index": ci,
                "correct_comments": gb.get("feedbackCorrect", ""),
                "incorrect_comments": gb.get("feedbackIncorrect", ""),
            }
        )
    for i, q in enumerate(cx["questions"]):
        choices = list(q["choices"]) + [EXTRA_CONTEXT[i]]
        ci = int(q["correctIndex"])
        out.append(
            {
                "group": "context",
                "prompt": q["prompt"],
                "choices": choices,
                "correct_index": ci,
                "correct_comments": cx.get("feedbackCorrect", ""),
                "incorrect_comments": cx.get("feedbackIncorrect", ""),
            }
        )
    return out


def main() -> None:
    env = load_env(REPO / "available_tools/.env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    desc_html = build_quiz_description_html(base, INSTRUCTION_ASSIGNMENT_ID)

    quiz_body = {
        "quiz": {
            "title": "Prepare: 1.1 - Green, Brown, Context",
            "description": desc_html,
            "quiz_type": "assignment",
            "published": True,
            "shuffle_answers": True,
            "allowed_attempts": -1,
            "scoring_policy": "keep_highest",
            "show_correct_answers": True,
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
    print("Created quiz id:", quiz_id)

    questions = build_questions()
    points_each = TOTAL_QUIZ_POINTS / len(questions)
    for pos, q in enumerate(questions, start=1):
        answers = []
        for j, text in enumerate(q["choices"]):
            weight = 100 if j == q["correct_index"] else 0
            answers.append({"answer_text": text, "answer_weight": weight})
        qbody = {
            "question": {
                "question_name": f"{q['group']} Q{pos}",
                "question_type": "multiple_choice_question",
                "question_text": f"<p>{html.escape(q['prompt'])}</p>",
                "points_possible": points_each,
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
        print("  Added question", pos, "/", len(questions))

    # Module order: 1 subheader, 2 Instruction, 3 this quiz, 4 Lab
    assoc = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "Quiz",
                "content_id": str(quiz_id),
                "position": 3,
                "title": "Prepare: 1.1 - Green, Brown, Context",
            }
        },
    )
    print("Module item:", assoc)

    out = {
        "canvas_quiz_id": quiz_id,
        "title": "Prepare: 1.1 - Green, Brown, Context",
        "question_count": len(questions),
        "sources": [
            "assessments/phase-1/week-1/green-brown.json",
            "assessments/phase-1/week-1/context.json",
        ],
    }
    index_path = ROOT / "index.json"
    idx = json.loads(index_path.read_text(encoding="utf-8"))
    idx.setdefault("syncs", []).append(
        {
            "kind": "quiz",
            "name": out["title"],
            "canvas_quiz_id": quiz_id,
            "sources": out["sources"],
        }
    )
    index_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
