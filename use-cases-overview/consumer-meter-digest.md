# Consumer Meter Digest

*A consumer's own meter readings, DISCOM-signed and packaged for sharing. The Digest is a [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) issued on consumer demand, holder-bound to their wallet (W3C Verifiable Credential), carrying readings for a specified period. A bank, installer or energy app verifies it offline instead of trusting an emailed PDF bill.*

**[Implementation Guide →](../use-cases/consumer-meter-digest/README.md)**

| Field | Value |
|---|---|
| Document | IES/CMD-PROFILE/0.6 |
| Status | Piloted (four pilot DISCOMs, completed 30-day DISCOM Challenge) — see [Status summary](../README.md) |
| Applicability | All distribution licensees |
| This version | Consumer Meter Digest *variant* of MeterDataCredential v0.6, holder-bound. Wraps [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) profiles. |

---

## 1. Scope and Purpose

The stakeholder is the consumer sharing verified consumption history with a bank, marketplace, energy app, housing society or installer, and the DISCOM that issues the digest. Today the consumer prints and emails PDF bills; verifiers can't confirm authenticity, so most call the DISCOM anyway.

This document defines the **Consumer Meter Digest** — a verifier-friendly, DISCOM-signed bundle of the consumer's telemetry. Not a new credential type: MeterDataCredential v0.6 is the schema, profiled for a consumer audience.

## 2. What It Records / Covers

| Records | Detail | Source |
|---|---|---|
| Meter & service-delivery point | `meterRefs` and the service-delivery-point reference | MeterDataCredential v0.6 wrapping MeterData v0.6 |
| Period | The window the readings cover | MeterData v0.6 |
| Readings | Profile-typed data (`intervals` for `INTERVAL`/`DAILY` cadence, `readings` for other profile types), discriminated by `profileType` | MeterData v0.6 (IS 15959 / DLMS-COSEM) |
| Data quality | Estimation flags, missing intervals | MeterData v0.6 |
| Issuer & proof | Issuing DISCOM (`did:web`) and cryptographic proof | MeterDataCredential v0.6 (W3C VC) |

Granularity: `DAILY`, `MONTHLY`, or `INTERVAL` (15-minute interval data expressed as `profileType: INTERVAL` with `intervalPeriod.duration: PT15M`). Typical max period: 24 months for `MONTHLY`, 90 days for 15-minute `INTERVAL` data.

## 3. How Each Item is Identified

Reuses the [Consumer Energy Passport](consumer-energy-passport.md#id-3.-how-each-item-is-identified) scheme:

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (issuer) | `did:web` on owned domain | `did:web:ies.discom.example` |
| Consumer (holder) | `did:key` (wallet) | `did:key:z6MkjVQ8r4f3rPuY…` |
| Meter | `did:web` under issuer domain | `did:web:ies.discom.example:assets:meter:NM-44091234` |

The meter identifier matches the one in the consumer's [Consumer Energy Passport](consumer-energy-passport.md) — a verifier sees the two as a coherent pair.

## 4. Definitions

- **Holder-bound** — `credentialSubject.id` set to the holder's wallet DID.
- **READING** — register value at a point in time; cumulative series must be non-decreasing.
- **USAGE** — delta / consumed amount over a period.
- **OBIS** — Object Identification System code (IEC 62056 / IS 15959) for a meter register.
- **Summary** — a derived aggregate computed from raw readings by downstream analytics; not itself a field defined by the MeterData v0.6 schema.

See **[IES Meter Data Model](../use-cases/smart-meter-data-exchange/ies-meter-data-model.md)** for the underlying meter-data terminology.

## 5. Basis of Standards

Fixed IES order of preference: **IS → CEA Regulations / IEGC → IEC → IEEE**.

| Standard | Role here |
|---|---|
| **IS 15959** | DLMS/COSEM; OBIS codes — metering reads |
| **IS 16444** | Smart meter specification |
| **W3C VC Data Model 2.0** | The credential envelope |

## 6. Where Indian Standards Do Not Yet Exist

The credential envelope (W3C VC) and the underlying compact-profile data model have no Indian equivalent; the MeterData v0.6 shapes are an IES specification on top of IEC 62056 / IS 15959.

## 7. The Record

One record: a Verifiable Credential wrapping a MeterData profile. Unlike the Passport, it's a **point-in-time snapshot** with a short `validUntil` (hours to days) — the consumer re-requests when fresh data is needed. Holder-bound; presentable to multiple verifiers within its validity window. Revocation rarely matters in practice, but the same DeDi-hash flow is available.

## 8. Schedule I — Static Fields of the Credential

Schedule I is the Consumer Meter Digest profile view over the real [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) wrapper and its embedded [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) payload. **Normative Path** names an actual path in those schemas. **Schema Requires** records schema-requiredness; **CMD Guidance** is informative profile guidance and does not add constraints to either schema. The complete field references remain canonical for fields not listed here.

### 8.1 Credential Envelope and Holder Binding

| **Normative Path** | **Type** | **Schema Requires** | **Standard** *(informative)* | **CMD Guidance** *(informative)* |
|---|---|---|---|---|
| `@context` | array of context URIs | Required by the externally referenced W3C Credential branch | W3C VC Data Model 2.0 | Include the W3C, EnergyCredential and MeterDataCredential contexts |
| `id` | credential URI / URN | Optional; permitted by the open credential envelope | W3C VC Data Model 2.0 | Unique per issued digest |
| `type` | array including `MeterDataCredential` | Required by the externally referenced W3C Credential branch | W3C VC Data Model 2.0 | Identify this credential family explicitly |
| `issuer` | issuer object | Optional at the EnergyCredential root; if present, `id`, `name` and `licenseNumber` are required | W3C VC; DID Core | Mandatory for this profile; use the DISCOM or authorised provider's registered `did:web` |
| `validFrom` / `validUntil` | date-time | Not required by the generated local wrapper schema | W3C VC Data Model 2.0 | Mandatory profile convention; use a short validity window appropriate to a point-in-time digest |
| `credentialStatus` | status object | Optional at the EnergyCredential root; if present, `id` and `type` are required | DeDi registry | Optional operational revocation/suspension reference |
| `proof` | proof object | Optional at the EnergyCredential root; required members apply if present | W3C VC Data Model 2.0 | Mandatory for an issued digest; sign the complete credential |
| `credentialSubject.id` | URI / DID | Optional when `credentialSubject` is present | DID Core | Mandatory for this holder-bound profile; use the consumer's verified holder identifier |
| `credentialSubject.meterData` | one MeterData profile or non-empty array of profiles | Required inside `credentialSubject`; the wrapper does not currently require `credentialSubject` itself | MeterData v0.6 | Mandatory; carry the descriptor plus the requested digest profiles when compact payloads are used |

Repository-local structural validation uses a permissive stub for the external EnergyCredential reference. Implementations must therefore enforce the envelope and CMD profile requirements above in addition to validating the embedded MeterData payload.

### 8.2 Digest Profiles and Time Windows

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **Standard** *(informative)* | **CMD Guidance** *(informative)* |
|---|---|---|---|---|
| `credentialSubject.meterData[].profileType` | `DESCRIPTOR` | Required on a descriptor profile | MeterData v0.6 | Include when another profile uses `payloadDescriptorSetRef` or compact `payloads[]` |
| `credentialSubject.meterData[].profileType` | `INTERVAL` | Required on an interval profile | IS 15959 / DLMS-COSEM | Use for 15- or 30-minute blocks; 15-minute cadence is `intervalPeriod.duration: PT15M` |
| `credentialSubject.meterData[].intervalPeriod.start` / `.duration` | date-time / ISO 8601 duration | Required on `INTERVAL` | ISO 8601 | Defines the first interval and cadence |
| `credentialSubject.meterData[].intervals[]` | interval objects | Optional in the schema | MeterData v0.6 | Populate for compact interval delivery; each `intervals[].id` is required and strictly increases within the profile |
| `credentialSubject.meterData[].profileType` | `DAILY` | Required on a daily profile | IS 15959 / DLMS-COSEM | Use for daily digest records |
| `credentialSubject.meterData[].intervalPeriod.start` / `.duration` | date-time / ISO 8601 duration | Required on `DAILY` | ISO 8601 | Use the requested daily window and cadence |
| `credentialSubject.meterData[].profileType` | `MONTHLY` | Required on a monthly profile | IS 15959 / DLMS-COSEM | Use for billing-cycle or multi-month history |
| `credentialSubject.meterData[].timePeriod.start` / `.duration` | date-time / ISO 8601 duration | Required on `MONTHLY` | ISO 8601 | Defines the month or billing period represented |
| `credentialSubject.meterData[].readings[]` | array of `Reading` | Required on `MONTHLY`; optional on `INTERVAL` / `DAILY` | MeterData v0.6 | Use explicit readings where the compact descriptor/sequence form is not used |
| `credentialSubject.meterData[].touBuckets[]` | time-of-use buckets | Optional on `MONTHLY` | SERC tariff order; MeterData v0.6 | Populate only when the requested digest includes ToU segmentation |

### 8.3 Meter and Descriptor Fields

The identity of the metering point and the dictionary that gives the readings meaning. Both are fixed for the digest; the readings themselves are in [Schedule II](#id-9.-schedule-ii-meter-readings-live-record).

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **Standard** *(informative)* | **CMD Guidance** *(informative)* |
|---|---|---|---|---|
| `meterRefs[]` | `Identifier` `{scheme, value, namespace?}` | Required on every telemetry profile | IS 16444; IES identifiers | Point to the same meter used by the Consumer Energy Passport |
| `serviceDeliveryPointRefs[]` | list of `Identifier` | Optional | CIM (IEC 61968-9) | Include when the verifier must bind the reading to a service point |
| `customerRefs[]` | list of `Identifier` | Optional | CIM (IEC 61968-9) | Minimise disclosure; the holder binding may be sufficient |
| `payloadDescriptorSetRef` / `compactSequenceRef` | text references | Optional | MeterData v0.6 | References must resolve to the accompanying `DESCRIPTOR` profile when compact payloads are used |
| `payloadDescriptorSets[].payloadDescriptors[].readingType` | text / governed short code | Required per descriptor | IS 15959 / OBIS | Declare every reading type carried by the compact sequence |
| `payloadDescriptors[].obis` / `.unit` / `.reportedMode` | OBIS text / unit enum / `READING` or `USAGE` | Optional | IEC 62056; IS 15959 | Use canonical OBIS and mode metadata where available |

## 9. Schedule II — Meter Readings (Live Record)

Schedule II is the **live half** of the digest — the measured values themselves. They are the reason the credential exists; everything in Schedule I describes which meter they came from, over what window, and under whose binding.

A digest is a *snapshot*: once issued, the readings inside one credential no longer change. The fields are still live-class — a new reading arrives every block at the meter — and a later digest carries later values.

### 9.1 Reading and Quality Fields

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **Standard** *(informative)* | **CMD Guidance** *(informative)* |
|---|---|---|---|---|
| `readings[].readingType` / `.value` | text / number | Both required per reading | IS 15959 / OBIS | Use the descriptor set's canonical reading type |
| `readings[].openingValue` / `.closingValue` | number | Optional; semantic rules apply to `USAGE` | MeterData v0.6 | Include together when the digest needs auditable block-delta arithmetic |
| `readings[].occurredAt` / `.timePeriod` | date-time / period object | Optional | ISO 8601 | Use the field appropriate to point-in-time or period data |
| `readings[].validationStatus` | `VALID`, `ESTIMATED`, `MANUAL`, `SUSPECT`, `REJECTED` | Optional | MeterData v0.6 | Populate so the verifier can distinguish measured and estimated values |
| `readings[].source` | `METER`, `HES`, `ESTIMATED`, `MANUAL`, `IMPORT`, `MDM_COMPUTED`, `CIS_COMPUTED` | Optional | MeterData v0.6 | Populate when provenance affects verifier decisions |

## 10. How It Fits Together

```
Consumer (wallet)                     DISCOM
  │── request via DigiLocker /  ────>│ verify entitlement (Passport)
  │   consented app                  │ pull readings from MDM
  │                                  │ build MeterData/v0.6 payload
  │                                  │ wrap: credentialSubject.id = wallet DID
  │<── signed Digest ────────────────│  validUntil = 24h–7d
  │
  │── present Digest ───> Verifier (offline verify)
```

## 11. Points for Confirmation

1. **Maximum-range policy** by granularity — to be tightened per use case.
2. **Summary-derivation formula** for any downstream analytics built on these readings, especially ToD bucket boundaries (may vary by SERC) — out of scope for the credential schema itself.
3. **Latency budget** — MDM read-path performance is the binding constraint.

---

## Schemas Used in This Use Case

Holder-bound issuance of **[MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6)**, wrapping a **[MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6)** payload. Entitlement is typically proven by a [Consumer Energy Passport](consumer-energy-passport.md).

## Value Unlock

The consumer proves actual consumption history, DISCOM-signed, verifiable without a callback. The DISCOM cuts bill-verification calls and gains a clean, consented data-sharing surface — a higher-trust input than emailed PDF bills.

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 15959 (Parts 1–3) | DLMS/COSEM companion spec; OBIS codes |
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IEC 62056 | DLMS/COSEM; OBIS |
| IEC 61968-9 | CIM — meter reading and control |
| W3C VC Data Model 2.0; W3C DID Core | Credential envelope; identifiers |
| RFC 3339 / ISO 8601 | Date-time format for `intervalPeriod` / `timePeriod` |

## Annexure B — Example Payload

- **[`example-customer-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-customer-profile.json)**
- **[`example-interval-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-interval-profile.json)**
- **[`example-monthly-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-monthly-profile.json)**

## Annexure C — JSON Schema

Canonical: `https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/` — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/schema.json), [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/context.jsonld), [`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/vocab.jsonld). The payload schema: [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6).

## Annexure D — Derived Views

Computed downstream by the recipient from the Schedules above. None is a field of MeterDataCredential v0.6, and none is exchanged.

| **Derived View** | **Source** | **Schema Status** | **Treatment** |
|---|---|---|---|
| Period total | `readings[]` or compact `intervals[].payloads[]` for the requested window | Not a MeterDataCredential / MeterData v0.6 field | Compute downstream and label the method and source period |
| Peak demand | Demand readings plus `occurredAt` / interval position | Not a schema field | Compute downstream; retain the source reading and timestamp for audit |
| Time-of-use breakdown | `touBuckets[]` or interval readings joined to tariff periods | `touBuckets[]` is native for `MONTHLY`; a rendered summary is derived | Keep native buckets in the signed payload; render labels and totals downstream |
| Missing-interval count | Expected cadence versus received interval IDs | Not a schema field | Compute downstream; do not insert a synthetic `dataQuality` object into the credential |
| Verifier-facing PDF / dashboard | Any of the above | Presentation only | May accompany the credential, but the signed JSON remains the authoritative record |
