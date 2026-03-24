"""
Canvas LMS MCP server — stdio transport.

Authentication: set these in `.env` beside this file (loaded automatically), or
export them in the shell — no need to duplicate them in MCP client `env` config.

  CANVAS_BASE_URL       e.g. https://your-school.instructure.com (no trailing slash)
  CANVAS_ACCESS_TOKEN   OAuth2 access token (see Canvas developer docs)

Canvas REST API: https://developerdocs.instructure.com/services/canvas
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(Path(__file__).resolve().parent / ".env")

mcp = FastMCP("canvas-lms")

ActivityKind = Literal["assignment", "quiz", "page"]
ModuleItemKind = Literal["Assignment", "Quiz", "Page"]


def _base_url() -> str:
    u = os.environ.get("CANVAS_BASE_URL", "").strip().rstrip("/")
    if not u:
        raise ValueError(
            "CANVAS_BASE_URL is not set (e.g. https://canvas.instructure.com)"
        )
    return u


def _token() -> str:
    t = os.environ.get("CANVAS_ACCESS_TOKEN", "").strip()
    if not t:
        raise ValueError("CANVAS_ACCESS_TOKEN is not set")
    return t


def _strip_none(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _strip_none(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [_strip_none(x) for x in obj if x is not None]
    return obj


def _fmt_response(r: httpx.Response) -> str:
    try:
        data = r.json()
    except Exception:
        return f"HTTP {r.status_code}\n{r.text[:8000]}"
    text = json.dumps(data, indent=2)
    if len(text) > 100_000:
        return text[:100_000] + "\n…(truncated)"
    return text


async def _request(
    method: str,
    path: str,
    *,
    json_body: dict[str, Any] | None = None,
    params: list[tuple[str, str]] | None = None,
) -> str:
    url = f"{_base_url()}/api/v1{path}"
    headers: dict[str, str] = {
        "Authorization": f"Bearer {_token()}",
        "Accept": "application/json",
    }
    if json_body is not None:
        headers["Content-Type"] = "application/json"
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.request(method, url, headers=headers, json=json_body, params=params)
    if r.is_error:
        return f"HTTP {r.status_code} {r.reason_phrase}\n{_fmt_response(r)}"
    if r.status_code == 204:
        return "(success, no content)"
    return _fmt_response(r)


@mcp.tool()
async def canvas_create_activity(
    course_id: int,
    activity_type: ActivityKind,
    title: str,
    description: str | None = None,
    due_at: str | None = None,
    unlock_at: str | None = None,
    lock_at: str | None = None,
    published: bool | None = None,
    points_possible: float | None = None,
    submission_types: list[str] | None = None,
    quiz_type: str | None = None,
    front_page: bool | None = None,
    publish_at: str | None = None,
) -> str:
    """Create a new assignment, classic quiz, or course page (wiki page).

    Args:
        course_id: Canvas course ID.
        activity_type: One of assignment, quiz, page.
        title: Assignment name, quiz title, or page title.
        description: HTML body. For assignments/quizzes this is the description; for pages it is page body.
        due_at: ISO 8601 datetime (assignments and quizzes).
        unlock_at: ISO 8601 datetime (assignments and quizzes).
        lock_at: ISO 8601 datetime (assignments and quizzes).
        published: Whether the activity is visible (draft state must be enabled for assignments).
        points_possible: Assignment or graded quiz points.
        submission_types: Assignment submission types, e.g. ['online_text_entry'] or ['online_upload'].
        quiz_type: quiz type: practice_quiz, assignment, graded_survey, survey (default assignment).
        front_page: If true, set this page as the course front page (pages only).
        publish_at: Schedule page publish time (pages only; requires account feature).
    """
    try:
        if activity_type == "assignment":
            assignment: dict[str, Any] = {
                "name": title,
                "description": description,
                "due_at": due_at,
                "unlock_at": unlock_at,
                "lock_at": lock_at,
                "published": published,
                "points_possible": points_possible,
                "submission_types": submission_types
                or ["online_text_entry"],
            }
            body = {"assignment": _strip_none(assignment)}
            return await _request(
                "POST", f"/courses/{course_id}/assignments", json_body=body
            )

        if activity_type == "quiz":
            quiz: dict[str, Any] = {
                "title": title,
                "description": description,
                "due_at": due_at,
                "unlock_at": unlock_at,
                "lock_at": lock_at,
                "published": published,
                "points_possible": points_possible,
                "quiz_type": quiz_type or "assignment",
            }
            body = {"quiz": _strip_none(quiz)}
            return await _request("POST", f"/courses/{course_id}/quizzes", json_body=body)

        wiki_page: dict[str, Any] = {
            "title": title,
            "body": description or "",
            "published": published if published is not None else True,
            "front_page": front_page,
            "publish_at": publish_at,
        }
        body = {"wiki_page": _strip_none(wiki_page)}
        return await _request("POST", f"/courses/{course_id}/pages", json_body=body)
    except ValueError as e:
        return f"Configuration error: {e}"


@mcp.tool()
async def canvas_update_activity(
    course_id: int,
    activity_type: ActivityKind,
    activity_identifier: str,
    name: str | None = None,
    title: str | None = None,
    description: str | None = None,
    body_html: str | None = None,
    due_at: str | None = None,
    unlock_at: str | None = None,
    lock_at: str | None = None,
    published: bool | None = None,
    points_possible: float | None = None,
    publish_at: str | None = None,
    front_page: bool | None = None,
    notify_of_update: bool | None = None,
) -> str:
    """Update an assignment, quiz, or page (metadata, dates, HTML, publish state).

    Args:
        course_id: Canvas course ID.
        activity_type: assignment, quiz, or page.
        activity_identifier: Numeric id as string for assignment/quiz (e.g. '42').
            For pages, use the page URL slug (e.g. 'week-1-overview') or 'page_id:123' for an explicit id.
        name: New assignment name (assignments).
        title: New quiz or page title.
        description: HTML description (assignments and quizzes).
        body_html: Page body HTML (pages). Alias for wiki body.
        due_at, unlock_at, lock_at: ISO 8601 datetimes.
        published: Publish/draft visibility.
        points_possible: Points for assignment or quiz.
        publish_at: Scheduled publish (pages).
        front_page: Set as wiki front page (pages).
        notify_of_update: Notify students on quiz update (quizzes).
    """
    try:
        if activity_type == "assignment":
            aid = activity_identifier.strip()
            assignment = _strip_none(
                {
                    "name": name,
                    "description": description,
                    "due_at": due_at,
                    "unlock_at": unlock_at,
                    "lock_at": lock_at,
                    "published": published,
                    "points_possible": points_possible,
                }
            )
            if not assignment:
                return "No fields to update; provide at least one optional parameter."
            return await _request(
                "PUT",
                f"/courses/{course_id}/assignments/{aid}",
                json_body={"assignment": assignment},
            )

        if activity_type == "quiz":
            qid = activity_identifier.strip()
            quiz = _strip_none(
                {
                    "title": title,
                    "description": description,
                    "due_at": due_at,
                    "unlock_at": unlock_at,
                    "lock_at": lock_at,
                    "published": published,
                    "points_possible": points_possible,
                    "notify_of_update": notify_of_update,
                }
            )
            if not quiz:
                return "No fields to update; provide at least one optional parameter."
            return await _request(
                "PUT",
                f"/courses/{course_id}/quizzes/{qid}",
                json_body={"quiz": quiz},
            )

        slug = activity_identifier.strip()
        wiki: dict[str, Any] = {}
        if title is not None:
            wiki["title"] = title
        if name is not None and "title" not in wiki:
            wiki["title"] = name
        if body_html is not None:
            wiki["body"] = body_html
        elif description is not None:
            wiki["body"] = description
        wiki.update(
            _strip_none(
                {
                    "published": published,
                    "publish_at": publish_at,
                    "front_page": front_page,
                }
            )
        )
        wiki = _strip_none(wiki)
        if not wiki:
            return "No fields to update; provide title, body, or date/publish fields."
        return await _request(
            "PUT",
            f"/courses/{course_id}/pages/{slug}",
            json_body={"wiki_page": wiki},
        )
    except ValueError as e:
        return f"Configuration error: {e}"


@mcp.tool()
async def canvas_delete_activity(
    course_id: int,
    activity_type: ActivityKind,
    activity_identifier: str,
) -> str:
    """Delete an assignment, classic quiz, or wiki page.

    Args:
        course_id: Canvas course ID.
        activity_type: assignment, quiz, or page.
        activity_identifier: Assignment or quiz id as a string (e.g. '42'). For pages,
            use the wiki URL slug or 'page_id:123' for an explicit page id.
    """
    try:
        ident = activity_identifier.strip()
        if activity_type == "assignment":
            return await _request("DELETE", f"/courses/{course_id}/assignments/{ident}")
        if activity_type == "quiz":
            return await _request("DELETE", f"/courses/{course_id}/quizzes/{ident}")
        return await _request("DELETE", f"/courses/{course_id}/pages/{ident}")
    except ValueError as e:
        return f"Configuration error: {e}"


@mcp.tool()
async def canvas_delete_module(course_id: int, module_id: int) -> str:
    """Delete a module from a course (module items are removed with the module)."""
    try:
        return await _request("DELETE", f"/courses/{course_id}/modules/{module_id}")
    except ValueError as e:
        return f"Configuration error: {e}"


@mcp.tool()
async def canvas_list_modules(
    course_id: int,
    include_items: bool = True,
    search_term: str | None = None,
) -> str:
    """List all modules in a course, optionally including module items.

    Args:
        course_id: Canvas course ID.
        include_items: When true, requests inline module items (Canvas may omit if too large).
        search_term: Filter modules (and items) by partial name.
    """
    try:
        params: list[tuple[str, str]] = []
        if include_items:
            params.append(("include[]", "items"))
        if search_term:
            params.append(("search_term", search_term))
        return await _request(
            "GET", f"/courses/{course_id}/modules", params=params or None
        )
    except ValueError as e:
        return f"Configuration error: {e}"


@mcp.tool()
async def canvas_create_module(
    course_id: int,
    name: str,
    position: int | None = None,
    unlock_at: str | None = None,
    require_sequential_progress: bool | None = None,
    prerequisite_module_ids: list[int] | None = None,
    publish_final_grade: bool | None = None,
) -> str:
    """Create a new module in a course.

    Args:
        course_id: Canvas course ID.
        name: Module name.
        position: 1-based order in the module list.
        unlock_at: ISO 8601 when the module unlocks.
        require_sequential_progress: Students must complete items in order.
        prerequisite_module_ids: Modules that must be completed first (must have lower position).
        publish_final_grade: Publish final grade when module completes.
    """
    try:
        mod: dict[str, Any] = {
            "name": name,
            "position": position,
            "unlock_at": unlock_at,
            "require_sequential_progress": require_sequential_progress,
            "publish_final_grade": publish_final_grade,
        }
        if prerequisite_module_ids:
            mod["prerequisite_module_ids"] = [str(i) for i in prerequisite_module_ids]
        body = {"module": _strip_none(mod)}
        return await _request("POST", f"/courses/{course_id}/modules", json_body=body)
    except ValueError as e:
        return f"Configuration error: {e}"


@mcp.tool()
async def canvas_update_module(
    course_id: int,
    module_id: int,
    name: str | None = None,
    position: int | None = None,
    unlock_at: str | None = None,
    require_sequential_progress: bool | None = None,
    prerequisite_module_ids: list[int] | None = None,
    publish_final_grade: bool | None = None,
    published: bool | None = None,
) -> str:
    """Update module metadata, dates, order, prerequisites, or publish state."""
    try:
        mod = _strip_none(
            {
                "name": name,
                "position": position,
                "unlock_at": unlock_at,
                "require_sequential_progress": require_sequential_progress,
                "publish_final_grade": publish_final_grade,
                "published": published,
            }
        )
        if prerequisite_module_ids is not None:
            mod["prerequisite_module_ids"] = [str(i) for i in prerequisite_module_ids]
        if not mod:
            return "No fields to update; provide at least one optional parameter."
        return await _request(
            "PUT",
            f"/courses/{course_id}/modules/{module_id}",
            json_body={"module": mod},
        )
    except ValueError as e:
        return f"Configuration error: {e}"


@mcp.tool()
async def canvas_add_module_item(
    course_id: int,
    module_id: int,
    item_type: ModuleItemKind,
    content_id: int | None = None,
    page_url: str | None = None,
    title: str | None = None,
    position: int | None = None,
    indent: int | None = None,
) -> str:
    """Add an assignment, quiz, or wiki page to a module.

    Args:
        course_id: Canvas course ID.
        module_id: Module ID.
        item_type: Assignment, Quiz, or Page (wiki page).
        content_id: ID of the assignment or quiz (required for Assignment and Quiz).
        page_url: Wiki page URL slug (required for Page type — e.g. 'intro-week-1').
        title: Optional display title override.
        position: 1-based position within the module.
        indent: Indentation level (0-based).
    """
    try:
        mi: dict[str, Any] = {
            "type": item_type,
            "title": title,
            "position": position,
            "indent": indent,
        }
        if item_type == "Page":
            if not page_url:
                return "page_url is required when item_type is Page."
            mi["page_url"] = page_url
        else:
            if content_id is None:
                return f"content_id is required for item_type {item_type}."
            mi["content_id"] = str(content_id)
        body = {"module_item": _strip_none(mi)}
        return await _request(
            "POST",
            f"/courses/{course_id}/modules/{module_id}/items",
            json_body=body,
        )
    except ValueError as e:
        return f"Configuration error: {e}"


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
