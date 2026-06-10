> **Files** — [attributes.yaml](./attributes.yaml) · [schema.json](./schema.json) · [context.jsonld](./context.jsonld) · [vocab.jsonld](./vocab.jsonld) · [examples/](./examples)

# MeterDataCredential v0.6

A **W3C Verifiable Credential (VC Data Model 2.0)** that wraps a [`MeterData v0.6`](../../MeterData/v0.6/) payload to attest the authenticity and provenance of delivered smart meter telemetry.

---

## Purpose

In a Beckn data-exchange flow, a **provider** (e.g., AMISP, MDM system) responds to a confirmed `MeterDataRequest` with an `on_status` message. The provider wraps the telemetry payload in a `MeterDataCredential` so that:

1. **Identity is bound** — the data is cryptographically tied to the issuing provider's DID.
2. **Provenance is verifiable** — any downstream system can verify who delivered the data and when.
3. **Tamper-evidence** — the payload cannot be altered without invalidating the signature.
4. **Revocation is supported** — the DeDi registry allows the provider to invalidate a credential if data is recalled (e.g., due to meter fault or privacy request).

The receiver checks: credential type is `MeterDataCredential`, `validUntil` has not passed, status is not revoked, and the embedded `meterData` profiles are within the contracted scope of the originating `MeterDataRequest`.

---

## Inheritance

`MeterDataCredential` is a **subclass of [`EnergyCredential v2.0`](https://schema.beckn.io/EnergyCredential/v2.0)** (defined in the [DEG specification](https://github.com/beckn/DEG)):

```
beckn:Credential
  └── EnergyCredential (https://schema.beckn.io/EnergyCredential/v2.0)
        └── MeterDataCredential
```

The common VC envelope is **inherited, not duplicated**:

| Inherited from EnergyCredential | Defined here |
|---|---|
| `issuer` (id, name, `licenseNumber`) | `credentialSubject.meterData` |
| `validFrom` / `validUntil` | `MeterDataCredential` type |
| `credentialStatus` (DeDi registry) | |
| `proof` (Ed25519Signature2020) | |

In `attributes.yaml` this is expressed as `allOf: - $ref: https://schema.beckn.io/EnergyCredential/v2.0`, matching the same pattern used by `MeterDataRequestCredential`, `ConsumptionProfileCredential`, and other DEG energy credentials.

The `@context` of a credential instance must include:
1. `https://www.w3.org/ns/credentials/v2`
2. `https://schema.beckn.io/EnergyCredential/v2.0/context.jsonld`
3. `https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterDataCredential/v0.6/context.jsonld`

---

## Schema Files

| File | Purpose |
|---|---|
| `attributes.yaml` | OpenAPI 3.1.1 source of truth with `x-jsonld` annotations |
| `schema.json` | JSON Schema Draft 2020-12 for validation |
| `context.jsonld` | JSON-LD context (semantic term mappings) |
| `vocab.jsonld` | RDF vocabulary / ontology definitions |
| `examples/example-customer-profile.json` | VC wrapping a single CustomerProfile |
| `examples/example-interval-profile.json` | VC wrapping a PayloadDescriptorProfile + IntervalProfile array |
| `examples/example-monthly-profile.json` | VC wrapping a MonthlyProfile with ToU buckets |

---

## Credential Structure

```
MeterDataCredential (W3C VC 2.0)
├── @context        — W3C credentials/v2 + EnergyCredential + MeterDataCredential context
├── id              — urn:uuid:...
├── type            — ["VerifiableCredential", "MeterDataCredential"]
├── issuer
│   ├── id          — DID of the data provider (AMISP, MDM, DISCOM)
│   ├── name        — Human-readable name
│   └── licenseNumber — Regulatory licence (e.g., KERC-AMISP-2025-007)
├── validFrom       — Issuance datetime
├── validUntil      — Expiry (typically 1 year)
├── credentialStatus — DeDi revocation registry reference
├── credentialSubject
│   ├── id          — DID of the consumer or asset entity
│   └── meterData   — MeterData v0.6 payload
│       ├── (single profile)  — one of CUSTOMER / INTERVAL / DAILY / MONTHLY /
│       │                        BILL_DETAILS / INSTANTANEOUS / EVENT / ALARM / DESCRIPTOR
│       └── (array of profiles) — mixed profile types, typically starting with DESCRIPTOR
└── proof           — Ed25519Signature2020 (or equivalent)
```

---

## meterData payload shapes

The `meterData` value follows the `MeterData v0.6` schema — either a **single** `EnergyData` profile object or an **array** of profile objects. All standard profile types are supported:

| `profileType` | Description |
|---|---|
| `CUSTOMER` | Slow-changing customer + service-point + meter-list summary |
| `INTERVAL` | Block Load Survey — PT15M / PT30M cadence interval blocks |
| `DAILY` | Daily Load Profile — P1D interval blocks |
| `MONTHLY` | Monthly billing readings (with optional ToU buckets) |
| `BILL_DETAILS` | Computed billing amount, bill number, due dates |
| `INSTANTANEOUS` | Snapshot of electrical quantities at one moment |
| `EVENT` | IS 15959 event log over a time period |
| `ALARM` | Real-time active alarm indicators |
| `DESCRIPTOR` | PayloadDescriptor sets (exchanged before or alongside compact interval data) |

Arrays typically start with a `DESCRIPTOR` profile followed by one or more data profiles that reference it via `payloadDescriptorSetRef`.

---

## Relationship to MeterDataRequestCredential

`MeterDataCredential` is the **response** counterpart to [`MeterDataRequestCredential`](../../MeterDataRequestCredential/v0.1/):

| | `MeterDataRequestCredential` | `MeterDataCredential` |
|---|---|---|
| Issued by | Requester (DISCOM) | Provider (AMISP / MDM) |
| Wraps | `MeterDataRequest` | `MeterData` payload |
| Used in | `confirm` — proves authorisation to request | `on_status` — attests delivered data |
| Subject | Requesting entity DID | Consumer / asset DID |

---

## Usage in Beckn Data Exchange (UC1)

### Provider side — `on_status`

The provider delivers the telemetry as a `MeterDataCredential` in `dataPayload`. The embedded `meterData` must cover the profile types and time window originally requested in the `MeterDataRequest`.

### Receiver side — verification

1. Resolve the issuer DID and retrieve the public key at `verificationMethod`.
2. Verify the `proof` signature over the canonical serialisation of the credential.
3. Check `validUntil` has not passed and `credentialStatus` is not revoked via the DeDi registry.
4. Validate `meterData` against the [MeterData v0.6 schema](../../MeterData/v0.6/schema.json).

---

## Examples

| File | Description |
|---|---|
| [`example-customer-profile.json`](./examples/example-customer-profile.json) | BESCOM AMISP attests CustomerProfile for consumer `RR-1234` |
| [`example-interval-profile.json`](./examples/example-interval-profile.json) | BESCOM AMISP attests PT15M interval data (with PayloadDescriptor) |
| [`example-monthly-profile.json`](./examples/example-monthly-profile.json) | BESCOM AMISP attests January 2026 monthly readings with ToU buckets |

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| v0.6 | 2026-06-06 | Initial draft — aligns with MeterData v0.6 |
