#!/usr/bin/env python3
"""Update Canvas rubric for Lab 1.2: Analysis Agent (30 pts, 4 criteria × 3 ratings)."""
from __future__ import annotations

import json
import ssl
import urllib.request
from pathlib import Path

COURSE_ID = 406352
RUBRIC_ID = 3594864

# (max_points, criterion description, partial-rating detail after "Partial — ")
RUBRIC: list[tuple[float, str, str]] = [
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


def build_criteria() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for i, (max_pts, description, partial_detail) in enumerate(RUBRIC):
        half = max_pts / 2.0
        out[str(i)] = {
            "description": description,
            "points": float(max_pts),
            "ratings": {
                "0": {"description": "Exceptional", "points": float(max_pts)},
                "1": {
                    "description": f"Partial — {partial_detail}",
                    "points": float(half),
                },
                "2": {"description": "Missing", "points": 0.0},
            },
        }
    return out


def main() -> None:
    repo = Path(__file__).resolve().parent.parent
    env = load_env(repo / "available_tools" / ".env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    api_request(
        "PUT",
        f"{base}/api/v1/courses/{COURSE_ID}/rubrics/{RUBRIC_ID}",
        token,
        body={
            "rubric": {
                "title": "Lab 1.2: Analysis Agent (30 pts)",
                "free_form_criterion_comments": False,
                "criteria": build_criteria(),
            }
        },
    )
    print(f"Rubric {RUBRIC_ID} updated: 4 criteria (5+10+5+10), 3 ratings each")


if __name__ == "__main__":
    main()
