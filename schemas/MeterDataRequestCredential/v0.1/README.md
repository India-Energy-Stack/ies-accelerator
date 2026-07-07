> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequestCredential/v0.1/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequestCredential/v0.1/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequestCredential/v0.1/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequestCredential/v0.1/vocab.jsonld) · [examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterDataRequestCredential/v0.1/examples)

# MeterDataRequestCredential v0.1

A **W3C Verifiable Credential (VC Data Model 2.0)** that wraps a [`MeterDataRequest`](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6) to prove a data requester's authorisation for accessing smart meter telemetry.

---

## Purpose

In a Beckn data-exchange flow, a **seeker** (e.g., DISCOM) discovers an AMI dataset offered by a **provider** (e.g., AMISP). The provider's offer policy requires the seeker to attach a `MeterDataRequestCredential` at `confirm` time. This credential:

1. **Identifies** the requesting entity (DID + regulatory licence number).
2. **Scopes** the request — which meters/feeders, what hierarchy, what time window, which profile types.
3. **Is cryptographically signed**, so the provider can verify it without a round-trip to the issuer.
4. **Can be revoked** via the DeDi registry if authorisation is withdrawn.

The provider checks: credential type is `MeterDataRequestCredential`, `validUntil` has not passed, status is not revoked, and the embedded `MeterDataRequest.resources` are within the contracted scope.

---

## Inheritance

`MeterDataRequestCredential` is a **subclass of [`EnergyCredential v2.0`](https://schema.beckn.io/EnergyCredential/v2.0)** (defined in the [DEG specification](https://github.com/beckn/DEG)):

```
beckn:Credential
  └── EnergyCredential (https://schema.beckn.io/EnergyCredential/v2.0)
        └── MeterDataRequestCredential
```

The common VC envelope is **inherited, not duplicated**:

| Inherited from EnergyCredential | Defined here |
|---|---|
| `issuer` (id, name, `licenseNumber`) | `credentialSubject.meterDataRequest` |
| `validFrom` / `validUntil` | `MeterDataRequestCredential` type |
| `credentialStatus` (DeDi registry) | |
| `proof` (Ed25519Signature2020) | |

In `attributes.yaml` this is expressed as `allOf: - $ref: https://schema.beckn.io/EnergyCredential/v2.0`, matching the same pattern used by `ConsumptionProfileCredential`, `GenerationProfileCredential`, and other DEG energy credentials.

The `@context` of a credential instance must include:
1. `https://www.w3.org/ns/credentials/v2`
2. `https://schema.beckn.io/EnergyCredential/v2.0/context.jsonld`
3. `https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequestCredential/v0.1/context.jsonld`

---

## Schema Files

| File | Purpose |
|---|---|
| `attributes.yaml` | OpenAPI 3.1.1 source of truth with `x-jsonld` annotations |
| `schema.json` | JSON Schema Draft 2020-12 for validation |
| `context.jsonld` | JSON-LD context (semantic term mappings) |
| `vocab.jsonld` | RDF vocabulary / ontology definitions |
| `examples/example.json` | Complete W3C VC 2.0 example |

---

## Credential Structure

```
MeterDataRequestCredential (W3C VC 2.0)
├── @context        — W3C credentials/v2 + IES MeterDataRequestCredential context
├── id              — urn:uuid:...
├── type            — ["VerifiableCredential", "MeterDataRequestCredential"]
├── issuer
│   ├── id          — DID of the requesting entity (e.g., DISCOM)
│   ├── name        — Human-readable name
│   └── licenseNumber — Regulatory licence (e.g., SERC-DISCOM-2025-001)
├── validFrom       — Issuance datetime
├── validUntil      — Expiry (short window, e.g., 30 days)
├── credentialStatus — DeDi revocation registry reference
├── credentialSubject
│   ├── id          — DID of the requesting entity
│   └── meterDataRequest (MeterDataRequest v0.6)
│       ├── consumers      — Optional list of consumer DIDs
│       ├── resources      — Optional list of meter/feeder DIDs to query
│       ├── scope          — ResourceOnly | ResourceAndChildren | ChildrenOnly
│       ├── from           — Start of data window (ISO 8601 UTC)
│       ├── duration       — Length of data window (ISO 8601 duration)
│       ├── consumerConsent — Optional list of consumer consent DIDs
│       ├── authorisation  — Reference or inline authorisation grant
│       ├── capabilitiesRequested — The requested capabilities (MeterDataCapabilities)
│       └── maxRecordsShared — Optional cap on returned records
└── proof           — Ed25519Signature2020 (or equivalent)
```

---

## Usage in Beckn Data Exchange (UC1)

### Provider side — `catalog/publish`

The provider advertises:
1. **`ies:dataSchema`** in `resourceAttributes` — URL to the MeterData v0.6 schema used for response payloads.
2. **`ies:capabilityProfile`** in `resourceAttributes` — a `MeterDataRequest` object describing the maximum scope the provider can serve (think of it as the provider's data-access envelope).
3. **`offerAttributes.policy.requiredCredentials`** — declares that a valid `MeterDataRequestCredential` must be attached at `confirm`.

### Seeker side — `confirm`

The seeker includes the signed credential in `commitmentAttributes.ies:meterDataRequest`. The embedded `MeterDataRequest` must be a subset of the provider's `capabilityProfile`.

### Provider side — `on_status`

The response `dataPayload` contains **IES MeterData v0.6** profile objects (e.g., `IntervalProfile`, `CustomerProfile`) — the schema advertised in `ies:dataSchema`.

---

## Example

See [`examples/example.json`](examples/example.json) for a complete W3C VC 2.0 instance where the DISCOM requests Q1 2026 interval + daily + monthly data for all meters under feeder `IN-KA-BLR-ZONE-A`.

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| v0.1 | 2026-05-26 | Initial draft |


---

<!-- FIELD-TABLE:START — auto-generated by scripts/generate_field_tables.py from schema.json; do not edit by hand -->
## Field reference

_Auto-generated from `schema.json`. A field name in **bold** with a trailing **\*** is required; all others are optional. **Type** shows units for QuantitativeValue models. Where a field is derived from a standard, its description begins with **Based on** and the standard reference (from the field's `x-standard` annotation). One table per object._

### MeterDataRequestCredential

| Field | Type | Description |
|----|-------|-----------------|
| `credentialSubject` | MeterDataRequestCredentialSubject | The subject of the credential: the requesting entity and the specific MeterDataRequest they are authorised to make. |

### MeterDataRequestCredentialSubject

| Field | Type | Description |
|----|-------|-----------------|
| `id` | uri | DID of the requesting entity (e.g., the DISCOM). |
| **`meterDataRequest`** \* | schema.json | The scoped, time-bounded data request. Specifies the meter resources, hierarchical scope, time window, and profile types being requested. The provider validates this against its capability profile before fulfilling delivery. |

<!-- FIELD-TABLE:END -->
