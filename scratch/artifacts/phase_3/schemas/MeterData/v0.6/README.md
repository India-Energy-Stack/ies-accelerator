# Meter Data Compact Profiles (v0.6)

This directory contains the **Meter Data Compact Profiles** (v0.6) schema definitions and semantic models for telemetry data exchange. It is tailored for high-efficiency, data-only transmissions of smart meter readings and events, omitting the heavy cryptographic wrapping when only raw telemetry payload is being exchanged.

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
python scripts/generate_schema.py schemas/MeterData/v0.6
```

---

## Telemetry Verification & Validation

Example JSON files are validated for structural compliance against `schema.json` using a dedicated validation script.

### To Validate Example Payloads
Run the following command from the repository root:

```bash
python scripts/validate_schema.py schemas/MeterData/v0.6/schema.json schemas/MeterData/v0.6/examples
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

## Reading vs. Usage Telemetry Modes

Smart meter telemetry values are explicitly categorized into one of two modes:
1. **`READING`**: Represents a cumulative register counter value (e.g. cumulative energy import) or a point-in-time snapshot (e.g. instantaneous voltage/current).
2. **`USAGE`**: Represents a delta or average value associated with a time interval (e.g. active energy block incremental consumption or Maximum Demand).

---

## Payload Shapes and Value Representation

The schema offers two distinct mechanisms for representing telemetry values, balancing explicit clarity with high-efficiency transmission.

### 1. Form A: Elaborated Representation (`readings` / `touBuckets`)
Telemetry is presented as an array of discrete `Reading` objects containing inline values, timestamps, and register details. Physical units and phases are resolved out-of-band via OBIS codes.

```json
"readings": [
  {
    "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp" },
    "value": 120.0,
    "reportedMode": "USAGE",
    "openingValue": 5000.0,
    "closingValue": 5120.0
  }
]
```

### 2. Form B: Flat OpenADR-Aligned Compact Representation (`intervals`)
Used for dense time-series telemetry (e.g. load surveys). Positional array formatting maps each payload value directly to a defined `compactSequenceRef` in `payloadDescriptorSet`. Rather than nesting data inside `intervalBlocks`, the profile uses a top-level `intervalPeriod` default duration and a flat `intervals` array.

```json
"payloadDescriptorSet": {
  "name": "IntervalLoadSurveySet",
  "payloadDescriptors": [
    { "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp block" }, "reportedMode": "USAGE" }
  ],
  "compactSequences": [
    {
      "name": "IntervalEnergySeq",
      "sequenceItems": [
        { "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp block" }, "reportedMode": "USAGE" }
      ]
    }
  ]
},
"compactSequenceRef": "IntervalEnergySeq",
"intervalPeriod": { "start": "2026-05-18T10:00:00+05:30", "duration": "PT15M" },
"intervals": [
  { "id": 0, "payloads": [2.1] },
  { "id": 1, "payloads": [2.4] }
]
```

---

## Data Annotations & Overrides

### Sparse Cell Overrides
Annotations like validation states or peak demand timestamps are applied directly to individual elements inside the flat `intervals` array:

```json
"intervals": [
  {
    "id": 2,
    "payloads": [5.21],
    "overrides": [
      {
        "intervalId": 2,
        "descriptorIndex": 0,
        "validationStatus": "ESTIMATED",
        "source": "ESTIMATED"
      }
    ]
  }
]
```

### Maximum Demand snapshoting
When transmitting Maximum Demand snapshots in Elaborated form (e.g. inside `readings`), the exact occurrence timestamp and integration window are provided:

```json
{
  "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.6.0.255" },
  "reportedMode": "USAGE",
  "value": 8.42,
  "integrationPeriod": "PT30M",
  "occurredAt": "2026-04-18T19:30:00+05:30"
}
```

---

## Interoperability & Custom Codes

> [!WARNING]
> **Important Note on Custom Codes**: The schema supports defining and using custom/additional OBIS or Short Codes within the `PayloadDescriptorSet` and mapping catalogs. However, to maintain standardization and interoperability across the ecosystem, we strongly recommend NOT defining custom codes and instead sticking to the canonical set defined in `OBISMapping.json`.
