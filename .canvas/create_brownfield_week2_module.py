#!/usr/bin/env python3
"""Create published Canvas module 'Brownfield - Week 2' with unlock (lock until) date."""
from __future__ import annotations

import json
import ssl
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CANVAS_DIR = Path(__file__).resolve().parent
REPO = CANVAS_DIR.parent
COURSE_ID = 406352

MODULE_NAME = "Brownfield - Week 2"
# "Lock until" in Canvas = students cannot access until this time → API field unlock_at
UNLOCK_AT = datetime(2026, 4, 25, 22, 0, 0, tzinfo=ZoneInfo("America/Boise"))


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


def api_request(method: str, url: str, token: str, *, body: dict | None = None) -> dict | list | str:
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

    unlock_iso = UNLOCK_AT.isoformat()
    created = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules",
        token,
        body={
            "module": {
                "name": MODULE_NAME,
                "published": True,
                "unlock_at": unlock_iso,
            }
        },
    )
    if not isinstance(created, dict):
        raise RuntimeError(f"unexpected response: {created!r}")
    mid = created.get("id")
    if not mid:
        raise RuntimeError("no module id in response")
    print("Created module id:", mid)
    print("unlock_at:", created.get("unlock_at"))

    idx_path = CANVAS_DIR / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    modules = idx.setdefault("modules", [])
    modules.append(
        {
            "name": MODULE_NAME,
            "canvas_module_id": mid,
            "lock_until": "2026-04-25T22:00:00 America/Boise",
            "note": "Canvas 'Lock until' → API unlock_at; module published",
        }
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
