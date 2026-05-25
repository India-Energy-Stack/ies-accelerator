# Meter Data Compact Profiles (v0.6)

This directory contains the **Meter Data Compact Profiles** (v0.6) schema definitions and semantic models for telemetry data exchange. It is tailored for high-efficiency, data-only transmissions of smart meter readings and events, omitting heavy cryptographic wrapping when only raw telemetry payload is being exchanged.

The `MeterData` schema standardizes telemetry exchanges into **eight compact profile shapes** representing different read cadences and data structures from smart meters:

1. **`CUSTOMER`** — Slow-changing customer metadata, service points, and meter installations.
2. **`INTERVAL`** — Block load survey profile at high-resolution intervals (e.g., 15-minute or 30-minute blocks).
3. **`DAILY`** — Daily accumulated load survey profiles.
4. **`MONTHLY`** — Monthly billing resets (billing history cumulative total energy registers, ToU buckets, and Maximum Demand).
5. **`BILL_DETAILS`** — Utility billing computed details (billing amount, bill number, due dates, currency, prepaid balance, and payment status).
6. **`INSTANTANEOUS`** — Real-time snapshots of electrical quantities (voltages, currents, active/reactive powers) at a specific moment.
7. **`EVENT`** — Event logs matching standard IS 15959 diagnostic codes and tamper events.
8. **`ALARM`** — Real-time active alerts representing immediate state conditions (tamper, low prepayment credit, voltage sag, overload) from the meter.

---

## Directory Structure and Files

| File | Description |
|------|-------------|
| [`attributes.yaml`](./attributes.yaml) | Canonical OpenAPI schema source of truth, describing all attributes, models, and types. |
| [`schema.json`](./schema.json) | Compiled Draft 2020-12 JSON Schema for standard validation of data payloads. |
| [`context.jsonld`](./context.jsonld) | Compiled JSON-LD context mapping telemetry attributes to semantic terms under `ies:` or `schema:` namespaces. |
| [`vocab.jsonld`](./vocab.jsonld) | Compiled JSON-LD vocabulary (ontology graph) defining all classes and properties. |
| [`examples/`](./examples) | Standard, JSON-LD augmented telemetry payload example files for all profile types. |

---

## Data Descriptor Engine & The Array Envelope

In v0.6, telemetry architecture has transitioned to a highly optimized, strict inheritance structure powered by the **Data Descriptor Engine**. 

Instead of transmitting bulky metadata inline with every physical reading, telemetry can be wrapped in a **JSON Array**.

### Centralized `PayloadDescriptorProfile`
A JSON array payload can contain one or more `PayloadDescriptorProfile` objects. This serves as the dictionary for all compact profiles inside the payload array:
* **`payloadDescriptors`**: Defines the metadata for specific registers (e.g., `readingType`, `unit`, `flowDirection`, `category`).
* **`compactSequences`**: Defines the physical column layout of the dense numerical payload matrices.

### Dynamic `SequenceItem` Columns (`attribute`)
A sequence defines what each column in the `payloads` array represents using the **`attribute`** property:
* `value`: The actual meter reading number.
* `occurredAt`: The timestamp string representing exactly when a specific demand or reading occurred.
* `openingValue` / `closingValue`: To provide mathematical proofs for `USAGE` deltas.
* `validationStatus`: Standard validation flags (e.g. `ESTIMATED`, `VALID`).

Because `payloads` allows mixed arrays of `number` and `string`, metadata is mapped densely alongside values without needing sparse overrides.

### Strict Derived Profiles
Inside the array, individual profiles inherit strictly from `BaseProfile`. `BaseProfile` only contains identity (`meterRefs`, `customerRefs`, `serviceDeliveryPointRefs`). Derived profiles (like `IntervalProfile`) strictly allow **only** their relevant properties (`intervals`, `payloadDescriptorSetRef`, `intervalPeriod`).

> [!NOTE]
> **Why doesn't `MonthlyProfile` use the compact matrix?**
> The compact form is prevented natively by the schema for `MonthlyProfile`. It strictly requires `readings` and `touBuckets`, and does not permit `intervals`. The compact matrix shines for dense, highly symmetrical time-series data. A `MonthlyProfile` typically captures a single sparse snapshot of total registers, ToU buckets, and Maximum Demand peaks at the end of the month. Encoding sparse, highly variable metadata (e.g., MD timestamps) into a flat numerical array offers negligible compression and becomes extremely brittle when dealing with **ad-hoc billing resets** or **meter swaps mid-cycle**.
> 
> *See [MonthlyProfile_MultipleResets.json](./examples/MonthlyProfile_MultipleResets.json) and [Billing_MeterChange.json](./examples/Billing_MeterChange.json) for examples of how the elaborated representation cleanly handles these edge cases.*

---

## Identifier Flexibility (OBIS vs. Short Codes)

The schema relies on `OBISMapping.json` as the canonical registry for interpreting physical quantities. The exact mapping of OBIS codes to physical units, phases, and categories is defined in this file.

When transmitting telemetry, you specify a simple **`readingType`** string. This can be:
* **Using OBIS Codes**: `"1.0.1.8.0.255"`
* **Using Short Names**: `"kWh imp"`
* **Using Canonical Links**: Payload descriptors can optionally include an `obis` string parameter to provide a direct physical mapping when a short name is used as the `readingType`.

*See the [MultiMeterBulkDataset.json](./examples/MultiMeterBulkDataset.json) (OBIS Codes) and [MultiMeterBulkDatasetShortCodes.json](./examples/MultiMeterBulkDatasetShortCodes.json) (Short Codes) for bulk examples of both representations.*

---

## TelemetryMode (READING vs USAGE)

The schema natively distinguishes between raw register readings and calculated usage:
- **`READING`**: Represents the physical register value at a point in time. For cumulative registers, this strictly increases monotonically.
- **`USAGE`**: Represents the delta or consumed amount over a period. Demand registers inherently use `USAGE` mode. For energy, this represents the exact block consumption.

Modes are indicated per-descriptor or per-reading via the `reportedMode` property.

---

## Schema Generation and Compilation

The `schema.json`, `context.jsonld`, and `vocab.jsonld` files are compiled automatically from the core `attributes.yaml`.

### To Compile Schemas
To recompile schemas following modifications in `attributes.yaml`, run the following python scripts from the repository root:

```bash
python scripts/generate_schema_permissive.py schemas/MeterData/v0.6
```

---

## Telemetry Verification & Validation

Example JSON files are validated for structural compliance against `schema.json` and semantic compliance against `OBISMapping.json` using the v0.6 validator.

### To Validate Example Payloads
Run the following command from the `validation/` directory:

```bash
python validate_v06.py ../examples
```

The validator dynamically parses JSON files. If they are arrays containing a `PayloadDescriptorProfile`, it matches `payloadDescriptorSetRef` against the array's descriptors, and asserts both matrix arity and strict column types based on the `attribute` enum.
