#!/usr/bin/env python3
"""Create Canvas assignment Lab 1.2: Analysis Agent + rubric + module item."""
from __future__ import annotations

import json
import ssl
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CANVAS_DIR = Path(__file__).resolve().parent
REPO = CANVAS_DIR.parent
sys.path.insert(0, str(CANVAS_DIR))
from build_canvas_content import build_html_from_markdown_string  # noqa: E402

COURSE_ID = 406352
MODULE_ID = 4542815
LABS_GROUP_ID = 2320237
DUE = datetime(2026, 4, 25, 23, 59, tzinfo=ZoneInfo("America/Boise"))

WHAT_TO_SUBMIT = """

## What to Submit

- Submit your work per **What you turn in** above (including `agents/analyze-repo.md` and referenced scripts in your fork).
- The lab is worth 30 points; your instructor uses the assignment rubric in Canvas (submission sidebar and SpeedGrader) for each criterion.
"""

# Mirrors .canvas/update_lab_1_2_rubric.py (Canvas is source of truth for grading).
RUBRIC_ROWS: list[tuple[float, str, str]] = [
    (
        5.0,
        'A link to your "agents/analyze-repo.md" in your personal repository.',
        "link missing, wrong file, or not in your personal fork",
    ),
    (
        10.0,
        "The agent must have instructions about creating index files",
        "index guidance is incomplete or unclear",
    ),
    (
        5.0,
        "Screenshot proving context management needs to be 40% or under when running the agent",
        "e.g. context use above 40% (such as ~50%), or evidence is weak",
    ),
    (
        10.0,
        "Agent has instructions to create scripts to run processes outside of LLM",
        "scripts/out-of-LLM steps described but incomplete",
    ),
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


def build_rubric_criteria() -> dict[str, dict]:
    criteria: dict[str, dict] = {}
    for i, (pts, desc, partial_detail) in enumerate(RUBRIC_ROWS):
        half = float(pts) / 2.0
        criteria[str(i)] = {
            "description": desc,
            "points": float(pts),
            "ratings": {
                "0": {"description": "Exceptional", "points": float(pts)},
                "1": {
                    "description": f"Partial — {partial_detail}",
                    "points": half,
                },
                "2": {"description": "Missing", "points": 0.0},
            },
        }
    return criteria


def main() -> None:
    env = load_env(REPO / "available_tools/.env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    md = (REPO / "content/phase-1/week-1/labs/lab-2.md").read_text(encoding="utf-8") + WHAT_TO_SUBMIT
    html = build_html_from_markdown_string(
        md,
        masthead="Applied AI · Lab 1.2",
        apply_preprocess=True,
        strip_reader_sections=True,
    )

    created = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/assignments",
        token,
        body={
            "assignment": {
                "name": "Lab 1.2: Analysis Agent",
                "description": html,
                "assignment_group_id": LABS_GROUP_ID,
                "points_possible": 30,
                "due_at": DUE.isoformat(),
                "published": True,
                "submission_types": ["online_text_entry"],
                "grading_type": "points",
            }
        },
    )
    if not isinstance(created, dict):
        raise RuntimeError("unexpected assignment response")
    aid = int(created["id"])
    print("Assignment id:", aid)

    rubric_body = {
        "rubric": {
            "title": "Lab 1.2: Analysis Agent (30 pts)",
            "free_form_criterion_comments": False,
            "criteria": build_rubric_criteria(),
        },
        "rubric_association": {
            "association_id": aid,
            "association_type": "Assignment",
            "use_for_grading": True,
            "purpose": "grading",
        },
    }
    rub_out = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/rubrics",
        token,
        body=rubric_body,
    )
    rubric_id = None
    if isinstance(rub_out, dict):
        r = rub_out.get("rubric", rub_out)
        if isinstance(r, dict):
            rubric_id = r.get("id")
    print("Rubric id:", rubric_id)

    items = api_request(
        "GET",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items?per_page=100",
        token,
    )
    pos = len(items) + 1 if isinstance(items, list) else 8

    api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "Assignment",
                "content_id": str(aid),
                "position": pos,
                "title": "Lab 1.2: Analysis Agent",
            }
        },
    )
    print("Module item position:", pos)

    idx_path = CANVAS_DIR / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    idx.setdefault("syncs", []).append(
        {
            "kind": "assignment",
            "name": "Lab 1.2: Analysis Agent",
            "source": "content/phase-1/week-1/labs/lab-2.md",
            "canvas_assignment_id": aid,
            "canvas_rubric_id": rubric_id,
            "due_at": "2026-04-25T23:59:00 America/Boise",
            "rubric_note": "Grading rubric lives in Canvas (not duplicated in assignment body)",
        }
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
