#!/usr/bin/env python3
"""Independently verify build_pdf.py's output.

Checks, by default, that every SUMMARY.md source referenced by the build is
safe and present, and that build/ies_combined.md is *exactly* what an
independent reconstruction of SUMMARY.md would produce. Two optional checks
add PDF and staged-site verification:

    --pdf PATH          SMOKE-check a built PDF (title, page floor, nontrivial
                         extracted text). Does not verify per-chapter
                         rendering completeness.
    --public-root PATH  Verify a staged public/ mirror contains every real
                         SUMMARY source, byte-identical to the repo copy.

Independence boundary: this script re-implements its own SUMMARY.md grammar,
version-filtering policy, schema prefix split / depth-shift policy, path
safety checks, and its own ROOT/BUILD location from scratch. The oracle
content used for every comparison below (the reconstructed combined
markdown) is built exclusively from this script's independent parsing and
filtering — build_pdf.parse_summary and build_pdf.filter_latest_versions are
never used to derive expected content. Those two producer functions are
called only once each, purely as a divergence assertion: this script's
independently-parsed/filtered tuples are compared against the producer's
output, and any mismatch is a hard failure. is_schema_entry and
shift_depth_to are reimplemented independently and never imported.
build_document is not called or imported.
The only other things reused from build_pdf are content-semantics helpers
that would otherwise duplicate substantial GitBook-quirk logic verbatim
(hint-stripping / glyph substitution / mermaid rendering / H1-stripping /
heading-shifting): preprocess, strip_leading_h1, shift_headings,
APPENDIX_INTRO, APPENDIX_TITLE. ROOT and BUILD are derived independently in
this module (Path(__file__).resolve().parent.parent and ROOT/'build') and
merely asserted equal to the producer's own ROOT/BUILD.

Fails closed: any expected validation problem prints a concise message and
exits 1 (no traceback). Never writes anything to disk.
"""
from __future__ import annotations

import argparse
import difflib
import pathlib
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_pdf as producer  # noqa: E402 -- see module docstring: bounded allowlist only
from build_pdf import (  # noqa: E402 -- see module docstring: bounded allowlist only
    APPENDIX_INTRO,
    APPENDIX_TITLE,
    preprocess,
    strip_leading_h1,
    shift_headings,
)

# Independently derived, not imported from build_pdf -- see module docstring.
ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
assert producer.ROOT == ROOT, (
    f"producer ROOT diverges from independently-derived ROOT: {producer.ROOT} != {ROOT}"
)
assert producer.BUILD == BUILD, (
    f"producer BUILD diverges from independently-derived BUILD: {producer.BUILD} != {BUILD}"
)

SUMMARY_PATH = ROOT / "SUMMARY.md"
COMBINED_MD = BUILD / "ies_combined.md"
APPENDIX_DIVIDER_MD = BUILD / "appendix_divider.md"
DIVIDER_ENTRY_PATH = "build/appendix_divider.md"

# Own copy — not imported from build_pdf. See module docstring.
SCHEMA_PATH_PREFIXES = ("what-ies-provides/schemas-overview/", "schemas/")
# Own copy — not imported from build_pdf. See module docstring.
VERSION_RE = re.compile(r"^v\d+(\.\d+)*$", re.IGNORECASE)
# Strict grammar: exactly "* [title](path)" with even-space indentation and
# nothing else on the line. Any bullet-looking line that doesn't match this
# is a hard failure rather than being silently skipped.
CANONICAL_ENTRY_RE = re.compile(r"^( *)\* \[([^\]]+)\]\(([^)]+)\)$")

# SMOKE-only: extracted PDF text must be at least this fraction of the
# combined logical source's character count. Deliberately low/conservative —
# this only guards against a badly truncated or near-empty render, it does
# not claim per-chapter completeness.
PDF_TEXT_MIN_FRACTION = 0.10


class VerifyError(Exception):
    """An expected validation failure — caught in main() for a concise,
    traceback-free error message."""


def is_schema_entry(path: str) -> bool:
    return path.startswith(SCHEMA_PATH_PREFIXES)


def parse_summary_strict(text: str) -> list[tuple[int, str, str]]:
    """Own anchored SUMMARY.md grammar.

    Any line that, after stripping leading spaces/tabs, begins with '*', '-'
    or '+' must be an exact canonical '* [title](path)' entry with even-space
    indentation, or parsing fails. Only '.md'-suffixed entries are kept.
    """
    entries: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip(" \t")
        if not stripped or stripped[0] not in "*+-":
            continue
        m = CANONICAL_ENTRY_RE.match(line)
        if not m:
            raise VerifyError(
                f"SUMMARY.md:{lineno}: malformed list entry, expected "
                f"'* [title](path)' with even-space indent: {line!r}"
            )
        indent, title, path = m.groups()
        if len(indent) % 2 != 0:
            raise VerifyError(f"SUMMARY.md:{lineno}: odd-space indentation: {line!r}")
        depth = len(indent) // 2
        if not path.endswith(".md"):
            continue
        entries.append((depth, title, path))
    return entries


def filter_latest_versions_strict(
    entries: list[tuple[int, str, str]],
) -> list[tuple[int, str, str]]:
    """Own keep-first-consecutive-same-depth version policy (see build_pdf's
    filter_latest_versions for the narrative rationale; reimplemented here
    independently rather than imported)."""
    result: list[tuple[int, str, str]] = []
    i, n = 0, len(entries)
    while i < n:
        depth, title, path = entries[i]
        if VERSION_RE.match(title.strip()):
            result.append(entries[i])
            j = i + 1
            while (
                j < n
                and entries[j][0] == depth
                and VERSION_RE.match(entries[j][1].strip())
            ):
                j += 1
            i = j
        else:
            result.append(entries[i])
            i += 1
    return result


def shift_depth_to_strict(
    entries: list[tuple[int, str, str]], target_min: int
) -> list[tuple[int, str, str]]:
    """Own depth-shift policy (see build_pdf's shift_depth_to; reimplemented
    independently rather than imported)."""
    if not entries:
        return entries
    min_depth = min(depth for depth, _, _ in entries)
    delta = target_min - min_depth
    if delta == 0:
        return entries
    return [(depth + delta, title, path) for depth, title, path in entries]


def resolve_safe_path(raw: str, base: pathlib.Path, *, label: str) -> pathlib.Path:
    """Own path-safety policy, independently reimplemented (not calling
    build_pdf.resolve_source_path) so a bug in the producer's resolver can't
    also hide from this check.

    Rejects: empty, any backslash, non-canonical POSIX spelling, absolute
    POSIX paths, any '..' segment, and any Windows drive/root/absolute
    spelling (covers /, C:/, C:relative, UNC, rooted Windows paths). Requires
    the resolved path stay strictly under `base` (symlink/junction escapes
    rejected) and exist as a file.
    """
    if not raw:
        raise VerifyError(f"{label}: empty path")
    if "\\" in raw:
        raise VerifyError(f"{label}: backslash not allowed: {raw!r}")
    pp = pathlib.PurePosixPath(raw)
    if str(pp) != raw:
        raise VerifyError(f"{label}: non-canonical path spelling: {raw!r}")
    if pp.is_absolute():
        raise VerifyError(f"{label}: absolute path not allowed: {raw!r}")
    if any(part == ".." for part in pp.parts):
        raise VerifyError(f"{label}: '..' segment not allowed: {raw!r}")
    wp = pathlib.PureWindowsPath(raw)
    if wp.drive or wp.root or wp.is_absolute():
        raise VerifyError(f"{label}: windows-rooted/drive path not allowed: {raw!r}")
    resolved_base = base.resolve()
    candidate = resolved_base.joinpath(*pp.parts)
    resolved = candidate.resolve()
    try:
        resolved.relative_to(resolved_base)
    except ValueError:
        raise VerifyError(f"{label}: path escapes root {base}: {raw!r}")
    if not resolved.is_file():
        raise VerifyError(f"{label}: missing or not a file: {raw!r}")
    return resolved


def _render_block(depth: int, title: str, raw_text: str, mmdc: str | None) -> list[str]:
    """Reconstruct one combined-document block with the producer's exact
    logical framing: synthesized heading, blank, processed body, blank."""
    body = shift_headings(strip_leading_h1(preprocess(raw_text, mmdc, no_generate=True)), depth)
    heading = "#" * (depth + 1) + " " + title
    return [heading, "", body, ""]


def reconstruct_combined(
    main_entries: list[tuple[int, str, str]],
    divider_entry: tuple[int, str, str],
    schema_entries: list[tuple[int, str, str]],
    mmdc: str | None,
) -> tuple[str, int]:
    out_lines: list[str] = []
    block_count = 0

    for depth, title, path in main_entries:
        resolved = resolve_safe_path(path, ROOT, label="SUMMARY source")
        out_lines.extend(_render_block(depth, title, resolved.read_text(), mmdc))
        block_count += 1

    d_depth, d_title, _ = divider_entry
    out_lines.extend(_render_block(d_depth, d_title, APPENDIX_INTRO, mmdc))
    block_count += 1

    for depth, title, path in schema_entries:
        resolved = resolve_safe_path(path, ROOT, label="SUMMARY source")
        out_lines.extend(_render_block(depth, title, resolved.read_text(), mmdc))
        block_count += 1

    return "\n".join(out_lines), block_count


def print_bounded_diff(expected: str, actual: str, limit: int = 200) -> None:
    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected (independent reconstruction)",
        tofile="actual (build/ies_combined.md)",
        n=3,
    )
    lines = list(diff)
    for line in lines[:limit]:
        sys.stderr.write(line)
    if len(lines) > limit:
        sys.stderr.write(f"... ({len(lines) - limit} more diff line(s) omitted)\n")


def run_pdfinfo(pdf_path: pathlib.Path) -> dict[str, list[str]]:
    try:
        proc = subprocess.run(
            ["pdfinfo", "-enc", "UTF-8", str(pdf_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            check=True,
        )
    except FileNotFoundError:
        raise VerifyError("pdfinfo not found on PATH (install poppler-utils)")
    except subprocess.CalledProcessError as exc:
        raise VerifyError(f"pdfinfo failed: {exc.stderr.strip()}")
    except UnicodeError as exc:
        raise VerifyError(f"pdfinfo output was not valid UTF-8: {exc}")
    info: dict[str, list[str]] = {}
    for line in proc.stdout.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            info.setdefault(key.strip(), []).append(value.strip())
    return info


def run_pdftotext(pdf_path: pathlib.Path) -> str:
    try:
        proc = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(pdf_path), "-"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            check=True,
        )
    except FileNotFoundError:
        raise VerifyError("pdftotext not found on PATH (install poppler-utils)")
    except subprocess.CalledProcessError as exc:
        raise VerifyError(f"pdftotext failed: {exc.stderr.strip()}")
    except UnicodeError as exc:
        raise VerifyError(f"pdftotext output was not valid UTF-8: {exc}")
    return proc.stdout


def verify_pdf_smoke(pdf_path: pathlib.Path, depth0_count: int, combined_char_count: int) -> None:
    """SMOKE checks only: PDF exists, correct Title, at least one page per
    top-level chapter, and nontrivial extracted text. Does NOT verify
    per-chapter rendering completeness."""
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        raise VerifyError(f"SMOKE: PDF missing or empty: {pdf_path}")

    info = run_pdfinfo(pdf_path)

    titles = info.get("Title", [])
    if len(titles) != 1:
        raise VerifyError(f"SMOKE: expected exactly one PDF Title, got {titles!r}")
    title = titles[0]
    if title != "IES Accelerator Implementation Guide":
        raise VerifyError(f"SMOKE: PDF Title mismatch: got {title!r}")

    pages_values = info.get("Pages", [])
    if len(pages_values) != 1:
        raise VerifyError(f"SMOKE: expected exactly one PDF Pages value, got {pages_values!r}")
    try:
        pages = int(pages_values[0])
    except ValueError:
        raise VerifyError(f"SMOKE: PDF Pages not an integer: {pages_values[0]!r}")
    if pages < depth0_count:
        raise VerifyError(
            f"SMOKE: PDF Pages ({pages}) below floor of {depth0_count} top-level chapter(s)"
        )

    text = run_pdftotext(pdf_path)
    normalized = " ".join(text.split())
    threshold = max(1, int(combined_char_count * PDF_TEXT_MIN_FRACTION))
    if len(normalized) < threshold:
        raise VerifyError(
            f"SMOKE: extracted PDF text too small ({len(normalized)} chars, "
            f"need >= {threshold} = {PDF_TEXT_MIN_FRACTION:.0%} of combined source)"
        )
    print(
        f"SMOKE: PDF OK -- title matches, {pages} page(s) (>= {depth0_count} chapter floor), "
        f"{len(normalized)} extracted char(s) (>= {threshold} floor)"
    )


def verify_public_mirror(
    public_root: pathlib.Path, real_entries: list[tuple[int, str, str]]
) -> int:
    """Every real SUMMARY source (the synthetic divider is exempt) must exist
    safely beneath `public_root` and be byte-identical to the repo source."""
    count = 0
    for _, _, path in real_entries:
        repo_resolved = resolve_safe_path(path, ROOT, label="SUMMARY source")
        public_resolved = resolve_safe_path(path, public_root, label="public mirror")
        if repo_resolved.read_bytes() != public_resolved.read_bytes():
            raise VerifyError(f"public mirror differs from repo source: {path}")
        count += 1
    print(f"Public mirror OK -- {count} source file(s) present and byte-identical")
    return count


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=pathlib.Path, help="built PDF to SMOKE-check")
    ap.add_argument("--public-root", type=pathlib.Path, help="staged public/ mirror directory to check")
    args = ap.parse_args()

    try:
        if not SUMMARY_PATH.is_file():
            raise VerifyError(f"missing {SUMMARY_PATH}")
        entries = parse_summary_strict(SUMMARY_PATH.read_text())
        producer_raw = producer.parse_summary()
        if entries != producer_raw:
            raise VerifyError(
                "divergence: independent SUMMARY parse != producer.parse_summary()"
            )

        entries = filter_latest_versions_strict(entries)
        producer_filtered = producer.filter_latest_versions(producer_raw)
        if entries != producer_filtered:
            raise VerifyError(
                "divergence: independent version-filter != producer.filter_latest_versions()"
            )

        main_entries = [e for e in entries if not is_schema_entry(e[2])]
        schema_entries = shift_depth_to_strict(
            [e for e in entries if is_schema_entry(e[2])], target_min=1
        )
        divider_entry = (0, APPENDIX_TITLE, DIVIDER_ENTRY_PATH)

        # Path safety, independently repeated for every real SUMMARY source.
        # The synthetic divider isn't parsed from SUMMARY.md and is exempt
        # only from public mirroring (see verify_public_mirror).
        errors: list[str] = []
        for _, _, path in main_entries + schema_entries:
            try:
                resolve_safe_path(path, ROOT, label="SUMMARY source")
            except VerifyError as exc:
                errors.append(str(exc))
        if errors:
            print("error: invalid or missing SUMMARY source(s):", file=sys.stderr)
            for err in errors:
                print(f"  {err}", file=sys.stderr)
            return 1

        if not APPENDIX_DIVIDER_MD.is_file():
            raise VerifyError(f"missing {APPENDIX_DIVIDER_MD}")
        if APPENDIX_DIVIDER_MD.read_text() != APPENDIX_INTRO:
            raise VerifyError(
                f"{APPENDIX_DIVIDER_MD} does not match APPENDIX_INTRO"
            )

        if not COMBINED_MD.is_file():
            raise VerifyError(f"missing combined markdown: {COMBINED_MD}")

        mmdc = shutil.which("mmdc")
        expected_text, block_count = reconstruct_combined(
            main_entries, divider_entry, schema_entries, mmdc
        )
        actual_text = COMBINED_MD.read_text()

        if actual_text != expected_text:
            print(
                "error: combined markdown does not match independent reconstruction",
                file=sys.stderr,
            )
            print_bounded_diff(expected_text, actual_text)
            return 1

        print(f"OK -- {block_count} source block(s) reconstructed exactly")

        if args.public_root:
            real_entries = main_entries + schema_entries
            verify_public_mirror(args.public_root, real_entries)

        if args.pdf:
            depth0_count = sum(
                1 for depth, _, _ in main_entries + [divider_entry] + schema_entries if depth == 0
            )
            verify_pdf_smoke(args.pdf, depth0_count, len(expected_text))

    except VerifyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
