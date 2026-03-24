#!/usr/bin/env python3
"""Create Canvas assignment Lab 2.1: Feature Agent + rubric + module item (Week 2)."""
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
MODULE_ID = 4543209  # Brownfield - Week 2
LABS_GROUP_ID = 2320237
DUE = datetime(2026, 4, 29, 23, 59, tzinfo=ZoneInfo("America/Boise"))
ASSIGNMENT_POINTS = 30

# Mirrors .canvas/update_lab_2_1_rubric.py (Canvas is source of truth for grading).
RUBRIC_ROWS: list[tuple[float, str, str, str]] = [
    (
        6.0,
        "Design considerations",
        "Thorough work",
        "design present but thin or incomplete",
    ),
    (
        6.0,
        "Functional requirements",
        "At least 5 clear, testable requirements",
        "fewer than five, or requirements weak / not testable",
    ),
    (
        6.0,
        "Non-functional requirements",
        "At least 3 (e.g. security, performance, accessibility, operability as relevant)",
        "fewer than three, or coverage is thin",
    ),
    (
        6.0,
        "Instructions on using the analyze-repo agent",
        "Clear, complete instructions for using the agent",
        "instructions incomplete, unclear, or missing key steps",
    ),
    (
        6.0,
        "Instructions on what will be tested, how it will be tested, and what success vs. failure looks like",
        "Covers what will be tested, how, and success vs. failure clearly",
        "scope, methods, or success/failure criteria incomplete",
    ),
]

WHAT_TO_SUBMIT = """

## What to Submit

- Submit your work per **What you turn in** above (including `agents/tasks/feature-1/implementation-research.md` in your fork).
- The lab is worth 30 points; your instructor uses the assignment rubric in Canvas (submission sidebar and SpeedGrader) for each criterion.
"""


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
    for i, (pts, title, exceptional_text, partial_detail) in enumerate(RUBRIC_ROWS):
        half = float(pts) / 2.0
        criteria[str(i)] = {
            "description": title,
            "points": float(pts),
            "ratings": {
                "0": {
                    "description": f"Exceptional — {exceptional_text}",
                    "points": float(pts),
                },
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

    raw = (REPO / "content/phase-1/week-2/labs/lab-3.md").read_text(encoding="utf-8")
    if "\n## Rubric\n" in raw:
        raw = raw.split("\n## Rubric\n", 1)[0]
    md = raw.rstrip() + WHAT_TO_SUBMIT
    html = build_html_from_markdown_string(
        md,
        masthead="Applied AI · Lab 2.1",
        apply_preprocess=True,
        strip_reader_sections=True,
    )

    created = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/assignments",
        token,
        body={
            "assignment": {
                "name": "Lab 2.1: Feature Agent",
                "description": html,
                "assignment_group_id": LABS_GROUP_ID,
                "points_possible": ASSIGNMENT_POINTS,
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
            "title": f"Lab 2.1: Feature Agent ({ASSIGNMENT_POINTS} pts)",
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
    if isinstance(items, list):
        positions = [
            int(x["position"]) for x in items if isinstance(x, dict) and "position" in x
        ]
        pos = max(positions, default=0) + 1
    else:
        pos = 1

    mod_item = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "Assignment",
                "content_id": str(aid),
                "position": pos,
                "title": "Lab 2.1: Feature Agent",
            }
        },
    )
    mi_id = mod_item.get("id") if isinstance(mod_item, dict) else None
    print("Module item id:", mi_id, "position:", pos)

    idx_path = CANVAS_DIR / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    idx.setdefault("syncs", []).append(
        {
            "kind": "assignment",
            "name": "Lab 2.1: Feature Agent",
            "source": "content/phase-1/week-2/labs/lab-3.md",
            "canvas_assignment_id": aid,
            "canvas_module_item_id": mi_id,
            "canvas_rubric_id": rubric_id,
            "due_at": "2026-04-29T23:59:00 America/Boise",
            "points_possible": ASSIGNMENT_POINTS,
            "rubric_note": "Grading rubric lives in Canvas (not duplicated in assignment body)",
        }
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
