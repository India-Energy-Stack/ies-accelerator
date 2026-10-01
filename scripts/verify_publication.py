#!/usr/bin/env python3
"""Verify a staged GitHub Pages tree before publication."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QAQC_HEADING_RE = re.compile(r"^#{1,6}\s+.*(?:qaqc|quality assurance / quality control)", re.I | re.M)


class PublicationError(RuntimeError):
    pass


def staged_paths(public_root: Path) -> list[str]:
    return sorted(path.relative_to(public_root).as_posix() for path in public_root.rglob("*") if path.is_file())


def assert_forbidden_absent(public_root: Path, paths: list[str]) -> None:
    literal_forbidden = [
        relative
        for relative in ("qaqc", "index.md")
        if os.path.lexists(public_root / relative)
    ]
    if literal_forbidden:
        raise PublicationError(
            f"forbidden public path exists (including empty directories/symlinks): {literal_forbidden}"
        )
    forbidden = [path for path in paths if path == "index.md" or path.startswith("qaqc/")]
    if forbidden:
        raise PublicationError(f"forbidden QA/release-index paths were staged: {forbidden[:20]}")


def tracked_schema_paths() -> list[str]:
    completed = subprocess.run(
        ("git", "ls-files", "schemas/"),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [line for line in completed.stdout.splitlines() if line]


def verify(public_root: Path, combined_markdown: Path, manifest: Path) -> None:
    if not public_root.is_dir():
        raise PublicationError(f"staged public directory does not exist: {public_root}")
    paths = staged_paths(public_root)
    assert_forbidden_absent(public_root, paths)

    required = tracked_schema_paths() + ["SUMMARY.md", "_sidebar.md", "ies-report.pdf"]
    missing = [relative for relative in required if not (public_root / relative).is_file()]
    if missing:
        raise PublicationError(f"required public artifacts are missing: {missing[:20]}")
    if (public_root / "ies-report.pdf").stat().st_size == 0:
        raise PublicationError("ies-report.pdf is empty")

    if not combined_markdown.is_file():
        raise PublicationError(f"combined PDF source does not exist: {combined_markdown}")
    combined = combined_markdown.read_text(encoding="utf-8")
    match = QAQC_HEADING_RE.search(combined)
    if match:
        raise PublicationError(f"QAQC heading leaked into PDF source: {match.group(0)!r}")

    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("\n".join(paths) + "\n", encoding="utf-8")
    manifest_text = manifest.read_text(encoding="utf-8")
    if re.search(r"(?m)^(?:qaqc/|index\.md$)", manifest_text):
        raise PublicationError("QAQC or retired index path leaked into the public manifest")


def self_test() -> int:
    fixtures = 0

    def expect_rejected(label: str, setup) -> bool:
        nonlocal fixtures
        fixtures += 1
        with tempfile.TemporaryDirectory(prefix="ies-publication-negative-") as temp:
            root = Path(temp)
            setup(root)
            try:
                assert_forbidden_absent(root, staged_paths(root))
            except PublicationError as exc:
                if "forbidden" in str(exc).lower():
                    print(f"PASS: {label} fixture was rejected")
                    return True
                print(f"FAIL: {label} failed for an unexpected reason: {exc}", file=sys.stderr)
                return False
        print(f"FAIL: {label} fixture was not rejected", file=sys.stderr)
        return False

    def file_fixture(root: Path) -> None:
        staged = root / "qaqc" / "record.md"
        staged.parent.mkdir(parents=True)
        staged.write_text("# QAQC fixture\n", encoding="utf-8")

    def empty_directory_fixture(root: Path) -> None:
        (root / "qaqc").mkdir()

    def symlink_fixture(root: Path) -> None:
        target = root / "private-qaqc-target"
        target.mkdir()
        (root / "qaqc").symlink_to(target, target_is_directory=True)

    results = [
        expect_rejected("staged public/qaqc", file_fixture),
        expect_rejected("empty public/qaqc directory", empty_directory_fixture),
    ]
    try:
        results.append(expect_rejected("symlinked public/qaqc directory", symlink_fixture))
    except OSError as exc:
        if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
            print("SKIP: symlink fixture requires Windows symbolic-link privilege; Linux CI enforces it")
        else:
            print(f"FAIL: could not create symlink fixture: {exc}", file=sys.stderr)
            return 1

    if all(results):
        print("PASS: all supported publication exclusion fixtures were rejected")
        return 0
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-root", type=Path, default=ROOT / "public")
    parser.add_argument("--combined-md", type=Path, default=ROOT / "build" / "ies_combined.md")
    parser.add_argument("--manifest", type=Path, default=ROOT / "build" / "public-manifest.txt")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    try:
        verify(args.public_root.resolve(), args.combined_md.resolve(), args.manifest.resolve())
    except (PublicationError, OSError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: staged publication is safe ({len(staged_paths(args.public_root.resolve()))} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
