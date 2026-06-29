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


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SKIP_DIRS = {".git", "venv", ".venv", "scratch", "node_modules", "build"}


def slugify(heading: str) -> str:
    """Slugify a markdown heading to match GitBook's observed behaviour.

    Verified against IDs embedded in the live deployment
    (india-energy-stack.gitbook.io/docs):

    1. Lowercase the text.
    2. Drop apostrophes, backticks, and asterisks outright — they
       evaporate with no separator (so "What's" → "whats", not "what-s").
    3. Periods, underscores, and hyphens are KEPT LITERALLY. So
       "did.json" stays "did.json" and "on_confirm" stays "on_confirm".
       Note that this means slugs are NOT always lowercase a-z + dash —
       periods can appear ("id-1.-sign-up-at-dedi.global").
    4. Every other character (parens, em-dash, comma, colon, slash,
       ?, +, &, whitespace, etc.) becomes a dash separator.
    5. Collapse runs of dashes to a single dash, then trim.
    6. If the result starts with a digit, GitBook prepends "id-" so
       the HTML id attribute starts with a letter. "### 5. Smoke test"
       → "id-5.-smoke-test".
    """
    text = heading.lower()
    # Apostrophes and inline-formatting markers vanish (no separator)
    text = re.sub(r"[`*'’‘\"“”]", "", text)
    # Keep word chars, hyphens, AND periods literally;
    # every other char becomes a dash separator
    text = re.sub(r"[^a-z0-9._-]+", "-", text)
    # Collapse runs of dashes and trim
    text = re.sub(r"-+", "-", text).strip("-")
    # Headings starting with a digit get an "id-" prefix
    # (HTML id attributes can't start with a digit in legacy parsers)
    if text and text[0].isdigit():
        text = "id-" + text
    return text


def collect_anchors(filepath: str) -> Set[str]:
    """Return the set of anchor slugs from real markdown headings.

    Skips lines starting with `#` that appear inside fenced code
    blocks — those are code comments, not headings, and the markdown
    renderer (and GitBook) does not generate anchors for them.
    """
    anchors: Set[str] = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return anchors
    in_fence = False
    for line in content.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            anchors.add(slugify(m.group(1)))
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
