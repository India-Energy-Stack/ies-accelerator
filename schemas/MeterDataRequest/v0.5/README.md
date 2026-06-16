> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.5/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.5/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.5/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.5/vocab.jsonld) · [examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterDataRequest/v0.5/examples)

# MeterDataRequest Schema (v0.5)

The smart meter telemetry data defined in [MeterData (v0.6)](../../MeterData/v0.6) is complemented with the `MeterDataRequest` schema – specifying **what meters**, **what data**, and **for how long** the query or permission spans.

This directory houses the **`MeterDataRequest` (v0.5)** schema for the India Energy Stack. This schema defines structural parameters for selecting and querying smart meter telemetry and profiles.

## Schema Overview

The `MeterDataRequest` schema allows a Data Consumer (BAP) to request precise datasets from a Data Provider (BPP) by specifying query boundaries, scopes, and target profiles.

### Fields and Definitions

1. **`resources`** (Required, array of URIs/strings):
   * List of target resource identifiers to query (e.g., meter DIDs like `did:dedi:ies:meter:IN-MH-MTR-89721`, service point IDs, or customer IDs).
2. **`scope`** (Required, string enum):
   * Defines the hierarchical scope of the query relative to the target resources:
     * `ResourceOnly`: Returns data matching the exact resource only.
     * `ResourceAndChildren`: Returns data for the resource and all its sub-elements/nested devices.
     * `ChildrenOnly`: Returns data exclusively for the children/sub-elements of the target resource.
3. **`from`** (Required, string date-time):
   * ISO 8601 UTC date-time indicating the start time of the requested data window (e.g., `2026-05-18T00:00:00Z`).
4. **`duration`** (Required, string duration):
   * ISO 8601 duration string representing the length of the requested data window (e.g., `PT15M`, `P1D`, `P30D`).
5. **`maxRecordsShared`** (Optional, integer):
   * Maximum number of records that should be shared or returned in a single batch/page. Must be $\ge 1$.
6. **`includeDetails`** (Optional, array of objects):
   * List of `ProfileRequest` objects to define exactly what telemetry is needed.
   * **`profileType`**: String identifying the target profile (e.g. `CustomerProfile`, `IntervalProfile`, `DailyProfile`, `MonthlyProfile`, `BillDetails`, `InstantaneousProfile`, `EventProfile`, `AlarmProfile`).
   * **`values`**: Optional list of short codes or OBIS codes requested.
   * **`requestedMode`**: Optional `TelemetryMode` (`READING` or `USAGE`). If omitted, uses the default mode for the requested value.

---

## Examples of Usage

To avoid clutter and maintain 100% compliance audits, the usage examples for this schema are saved as standalone JSON files in the `examples/` directory:

### 1. Embedded in a Credential (DISCOM-to-TSP Data Sharing Allowance)
* **Goal**: A DISCOM grants permission to a Third Party Service Provider (TSP) to access smart meter telemetry on behalf of a consumer, restricted to **only interval (block load survey) data** for **all child meters** under a specific feeder (`did:dedi:ies:feeder:IN-MH-FDR-101`).
* **Implementation**: The credential embeds a `MeterDataRequest` object defining the allowed query boundaries.
* **Telemetry Query Profile**: [MeterDataRequest_FeederAllowance.json](./examples/MeterDataRequest_FeederAllowance.json)

### 2. Provider Capabilities (Advertised Capability Profiles)
Data providers advertise what subset of profile queries they support relative to specific electrical hierarchy nodes:
* **MDM (Meter Data Management System) Capability**: Hosts raw meter readings (Interval, Daily, Instantaneous, Event, and Alarm profiles) for all target substations and their child elements.
  * **Capability Profile**: [MeterDataRequest_MDM_Capability.json](./examples/MeterDataRequest_MDM_Capability.json)
* **Billing System Capability**: Hosts customer profile metadata and detailed invoice/prepayment records.
  * **Capability Profile**: [MeterDataRequest_Billing_Capability.json](./examples/MeterDataRequest_Billing_Capability.json)

### 3. Requesting Data (As a Query Filter)
* **Goal**: An authorized application requests the exact telemetry dataset needed to compile a **Meter Digest Credential** for a single customer (querying the customer profile, billing details, monthly registers, and daily summaries for the last 30 days).
* **Telemetry Query Filter**: [MeterDataRequest_DigestCredentialFilter.json](./examples/MeterDataRequest_DigestCredentialFilter.json)
* **Standard Query Filter**: [MeterDataRequest_Example.json](./examples/MeterDataRequest_Example.json)

---

## Build and Compilation

The JSON Schema, JSON-LD Context, and RDF Vocabulary are automatically compiled from `attributes.yaml` using our Python automation script:

```bash
# From the repository root
python scripts/generate_schema.py schemas/MeterDataRequest/v0.5
```

This compiles:
* `schema.json`: Standard JSON Schema (Draft 2020-12)
* `context.jsonld`: Linked Data context file mapping attributes to `ies:` terms
* `vocab.jsonld`: Ontological vocabulary definition file

---

## Verification and Validation

All JSON example queries located under the `examples/` directory are verified against the compiled Draft 2020-12 schema using our validator utility:

```bash
# Run validation check
python scripts/validate_schema.py schemas/MeterDataRequest/v0.5/schema.json schemas/MeterDataRequest/v0.5/examples
```
