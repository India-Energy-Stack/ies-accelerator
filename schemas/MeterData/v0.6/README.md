# Meter Data Compact Profiles (v0.6)

This directory contains the **Meter Data Compact Profiles** (v0.6) schema definitions and semantic models for telemetry data exchange. It is tailored for high-efficiency, data-only transmissions of smart meter readings and events, omitting the heavy cryptographic wrapping when only raw telemetry payload is being exchanged.

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
python scripts/generate_schema_permissive.py schemas/MeterData/v0.6
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

## Example Payloads and Scenarios
This directory includes standard example payloads representing different profiles and encoding formats:
* [CustomerProfile.json](./examples/CustomerProfile.json): Slow-changing customer metadata, service points, and meter installations.
* [IntervalProfile.json](./examples/IntervalProfile.json): Block load survey telemetry represented in compact Form B (matrix with overrides) using short codes.
* [DailyProfile.json](./examples/DailyProfile.json): Daily accumulated active and reactive energy registers represented in compact Form B using short codes.
* [MonthlyProfile.json](./examples/MonthlyProfile.json): Monthly physical register reset cumulative readings and Time-of-Use (ToU) buckets represented in Form A using short codes.
* [BillDetails.json](./examples/BillDetails.json): Computed out-of-band billing details including invoice amount due, currency, and prepayment balance.
* [InstantaneousProfile.json](./examples/InstantaneousProfile.json): Real-time snapshot of electrical quantities (voltages, currents, power factors) represented in Form A using short codes.
* [EventProfile.json](./examples/EventProfile.json): Tamper logs and diagnostic event history mapped to standard IS 15959 event records.
* [AlarmProfile.json](./examples/AlarmProfile.json): Immediate, active meter alarm conditions (e.g. cover open, neutral disturbance, voltage sag).
* [AggregatedFeeder.json](./examples/AggregatedFeeder.json): Feeder-level summary readings represented in Form A using short codes.
* [MultiMeterBulkDataset.json](./examples/MultiMeterBulkDataset.json): Bulk smart meter telemetry data for multiple meters using exact OBIS codes.
* [MultiMeterBulkDatasetShortCodes.json](./examples/MultiMeterBulkDatasetShortCodes.json): Bulk smart meter telemetry data for multiple meters using human-readable short codes.

---

## OBIS Mapping and Identifiers

The `MeterData` schema relies on flexible identifiers to reference physical quantities. The exact mapping of OBIS codes to physical units, phases, and categories is defined in the [OBISMapping.json](./OBISMapping.json) file.

### Interpreting OBISMapping.json
The `OBISMapping` file serves as the canonical dictionary for interpreting IS 15959 standard meter registers. It contains both OBIS codes and detailed event taxonomies.

**Snapshot:**
```json
{
  "obis": "1.0.1.8.0.255",
  "name": "Active energy import - cumulative (kWh)",
  "shortLabel": "kWh imp",
  "unit": "kWh",
  "flowDirection": "IMPORT",
  "accumulationBehaviour": "CUMULATIVE",
  "category": "energyCumulative",
  "meterCategories": ["A", "B", "C", "D1", "D2", "D3", "D4"],
  "profiles": ["DAILY", "MONTHLY"],
  "source": "IS 15959 Part 1 Table 22; Part 2 Table A14; Part 3 Table 1"
}
```

### Identifier Flexibility (OBIS vs. Short Names)
When structuring your payload descriptors or values, you have the flexibility to use either exact OBIS codes or human-readable short names.

* **Using OBIS Codes**: `{"scheme": "OBIS", "value": "1.0.1.8.0.255"}`
* **Using Short Names**: `{"scheme": "SHORT_CODE", "value": "kWh imp"}`

*See the [MultiMeterBulkDataset.json](./examples/MultiMeterBulkDataset.json) (OBIS Codes) and [MultiMeterBulkDatasetShortCodes.json](./examples/MultiMeterBulkDatasetShortCodes.json) (Short Codes) for bulk examples of both representations.*

---

## Payload Shapes and Value Representation

The schema offers two distinct mechanisms for representing telemetry values, balancing explicit clarity with high-efficiency transmission.

### 1. Form A: Elaborated Representation (`readings` / `touBuckets`)
Telemetry is presented as an array of discrete `Reading` objects containing inline values, timestamps, and register details. Physical units and phases are resolved out-of-band via short codes (or OBIS codes).

```json
"readings": [
  {
    "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp" },
    "value": 412.5,
    "openingValue": 18432.5,
    "closingValue": 18845.0
  }
]
```

### 2. Form B: Compact Matrix Representation (`intervals`)
Used heavily for dense time-series telemetry. Descriptors are declared once at the block level in `payloadDescriptorSet`, and time-series data is transmitted as simple arrays of numbers (`Interval`) that map positionally to the descriptors defined in a `CompactSequence`.

```json
  "payloadDescriptorSet": {
    "name": "DailyLoadSurveySet",
    "payloadDescriptors": [
      {
        "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp" },
        "reportedMode": "READING",
        "powerOfTenMultiplier": 0
      }
    ],
    "compactSequences": [
      {
        "name": "DailyEnergySeq",
        "sequenceItems": [
          {
            "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp" },
            "reportedMode": "READING"
          }
        ]
      }
    ]
  },
  "compactSequenceRef": "DailyEnergySeq",
  "intervalPeriod": { "start": "2026-05-18T10:00:00+05:30", "duration": "PT30M" },
  "intervals": [
    { "id": 0, "payloads": [600] },
    { "id": 1, "payloads": [580] }
  ]
```

---

## TelemetryMode (READING vs USAGE)

The schema natively supports distinguishing between raw register readings and calculated usage:
- **`READING`**: Represents the physical register value at a point in time. For cumulative registers, this strictly increases monotonically.
- **`USAGE`**: Represents the delta or consumed amount over a period. 
  - For `USAGE` values, an optional `openingValue` and `closingValue` can be provided for transparent mathematical proof (e.g. `value == closingValue - openingValue`).
  - Demand registers (e.g., kW) inherently use `USAGE` mode.

Modes are indicated per-descriptor or per-reading via the `reportedMode` property. Valid fallback and support behaviors for specific OBIS codes are declared in the `OBISMapping.json` file via `supportedModes` and `defaultMode`.

---

## Data Annotations

The schema supports sparse annotations to add metadata exactly where needed without bloating the compact matrix payload.

### Sparse Cell Overrides
By default, all readings are assumed to be `{VALID, METER}`. If a specific interval was estimated or has a specific occurred timestamp, you can inject a sparse `Override` in the array (if supported by your specific payload model extension). *(Note: Base schema v0.6 moves towards explicit modes rather than generic overrides for demand)*.
*See [`MultiMeterBulkDatasetShortCodes.json`](./examples/MultiMeterBulkDatasetShortCodes.json) (Short Codes) or [`MultiMeterBulkDataset.json`](./examples/MultiMeterBulkDataset.json) (OBIS Codes) for full examples of sparse overrides.*

### Maximum Demand snapshoting
When transmitting Maximum Demand snapshot aggregates in Elaborated form (e.g. inside a [`MonthlyProfile`](./examples/MonthlyProfile.json)), the exact timestamp of the peak is annotated using the `occurredAt` property.

```json
{
  "readingTypeRef": { "scheme": "SHORT_CODE", "value": "MD kW" },
  "value": 15.2,
  "occurredAt": "2026-05-18T14:30:00+05:30",
  "integrationPeriod": "PT30M"
}
```
