#!/usr/bin/env python3
"""Require SUMMARY.md and _sidebar.md to publish the same ordered page set."""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_PATHWAYS = {
    "pathways/README.md",
    "pathways/authority.md",
    "pathways/utility.md",
    "pathways/tsp.md",
    "pathways/researcher.md",
    "pathways/secretariat.md",
}


def links(path: Path) -> list[str]:
    result: list[str] = []
    for raw in LINK_RE.findall(path.read_text(encoding="utf-8")):
        if raw.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        clean = urllib.parse.unquote(raw.split("#", 1)[0]).lstrip("/")
        if clean:
            result.append(clean)
    return result


def main() -> int:
    summary = links(ROOT / "SUMMARY.md")
    sidebar = links(ROOT / "_sidebar.md")
    errors: list[str] = []
    if summary != sidebar:
        summary_only = sorted(set(summary) - set(sidebar))
        sidebar_only = sorted(set(sidebar) - set(summary))
        errors.append(f"ordered navigation differs; SUMMARY-only={summary_only}, sidebar-only={sidebar_only}")
    if len(summary) != len(set(summary)):
        errors.append("SUMMARY.md contains duplicate navigation targets")
    if len(sidebar) != len(set(sidebar)):
        errors.append("_sidebar.md contains duplicate navigation targets")
    missing_pathways = sorted(REQUIRED_PATHWAYS - set(summary))
    if missing_pathways:
        errors.append(f"Pathways entries are missing: {missing_pathways}")
    if "index.md" in summary or "index.md" in sidebar:
        errors.append("retired index.md must not be part of release navigation")
    for relative in summary:
        if not (ROOT / relative).is_file():
            errors.append(f"navigation target is missing: {relative}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: canonical navigation is synchronized across {len(summary)} ordered targets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
