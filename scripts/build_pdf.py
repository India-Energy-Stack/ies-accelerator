#!/usr/bin/env python3
"""Walk SUMMARY.md and build a single combined Markdown ready for pandoc.

- Strips GitBook `{% hint %}` wrappers (keeps inner content).
- Substitutes emoji / math glyphs that the default LaTeX font cannot render.
- Renders ```mermaid``` fenced blocks to PNG via mermaid-cli (`mmdc`) and
  replaces the block with a markdown image reference. If `mmdc` is not on
  PATH the block is left as a code block (and a warning is printed).
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUMMARY = ROOT / "SUMMARY.md"
BUILD = ROOT / "build"
MERMAID_DIR = BUILD / "mermaid"
OUT_MD = BUILD / "ies_combined.md"

GLYPH_FALLBACKS = {
    "←": "<-",
    "→": "->",
    "↓": "v",
    "↔": "<->",
    "☐": "[ ]",
    "≤": "<=",
    "≥": ">=",
    "∈": " in ",
    "▶": ">",
    "▼": "v",
    "★": "*",
    "💡": "[tip]",
    "📋": "[checklist]",
    "⚠️": "[warn]",
    "⚠": "[warn]",
    "️": "",
    "✅": "[x]",
    "✓": "[x]",
}

ENTRY_RE = re.compile(r"^(\s*)\*\s+\[([^\]]+)\]\(([^)]+)\)")
MERMAID_RE = re.compile(r"^```mermaid\s*\n(.*?)\n```\s*$", re.MULTILINE | re.DOTALL)
# A SUMMARY entry whose title is a version label, e.g. "v1.2", "v0.6", "v0.1".
VERSION_RE = re.compile(r"^v\d+(\.\d+)*$", re.IGNORECASE)


def filter_latest_versions(
    entries: list[tuple[int, str, str]],
) -> list[tuple[int, str, str]]:
    """Keep only the latest version page per schema family.

    SUMMARY.md lists a family's versions newest-first as consecutive siblings at
    the same depth (e.g. v1.2, v1.1, v1.0). For each such run we keep the first
    (latest) entry and drop the older ones. Non-version entries are untouched.
    SUMMARY.md / GitBook itself is not modified.
    """
    result: list[tuple[int, str, str]] = []
    i, n = 0, len(entries)
    while i < n:
        depth, title, path = entries[i]
        if VERSION_RE.match(title.strip()):
            result.append(entries[i])  # latest (first listed)
            j = i + 1
            while (
                j < n
                and entries[j][0] == depth
                and VERSION_RE.match(entries[j][1].strip())
            ):
                j += 1  # skip older versions in the same run
            i = j
        else:
            result.append(entries[i])
            i += 1
    return result


def parse_summary() -> list[tuple[int, str, str]]:
    entries: list[tuple[int, str, str]] = []
    for line in SUMMARY.read_text().splitlines():
        m = ENTRY_RE.match(line)
        if not m:
            continue
        indent, title, path = m.groups()
        if not path.endswith(".md"):
            continue
        depth = len(indent) // 2
        entries.append((depth, title, path))
    return entries


def render_mermaid(source: str, mmdc: str | None) -> str:
    """Replace each ```mermaid``` block with a PNG image reference."""
    if mmdc is None:
        return source

    def replace(match: re.Match[str]) -> str:
        diagram = match.group(1)
        digest = hashlib.sha1(diagram.encode()).hexdigest()[:12]
        out_png = MERMAID_DIR / f"{digest}.png"
        if not out_png.exists():
            src = MERMAID_DIR / f"{digest}.mmd"
            src.write_text(diagram)
            cmd = [mmdc, "-i", str(src), "-o", str(out_png), "-b", "white", "-s", "2"]
            puppeteer_cfg = MERMAID_DIR / "puppeteer.json"
            if puppeteer_cfg.exists():
                cmd += ["-p", str(puppeteer_cfg)]
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as exc:
                print(f"WARN: mmdc failed for {digest}: {exc.stderr}", file=sys.stderr)
                return match.group(0)
        # Emit raw LaTeX (PDF-only path) so we can bound BOTH width and height
        # with keepaspectratio: a tall diagram is scaled down to fit the current
        # page rather than pushed to the next one (which leaves it far from the
        # text that references it), without distorting its proportions.
        return (
            "\n```{=latex}\n"
            f"\\begin{{center}}\\includegraphics[width=\\linewidth,"
            f"height=0.6\\textheight,keepaspectratio]{{{out_png}}}\\end{{center}}\n"
            "```\n"
        )

    return MERMAID_RE.sub(replace, source)


# Auto-generated field-reference tables (between these markers) are dense; render
# them a step smaller in the PDF so the wide Description column stays readable.
FIELD_TABLE_LATEX_BEGIN = "\n```{=latex}\n\\begingroup\\scriptsize\n```\n"
FIELD_TABLE_LATEX_END = "\n```{=latex}\n\\endgroup\n```\n"


def shrink_field_tables(text: str) -> str:
    text = re.sub(r"<!--\s*FIELD-TABLE:START.*?-->", lambda m: FIELD_TABLE_LATEX_BEGIN, text)
    text = re.sub(r"<!--\s*FIELD-TABLE:END\s*-->", lambda m: FIELD_TABLE_LATEX_END, text)
    return text


def strip_leading_h1(body: str) -> str:
    """Drop the body's own leading level-1 heading.

    Each SUMMARY entry already contributes a synthesized heading at the right
    depth. GitBook pages additionally open with their own `# Title`, so without
    this the PDF gets two stacked chapter headings — an empty chapter page plus
    a duplicate TOC entry (e.g. "Getting Started", "Glossary", "Home"). We keep
    the synthesized heading and remove the body's duplicate. Only strips when the
    first non-blank line is an H1, so pages that open with content are untouched.
    """
    lines = body.splitlines()
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and re.match(r"^#\s+\S", lines[i]):
        del lines[i]
        if i < len(lines) and lines[i].strip() == "":
            del lines[i]
        return "\n".join(lines)
    return body


def shift_headings(body: str, levels: int) -> str:
    """Demote a page's body headings by its SUMMARY nesting depth.

    A page nested N levels deep gets a synthesized heading at level N+1. Without
    shifting, its own `##`/`###` body headings stay at the same level as the
    parent chapter's sections and accumulate there — e.g. "Consumer Meter Digest"
    landing at 10.21 instead of nesting under "Use Cases". Demoting the body by
    `levels` makes its in-page headings nest beneath the page. Fenced code is
    skipped so `#` comments are untouched; levels cap at 6 (LaTeX's deepest unit).
    """
    if levels <= 0:
        return body
    out: list[str] = []
    in_fence = False
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            continue
        m = re.match(r"(#{1,6})(\s)", line)
        if m and not in_fence:
            new_level = min(len(m.group(1)) + levels, 6)
            line = "#" * new_level + line[len(m.group(1)):]
        out.append(line)
    return "\n".join(out)


def preprocess(text: str, mmdc: str | None) -> str:
    text = re.sub(r"\{%\s*hint\s+style=\"[^\"]*\"\s*%\}", "", text)
    text = re.sub(r"\{%\s*endhint\s*%\}", "", text)
    for ch, sub in GLYPH_FALLBACKS.items():
        text = text.replace(ch, sub)
    text = shrink_field_tables(text)
    text = render_mermaid(text, mmdc)
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--all-versions",
        action="store_true",
        help="include every schema version (default: only the latest version per family)",
    )
    args = ap.parse_args()

    BUILD.mkdir(exist_ok=True)
    MERMAID_DIR.mkdir(exist_ok=True)

    mmdc = shutil.which("mmdc")
    if mmdc is None:
        print("NOTE: mmdc (mermaid-cli) not on PATH; mermaid blocks will render as code.", file=sys.stderr)

    entries = parse_summary()
    if not args.all_versions:
        before = len(entries)
        entries = filter_latest_versions(entries)
        dropped = before - len(entries)
        if dropped:
            print(f"Including latest version only — dropped {dropped} older version page(s). Use --all-versions to include all.")
    out_lines: list[str] = []
    missing: list[str] = []
    for depth, title, path in entries:
        p = ROOT / path
        if not p.exists():
            missing.append(path)
            continue
        body = shift_headings(strip_leading_h1(preprocess(p.read_text(), mmdc)), depth)
        heading = "#" * (depth + 1) + " " + title
        # depth 0 maps to \chapter, which already starts a fresh page; an extra
        # \newpage there leaves a blank page (e.g. before "Home" after the TOC).
        # Deeper entries map to \section/\subsection, so force a page break to
        # keep each nav page on its own page.
        if depth > 0:
            out_lines.append("\\newpage")
            out_lines.append("")
        out_lines.append(heading)
        out_lines.append("")
        out_lines.append(body)
        out_lines.append("")

    OUT_MD.write_text("\n".join(out_lines))
    print(f"Combined {len(entries) - len(missing)} of {len(entries)} files into {OUT_MD}")
    if missing:
        print("Missing files:", *missing, sep="\n  ", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
