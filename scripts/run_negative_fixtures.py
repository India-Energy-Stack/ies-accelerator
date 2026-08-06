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


def decode_pointer(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {pointer!r}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def apply_mutations(document, mutations: list[dict]) -> None:
    for mutation in mutations:
        parts = decode_pointer(mutation.get("pointer", ""))
        parent = document
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        leaf = parts[-1]
        operation = mutation.get("operation", "replace")
        if operation == "remove":
            if isinstance(parent, list):
                del parent[int(leaf)]
            else:
                del parent[leaf]
        elif operation == "replace":
            if isinstance(parent, list):
                parent[int(leaf)] = mutation.get("value")
            else:
                parent[leaf] = mutation.get("value")
        else:
            raise ValueError(f"unsupported mutation operation: {operation!r}")


def run_payload_fixture(python: str, fixture_path: Path) -> bool:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    try:
        source = (ROOT / fixture["source"]).resolve()
        source.relative_to(ROOT)
        document = json.loads(source.read_text(encoding="utf-8"))
        apply_mutations(document, fixture["mutations"])
        validator = fixture["validator"]
        expected = fixture["expectedDiagnostic"]
    except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: invalid payload fixture {fixture_path}: {error}", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory(prefix="ies-payload-negative-") as temp:
        mutated = Path(temp) / source.name
        mutated.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if validator.get("kind") == "schema":
            command = (
                python,
                "-X",
                "utf8",
                "-B",
                str(ROOT / "scripts" / "validate_schema.py"),
                str(ROOT / validator["schema"]),
                str(mutated),
            )
        elif validator.get("kind") == "semantic":
            command = (
                python,
                "-X",
                "utf8",
                "-B",
                str(ROOT / validator["script"]),
                str(mutated),
            )
        else:
            print(f"FAIL: unknown validator kind in {fixture_path}", file=sys.stderr)
            return False
        return run_expected(command, 1, expected)


def run_jsonld_scope_drift_fixture(python: str, fixture_path: Path) -> bool:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    targets = fixture.get("targets")
    if not isinstance(targets, list) or not targets:
        print(f"FAIL: invalid JSON-LD drift fixture: {fixture_path}", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory(prefix="ies-jsonld-scope-negative-") as temp:
        isolated_root = Path(temp)
        shutil.copytree(ROOT / "schemas", isolated_root / "schemas")
        isolated_scripts = isolated_root / "scripts"
        isolated_scripts.mkdir()
        for name in ("check_jsonld.py", "run_jsonld_checks.py", "jsonld_conformance_scope.json"):
            shutil.copy2(ROOT / "scripts" / name, isolated_scripts / name)

        try:
            for target_fixture in targets:
                target = (isolated_root / target_fixture["relativePath"]).resolve()
                target.relative_to(isolated_root)
                document = json.loads(target.read_text(encoding="utf-8"))
                apply_mutations(document, target_fixture["mutations"])
                target.write_text(
                    json.dumps(document, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
        except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
            print(f"FAIL: invalid JSON-LD drift fixture {fixture_path}: {error}", file=sys.stderr)
            return False
        return run_expected(
            (
                python,
                "-X",
                "utf8",
                "-B",
                str(isolated_scripts / "run_jsonld_checks.py"),
            ),
            1,
            "deferred check must exit 1 with exact issues",
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
                str(fixtures / "migration_row_timestamp_swap.json"),
            ),
            1,
            "row timestamp associations changed",
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
    failures += not run_payload_fixture(python, fixtures / "cep_schedule_i_missing_customer_number.json")
    failures += not run_payload_fixture(python, fixtures / "derv_schedule_ii_unknown_reading_type.json")
    failures += not run_jsonld_scope_drift_fixture(python, fixtures / "jsonld_masked_expansion_drift.json")
    failures += not run_mirror_drift_fixture(python, fixtures / "ec_mirror_drift.json")
    if failures:
        return 1
    print(f"PASS: all {len(checks) + 4} negative fixture checks succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
