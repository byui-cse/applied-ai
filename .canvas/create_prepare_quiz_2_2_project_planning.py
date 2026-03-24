#!/usr/bin/env python3
"""Insert Day 4 subheader + quiz Prepare: 2.2 - Project Planning before Instruction 2.2 assignment."""
from __future__ import annotations

import html
import json
import ssl
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

COURSE_ID = 406352
MODULE_ID = 4543209
PREPARE_GROUP_ID = 2320233
TOTAL_POINTS = 10.0
INSTRUCTION_2_2_ASSIGNMENT_ID = 16668229

DUE = datetime(2026, 4, 30, 10, 15, tzinfo=ZoneInfo("America/Boise"))

SUBHEADER_TITLE = "Day 4 - Project Planning"
QUIZ_TITLE = "Prepare: 2.2 - Project Planning"
ASSESSMENT = REPO / "assessments/phase-1/week-2/mcp.json"


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


def build_quiz_description_html(canvas_base_url: str) -> str:
    """Link to Instruction 2.2 assignment (not a wiki page)."""
    assignment_url = f"{canvas_base_url}/courses/{COURSE_ID}/assignments/{INSTRUCTION_2_2_ASSIGNMENT_ID}"
    return f"""<div style="margin:0;padding:0;font-family:Georgia,'Times New Roman',Times,serif;font-size:17px;line-height:1.68;color:#0f0e0d;background-color:#ebe6dc;padding:clamp(12px,3vw,22px);">
<div style="max-width:52rem;margin:0 auto;">
<div style="background-color:#faf6ef;border:1px solid rgba(15,14,13,0.12);border-radius:3px;box-shadow:0 1px 0 rgba(255,255,255,0.55) inset,0 10px 28px rgba(15,12,8,0.05);padding:clamp(20px,3vw,32px);">
<ul style="margin:0;padding-left:1.35em;">
<li style="margin:0.4em 0;">Before answering, review the Day 4 definitions (MCP, PAT, project, story) in your reader or in <a href="{assignment_url}" style="color:#6b1414;text-decoration:underline;text-underline-offset:0.2em;">Instruction 2.2: Project Planning</a> (directly <strong>below</strong> this quiz in the module). This quiz checks that vocabulary.</li>
<li style="margin:0.4em 0;"><strong>Unlimited attempts.</strong> Your <strong>highest</strong> score is kept.</li>
</ul>
</div>
</div>
</div>"""


def load_questions() -> list[dict]:
    data = json.loads(ASSESSMENT.read_text(encoding="utf-8"))
    out: list[dict] = []
    for q in data["questions"]:
        if len(q["choices"]) != 4:
            raise ValueError(f"Each question must have 4 choices, got {len(q['choices'])}")
        out.append(
            {
                "prompt": q["prompt"],
                "choices": list(q["choices"]),
                "correct_index": int(q["correctIndex"]),
                "correct_comments": data.get("feedbackCorrect", ""),
                "incorrect_comments": data.get("feedbackIncorrect", ""),
            }
        )
    return out


def points_split(n: int, total: float) -> list[float]:
    base = round(total / n, 2)
    pts = [base] * n
    pts[-1] = round(pts[-1] + (total - sum(pts)), 2)
    return pts


def find_instruction_2_2_position(base: str, token: str) -> int:
    """Module item position for Instruction 2.2 assignment (content_id matches)."""
    url: str | None = (
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items?per_page=100"
    )
    target = str(INSTRUCTION_2_2_ASSIGNMENT_ID)
    while url:
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        req = urllib.request.Request(url, headers=headers)
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx) as resp:
            items = json.loads(resp.read().decode())
            link = resp.headers.get("Link", "")
        if not isinstance(items, list):
            break
        for it in items:
            if not isinstance(it, dict):
                continue
            if it.get("type") != "Assignment":
                continue
            cid = it.get("content_id")
            if cid is not None and str(cid) == target:
                return int(it["position"])
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                m = part.split(";")[0].strip()
                if m.startswith("<") and m.endswith(">"):
                    url = m[1:-1]
                break
    raise RuntimeError(
        f"Could not find module item for assignment id {INSTRUCTION_2_2_ASSIGNMENT_ID}"
    )


def main() -> None:
    env = load_env(REPO / "available_tools/.env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    insert_at = find_instruction_2_2_position(base, token)
    print("Instruction 2.2 currently at module position:", insert_at)

    desc_html = build_quiz_description_html(base)
    questions = load_questions()
    n = len(questions)
    if n != 10:
        raise RuntimeError(f"Expected 10 questions in mcp.json, got {n}")
    point_list = points_split(n, TOTAL_POINTS)

    sub = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "SubHeader",
                "title": SUBHEADER_TITLE,
                "position": insert_at,
            }
        },
    )
    sub_id = sub.get("id") if isinstance(sub, dict) else None
    print("SubHeader module item:", sub_id, "@", insert_at)

    quiz_body = {
        "quiz": {
            "title": QUIZ_TITLE,
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

    quiz_pos = insert_at + 1
    mod = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "Quiz",
                "content_id": str(quiz_id),
                "position": quiz_pos,
                "title": QUIZ_TITLE,
            }
        },
    )
    mod_item_id = mod.get("id") if isinstance(mod, dict) else None
    print("Quiz module item:", mod_item_id, "@", quiz_pos)

    idx_path = ROOT / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    syncs = idx.setdefault("syncs", [])
    syncs.append(
        {
            "kind": "module_subheader",
            "title": SUBHEADER_TITLE,
            "canvas_module_item_id": sub_id,
            "canvas_module_id": MODULE_ID,
        }
    )
    syncs.append(
        {
            "kind": "quiz",
            "name": QUIZ_TITLE,
            "canvas_quiz_id": quiz_id,
            "canvas_assignment_id": assignment_id,
            "points_total": int(TOTAL_POINTS),
            "due_at": "2026-04-30T10:15:00 America/Boise",
            "attempts": "unlimited",
            "scoring_policy": "keep_highest",
            "sources": ["assessments/phase-1/week-2/mcp.json"],
            "canvas_module_item_id": mod_item_id,
            "note": "Placed before Instruction 2.2; description links to that assignment",
        }
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
