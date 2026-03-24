#!/usr/bin/env python3
"""Add SubHeader + wiki page Instruction 2.1: Feature Planning to Brownfield - Week 2 module."""
from __future__ import annotations

import json
import ssl
import sys
import urllib.request
from pathlib import Path

CANVAS_DIR = Path(__file__).resolve().parent
REPO = CANVAS_DIR.parent
sys.path.insert(0, str(CANVAS_DIR))
from build_canvas_content import build_from_markdown  # noqa: E402

COURSE_ID = 406352
MODULE_ID = 4543209

SUBHEADER_TITLE = "Day 3 - Feature Planning"
PAGE_TITLE = "Instruction 2.1: Feature Planning"
MD_SOURCE = REPO / "content/phase-1/week-2/day-1.md"


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


def list_module_item_positions(base: str, token: str) -> list[int]:
    """Return all module item `position` values (paginated)."""
    positions: list[int] = []
    url: str | None = (
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items"
        f"?per_page=100"
    )
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
            if isinstance(it, dict) and "position" in it:
                positions.append(int(it["position"]))
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                m = part.split(";")[0].strip()
                if m.startswith("<") and m.endswith(">"):
                    url = m[1:-1]
                break
    return positions


def main() -> None:
    env = load_env(REPO / "available_tools/.env")
    base = env["CANVAS_BASE_URL"].strip().rstrip("/")
    token = env["CANVAS_ACCESS_TOKEN"].strip()

    positions = list_module_item_positions(base, token)
    next_pos = max(positions, default=0) + 1

    page_html = build_from_markdown(
        MD_SOURCE,
        masthead="Applied AI · Instruction 2.1",
        strip_reader_sections=True,
    )

    created = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/pages",
        token,
        body={
            "wiki_page": {
                "title": PAGE_TITLE,
                "body": page_html,
                "published": True,
                "editing_roles": "teachers",
            }
        },
    )
    if not isinstance(created, dict):
        raise RuntimeError("unexpected wiki_page response")
    page_slug = created.get("url") or created.get("page_id")
    if not page_slug:
        raise RuntimeError(f"no slug in page response: {created.keys()}")
    print("Wiki page:", page_slug, created.get("html_url"))

    sub = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "SubHeader",
                "title": SUBHEADER_TITLE,
                "position": next_pos,
            }
        },
    )
    sub_id = sub.get("id") if isinstance(sub, dict) else None
    print("SubHeader module item:", sub_id, "@", next_pos)

    mi = api_request(
        "POST",
        f"{base}/api/v1/courses/{COURSE_ID}/modules/{MODULE_ID}/items",
        token,
        body={
            "module_item": {
                "type": "Page",
                "page_url": str(page_slug),
                "position": next_pos + 1,
                "title": PAGE_TITLE,
            }
        },
    )
    mi_id = mi.get("id") if isinstance(mi, dict) else None
    print("Page module item:", mi_id, "@", next_pos + 1)

    idx_path = CANVAS_DIR / "index.json"
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
            "kind": "wiki_page",
            "name": PAGE_TITLE,
            "source": "content/phase-1/week-2/day-1.md",
            "canvas_page_slug": str(page_slug),
            "canvas_module_item_id": mi_id,
            "canvas_module_id": MODULE_ID,
        }
    )
    idx_path.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")
    print("Updated .canvas/index.json")


if __name__ == "__main__":
    main()
