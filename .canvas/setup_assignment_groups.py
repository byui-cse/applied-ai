#!/usr/bin/env python3
"""Create weighted Canvas assignment groups and place known assignments.

Prepare 20%, Class Work 20%, Labs 60%. Enables course.apply_assignment_group_weights.
"""
from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
COURSE_ID = 406352

# Known assignment IDs from .canvas/index.json
MOVE = {
    "Prepare": [16666679],
    "Class Work": [16666079],
    "Labs": [16666081],
}

GROUPS = [
    ("Prepare", 20.0),
    ("Class Work", 20.0),
    ("Labs", 60.0),
]

CORE = {name for name, _ in GROUPS}


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


def list_assignment_groups(base: str, token: str) -> list[dict]:
    url = f"{base}/api/v1/courses/{COURSE_ID}/assignment_groups?per_page=100&include[]=assignments"
    out = api_request("GET", url, token)
    if not isinstance(out, list):
        raise RuntimeError("Unexpected assignment_groups response")
    return out


def main() -> None:
    env = load_env(REPO / "available_tools/.env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()
    ag_url = f"{base}/api/v1/courses/{COURSE_ID}/assignment_groups"

    api_request(
        "PUT",
        f"{base}/api/v1/courses/{COURSE_ID}",
        token,
        body={"course": {"apply_assignment_group_weights": True}},
    )

    existing = list_assignment_groups(base, token)
    by_name = {g["name"]: g for g in existing}

    # Canvas accepts flat JSON for assignment group create/update (not nested
    # under assignment_group), otherwise name/weight are ignored.
    group_ids: dict[str, int] = {}
    for pos, (name, weight) in enumerate(GROUPS, start=1):
        if name in by_name:
            gid = by_name[name]["id"]
            api_request(
                "PUT",
                f"{ag_url}/{gid}",
                token,
                body={
                    "name": name,
                    "group_weight": weight,
                    "position": pos,
                },
            )
        else:
            created = api_request(
                "POST",
                ag_url,
                token,
                body={
                    "name": name,
                    "group_weight": weight,
                    "position": pos,
                },
            )
            if not isinstance(created, dict):
                raise RuntimeError("Unexpected create response")
            gid = int(created["id"])
        group_ids[name] = gid

    for gname, aids in MOVE.items():
        gid = group_ids[gname]
        for aid in aids:
            api_request(
                "PUT",
                f"{base}/api/v1/courses/{COURSE_ID}/assignments/{aid}",
                token,
                body={"assignment": {"assignment_group_id": gid}},
            )

    # Drop empty legacy groups; warn if a non-core group still has assignments
    final = list_assignment_groups(base, token)
    for g in final:
        if g["name"] in CORE:
            continue
        assigns = g.get("assignments") or []
        n = len(assigns) if isinstance(assigns, list) else 0
        gid = g["id"]
        if n == 0:
            try:
                api_request("DELETE", f"{ag_url}/{gid}", token)
            except urllib.error.HTTPError as e:
                err = e.read().decode()[:500]
                print(f"Could not delete empty group {g['name']!r}: HTTP {e.code} {err}")
        else:
            titles = [a.get("name", "?") for a in assigns[:5]]
            print(
                f"Note: group {g['name']!r} still has {n} assignment(s): {titles!r}. "
                "Move or remove them in Canvas, then re-run to delete the group."
            )

    print("Configured groups:", json.dumps(group_ids, indent=2))


if __name__ == "__main__":
    main()
