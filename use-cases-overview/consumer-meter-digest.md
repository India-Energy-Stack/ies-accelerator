# Consumer Meter Digest

*A [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) issued on consumer demand, holder-bound, carrying their own meter readings for a specified period (W3C Verifiable Credential).*

**[Implementation Guide →](../use-cases/consumer-meter-digest/README.md)**

| Field | Value |
|---|---|
| Document | IES/CMD-PROFILE/0.6 |
| Status | Live in pilot |
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
| Readings | Raw profiles (`INTERVAL`, `DAILY`, `MONTHLY`) or derived summaries (`SUMMARY_TOTAL`, `SUMMARY_PEAK`, `SUMMARY_TOD`) | MeterData v0.6 (IS 15959 / DLMS-COSEM) |
| Data quality | Estimation flags, missing intervals | MeterData v0.6 |
| Issuer & proof | Issuing DISCOM (`did:web`) and cryptographic proof | MeterDataCredential v0.6 (W3C VC) |

Granularity: `RAW_15M`, `DAILY`, `MONTHLY`, plus derived summaries. Typical max period: 24 months (`MONTHLY`), 90 days (`RAW_15M`).

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
- **READING** — register value at a point in time (cumulative; strictly increasing).
- **USAGE** — delta / consumed amount over a period.
- **OBIS** — Object Identification System code (IEC 62056 / IS 15959) for a meter register.
- **Summary** — a derived aggregate computed from raw readings.

See **[IES Meter Data Model](../use-cases/smart-meter-data-exchange/ies-meter-data-model.md)** for the underlying meter-data terminology.

## 5. Basis of Standards

See [Schemas — Standards precedence](../schemas/README.md#standards-precedence) for the fixed IES order of preference.

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

| Part | Fields | Basis |
|---|---|---|
| Credential envelope | `@context`, `id`, `type`, `issuer`, `credentialSubject`, `proof` | Standard W3C VC |
| Payload | `meterReference`, `period`, `readings`, `summary`, `dataQuality` | [MeterData v0.6 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) |

## 9. Schedule II

| Wrapping / dependency | Detail |
|---|---|
| Not applicable as a populated report | The closest analogue is the **summary** profile, deriving `SUMMARY_TOTAL` / `SUMMARY_PEAK` / `SUMMARY_TOD` aggregates from raw readings — documented per summary kind in the schema. |

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
2. **Summary-derivation formula** per kind, especially ToD bucket boundaries (may vary by SERC).
3. **Latency budget** — MDM read-path performance is the binding constraint.

---

## Schemas Used in This Use Case

Holder-bound issuance of **[MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6)**, wrapping a **[MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6)** payload. Entitlement is typically proven by a [Consumer Energy Passport](consumer-energy-passport.md).

## Value Unlock

The consumer proves actual consumption history, DISCOM-signed, verifiable in seconds with no callback. The DISCOM cuts the steady drip of bill-verification calls and gains a clean, consented data-sharing surface — a much higher-trust input than emailed PDF bills.

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 15959 (Parts 1–3) | DLMS/COSEM companion spec; OBIS codes |
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IEC 62056 | DLMS/COSEM; OBIS |
| IEC 61968-9 | CIM — meter reading and control |
| W3C VC Data Model 2.0; W3C DID Core | Credential envelope; identifiers |
| RFC 3339 / ISO 8601 | Date-time format for `period` |

## Annexure B — Example Payload

- **[`example-customer-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-customer-profile.json)**
- **[`example-interval-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-interval-profile.json)**
- **[`example-monthly-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-monthly-profile.json)**

## Annexure C — JSON Schema

Canonical: `https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/` — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/schema.json), [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/context.jsonld), [`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/vocab.jsonld). The payload schema: [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6).
