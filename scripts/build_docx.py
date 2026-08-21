#!/usr/bin/env python3
"""Build the Word (.docx) deliverable from SUMMARY.docx.md.

Reuses the SUMMARY-walking, mermaid-rendering and heading-shifting machinery
of scripts/build_pdf.py, but reads the .docx manifest (SUMMARY.docx.md —
the technical reference without Propose a Schema, Pathways or draft/) and
hands the combined Markdown to pandoc for a .docx with a native Word table
of contents.

The TOC is a real Word TOC field. The script sets <w:updateFields> in the
document settings so Word populates it the first time the file opens (Word
asks to update fields — answer Yes). LibreOffice users: Tools > Update >
Update All.

Usage:  python3 scripts/build_docx.py [--all-versions]
        (or: bash scripts/build_docx.sh)

Output: build/IES_Technical_Reference.docx
"""

import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_pdf as bp

ROOT = bp.ROOT
OUT_MD = bp.BUILD / "ies_docx_combined.md"
OUT_DOCX = bp.BUILD / "IES_Technical_Reference.docx"


def combined_markdown(all_versions: bool) -> int:
    """Assemble the combined Markdown for the .docx scope, mirroring the
    GitBook nav via the shared grouped assembly in build_pdf."""
    bp.SUMMARY = ROOT / "SUMMARY.docx.md"

    bp.BUILD.mkdir(exist_ok=True)
    bp.MERMAID_DIR.mkdir(exist_ok=True)

    mmdc = shutil.which("mmdc")
    if mmdc is None:
        print(
            "NOTE: mmdc (mermaid-cli) not on PATH; mermaid blocks render as code.",
            file=sys.stderr,
        )

    combined = bp.grouped_entries(all_versions)

    errors = []
    for _, _, path in combined:
        try:
            bp.resolve_source_path(path)
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        print("Invalid or missing SUMMARY.docx.md entries:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    missing = bp.build_document(combined, OUT_MD, mmdc)
    if not missing:
        number_headings(OUT_MD)
    return missing


STEP_RE = re.compile(r"(\d+)\.(\d+)( — .*)$")
SINGLE_RE = re.compile(r"(\d+)\.\s+(.*)$")


def number_headings(md_path: pathlib.Path) -> None:
    """Hierarchical numbering over H1/H2/H3: chapters 'N.', pages 'N.M',
    sections 'N.M.K' — matching the GitBook nav structure.

    Headings that carry authored numbers are *renumbered into* the hierarchy
    (the authored index becomes the last component, so prose references like
    '§9.1' stay suffix-recognisable). Where a parent mixes authored and
    unnumbered children, only the authored ones are numbered — generated
    numbers would collide with them. Number prefixes never change pandoc's
    auto identifiers (they strip to the first letter), so anchors survive.
    """
    lines = md_path.read_text().split("\n")

    # Pass 1 — which parents have authored-numbered children.
    ch_i, h2_i = -1, -1
    ch_has_authored: list[bool] = []
    h2_has_authored: dict[tuple[int, int], bool] = {}
    in_code = False
    for ln in lines:
        if ln.startswith("```"):
            in_code = not in_code
        elif not in_code and ln.startswith("# "):
            ch_i += 1
            h2_i = -1
            ch_has_authored.append(False)
        elif not in_code and ln.startswith("## "):
            h2_i += 1
            h2_has_authored.setdefault((ch_i, h2_i), False)
            if re.match(r"## \d", ln):
                ch_has_authored[ch_i] = True
        elif not in_code and ln.startswith("### ") and re.match(r"### \d", ln):
            h2_has_authored[(ch_i, h2_i)] = True

    # Pass 2 — assign labels.
    out: list[str] = []
    in_code = False
    ch = 0
    ch_i, h2_i = -1, -1
    sec = subsec = 0
    sec_label: str | None = None
    for ln in lines:
        if ln.startswith("```"):
            in_code = not in_code
        elif not in_code and ln.startswith("# "):
            ch += 1
            ch_i += 1
            h2_i, sec, sec_label = -1, 0, None
            ln = f"# {ch}. {ln[2:]}"
        elif not in_code and ln.startswith("## "):
            h2_i += 1
            subsec = 0
            rest = ln[3:]
            if m := STEP_RE.match(rest):
                sec_label = f"{ch}.{m.group(2)}"
                ln = f"## {sec_label}{m.group(3)}"
            elif m := SINGLE_RE.match(rest):
                sec_label = f"{ch}.{m.group(1)}"
                ln = f"## {sec_label} {m.group(2)}"
            elif not ch_has_authored[ch_i]:
                sec += 1
                sec_label = f"{ch}.{sec}"
                ln = f"## {sec_label} {rest}"
            else:
                sec_label = None
        elif not in_code and ln.startswith("### ") and sec_label:
            rest = ln[4:]
            if m := STEP_RE.match(rest):
                ln = f"### {sec_label}.{m.group(2)}{m.group(3)}"
            elif m := SINGLE_RE.match(rest):
                ln = f"### {sec_label}.{m.group(1)} {m.group(2)}"
            elif not h2_has_authored.get((ch_i, h2_i), False):
                subsec += 1
                ln = f"### {sec_label}.{subsec} {rest}"
        out.append(ln)
    md_path.write_text("\n".join(out))


REFERENCE_DOCX = bp.BUILD / "docx_reference.docx"


def make_reference_docx() -> pathlib.Path:
    """Densified styling: 10pt body, 9pt code, tighter paragraph spacing,
    0.75in margins. Built by patching pandoc's default reference docx, so
    the whole pipeline stays reproducible with no binary checked in."""
    default = bp.BUILD / "docx_reference_default.docx"
    with default.open("wb") as fh:
        subprocess.run(
            ["pandoc", "--print-default-data-file", "reference.docx"],
            stdout=fh,
            check=True,
        )
    with zipfile.ZipFile(default) as zin, zipfile.ZipFile(
        REFERENCE_DOCX, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                text = data.decode("utf-8")
                # Theme-font indirection (minorHAnsi/majorHAnsi) breaks in
                # Google Docs, which can't resolve Word themes and
                # substitutes an unrelated face. Pin explicit fonts that
                # exist in both Word and Google Docs.
                for attr, val in (
                    ("asciiTheme", "ascii"),
                    ("hAnsiTheme", "hAnsi"),
                    ("cstheme", "cs"),
                ):
                    text = re.sub(
                        rf'w:{attr}="(?:minor|major)[A-Za-z]*"',
                        f'w:{val}="Calibri"',
                        text,
                    )
                text = re.sub(r'\s*w:eastAsiaTheme="[^"]*"', "", text)
                text = text.replace(
                    'w:ascii="Consolas" w:hAnsi="Consolas"',
                    'w:ascii="Courier New" w:hAnsi="Courier New"',
                )
                # 12pt -> 10pt document default
                text = re.sub(
                    r'(<w:rPrDefault>\s*<w:rPr>.*?)<w:sz w:val="24" />(\s*)<w:szCs w:val="24" />',
                    r'\1<w:sz w:val="20" />\2<w:szCs w:val="20" />',
                    text,
                    count=1,
                    flags=re.DOTALL,
                )
                # body paragraphs: 180 twips of space either side -> 60
                text = text.replace(
                    '<w:spacing w:before="180" w:after="180" />',
                    '<w:spacing w:before="60" w:after="60" />',
                )
                # code (inline + blocks): 11pt -> 9pt
                text = re.sub(
                    r'(w:styleId="VerbatimChar">.*?)<w:sz w:val="22" />',
                    r'\1<w:sz w:val="18" />',
                    text,
                    count=1,
                    flags=re.DOTALL,
                )
                data = text.encode("utf-8")
            elif item.filename == "word/document.xml":
                text = data.decode("utf-8")
                if "<w:pgMar" not in text:
                    text = text.replace(
                        "</w:sectPr>",
                        '<w:pgSz w:w="12240" w:h="15840" />'
                        '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" '
                        'w:left="1080" w:header="720" w:footer="720" w:gutter="0" />'
                        "</w:sectPr>",
                        1,
                    )
                data = text.encode("utf-8")
            zout.writestr(item, data)
    return REFERENCE_DOCX


def enable_update_fields_on_open(docx_path: pathlib.Path) -> None:
    """Ask Word to refresh fields (the TOC) the first time the file opens."""
    tmp = docx_path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(docx_path) as zin, zipfile.ZipFile(
        tmp, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/settings.xml":
                text = data.decode("utf-8")
                if "<w:updateFields" not in text:
                    text = re.sub(
                        r"(<w:settings\b[^>]*>)",
                        r'\1<w:updateFields w:val="true"/>',
                        text,
                        count=1,
                    )
                data = text.encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(docx_path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--all-versions",
        action="store_true",
        help="include every schema version (default: latest per family)",
    )
    args = ap.parse_args()

    if shutil.which("pandoc") is None:
        print("error: pandoc not found. Install with: brew install pandoc", file=sys.stderr)
        return 1

    if combined_markdown(args.all_versions):
        return 1

    date = subprocess.run(
        ["git", "-C", str(ROOT), "show", "-s", "--format=%cs", "HEAD"],
        capture_output=True,
        text=True,
    ).stdout.strip()

    cmd = [
        "pandoc",
        str(OUT_MD),
        "--output=" + str(OUT_DOCX),
        "--from=markdown-task_lists",
        "--toc",
        "--toc-depth=2",
        "--metadata",
        "title=India Energy Stack (IES) — Technical Documentation",
        "--metadata",
        "author=India Energy Stack",
        "--metadata",
        f"date={date}",
        "--metadata",
        "toc-title=Contents",
        "--reference-doc=" + str(make_reference_docx()),
        "--resource-path=" + str(ROOT),
    ]
    log = bp.BUILD / "pandoc-docx.log"
    with log.open("w") as fh:
        proc = subprocess.run(cmd, stderr=fh)
    if proc.returncode != 0:
        print(f"error: pandoc failed; see {log}", file=sys.stderr)
        return 1

    enable_update_fields_on_open(OUT_DOCX)

    size = OUT_DOCX.stat().st_size / (1024 * 1024)
    print(f"Built: {OUT_DOCX} ({size:.1f} MB)")
    print("Open in Word and confirm the 'update fields' prompt to populate the Contents page.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
