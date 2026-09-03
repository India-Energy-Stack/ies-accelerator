#!/usr/bin/env python3
"""Require every compiled schema to identify itself under the canonical host.

The canonical schema registry is GitHub Pages
(https://india-energy-stack.github.io/ies-accelerator/schemas). A schema whose
attributes.yaml does not pin ``$id`` used to inherit the generator's fallback
host, so a routine regeneration could silently move one family onto a
different origin than its siblings and than the ``$ref``s pointing at it.
This gate fails on any such drift: the source must pin ``$id``, the compiled
``schema.json`` must carry it, the JSON-LD ``ies`` prefix must live on the
same host, and no IES-internal ``$ref`` may use another host.

ElectricityCredential is a frozen mirror of the upstream DEG revision and is
verified byte-for-byte by ``verify_ec_mirror.py``; it keeps its upstream
identifiers and is excluded here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
CANONICAL = "https://india-energy-stack.github.io/ies-accelerator/schemas"
IES_VOCAB = f"{CANONICAL}/ies"
NON_CANONICAL_HOSTS = (
    "https://raw.githubusercontent.com/India-Energy-Stack/",
    "https://github.com/India-Energy-Stack/",
    "https://india-energy-stack.gitbook.io/",
)
EXCLUDED_FAMILIES = {"ElectricityCredential"}


def iter_refs(node: object):
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            yield ref
        for value in node.values():
            yield from iter_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_refs(value)


def check_version(version_dir: Path) -> list[str]:
    family = version_dir.parent.name
    version = version_dir.name
    relative = version_dir.relative_to(ROOT).as_posix()
    expected_id = f"{CANONICAL}/{family}/{version}/schema.json"
    errors: list[str] = []

    source = yaml.safe_load((version_dir / "attributes.yaml").read_text(encoding="utf-8"))
    root = (source.get("components") or {}).get("schemas", {}).get(family)
    if root is None:
        errors.append(f"{relative}: attributes.yaml has no root component named {family}")
    elif root.get("$id") != expected_id:
        errors.append(f"{relative}: attributes.yaml root $id is {root.get('$id')!r}, expected {expected_id!r}")

    schema_path = version_dir / "schema.json"
    if schema_path.is_file():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if schema.get("$id") != expected_id:
            errors.append(f"{relative}: schema.json $id is {schema.get('$id')!r}, expected {expected_id!r}")
        for ref in iter_refs(schema):
            if ref.startswith(NON_CANONICAL_HOSTS):
                errors.append(f"{relative}: schema.json $ref uses a non-canonical host: {ref}")
    else:
        errors.append(f"{relative}: schema.json is missing")

    for name, expected_prefix in (("context.jsonld", f"{IES_VOCAB}#"), ("vocab.jsonld", f"{IES_VOCAB}/")):
        path = version_dir / name
        if not path.is_file():
            errors.append(f"{relative}: {name} is missing")
            continue
        context = json.loads(path.read_text(encoding="utf-8")).get("@context", {})
        ies = context.get("ies")
        if ies != expected_prefix:
            errors.append(f"{relative}: {name} ies prefix is {ies!r}, expected {expected_prefix!r}")

    return errors


def main() -> int:
    errors: list[str] = []
    checked = 0
    for source in sorted(SCHEMAS.glob("*/v*/attributes.yaml")):
        if source.parent.parent.name in EXCLUDED_FAMILIES:
            continue
        checked += 1
        errors.extend(check_version(source.parent))

    if errors:
        print("FAIL: schema identifiers drifted from the canonical host:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"PASS: {checked} schema versions identify themselves under {CANONICAL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
