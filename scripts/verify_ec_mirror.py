#!/usr/bin/env python3
"""Verify the frozen ElectricityCredential v1.2 mirror against a pinned DEG revision.

The upstream revision is deliberately immutable.  Following ``main`` would make
the result depend on when the check ran and would create different outcomes on
otherwise identical release candidates.  Line endings are normalized so the
same content produces the same result on Windows and Linux; every other byte is
contractual.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_MIRROR = ROOT / "schemas" / "ElectricityCredential" / "v1.2"
UPSTREAM_REPOSITORY = "https://github.com/beckn/DEG"
UPSTREAM_COMMIT = "84a4de0d749ce17b58ec37d18c4a13deace9c023"
UPSTREAM_PREFIX = "specification/schema/ElectricityCredential/v1.2"
RAW_BASE = f"https://raw.githubusercontent.com/beckn/DEG/{UPSTREAM_COMMIT}/{UPSTREAM_PREFIX}"

MIRRORED_FILES = (
    "README.md",
    "attributes.yaml",
    "context.jsonld",
    "schema.json",
    "vocab.jsonld",
    "examples/example-parallel-metering.json",
    "examples/example-submetering.json",
    "examples/example.json",
)


class MirrorError(RuntimeError):
    pass


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(normalize(data)).hexdigest()


def read_tree(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        raise MirrorError(f"mirror directory does not exist: {root}")
    expected = set(MIRRORED_FILES)
    found = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }
    missing = sorted(expected - found)
    unexpected = sorted(found - expected)
    if missing or unexpected:
        raise MirrorError(
            f"mirror file set mismatch: missing={missing}, unexpected={unexpected}"
        )
    result: dict[str, bytes] = {}
    for relative in MIRRORED_FILES:
        path = root / Path(relative)
        if not path.is_file():
            raise MirrorError(f"required mirror file is missing: {path}")
        result[relative] = path.read_bytes()
    return result


def fetch_pinned_tree() -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for relative in MIRRORED_FILES:
        url = f"{RAW_BASE}/{relative}"
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "ies-accelerator-ec-mirror-verifier/0.6"},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status != 200:
                    raise MirrorError(f"upstream returned HTTP {response.status}: {url}")
                result[relative] = response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            raise MirrorError(f"could not fetch pinned upstream file {url}: {exc}") from exc
    return result


def compare_trees(local: dict[str, bytes], upstream: dict[str, bytes]) -> list[tuple[str, str, str]]:
    drift: list[tuple[str, str, str]] = []
    for relative in MIRRORED_FILES:
        local_hash = digest(local[relative])
        upstream_hash = digest(upstream[relative])
        if local_hash != upstream_hash:
            drift.append((relative, local_hash, upstream_hash))
    return drift


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-dir", type=Path, default=LOCAL_MIRROR)
    parser.add_argument(
        "--upstream-dir",
        type=Path,
        help="read the pinned upstream tree from a local checkout (offline/reviewer use)",
    )
    args = parser.parse_args()

    try:
        local = read_tree(args.local_dir.resolve())
        upstream_root = args.upstream_dir.resolve() if args.upstream_dir else None
        upstream = read_tree(upstream_root) if upstream_root else fetch_pinned_tree()
        drift = compare_trees(local, upstream)
    except MirrorError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Pinned upstream: {UPSTREAM_REPOSITORY}/commit/{UPSTREAM_COMMIT}")
    if drift:
        print(f"DRIFT: {len(drift)} mirrored file(s) differ from the pinned upstream revision:")
        for relative, local_hash, upstream_hash in drift:
            print(f"  {relative}")
            print(f"    local:    {local_hash}")
            print(f"    upstream: {upstream_hash}")
        return 1

    print(f"PASS: all {len(MIRRORED_FILES)} ElectricityCredential v1.2 files match upstream")
    return 0


if __name__ == "__main__":
    sys.exit(main())
