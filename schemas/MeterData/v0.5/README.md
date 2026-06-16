> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.5/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.5/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.5/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.5/vocab.jsonld) · [examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.5/examples)

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

---

## OBIS Mapping and Identifiers

The `MeterData` schema relies on flexible identifiers to reference physical quantities. The exact mapping of OBIS codes to physical units, phases, and categories is defined in the [OBISMapping.json](./OBISMapping.json) file.

### Interpreting OBISMapping.json
The `OBISMapping` file serves as the canonical dictionary for interpreting IS 15959 standard meter registers. It contains both OBIS codes and detailed event taxonomies.

**Snapshot:**
```json
"1.0.1.8.0.255": {
  "name": "Active energy import - cumulative (kWh)",
  "shortLabel": "kWh imp",
  "unit": "kWh",
  "flowDirection": "IMPORT",
  "accumulationBehaviour": "CUMULATIVE",
  "category": "energyCumulative",
  "meterCategories": ["A", "B", "C", "D1", "D2", "D3", "D4"],
  "source": "IS 15959 Part 1 Table 22; Part 2 Table A14; Part 3 Table 1"
}
```

### Identifier Flexibility (OBIS vs. Short Names)
When structuring your payload descriptors or values, you have the flexibility to use either exact OBIS codes or human-readable short names.

* **Using OBIS Codes**: `{"scheme": "OBIS", "value": "1.0.1.8.0.255"}`
* **Using Short Names**: `{"scheme": "SHORT_CODE", "value": "kWh imp"}`

*See the [MultiMeterBulkDataset.json](./examples/MultiMeterBulkDataset.json) for OBIS examples and [AggregatedFeeder.json](./examples/AggregatedFeeder.json) for Short Code examples.*

---

## Payload Shapes and Value Representation

The schema offers two distinct mechanisms for representing telemetry values, balancing explicit clarity with high-efficiency transmission.

### 1. Elaborated Representation
Used primarily in the [`InstantaneousProfile`](./examples/InstantaneousProfile.json), each value explicitly declares its reading type, unit, and phase inline. This is highly descriptive but less compact.

```json
"values": [
  {
    "readingTypeRef": { "scheme": "OBIS", "value": "1.0.32.7.0.255" },
    "value": 235.5,
    "unit": "V",
    "phase": "R"
  }
]
```

### 2. Compact `IntervalRow` Representation
Used heavily in the [`IntervalProfile`](./examples/IntervalProfile.json) and [`DailyProfile`](./examples/DailyProfile.json). Descriptors are declared once in a `payloadDescriptors` array, and time-series data is transmitted as simple arrays of numbers (`IntervalRow`) that map positionally to the descriptors.

```json
"payloadDescriptors": [
  { "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp block" } },
  { "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh exp block" } }
],
"intervals": [
  { "id": 0, "values": [600, 0] },
  { "id": 1, "values": [580, 0] }
]
```

---

## Data Annotations

The schema supports sparse annotations to add metadata exactly where needed without bloating the payload.

### Quality Overrides
By default, all readings are assumed to be `{VALID, METER}`. If a specific interval was estimated or rejected, you can inject a sparse `QualityOverride` targeting its specific `intervalId`.

```json
"qualityOverrides": [
  {
    "intervalId": 45,
    "descriptorIndex": 0,
    "validationStatus": "ESTIMATED",
    "source": "ESTIMATED"
  }
]
```
*See the [`MultiMeterBulkDataset.json`](./examples/MultiMeterBulkDataset.json) for a full example of sparse quality overrides.*

### Maximum Demand Timestamps
When transmitting Maximum Demand snapshots (e.g. inside a [`BillingProfile`](./examples/BillingProfile.json)), the exact timestamp of the peak is annotated using the `occurredAt` property.

```json
{
  "readingTypeRef": { "scheme": "SHORT_CODE", "value": "MD kW" },
  "value": 15.2,
  "occurredAt": "2026-05-18T14:30:00+05:30",
  "integrationPeriod": "PT30M"
}
```
