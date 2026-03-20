#!/usr/bin/env python3
"""Serve the static course site locally (index.html, content/, styles/, js/)."""

from __future__ import annotations

import argparse
import http.server
import socketserver
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a local HTTP server for the Applied AI static site.",
    )
    parser.add_argument(
        "--bind",
        default="127.0.0.1",
        metavar="ADDR",
        help="Address to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8765,
        help="Port (default: 8765)",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        default=None,
        metavar="DIR",
        help="Document root (default: repository root, i.e. parent of scripts/)",
    )
    args = parser.parse_args()

    root = (args.directory or Path(__file__).resolve().parent.parent).resolve()
    if not (root / "index.html").is_file():
        print(f"error: no index.html in {root}", file=sys.stderr)
        return 1

    docroot = str(root)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=docroot, **kw)

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer((args.bind, args.port), Handler) as httpd:
            display_host = "127.0.0.1" if args.bind in ("0.0.0.0", "::") else args.bind
            base = f"http://{display_host}:{args.port}/"
            print(f"Serving {root}")
            print(f"  {base}")
            print(f"  Example: {base}?page=content/phase-1/week-1/day-1.md")
            print("  Press Ctrl+C to stop.")
            httpd.serve_forever()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
