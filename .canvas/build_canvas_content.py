#!/usr/bin/env python3
"""Build Canvas-ready HTML from markdown + template (inline styles only)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

PROSE_STYLES: dict[str, str] = {
    "h1": "font-family:Georgia,'Times New Roman',Times,serif;font-size:clamp(2rem,4vw+1rem,3rem);font-weight:700;line-height:1.02;letter-spacing:-0.035em;margin:0 0 1.5rem 0;color:#0f0e0d;",
    "h2": "font-family:Georgia,'Times New Roman',Times,serif;font-size:clamp(1.45rem,2vw+0.9rem,2.1rem);font-weight:700;line-height:1.12;letter-spacing:-0.03em;margin:2.25rem 0 0.75rem 0;padding-bottom:0.35rem;border-bottom:1px solid rgba(15,14,13,0.22);color:#0f0e0d;",
    "h3": "font-family:Georgia,'Times New Roman',Times,serif;font-size:clamp(1.05rem,0.55vw+0.95rem,1.25rem);font-weight:600;line-height:1.28;letter-spacing:-0.02em;margin:1.75rem 0 0.5rem 0;color:#0f0e0d;",
    "h4": "font-family:system-ui,-apple-system,sans-serif;font-size:0.95rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin:1.5rem 0 0.5rem 0;color:#3d3832;",
    "p": "margin:0 0 1.1em 0;",
    "blockquote": "margin:1.25rem 0;padding:0.25rem 0 0.25rem 1.25rem;border-left:3px solid rgba(15,14,13,0.22);color:#3d3832;font-style:italic;",
    "a": "color:#6b1414;text-decoration:underline;text-underline-offset:0.2em;",
    "strong": "font-weight:700;font-style:normal;color:#0f0e0d;",
    "em": "font-style:italic;",
    "ul": "margin:0 0 1.1em 0;padding-left:1.35em;",
    "ol": "margin:0 0 1.1em 0;padding-left:1.35em;",
    "li": "margin:0.35em 0;",
    "code": "font-family:ui-monospace,'Cascadia Code',monospace;font-size:0.92em;background-color:#f2ede4;padding:0.12em 0.35em;border-radius:3px;border:1px solid rgba(15,14,13,0.12);",
    "pre": "font-family:ui-monospace,'Cascadia Code',monospace;font-size:0.85rem;line-height:1.55;margin:1.25rem 0;padding:1rem 1.1rem;overflow-x:auto;background-color:#0f0e0d;color:#e8e4dc;border-radius:3px;border:1px solid rgba(15,14,13,0.22);",
    "hr": "border:0;height:1px;background:rgba(15,14,13,0.22);margin:2rem 0;",
    "table": "width:100%;border-collapse:collapse;font-size:0.95rem;margin:1.25rem 0;",
    "th": "text-align:left;padding:0.6rem 0.75rem;border-bottom:1px solid rgba(15,14,13,0.22);font-family:ui-monospace,monospace;font-size:0.75rem;font-weight:500;letter-spacing:0.08em;text-transform:uppercase;color:#3d3832;",
    "td": "text-align:left;padding:0.6rem 0.75rem;border-bottom:1px solid rgba(15,14,13,0.12);",
}


def _merge_style(tag, extra: str) -> None:
    cur = tag.get("style", "").strip()
    tag["style"] = (cur + ";" + extra).strip(";") if cur else extra


def preprocess(md: str) -> str:
    md = re.sub(
        r"<%\s*slides\s+[^%]+%>",
        "\n\n**Slides.** The full slide deck for this session is available in the **course reader**.\n\n",
        md,
    )
    md = re.sub(
        r"<%\s*quiz\s+[^%]+%>",
        "\n\n**Quiz.** Complete the embedded quiz in the **course reader** for this section.\n\n",
        md,
    )
    md = re.sub(
        r"<%\s*editor\s+[^%]+%>",
        "\n\n**Practice.** Markdown practice for this section is included in the **Prepare** quiz for Day 2.\n\n",
        md,
    )

    def links_block(m: re.Match[str]) -> str:
        inner = m.group(1).strip()
        return (
            "\n\n### Quick links\n\n"
            + inner
            + "\n\n"
        )

    md = re.sub(r"<%\s*links\s*\n(.*?)%>", links_block, md, flags=re.DOTALL)

    def checklist_block(m: re.Match[str]) -> str:
        lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
        body = "\n".join(f"- {line}" for line in lines)
        return f"\n\n### Session checklist\n\n{body}\n\n"

    md = re.sub(r"<%\s*checklist\s*\n(.*?)%>", checklist_block, md, flags=re.DOTALL)
    return md


def apply_prose_styles(fragment_html: str) -> str:
    wrapper = BeautifulSoup(f"<div>{fragment_html}</div>", "html.parser")
    root = wrapper.div
    assert root is not None

    for tag in root.find_all(True):
        name = tag.name
        if name in PROSE_STYLES and PROSE_STYLES[name]:
            _merge_style(tag, PROSE_STYLES[name])

    for bq in root.find_all("blockquote"):
        for p in bq.find_all("p"):
            _merge_style(p, "margin:0;")

    for pre in root.find_all("pre"):
        for code in pre.find_all("code"):
            code["style"] = (
                "background:none;border:0;padding:0;color:inherit;font-size:inherit;"
                "font-family:inherit;"
            )

    return "".join(str(c) for c in root.contents)


def strip_reader_sections_from_fragment(fragment_html: str) -> str:
    """Remove Quick links, Session checklist, Slides/quiz placeholders, Session 2 cross-refs, and .md links.

    Used when syncing to Canvas so the assignment body matches what students see in Canvas only,
    without editing the source markdown.
    """
    wrapper = BeautifulSoup(f"<div>{fragment_html}</div>", "html.parser")
    root = wrapper.div
    assert root is not None

    # --- h2 "Slides" + following placeholder paragraph
    for h2 in list(root.find_all("h2")):
        if h2.get_text(strip=True).lower() == "slides":
            nxt = h2.find_next_sibling()
            h2.decompose()
            if nxt and getattr(nxt, "name", None) == "p":
                txt = nxt.get_text(strip=True).lower()
                if "slides" in txt and "course reader" in txt:
                    nxt.decompose()
            break

    # --- Quiz / Slides placeholder paragraphs (embedded reader activities)
    for p in list(root.find_all("p")):
        t = p.get_text(strip=True)
        tl = t.lower()
        if "quiz." in tl and "embedded quiz" in tl:
            p.decompose()
            continue
        if "slides." in tl and "slide deck" in tl and "course reader" in tl:
            p.decompose()

    # --- h3 "Quick links" … until h3 Session checklist or top-level h2
    for h3 in list(root.find_all("h3")):
        if h3.get_text(strip=True).lower() != "quick links":
            continue
        el = h3
        while el is not None:
            nxt = el.next_sibling
            if el is not h3:
                name = getattr(el, "name", None)
                if name == "h2":
                    break
                if name == "h3" and "session checklist" in el.get_text(strip=True).lower():
                    break
            el.decompose()
            el = nxt
        break

    # --- h3 "Session checklist" … until next h2
    for h3 in list(root.find_all("h3")):
        if "session checklist" not in h3.get_text(strip=True).lower():
            continue
        el = h3
        while el is not None:
            nxt = el.next_sibling
            if el is not h3 and getattr(el, "name", None) == "h2":
                break
            el.decompose()
            el = nxt
        break

    # --- h2 "Session 2" block (follow-on / day-2.md reference)
    for h2 in list(root.find_all("h2")):
        if "session 2" not in h2.get_text(strip=True).lower():
            continue
        el = h2
        while el is not None:
            nxt = el.next_sibling
            if el is not h2 and getattr(el, "name", None) == "h2":
                break
            el.decompose()
            el = nxt
        break

    # --- h2 "Rubric" … until h3 Quick links or Session checklist (rubric lives in Canvas)
    for h2 in list(root.find_all("h2")):
        if h2.get_text(strip=True).lower() != "rubric":
            continue
        el = h2
        while el is not None:
            nxt = el.next_sibling
            if el is not h2:
                name = getattr(el, "name", None)
                if name == "h3":
                    t = el.get_text(strip=True).lower()
                    if "quick links" in t or "session checklist" in t:
                        break
                if name == "h2":
                    break
            el.decompose()
            el = nxt
        break

    # --- Any link to .md resources
    for a in list(root.find_all("a")):
        href = (a.get("href") or "").lower()
        if ".md" in href or href.endswith(".md"):
            parent = a.parent
            a.decompose()
            if parent and parent.name == "p" and not parent.get_text(strip=True):
                parent.decompose()

    return "".join(str(c) for c in root.contents)


def build_from_markdown(
    md_path: Path,
    masthead: str = "Applied AI · Course reader",
    *,
    strip_reader_sections: bool = False,
) -> str:
    raw = md_path.read_text(encoding="utf-8")
    md = preprocess(raw)
    fragment = markdown.markdown(md, extensions=["markdown.extensions.tables", "markdown.extensions.fenced_code"])
    styled = apply_prose_styles(fragment)
    if strip_reader_sections:
        styled = strip_reader_sections_from_fragment(styled)

    template = (ROOT / "template.html").read_text(encoding="utf-8")
    # Strip HTML comment header for Canvas (optional: keep — Canvas often allows comments)
    if "-->" in template:
        template = template.split("-->", 1)[-1].strip()

    html = template.replace("{{CONTENT}}", styled).replace("{{MASTHEAD_LABEL}}", masthead)
    return html


def build_html_from_markdown_string(
    md: str,
    masthead: str = "Applied AI · Course reader",
    *,
    strip_reader_sections: bool = False,
    apply_preprocess: bool = False,
) -> str:
    """Like build_from_markdown but from raw markdown text (no file)."""
    body = preprocess(md) if apply_preprocess else md
    fragment = markdown.markdown(
        body,
        extensions=["markdown.extensions.tables", "markdown.extensions.fenced_code"],
    )
    styled = apply_prose_styles(fragment)
    if strip_reader_sections:
        styled = strip_reader_sections_from_fragment(styled)

    template = (ROOT / "template.html").read_text(encoding="utf-8")
    if "-->" in template:
        template = template.split("-->", 1)[-1].strip()

    return template.replace("{{CONTENT}}", styled).replace("{{MASTHEAD_LABEL}}", masthead)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: build_canvas_content.py <markdown.md> [--stdout] [--masthead LABEL] [--strip-reader]",
            file=sys.stderr,
        )
        sys.exit(1)
    md_path = Path(sys.argv[1])
    masthead = "Applied AI · Course reader"
    if "--masthead" in sys.argv:
        i = sys.argv.index("--masthead")
        if i + 1 < len(sys.argv):
            masthead = sys.argv[i + 1]
    strip = "--strip-reader" in sys.argv
    out = build_from_markdown(md_path, masthead=masthead, strip_reader_sections=strip)
    if "--stdout" in sys.argv:
        print(out)
        return
    print(len(out), "characters — use --stdout to emit full HTML")


if __name__ == "__main__":
    main()
