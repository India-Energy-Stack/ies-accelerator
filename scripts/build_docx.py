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


def _strip_frontmatter(body: str) -> str:
    """Drop a leading GitBook YAML frontmatter block (--- ... ---)."""
    return re.sub(r"\A---\n.*?\n---\n+", "", body, count=1, flags=re.DOTALL)


def combined_markdown(all_versions: bool) -> int:
    """Assemble the combined Markdown for the .docx scope."""
    bp.SUMMARY = ROOT / "SUMMARY.docx.md"

    # GitBook page frontmatter (e.g. layout hints on README.md) hides the
    # page's leading H1 from build_pdf's strip_leading_h1, which doubles the
    # chapter heading in the .docx. Strip it before the H1 pass.
    _orig_strip_h1 = bp.strip_leading_h1
    bp.strip_leading_h1 = lambda body: _orig_strip_h1(_strip_frontmatter(body))

    bp.BUILD.mkdir(exist_ok=True)
    bp.MERMAID_DIR.mkdir(exist_ok=True)

    mmdc = shutil.which("mmdc")
    if mmdc is None:
        print(
            "NOTE: mmdc (mermaid-cli) not on PATH; mermaid blocks render as code.",
            file=sys.stderr,
        )

    entries = bp.parse_summary()
    if not all_versions:
        entries = bp.filter_latest_versions(entries)

    main_entries = [
        e
        for e in entries
        if not bp.is_schema_entry(e[2]) and e[2] not in bp.BACK_MATTER_PATHS
    ]
    schema_entries = bp.shift_depth_to(
        [e for e in entries if bp.is_schema_entry(e[2])], target_min=1
    )
    back_entries = [e for e in entries if e[2] in bp.BACK_MATTER_PATHS]

    bp.APPENDIX_DIVIDER_MD.write_text(bp.APPENDIX_INTRO)
    divider = (
        0,
        bp.APPENDIX_TITLE,
        bp.APPENDIX_DIVIDER_MD.relative_to(ROOT).as_posix(),
    )

    combined = main_entries + [divider] + schema_entries + back_entries

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


def number_headings(md_path: pathlib.Path) -> None:
    """Prepend chapter/section numbers: H1 -> 'N.', H2 -> 'N.M'.

    H2s that already start with a digit keep their authored numbering
    (the templated '1. Scope and Purpose' style) — prefixing those would
    double-number them. Literal prefixes are anchor-safe: pandoc's auto
    identifiers strip everything before the first letter, so link targets
    do not change.
    """
    lines = md_path.read_text().split("\n")
    out, in_code, ch, sec = [], False, 0, 0
    for ln in lines:
        if ln.startswith("```"):
            in_code = not in_code
        elif not in_code and ln.startswith("# "):
            ch, sec = ch + 1, 0
            ln = f"# {ch}. {ln[2:]}"
        elif not in_code and ln.startswith("## ") and not re.match(r"## \d", ln):
            sec += 1
            ln = f"## {ch}.{sec} {ln[3:]}"
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
