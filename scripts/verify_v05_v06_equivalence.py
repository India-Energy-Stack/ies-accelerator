#!/usr/bin/env python3
"""Verify the intentional MeterData v0.5 -> v0.6 migration contract.

This is not a strict shape/count equivalence test.  It checks four independent
gates: every v0.5 example has an explicit disposition; every source profile is
covered by its declared v0.6 target; telemetry and critical business values are
preserved; and the current v0.6 examples pass structural and semantic validation.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V5_DIR = ROOT / "schemas" / "MeterData" / "v0.5" / "examples"
V6_DIR = ROOT / "schemas" / "MeterData" / "v0.6" / "examples"
OBIS_MAPPING_PATH = ROOT / "schemas" / "MeterData" / "v0.6" / "IES codes.json"
TEMPORAL_KEYS = {"occurredAt", "_mdOccurredAt", "timestamp", "capturedAt"}

PROFILE_TYPE_MAP = {"BILLING": "BILL_DETAILS"}
CRITICAL_KEYS = {
    "CUSTOMER": (
        "name",
        "consumerCategory",
        "sanctionedLoadKw",
        "billingCycleDay",
        "addressLine",
        "city",
        "postalCode",
        "latitude",
        "longitude",
        "manufacturer",
        "modelNumber",
        "meterCategory",
        "serviceKind",
    ),
    "BILLING": ("billNumber", "billDate", "dueDate", "currency", "amountDue"),
}

# The table is mirrored in schemas/MeterData/v0.6/MIGRATION_FROM_V0.5.md.
DISPOSITIONS = {
    "AggregatedFeeder.json": {
        "target": "AggregatedFeeder.json",
        "reason": "The v0.6 file adds an explicit descriptor profile.",
    },
    "BillingProfile.json": {
        "target": "CustomerBillingSummary.json",
        "reason": "The duplicate v0.5 billing shape is coalesced into BillDetails.",
    },
    "CustomerBillingSummary.json": {
        "target": "CustomerBillingSummary.json",
        "reason": "BILLING is intentionally renamed and reshaped as BILL_DETAILS.",
    },
    "CustomerProfile.json": {
        "target": "CustomerProfile.json",
        "reason": "The identified profile is retained and an anonymised variant is added.",
        "allowed_additions": {"CUSTOMER": 1},
    },
    "DailyProfile.json": {
        "target": "DailyProfile.json",
        "reason": "The v0.6 file adds a descriptor, corrects cumulative examples, and leaves consumer linkage to the meter/customer profile.",
        "ignored_identifiers": ["RR-1234"],
        "approved_replacements": {
            "1.0.1.8.0.255": {
                "source": [98.4, 105.2, 101.8, 96.5, 108.7, 74.3, 71.9],
                "target": [1000.0, 1005.2, 1011.8, 1016.5, 1022.7, 1028.3, 1034.9],
                "reason": "v0.6 replaces malformed daily deltas with a monotonic cumulative import register example.",
            }
        },
        "allowed_target_codes": ["1.0.5.8.0.255"],
    },
    "EventProfile.json": {
        "target": "EventProfile.json",
        "reason": "The event profile is retained and consumer linkage is resolved separately through the meter.",
        "ignored_identifiers": ["RR-1234"],
    },
    "InstantaneousProfile.json": {
        "target": "InstantaneousProfile.json",
        "reason": "The v0.6 file adds a descriptor and leaves consumer linkage to the meter/customer profile.",
        "ignored_identifiers": ["RR-1234"],
    },
    "IntervalProfile.json": {
        "target": "IntervalProfile.json",
        "reason": "Cumulative registers migrate to block registers and consumer linkage is resolved separately through the meter.",
        "ignored_identifiers": ["RR-1234"],
        "allowed_target_codes": ["1.0.2.29.0.255"],
    },
    "MultiMeterBulkDataset.json": {
        "target": "MultiMeterBulkDataset.json",
        "reason": "The v0.6 file adds a descriptor and one new alarm profile.",
        "allowed_additions": {"ALARM": 1},
        "ignored_critical_keys": ["name"],
        "ignored_identifiers_by_type": {
            "INTERVAL": ["CONSUMER-ACME-8888"],
            "DAILY": ["CONSUMER-ACME-8888"],
            "BILLING": ["CONSUMER-ACME-8888"],
            "INSTANTANEOUS": ["CONSUMER-ACME-8888"],
            "EVENT": ["CONSUMER-ACME-8888"],
        },
    },
    "MultiMeterBulkDatasetShortCodes.json": {
        "target": "MultiMeterBulkDatasetShortCodes.json",
        "reason": "The v0.6 file adds a descriptor and one new alarm profile.",
        "allowed_additions": {"ALARM": 1},
        "ignored_critical_keys": ["name"],
        "ignored_identifiers_by_type": {
            "INTERVAL": ["CONSUMER-ACME-8888"],
            "DAILY": ["CONSUMER-ACME-8888"],
            "BILLING": ["CONSUMER-ACME-8888"],
            "INSTANTANEOUS": ["CONSUMER-ACME-8888"],
            "EVENT": ["CONSUMER-ACME-8888"],
        },
        "identifier_rewrites": {
            "METER-GENUS-01": "METER-GENUS-01-ELABORATED",
            "METER-HPL-02": "METER-HPL-02-COMPACT",
        },
        "allowed_target_codes": ["1.0.2.8.0.255"],
    },
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def as_items(document) -> list[dict]:
    return document if isinstance(document, list) else [document]


def load_obis_mapping() -> dict:
    codes = load_json(OBIS_MAPPING_PATH).get("codes", [])
    if isinstance(codes, list):
        return {entry["obis"]: entry for entry in codes if isinstance(entry, dict) and entry.get("obis")}
    return codes


OBIS_MAPPING = load_obis_mapping()


def get_obis_info(ref_value):
    for code, info in OBIS_MAPPING.items():
        if code == ref_value or info.get("shortLabel") == ref_value:
            return code, info
    return ref_value, {}


def check_code_match(v5_code, v6_code) -> bool:
    if v5_code == v6_code:
        return True
    mappings = {
        "1.0.1.8.0.255": "1.0.1.29.0.255",
        "1.0.9.8.0.255": "1.0.9.29.0.255",
        "1.0.2.8.0.255": "1.0.2.29.0.255",
        "1.0.10.8.0.255": "1.0.10.29.0.255",
        "1.0.3.8.0.255": "1.0.3.29.0.255",
        "1.0.4.8.0.255": "1.0.4.29.0.255",
    }
    resolved_v5, _ = get_obis_info(v5_code)
    resolved_v6, _ = get_obis_info(v6_code)
    return (
        resolved_v5 == resolved_v6
        or mappings.get(resolved_v5) == resolved_v6
        or mappings.get(resolved_v6) == resolved_v5
    )


def reading_code(reading: dict):
    ref = reading.get("readingTypeRef")
    if isinstance(ref, dict):
        return ref.get("value")
    return reading.get("readingType") or reading.get("obis")


def descriptor_index(items: list[dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for item in items:
        if item.get("profileType") != "DESCRIPTOR":
            continue
        for descriptor_set in item.get("payloadDescriptorSets", []):
            name = descriptor_set.get("name")
            if name:
                result[name] = descriptor_set
    return result


def normalize_timestamp(value):
    if not isinstance(value, str):
        return value
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    if parsed.tzinfo is None:
        return parsed.isoformat()
    return parsed.astimezone(timezone.utc).isoformat()


def extract_telemetry(profile: dict, *, v6_descriptors: dict[str, dict] | None = None):
    telemetry_values: dict[tuple[object, object], list[tuple[object, float]]] = {}
    overrides: list[tuple[object, object, object, object]] = []
    events: list[tuple[object, object]] = []

    def add_value(code, zone, value, association=None):
        if code is None or value is None:
            return
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            # Compact sequences may carry timestamps or status tokens beside
            # numeric registers; those are not telemetry magnitudes.
            return
        normalized_code, _ = get_obis_info(code)
        telemetry_values.setdefault((normalized_code, zone), []).append(
            (normalize_timestamp(association), numeric_value)
        )

    profile_timestamp = profile.get("timestamp") or profile.get("capturedAt")

    for key in ("readings", "totals", "values"):
        for reading in profile.get(key, []):
            if isinstance(reading, dict):
                add_value(
                    reading_code(reading),
                    reading.get("touZone"),
                    reading.get("value"),
                    reading.get("occurredAt") or profile_timestamp,
                )

    for bucket in profile.get("touBuckets", []):
        zone = bucket.get("zone")
        readings = bucket.get("readings", [])
        if readings:
            for reading in readings:
                add_value(
                    reading_code(reading),
                    zone,
                    reading.get("value"),
                    reading.get("occurredAt") or profile_timestamp,
                )
        else:
            add_value(
                reading_code(bucket),
                zone,
                bucket.get("value"),
                bucket.get("occurredAt") or profile_timestamp,
            )

    for block in profile.get("intervalBlocks", []):
        descriptors = [reading_code(item) for item in block.get("payloadDescriptors", [])]
        zones = [item.get("touZone") for item in block.get("payloadDescriptors", [])]
        for row in block.get("intervals", []):
            for index, value in enumerate(row.get("values", [])):
                if index < len(descriptors):
                    add_value(descriptors[index], zones[index], value, row.get("id"))
        for override in block.get("qualityOverrides") or block.get("overrides") or []:
            index = override.get("descriptorIndex", 0)
            code = descriptors[index] if index < len(descriptors) else None
            normalized, _ = get_obis_info(code)
            overrides.append(
                (
                    override.get("intervalId"),
                    normalized,
                    override.get("validationStatus"),
                    override.get("source"),
                )
            )

    if "intervals" in profile and v6_descriptors is not None:
        descriptor_set = v6_descriptors.get(profile.get("payloadDescriptorSetRef"), {})
        sequence_name = profile.get("compactSequenceRef")
        sequence_items: list[dict] = []
        for sequence in descriptor_set.get("compactSequences", []):
            if sequence.get("name") == sequence_name:
                sequence_items = sequence.get("sequenceItems", [])
                break
        if not sequence_items:
            sequence_items = descriptor_set.get("payloadDescriptors", [])
        descriptors = [reading_code(item) for item in sequence_items]
        zones = [item.get("touZone") for item in sequence_items]
        for row in profile.get("intervals", []):
            for index, value in enumerate(row.get("payloads", [])):
                if index < len(descriptors):
                    add_value(descriptors[index], zones[index], value, row.get("id"))
            for override in row.get("overrides", []):
                index = override.get("descriptorIndex", 0)
                code = descriptors[index] if index < len(descriptors) else None
                normalized, _ = get_obis_info(code)
                overrides.append(
                    (
                        override.get("intervalId") or row.get("id"),
                        normalized,
                        override.get("validationStatus"),
                        override.get("source"),
                    )
                )

    for event in profile.get("events", []):
        events.append((event.get("eventId"), event.get("timestamp")))

    return telemetry_values, overrides, events


def compare_telemetry(
    source,
    target,
    *,
    approved_replacements: dict,
    allowed_target_codes: set[str],
) -> list[str]:
    errors: list[str] = []
    source_values, source_overrides, source_events = source
    target_values, target_overrides, target_events = target

    matched_target_keys: set[tuple[object, object]] = set()
    for (source_code, source_zone), observations in source_values.items():
        target_match = next(
            (
                ((target_code, target_zone), candidate)
                for (target_code, target_zone), candidate in target_values.items()
                if source_zone == target_zone and check_code_match(source_code, target_code)
            ),
            None,
        )
        if target_match is None:
            errors.append(f"missing readings for {source_code!r} in zone {source_zone!r}")
            continue
        target_key, target_observations = target_match
        matched_target_keys.add(target_key)
        if len(observations) != len(target_observations):
            errors.append(
                f"reading count changed for {source_code!r}: v0.5={len(observations)}, v0.6={len(target_observations)}"
            )
            continue

        source_associations = [association for association, _ in observations]
        target_associations = [association for association, _ in target_observations]
        if any(association is not None for association in source_associations) and (
            source_associations != target_associations
        ):
            errors.append(
                f"reading associations changed for {source_code!r}: "
                f"v0.5={source_associations}, v0.6={target_associations}"
            )

        source_numbers = [value for _, value in observations]
        target_numbers = [value for _, value in target_observations]
        replacement = approved_replacements.get(source_code)
        if replacement:
            expected_source = [float(value) for value in replacement.get("source", [])]
            expected_target = [float(value) for value in replacement.get("target", [])]
            if source_numbers != expected_source:
                errors.append(
                    f"approved source readings changed for {source_code!r}: "
                    f"expected={expected_source}, found={source_numbers}"
                )
            if target_numbers != expected_target:
                errors.append(
                    f"approved target readings changed for {source_code!r}: "
                    f"expected={expected_target}, found={target_numbers}"
                )
            if any(value < 0 for value in target_numbers) or any(
                later < earlier for earlier, later in zip(target_numbers, target_numbers[1:])
            ):
                errors.append(
                    f"approved cumulative readings for {source_code!r} are negative or decreasing"
                )
        else:
            for index, (old, new) in enumerate(zip(source_numbers, target_numbers)):
                if abs(old - new) > 1e-4:
                    errors.append(
                        f"reading changed for {source_code!r} at index {index}: v0.5={old}, v0.6={new}"
                    )

    unexpected_target_keys = sorted(
        key
        for key in set(target_values) - matched_target_keys
        if key[0] not in allowed_target_codes
    )
    if unexpected_target_keys:
        errors.append(f"unapproved target-only readings were added: {unexpected_target_keys}")

    for row_id, source_code, status, source_name in source_overrides:
        if not any(
            row_id == target_row
            and check_code_match(source_code, target_code)
            and status == target_status
            and source_name == target_source
            for target_row, target_code, target_status, target_source in target_overrides
        ):
            errors.append(f"quality override was not preserved: {(row_id, source_code, status, source_name)}")

    missing_events = set(source_events) - set(target_events)
    if missing_events:
        errors.append(f"events were not preserved: {sorted(missing_events)}")
    return errors


def compact_sequence_items(profile: dict, descriptors: dict[str, dict]) -> list[dict]:
    descriptor_set = descriptors.get(profile.get("payloadDescriptorSetRef"), {})
    sequence_name = profile.get("compactSequenceRef")
    for sequence in descriptor_set.get("compactSequences", []):
        if sequence.get("name") == sequence_name:
            return sequence.get("sequenceItems", [])
    return descriptor_set.get("payloadDescriptors", [])


def extract_timestamps(profile: dict, descriptors: dict[str, dict]) -> set[object]:
    timestamps: set[object] = set()

    def visit(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in TEMPORAL_KEYS:
                    timestamps.add(normalize_timestamp(value))
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(profile)
    sequence_items = compact_sequence_items(profile, descriptors)
    temporal_indexes = [
        index
        for index, item in enumerate(sequence_items)
        if item.get("attribute") in {"occurredAt", "timestamp", "capturedAt"}
    ]
    for row in profile.get("intervals", []):
        payloads = row.get("payloads", [])
        for index in temporal_indexes:
            if index < len(payloads):
                timestamps.add(normalize_timestamp(payloads[index]))
    return timestamps


def extract_row_timestamp_associations(
    profile: dict,
    descriptors: dict[str, dict],
) -> list[tuple[object, tuple[object, ...]]]:
    """Return timestamps grouped by the interval row that carries them."""
    associations: list[tuple[object, tuple[object, ...]]] = []
    sequence_items = compact_sequence_items(profile, descriptors)
    temporal_indexes = [
        index
        for index, item in enumerate(sequence_items)
        if item.get("attribute") in TEMPORAL_KEYS
    ]

    def direct_timestamps(node) -> list[object]:
        values: list[object] = []
        if isinstance(node, dict):
            for key, value in node.items():
                if key in TEMPORAL_KEYS:
                    values.append(normalize_timestamp(value))
                elif isinstance(value, (dict, list)):
                    values.extend(direct_timestamps(value))
        elif isinstance(node, list):
            for value in node:
                values.extend(direct_timestamps(value))
        return values

    def add_rows(rows: list[dict], *, compact: bool) -> None:
        for position, row in enumerate(rows):
            timestamps = direct_timestamps(row)
            if compact:
                payloads = row.get("payloads", [])
                timestamps.extend(
                    normalize_timestamp(payloads[index])
                    for index in temporal_indexes
                    if index < len(payloads)
                )
            if timestamps:
                associations.append((row.get("id", position), tuple(timestamps)))

    for block in profile.get("intervalBlocks", []):
        add_rows(block.get("intervals", []), compact=False)
    add_rows(profile.get("intervals", []), compact=True)
    return associations


def extract_schedules(profile: dict) -> list[tuple[object, object, tuple[object, ...]]]:
    schedules: list[tuple[object, object, tuple[object, ...]]] = []
    for block in profile.get("intervalBlocks", []):
        period = block.get("intervalPeriod", {})
        schedules.append(
            (
                normalize_timestamp(period.get("start")),
                block.get("intervalLength"),
                tuple(row.get("id") for row in block.get("intervals", [])),
            )
        )
    if profile.get("intervals"):
        period = profile.get("intervalPeriod", {})
        schedules.append(
            (
                normalize_timestamp(period.get("start")),
                period.get("duration"),
                tuple(row.get("id") for row in profile.get("intervals", [])),
            )
        )
    return schedules


def compare_temporal_association(
    source: dict,
    target: dict,
    *,
    target_descriptors: dict[str, dict],
) -> list[str]:
    errors: list[str] = []
    source_schedules = extract_schedules(source)
    target_schedules = extract_schedules(target)
    if source_schedules and source_schedules != target_schedules:
        errors.append(
            f"interval schedule or row association changed: "
            f"v0.5={source_schedules}, v0.6={target_schedules}"
        )

    source_timestamps = extract_timestamps(source, {})
    target_timestamps = extract_timestamps(target, target_descriptors)
    if source_timestamps and source_timestamps != target_timestamps:
        errors.append(
            f"timestamps changed: v0.5={sorted(source_timestamps)}, "
            f"v0.6={sorted(target_timestamps)}"
        )

    source_row_timestamps = extract_row_timestamp_associations(source, {})
    target_row_timestamps = extract_row_timestamp_associations(target, target_descriptors)
    if source_row_timestamps and source_row_timestamps != target_row_timestamps:
        errors.append(
            f"row timestamp associations changed: "
            f"v0.5={source_row_timestamps}, v0.6={target_row_timestamps}"
        )
    return errors


def values_for_key(node, wanted: str) -> list[object]:
    result: list[object] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == wanted and not isinstance(value, (dict, list)):
                result.append(value)
            result.extend(values_for_key(value, wanted))
    elif isinstance(node, list):
        for item in node:
            result.extend(values_for_key(item, wanted))
    return result


def id_values(node) -> list[str]:
    result: list[str] = []
    if isinstance(node, dict):
        scheme = node.get("scheme")
        if (
            isinstance(scheme, str)
            and scheme.upper() not in {"OBIS", "SHORT_NAME", "SHORT_CODE"}
            and isinstance(node.get("value"), str)
        ):
            result.append(node["value"])
        for value in node.values():
            result.extend(id_values(value))
    elif isinstance(node, list):
        for item in node:
            result.extend(id_values(item))
    return result


def identifier_matches(source_id: str, target_id: str, rewrites: dict[str, str]) -> bool:
    expected = rewrites.get(source_id, source_id)
    return target_id == expected or target_id.endswith(f":{expected}")


def ignored_identifiers_for(disposition: dict, source_type: str | None) -> set[str]:
    ignored = set(disposition.get("ignored_identifiers", []))
    ignored.update(disposition.get("ignored_identifiers_by_type", {}).get(source_type, []))
    return ignored


def identifier_preservation_errors(source: dict, target: dict, disposition: dict) -> list[str]:
    ignored = ignored_identifiers_for(disposition, source.get("profileType"))
    rewrites = disposition.get("identifier_rewrites", {})
    target_ids = id_values(target)
    errors: list[str] = []
    for source_id in id_values(source):
        if source_id in ignored:
            continue
        if not any(identifier_matches(source_id, target_id, rewrites) for target_id in target_ids):
            errors.append(f"identifier value {source_id!r} was not preserved in the paired profile")
    return errors


def compare_critical_values(
    source: dict,
    target: dict,
    *,
    ignored_keys: set[str],
    disposition: dict,
) -> list[str]:
    errors: list[str] = []
    source_type = source.get("profileType")
    for key in CRITICAL_KEYS.get(source_type, ()):
        if key in ignored_keys:
            continue
        old_values = values_for_key(source, key)
        new_values = values_for_key(target, key)
        for value in old_values:
            if value not in new_values:
                errors.append(f"critical value {key}={value!r} was not preserved")

    errors.extend(identifier_preservation_errors(source, target, disposition))
    return errors


def pair_profiles(source_items: list[dict], target_items: list[dict], disposition: dict):
    candidates = [item for item in target_items if item.get("profileType") != "DESCRIPTOR"]
    pairs: list[tuple[dict, dict]] = []
    used: set[int] = set()
    errors: list[str] = []

    for source in source_items:
        expected_type = PROFILE_TYPE_MAP.get(source.get("profileType"), source.get("profileType"))
        index = next(
            (
                idx
                for idx, target in enumerate(candidates)
                if idx not in used
                and target.get("profileType") == expected_type
                and not identifier_preservation_errors(source, target, disposition)
            ),
            None,
        )
        if index is None:
            errors.append(
                f"no v0.6 profile with preserved identifiers covers source type "
                f"{source.get('profileType')!r}"
            )
            continue
        used.add(index)
        pairs.append((source, candidates[index]))

    additions = Counter(
        candidates[index].get("profileType") for index in range(len(candidates)) if index not in used
    )
    allowed = Counter(disposition.get("allowed_additions", {}))
    if additions != allowed:
        errors.append(f"unexpected v0.6 additions: found {dict(additions)}, allowed {dict(allowed)}")
    return pairs, errors


def load_fixture(path: Path | None, dispositions: dict) -> tuple[dict, dict]:
    result = {name: dict(value) for name, value in dispositions.items()}
    if path is None:
        return result, {}
    fixture = load_json(path)
    for name in fixture.get("omitDispositions", []):
        result.pop(name, None)
    return result, fixture


def apply_target_mutations(target_name: str, document, fixture: dict):
    for mutation in fixture.get("targetMutations", []):
        if mutation.get("file") != target_name:
            continue
        pointer = mutation.get("pointer")
        if not isinstance(pointer, str) or not pointer.startswith("/"):
            raise ValueError(f"invalid target mutation pointer: {pointer!r}")
        parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
        parent = document
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        leaf = parts[-1]
        if isinstance(parent, list):
            parent[int(leaf)] = mutation.get("value")
        else:
            parent[leaf] = mutation.get("value")
    return document


def run_current_validity() -> bool:
    commands = (
        (
            sys.executable,
            "-X",
            "utf8",
            "-B",
            str(ROOT / "scripts" / "validate_schema.py"),
            str(ROOT / "schemas" / "MeterData" / "v0.6" / "schema.json"),
            str(V6_DIR),
        ),
        (
            sys.executable,
            "-X",
            "utf8",
            "-B",
            str(ROOT / "schemas" / "MeterData" / "v0.6" / "validation" / "validator.py"),
            str(V6_DIR),
        ),
    )
    for command in commands:
        completed = subprocess.run(command, cwd=ROOT)
        if completed.returncode != 0:
            print(f"FAIL: current-version validity command exited {completed.returncode}: {' '.join(command)}")
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        type=Path,
        help="apply a negative-test manifest mutation before evaluating coverage",
    )
    args = parser.parse_args()

    dispositions, fixture = load_fixture(args.fixture.resolve() if args.fixture else None, DISPOSITIONS)
    source_files = {path.name for path in V5_DIR.glob("*.json")}
    declared_files = set(dispositions)
    missing = sorted(source_files - declared_files)
    stale = sorted(declared_files - source_files)
    if missing:
        print(f"FAIL: missing intentional disposition for: {', '.join(missing)}")
    if stale:
        print(f"FAIL: dispositions name absent v0.5 examples: {', '.join(stale)}")
    if missing or stale:
        return 1
    print(f"PASS: intentional disposition covers all {len(source_files)} v0.5 example files")

    overall_errors: list[str] = []
    for source_name in sorted(source_files):
        disposition = dispositions[source_name]
        target_name = disposition.get("target")
        reason = disposition.get("reason")
        if not isinstance(target_name, str) or not isinstance(reason, str) or not reason:
            overall_errors.append(f"{source_name}: disposition lacks target or reason")
            continue
        target_path = V6_DIR / target_name
        if not target_path.is_file():
            overall_errors.append(f"{source_name}: target does not exist: {target_name}")
            continue

        source_items = as_items(load_json(V5_DIR / source_name))
        target_document = apply_target_mutations(target_name, load_json(target_path), fixture)
        target_items = as_items(target_document)
        pairs, errors = pair_profiles(source_items, target_items, disposition)
        descriptors = descriptor_index(target_items)
        for index, (source, target) in enumerate(pairs):
            source_telemetry = extract_telemetry(source)
            target_telemetry = extract_telemetry(target, v6_descriptors=descriptors)
            pair_errors = compare_telemetry(
                source_telemetry,
                target_telemetry,
                approved_replacements=disposition.get("approved_replacements", {}),
                allowed_target_codes=set(disposition.get("allowed_target_codes", [])),
            )
            pair_errors.extend(
                compare_temporal_association(
                    source,
                    target,
                    target_descriptors=descriptors,
                )
            )
            pair_errors.extend(
                compare_critical_values(
                    source,
                    target,
                    ignored_keys=set(disposition.get("ignored_critical_keys", [])),
                    disposition=disposition,
                )
            )
            errors.extend(f"profile {index}: {message}" for message in pair_errors)

        if errors:
            overall_errors.extend(f"{source_name}: {message}" for message in errors)
        else:
            print(f"PASS: {source_name} -> {target_name} ({len(pairs)} profile(s) covered)")

    if overall_errors:
        print("FAIL: migration coverage or semantic preservation errors:")
        for error in overall_errors:
            print(f"  - {error}")
        return 1

    print("PASS: migration coverage and semantic preservation checks succeeded")
    if not run_current_validity():
        return 1
    print("PASS: current MeterData v0.6 structural and semantic validation succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
