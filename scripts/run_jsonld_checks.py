#!/usr/bin/env python3
"""Execute and enforce the declared JSON-LD conformance scope."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts" / "jsonld_conformance_scope.json"
CHECKER = ROOT / "scripts" / "check_jsonld.py"


def discover_contexts() -> set[str]:
    return {
        path.parent.relative_to(ROOT).as_posix()
        for path in (ROOT / "schemas").glob("*/*/context.jsonld")
    }


def main() -> int:
    scope = json.loads(MANIFEST.read_text(encoding="utf-8"))
    declared = set(scope)
    discovered = discover_contexts()
    missing = sorted(discovered - declared)
    stale = sorted(declared - discovered)
    if missing or stale:
        print(
            f"FAIL: JSON-LD scope inventory mismatch: undeclared={missing}, stale={stale}",
            file=sys.stderr,
        )
        return 1

    failures: list[str] = []
    enforced = 0
    deferred = 0
    for relative in sorted(scope):
        entry = scope[relative]
        status = entry.get("status")
        reason = entry.get("reason")
        if status not in {"enforced-pass", "deferred-fail"} or not isinstance(reason, str) or not reason:
            failures.append(f"{relative}: invalid status or missing reason")
            continue

        completed = subprocess.run(
            (sys.executable, "-X", "utf8", "-B", str(CHECKER), str(ROOT / relative)),
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        output = completed.stdout + completed.stderr
        if status == "enforced-pass":
            enforced += 1
            if completed.returncode != 0:
                failures.append(
                    f"{relative}: enforced JSON-LD check exited {completed.returncode}\n{output}"
                )
            else:
                print(f"ENFORCED PASS: {relative}")
            continue

        deferred += 1
        expected = entry.get("expectedDiagnostic")
        if completed.returncode != 1 or not isinstance(expected, str) or expected not in output:
            failures.append(
                f"{relative}: deferred check must exit 1 for {expected!r}; "
                f"got {completed.returncode}\n{output}"
            )
        else:
            print(f"DEFERRED (observed {expected!r}): {relative} -- {reason}")

    if failures:
        print("FAIL: JSON-LD conformance scope is not satisfied:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(
        f"PASS: JSON-LD executed for {len(scope)} schema versions "
        f"({enforced} enforced pass, {deferred} explicit frozen deferrals)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
