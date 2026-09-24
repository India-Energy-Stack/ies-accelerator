#!/usr/bin/env python3
"""Run intended-valid schema examples and dedicated semantic test suites."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
CEP_EXAMPLES = ROOT / "use-cases" / "consumer-energy-passport" / "examples"
DERV_EXAMPLES = ROOT / "use-cases" / "der-visibility" / "examples"


def run(command: tuple[str, ...]) -> bool:
    print(f"\n==> {' '.join(command)}", flush=True)
    completed = subprocess.run(command, cwd=ROOT)
    if completed.returncode:
        print(f"FAIL: command exited {completed.returncode}", file=sys.stderr)
        return False
    return True


def main() -> int:
    commands: list[tuple[str, ...]] = []
    validator = str(ROOT / "scripts" / "validate_schema.py")
    for schema_path in sorted(SCHEMAS.glob("*/v*/schema.json")):
        examples = schema_path.parent / "examples"
        if examples.is_dir() and any(examples.glob("*.json")):
            commands.append(
                (
                    sys.executable,
                    "-X",
                    "utf8",
                    "-B",
                    validator,
                    str(schema_path),
                    str(examples),
                )
            )

    commands.extend(
        (
            (
                sys.executable,
                "-X",
                "utf8",
                "-B",
                validator,
                str(SCHEMAS / "ElectricityCredential" / "v1.2" / "schema.json"),
                str(CEP_EXAMPLES / "schedule-i-example.json"),
            ),
            (
                sys.executable,
                "-X",
                "utf8",
                "-B",
                validator,
                str(SCHEMAS / "MeterData" / "v0.6" / "schema.json"),
                str(DERV_EXAMPLES / "schedule-ii-example.json"),
            ),
            (
                sys.executable,
                "-X",
                "utf8",
                "-B",
                str(SCHEMAS / "MeterData" / "v0.6" / "validation" / "validator.py"),
                str(DERV_EXAMPLES / "schedule-ii-example.json"),
            ),
            (
                sys.executable,
                "-X",
                "utf8",
                "-B",
                str(SCHEMAS / "MeterData" / "v0.6" / "validation" / "validator.py"),
                str(SCHEMAS / "MeterData" / "v0.6" / "examples"),
            ),
            (
                sys.executable,
                "-X",
                "utf8",
                "-B",
                str(SCHEMAS / "MeterDataRequest" / "v0.6" / "validation" / "validator.py"),
                str(SCHEMAS / "MeterDataRequest" / "v0.6" / "examples"),
            ),
            (
                sys.executable,
                "-X",
                "utf8",
                "-B",
                str(SCHEMAS / "MeterData" / "v0.6" / "validation" / "test_runner.py"),
            ),
            (
                sys.executable,
                "-X",
                "utf8",
                "-B",
                str(SCHEMAS / "MeterDataRequest" / "v0.6" / "validation" / "test_runner.py"),
            ),
        )
    )

    failures = sum(not run(command) for command in commands)
    if failures:
        print(f"\nFAIL: {failures} schema/semantic command(s) failed", file=sys.stderr)
        return 1
    print(f"\nPASS: {len(commands)} schema and semantic commands succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
