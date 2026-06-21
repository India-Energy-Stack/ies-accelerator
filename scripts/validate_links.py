#!/usr/bin/env python3
"""Markdown link / anchor validator for the IES accelerator docs.

By default walks the entire repository root and checks every relative
markdown link (and its anchor fragment, when present) for resolvability.
Pass an explicit root directory as the first argument to scope it down.

Examples:
    python scripts/validate_links.py                     # whole repo
    python scripts/validate_links.py schemas/MeterData/v0.6   # one subtree
"""
import os
import re
import sys
import urllib.parse
from typing import Set


HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SKIP_DIRS = {".git", "venv", ".venv", "scratch", "node_modules", "build"}


def slugify(heading: str) -> str:
    """Approximate GitHub / GitBook heading-anchor slugification.

    GitBook's observed behaviour on these docs:
    - Lowercases the heading.
    - Drops inline-code backticks and most punctuation.
    - Drops em-dashes and en-dashes outright (surrounding spaces survive,
      so " — " between words becomes "--" once spaces map to dashes).
    - Maps each whitespace character to one dash (multiple spaces are
      NOT collapsed — that's what preserves the "--" separator).
    - Trims leading/trailing dashes.
    """
    text = heading.lower()
    text = re.sub(r"[`*]", "", text)  # Strip backticks and bold/italic markers; keep underscores (GitBook preserves them in slugs).
    # Drop em-dash, en-dash, and arrows — their surrounding spaces become
    # adjacent dashes once whitespace is mapped 1-for-1.
    for ch in ("—", "–", "→", "←", "↔", "⇒", "⇐"):
        text = text.replace(ch, "")
    text = re.sub(r"[.,!?;:/\\\"'()\[\]{}<>|=+&]", "", text)
    text = re.sub(r"\s", "-", text)
    return text.strip("-")


def collect_anchors(filepath: str) -> Set[str]:
    """Return the set of anchor slugs derived from markdown headings."""
    anchors: Set[str] = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return anchors
    for match in HEADING_RE.findall(content):
        anchors.add(slugify(match))
    return anchors


def check_markdown_links(root_dir: str) -> int:
    root_dir = os.path.abspath(root_dir)
    markdown_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".md"):
                markdown_files.append(os.path.join(dirpath, filename))

    anchors_cache: dict[str, Set[str]] = {}

    broken = 0
    checked = 0
    print(f"Checking markdown links under {root_dir}…")

    for filepath in sorted(markdown_files):
        rel_filepath = os.path.relpath(filepath, root_dir)
        file_dir = os.path.dirname(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        for text, url in LINK_RE.findall(content):
            # Skip external + mailto
            if url.startswith(("http://", "https://", "mailto:", "tel:")):
                continue

            # Split path and anchor
            if "#" in url:
                path_part, anchor = url.split("#", 1)
            else:
                path_part, anchor = url, ""
            path_part = path_part.split("?")[0]

            checked += 1

            # Anchor-only link (#section) — resolve against the same file
            if path_part == "":
                target_path = filepath
            else:
                if path_part.startswith("file:///"):
                    target_path = path_part.replace("file://", "")
                else:
                    decoded = urllib.parse.unquote(path_part)
                    target_path = os.path.abspath(os.path.join(file_dir, decoded))

            if not os.path.exists(target_path):
                print(f"❌ Broken link in [{rel_filepath}]: [{text}]({url})")
                print(f"   target not found: {target_path}")
                broken += 1
                continue

            # If anchor present and target is a markdown file, verify the anchor exists
            if anchor and target_path.endswith(".md"):
                if target_path not in anchors_cache:
                    anchors_cache[target_path] = collect_anchors(target_path)
                if anchor not in anchors_cache[target_path]:
                    print(f"❌ Broken anchor in [{rel_filepath}]: [{text}]({url})")
                    print(f"   #{anchor} not found in {os.path.relpath(target_path, root_dir)}")
                    broken += 1

    print(f"\nLink check summary: Checked {checked} links. Found {broken} broken.")
    return 0 if broken == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.path.join(os.path.dirname(__file__), "..")
    sys.exit(check_markdown_links(root))
