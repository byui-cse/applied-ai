#!/usr/bin/env python3
"""Create Canvas assignment Instruction 2.2: Project Planning (Class Work, Week 2 module)."""
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
CLASS_WORK_GROUP_ID = 2320235
DUE = datetime(2026, 4, 30, 23, 59, tzinfo=ZoneInfo("America/Boise"))
ASSIGNMENT_POINTS = 20

WHAT_TO_SUBMIT = """

## What to Submit

**In class:** Explain your **feature** to your **table group**—the problem it solves, who it is for, and what you are planning to build at a high level (aligned with your feature brief and planning work).

Your **table** must **give you feedback** on the idea (for example: strengths, risks, missing pieces, or suggestions).

**In Canvas:** Submit the **feedback your table provided** (paste quotes, bullet points, or a faithful summary). You may add a short reflection on how you will use that feedback. Your instructor is checking that you participated in the discussion and captured substantive peer input.

This assignment is worth **20 points.**
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


def main() -> None:
    env = load_env(REPO / "available_tools/.env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    md = (
        REPO / "content/phase-1/week-2/day-2.md"
    ).read_text(encoding="utf-8").rstrip() + WHAT_TO_SUBMIT
    html = build_html_from_markdown_string(
        md,
        masthead="Applied AI · Instruction 2.2",
        apply_preprocess=True,
        strip_reader_sections=True,
    )

    created = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/assignments",
        token,
        body={
            "assignment": {
                "name": "Instruction 2.2: Project Planning",
                "description": html,
                "assignment_group_id": CLASS_WORK_GROUP_ID,
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
                "title": "Instruction 2.2: Project Planning",
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
            "name": "Instruction 2.2: Project Planning",
            "source": "content/phase-1/week-2/day-2.md",
            "canvas_assignment_id": aid,
            "canvas_module_item_id": mi_id,
            "due_at": "2026-04-30T23:59:00 America/Boise",
            "points_possible": ASSIGNMENT_POINTS,
            "assignment_group": "Class Work",
            "note": "Table pitch + peer feedback submitted in Canvas (no separate wiki page)",
        }
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
