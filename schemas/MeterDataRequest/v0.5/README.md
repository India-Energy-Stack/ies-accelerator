# MeterDataRequest Schema (v0.5)

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
   * List of specific profile types to include in the query result. Allowed types:
     * `CustomerProfile`
     * `IntervalProfile`
     * `DailyProfile`
     * `BillingProfile`
     * `InstantaneousProfile`
     * `EventProfile`

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
