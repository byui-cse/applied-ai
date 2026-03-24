#!/usr/bin/env python3
"""Ensure Lab 2.1 assignment is 30 points and rubric matches update_lab_2_1_rubric.py."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ASSIGNMENT_ID = 16668221


def _rubric_module():
    p = Path(__file__).resolve().parent / "update_lab_2_1_rubric.py"
    spec = importlib.util.spec_from_file_location("lab21_rubric", p)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load update_lab_2_1_rubric.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main() -> None:
    m = _rubric_module()
    repo = Path(__file__).resolve().parent.parent
    env = m.load_env(repo / "available_tools" / ".env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    m.api_request(
        "PUT",
        f"{base}/api/v1/courses/{m.COURSE_ID}/assignments/{ASSIGNMENT_ID}",
        token,
        body={"assignment": {"points_possible": 30}},
    )
    print("Assignment points_possible -> 30")

    m.api_request(
        "PUT",
        f"{base}/api/v1/courses/{m.COURSE_ID}/rubrics/{m.RUBRIC_ID}",
        token,
        body={
            "rubric": {
                "title": "Lab 2.1: Feature Agent (30 pts)",
                "free_form_criterion_comments": False,
                "criteria": m.build_criteria(),
            }
        },
    )
    print("Rubric refreshed (5 × 6 pts, Exceptional / Partial / Missing)")


if __name__ == "__main__":
    main()
