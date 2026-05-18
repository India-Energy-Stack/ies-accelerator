# Meter Data Compact Profiles (v0.5)

This directory contains the **Meter Data Compact Profiles** (v0.5) schema definitions and semantic models for telemetry data exchange. It is tailored for high-efficiency, data-only transmissions of smart meter readings and events, omitting the heavy cryptographic wrapping when only raw telemetry payload is being exchanged.

## Overview

The `MeterData` schema standardizes telemetry exchanges into **six compact profile shapes** representing different read cadences and data structures from smart meters:

1. **`CUSTOMER`** — Slow-changing customer metadata, service points, and meter installations.
2. **`INTERVAL`** — Block load survey profile at high-resolution intervals (e.g., 15-minute or 30-minute blocks).
3. **`DAILY`** — Daily accumulated load survey profiles.
4. **`BILLING`** — Monthly billing summaries, including billing registers, tariff buckets (Time-of-Use), and billing values.
5. **`INSTANTANEOUS`** — Real-time snapshots of electrical quantities (voltages, currents, active/reactive powers) at a specific moment.
6. **`EVENT`** — Event logs matching standard IS 15959 diagnostic codes and tamper events.

---

## Directory Structure and Files

| File | Description |
|------|-------------|
| [`attributes.yaml`](./attributes.yaml) | Canonical OpenAPI 3.1.1 schema source of truth, describing all attributes, models, and types. |
| [`schema.json`](./schema.json) | Compiled Draft 2020-12 JSON Schema for standard validation of data payloads. |
| [`context.jsonld`](./context.jsonld) | Compiled JSON-LD context mapping telemetry attributes to semantic terms under `ies:` or `schema:` namespaces. |
| [`vocab.jsonld`](./vocab.jsonld) | Compiled JSON-LD vocabulary (ontology graph) defining all classes and properties. |
| [`examples/`](./examples) | Standard, JSON-LD augmented telemetry payload example files for all profile types. |

---

## Schema Generation and Compilation

The `schema.json`, `context.jsonld`, and `vocab.jsonld` files are compiled automatically from the core `attributes.yaml` using a generic Python build script.

### To Compile Schemas
To recompile schemas following modifications in `attributes.yaml`, run the following command from the repository root inside your virtual environment:

```bash
python scripts/generate_schema.py schemas/MeterData/v0.5
```

---

## Telemetry Verification & Validation

Example JSON files are validated for structural compliance against `schema.json` using a dedicated validation script.

### To Validate Example Payloads
Run the following command from the repository root:

```bash
python scripts/validate_schema.py schemas/MeterData/v0.5/schema.json schemas/MeterData/v0.5/examples
```

---

## JSON-LD Integration

All example payloads in the `examples/` directory have been augmented to support Linked Data semantics:
1. **`@context`** — Points to `../context.jsonld` for semantic property resolution.
2. **`@type`** — Indicates the profile class shape (e.g. `CustomerProfile`, `IntervalProfile`, `DailyProfile`, etc.), aligning the compact profiles to the broader Beckn/IES semantic web ecosystem.
