#!/usr/bin/env python3
"""Lab 1.1: Setup Canvas — two 15-point criteria (fork URL + EC2 screenshot)."""
from __future__ import annotations

import json
import ssl
import urllib.request
from pathlib import Path

COURSE_ID = 406352
RUBRIC_ID = 3594660

PTS_EACH = 15.0

DESC_LINK = "Submitted a link to your forked course repo under personal GitHub account"
DESC_SHOT = (
    "Submit a screenshot of the cloned fork (not template repo) to the EC2 instance"
)


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


def _kind(description: str) -> str | None:
    d = description.lower()
    if "screenshot" in d:
        return "shot"
    if "submitted a link" in d or ("link" in d and "fork" in d and "github" in d):
        return "link"
    return None


def _criterion_block(
    points: float,
    description: str,
    existing_ratings: list[dict],
) -> dict:
    return {
        "description": description,
        "points": points,
        "ratings": {
            r["id"]: {
                "description": r["description"],
                "points": points if float(r["points"]) > 0 else 0.0,
            }
            for r in existing_ratings
        },
    }


def _new_criterion_block(points: float, description: str) -> dict:
    return {
        "description": description,
        "points": points,
        "ratings": {
            "0": {"description": "Meets requirement", "points": points},
            "1": {"description": "Does not meet", "points": 0.0},
        },
    }


def build_criteria_body(rows: list[dict]) -> dict[str, dict]:
    """Build Canvas PUT criteria from current GET rows + desired copy."""
    by_kind: dict[str, dict] = {}
    for c in rows:
        k = _kind(c.get("description") or "")
        if k:
            by_kind[k] = c

    crit_body: dict[str, dict] = {}

    if "link" in by_kind:
        c = by_kind["link"]
        crit_body[c["id"]] = _criterion_block(
            PTS_EACH, DESC_LINK, c["ratings"]
        )
    if "shot" in by_kind:
        c = by_kind["shot"]
        crit_body[c["id"]] = _criterion_block(
            PTS_EACH, DESC_SHOT, c["ratings"]
        )

    if len(crit_body) == 2:
        return crit_body

    if len(crit_body) == 1 and len(rows) == 1:
        # One row on Canvas: update it and add the missing row with key "1".
        c = rows[0]
        k = _kind(c.get("description") or "")
        if k == "link":
            crit_body = {
                c["id"]: _criterion_block(PTS_EACH, DESC_LINK, c["ratings"]),
                "1": _new_criterion_block(PTS_EACH, DESC_SHOT),
            }
        elif k == "shot":
            crit_body = {
                c["id"]: _criterion_block(PTS_EACH, DESC_SHOT, c["ratings"]),
                "1": _new_criterion_block(PTS_EACH, DESC_LINK),
            }
        else:
            # Unknown single row — replace with link row + new screenshot row.
            crit_body = {
                c["id"]: _criterion_block(PTS_EACH, DESC_LINK, c["ratings"]),
                "1": _new_criterion_block(PTS_EACH, DESC_SHOT),
            }
        return crit_body

    if len(rows) == 0:
        return {
            "0": _new_criterion_block(PTS_EACH, DESC_LINK),
            "1": _new_criterion_block(PTS_EACH, DESC_SHOT),
        }

    raise RuntimeError(
        f"unexpected rubric shape: {len(rows)} rows, could not map link/screenshot"
    )


def main() -> None:
    repo = Path(__file__).resolve().parent.parent
    env = load_env(repo / "available_tools" / ".env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    rubric = api_request(
        "GET",
        f"{base}/api/v1/courses/{COURSE_ID}/rubrics/{RUBRIC_ID}",
        token,
    )
    if not isinstance(rubric, dict) or "data" not in rubric:
        raise RuntimeError("unexpected rubric GET")

    crit_body = build_criteria_body(rubric["data"])

    api_request(
        "PUT",
        f"{base}/api/v1/courses/{COURSE_ID}/rubrics/{RUBRIC_ID}",
        token,
        body={
            "rubric": {
                "title": "Lab 1 — Setup Canvas (30 pts)",
                "criteria": crit_body,
            }
        },
    )
    print(
        f"Rubric {RUBRIC_ID}: 2 × {PTS_EACH:g} pts —\n"
        f"  1. {DESC_LINK}\n"
        f"  2. {DESC_SHOT}"
    )


if __name__ == "__main__":
    main()
