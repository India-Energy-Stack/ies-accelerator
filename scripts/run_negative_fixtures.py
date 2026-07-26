#!/usr/bin/env python3
"""Prove release gates reject their committed negative fixtures."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EC_MIRROR = ROOT / "schemas" / "ElectricityCredential" / "v1.2"


def run_expected(command: tuple[str, ...], expected_code: int, expected_text: str) -> bool:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    output = completed.stdout + completed.stderr
    if completed.returncode != expected_code or expected_text not in output:
        print(f"FAIL: {' '.join(command)}", file=sys.stderr)
        print(f"expected code {expected_code} and text {expected_text!r}; got {completed.returncode}", file=sys.stderr)
        print(output, file=sys.stderr)
        return False
    print(f"PASS: fixture produced code {expected_code} and diagnostic {expected_text!r}")
    return True


def run_mirror_drift_fixture(python: str, fixture_path: Path) -> bool:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    relative = fixture.get("relativePath")
    appended = fixture.get("append")
    if not isinstance(relative, str) or not isinstance(appended, str) or not appended:
        print(f"FAIL: invalid mirror drift fixture: {fixture_path}", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory(prefix="ies-ec-mirror-negative-") as temp:
        drifted = Path(temp) / "v1.2"
        shutil.copytree(EC_MIRROR, drifted)
        target = drifted / Path(relative)
        if not target.is_file():
            print(f"FAIL: mirror fixture target is missing: {relative}", file=sys.stderr)
            return False
        target.write_bytes(target.read_bytes() + appended.encode("utf-8"))
        return run_expected(
            (
                python,
                "-X",
                "utf8",
                "-B",
                str(ROOT / "scripts" / "verify_ec_mirror.py"),
                "--local-dir",
                str(drifted),
                "--upstream-dir",
                str(EC_MIRROR),
            ),
            1,
            f"DRIFT: 1 mirrored file(s)",
        )


def main() -> int:
    python = sys.executable
    fixtures = ROOT / "scripts" / "fixtures"
    checks = (
        (
            (
                python,
                "-X",
                "utf8",
                "-B",
                str(ROOT / "scripts" / "verify_v05_v06_equivalence.py"),
                "--fixture",
                str(fixtures / "migration_missing_disposition.json"),
            ),
            1,
            "missing intentional disposition",
        ),
        (
            (
                python,
                "-X",
                "utf8",
                "-B",
                str(ROOT / "scripts" / "verify_v05_v06_equivalence.py"),
                "--fixture",
                str(fixtures / "migration_daily_value_drift.json"),
            ),
            1,
            "approved target readings changed",
        ),
        (
            (
                python,
                "-X",
                "utf8",
                "-B",
                str(ROOT / "scripts" / "verify_v05_v06_equivalence.py"),
                "--fixture",
                str(fixtures / "migration_timestamp_drift.json"),
            ),
            1,
            "timestamps changed",
        ),
        (
            (
                python,
                "-X",
                "utf8",
                "-B",
                str(ROOT / "scripts" / "verify_v05_v06_equivalence.py"),
                "--fixture",
                str(fixtures / "migration_association_drift.json"),
            ),
            1,
            "no v0.6 profile with preserved identifiers",
        ),
        (
            (
                python,
                "-X",
                "utf8",
                "-B",
                str(ROOT / "scripts" / "verify_publication.py"),
                "--self-test",
            ),
            0,
            "public/qaqc fixture was rejected",
        ),
        (
            (
                python,
                "-S",
                "-X",
                "utf8",
                "-B",
                str(ROOT / "scripts" / "check_jsonld.py"),
                str(ROOT / "schemas" / "MeterDataRequest" / "v0.6"),
            ),
            2,
            "PyLD is required",
        ),
    )
    failures = sum(not run_expected(*check) for check in checks)
    failures += not run_mirror_drift_fixture(python, fixtures / "ec_mirror_drift.json")
    if failures:
        return 1
    print(f"PASS: all {len(checks) + 1} negative fixture checks succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
