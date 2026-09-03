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
ISSUES_PREFIX = "JSONLD_ISSUES_JSON="


def discover_contexts() -> set[str]:
    return {
        path.parent.relative_to(ROOT).as_posix()
        for path in (ROOT / "schemas").glob("*/*/context.jsonld")
    }


def parse_issues(output: str) -> list[str] | None:
    summaries = [line[len(ISSUES_PREFIX):] for line in output.splitlines() if line.startswith(ISSUES_PREFIX)]
    if len(summaries) != 1:
        return None
    try:
        issues = json.loads(summaries[0])
    except json.JSONDecodeError:
        return None
    if not isinstance(issues, list) or not all(isinstance(issue, str) for issue in issues):
        return None
    return issues


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
        observed_issues = parse_issues(output)
        if observed_issues is None:
            failures.append(f"{relative}: checker did not emit one valid issue summary\n{output}")
            continue
        if status == "enforced-pass":
            enforced += 1
            if completed.returncode != 0 or observed_issues:
                failures.append(
                    f"{relative}: enforced JSON-LD check exited {completed.returncode} "
                    f"with issues {observed_issues}\n{output}"
                )
            else:
                print(f"ENFORCED PASS: {relative}")
            continue

        deferred += 1
        expected = entry.get("expectedIssues")
        if (
            completed.returncode != 1
            or not isinstance(expected, list)
            or not all(isinstance(issue, str) for issue in expected)
            or observed_issues != sorted(expected)
        ):
            failures.append(
                f"{relative}: deferred check must exit 1 with exact issues {expected!r}; "
                f"got {completed.returncode} with {observed_issues!r}\n{output}"
            )
        else:
            print(f"DEFERRED ({len(observed_issues)} exact issue(s)): {relative} -- {reason}")

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
