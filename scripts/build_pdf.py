#!/usr/bin/env python3
"""Walk SUMMARY.md and build a single combined Markdown ready for pandoc.

- Strips GitBook `{% hint %}` wrappers (keeps inner content).
- Substitutes emoji / math glyphs that the default LaTeX font cannot render.
- Renders ```mermaid``` fenced blocks to PNG via mermaid-cli (`mmdc`) and
  replaces the block with a markdown image reference. If `mmdc` is not on
  PATH the block is left as a code block (and a warning is printed).
"""
from __future__ import annotations

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
        return f"![]({out_png})"

    return MERMAID_RE.sub(replace, source)


def preprocess(text: str, mmdc: str | None) -> str:
    text = re.sub(r"\{%\s*hint\s+style=\"[^\"]*\"\s*%\}", "", text)
    text = re.sub(r"\{%\s*endhint\s*%\}", "", text)
    for ch, sub in GLYPH_FALLBACKS.items():
        text = text.replace(ch, sub)
    text = render_mermaid(text, mmdc)
    return text


def main() -> int:
    BUILD.mkdir(exist_ok=True)
    MERMAID_DIR.mkdir(exist_ok=True)

    mmdc = shutil.which("mmdc")
    if mmdc is None:
        print("NOTE: mmdc (mermaid-cli) not on PATH; mermaid blocks will render as code.", file=sys.stderr)

    entries = parse_summary()
    out_lines: list[str] = []
    missing: list[str] = []
    for depth, title, path in entries:
        p = ROOT / path
        if not p.exists():
            missing.append(path)
            continue
        body = preprocess(p.read_text(), mmdc)
        heading = "#" * (depth + 1) + " " + title
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
