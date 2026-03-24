#!/usr/bin/env python3
"""Update Canvas rubric for Lab 2.1: Feature Agent (30 pts, 5 criteria × 3 ratings)."""
from __future__ import annotations

import json
import ssl
import urllib.request
from pathlib import Path

COURSE_ID = 406352
RUBRIC_ID = 3594882

# (max_points, criterion title, exceptional-rating text, partial detail after "Partial — ")
RUBRIC: list[tuple[float, str, str, str]] = [
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
    for i, (max_pts, title, exceptional_text, partial_detail) in enumerate(RUBRIC):
        half = max_pts / 2.0
        out[str(i)] = {
            "description": title,
            "points": float(max_pts),
            "ratings": {
                "0": {
                    "description": f"Exceptional — {exceptional_text}",
                    "points": float(max_pts),
                },
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
                "title": "Lab 2.1: Feature Agent (30 pts)",
                "free_form_criterion_comments": False,
                "criteria": build_criteria(),
            }
        },
    )
    print(f"Rubric {RUBRIC_ID} updated: 5 criteria × 6 pts, 3 ratings each (Exceptional / Partial / Missing)")


if __name__ == "__main__":
    main()
