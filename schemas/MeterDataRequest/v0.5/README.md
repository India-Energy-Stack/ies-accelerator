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
6. **`includeDetails`** (Optional, array of strings):
   * List of specific profile types to include in the query result. Allowed types (corresponding to [MeterData (v0.6)](../../MeterData/v0.6) profiles):
     * `CustomerProfile`
     * `IntervalProfile`
     * `DailyProfile`
     * `MonthlyProfile`
     * `BillDetails`
     * `InstantaneousProfile`
     * `EventProfile`
     * `AlarmProfile`

---

## Examples of Usage

### 1. Embedded in a Credential (DISCOM-to-TSP Data Sharing Allowance)
When a DISCOM grants permission to a Third Party Service Provider (TSP) to access telemetry on behalf of a consumer, the DISCOM issues a Verifiable Credential containing the `MeterDataRequest` query parameters as the allowed access boundary.

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterDataRequest/v0.5/context.jsonld"
  ],
  "id": "urn:uuid:e5f6a7b8-9012-34ab-cdef-567890123456",
  "type": ["VerifiableCredential", "MeterDataAllowanceCredential"],
  "issuer": "did:web:discom.example.com",
  "validFrom": "2026-05-22T12:00:00Z",
  "credentialSubject": {
    "id": "did:web:tsp.example.com",
    "allowedMeterDataRequest": {
      "resources": ["did:dedi:ies:meter:IN-MH-MTR-89721"],
      "scope": "ResourceOnly",
      "from": "2026-05-01T00:00:00Z",
      "duration": "P30D",
      "includeDetails": ["IntervalProfile", "DailyProfile"]
    }
  }
}
```

### 2. Provider Capabilities (Advertised Capability Profiles)
Data providers (e.g. an MDM system or a Customer Information/Billing system) use the `includeDetails` array to advertise what profiles they host.

#### MDM (Meter Data Management) Capability:
An MDM typically handles high-frequency interval load surveys, instant electrical quantities, and diagnostic logs.
```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterDataRequest/v0.5/context.jsonld",
  "@type": "MeterDataRequest",
  "resources": ["did:dedi:ies:meter:IN-MH-MTR-89721"],
  "scope": "ResourceOnly",
  "from": "2020-01-01T00:00:00Z",
  "duration": "P10Y",
  "includeDetails": [
    "IntervalProfile",
    "DailyProfile",
    "InstantaneousProfile",
    "AlarmProfile",
    "EventProfile"
  ]
}
```

#### Billing System Capability:
A billing system hosts computed financial parameters, billing registers, and invoice records.
```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterDataRequest/v0.5/context.jsonld",
  "@type": "MeterDataRequest",
  "resources": ["did:dedi:ies:meter:IN-MH-MTR-89721"],
  "scope": "ResourceOnly",
  "from": "2020-01-01T00:00:00Z",
  "duration": "P10Y",
  "includeDetails": [
    "MonthlyProfile",
    "BillDetails"
  ]
}
```

### 3. Requesting Data (As a Query Filter)
Consumers or authorized clients submit a `MeterDataRequest` directly inside their query payloads to filter for specific telemetry windows and profiles.

```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterDataRequest/v0.5/context.jsonld",
  "@type": "MeterDataRequest",
  "resources": ["did:dedi:ies:meter:IN-MH-MTR-89721"],
  "scope": "ResourceOnly",
  "from": "2026-05-18T00:00:00Z",
  "duration": "P1D",
  "maxRecordsShared": 100,
  "includeDetails": [
    "IntervalProfile"
  ]
}
```

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
