# Consumer Meter Digest

A **[MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md)** issued on consumer demand, holder-bound to the consumer's wallet, carrying their own meter readings for a specified period (W3C Verifiable Credential).

| | |
|---|---|
| **Document** | IES/CMD-PROFILE/0.6 |
| **Status** | Live in pilot |
| **Applicability** | All distribution licensees |
| **This version** | Consumer Meter Digest *variant* of [MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md), holder-bound. It wraps [MeterData v0.6](../../schemas/MeterData/v0.6/README.md) profiles. |

---

## 1. Scope and Purpose

The **stakeholder** is the consumer who needs to share verified consumption history with a bank, marketplace, energy app, housing society or installer, and the DISCOM that issues the digest. Today the consumer prints PDFs of monthly bills and emails scans; verifiers have no way to confirm the bill is real and unaltered, so most of them call the DISCOM anyway.

This document defines the **Consumer Meter Digest** — a verifier-friendly bundle of the consumer's telemetry, signed by the DISCOM and delivered into the consumer's wallet. It is **not** a new credential type: MeterDataCredential v0.6 is the schema, and the Digest profiles how that one credential is configured when a *consumer* (rather than another DISCOM or AMISP) is the audience.

## 2. What It Records / Covers

For one consumer's meter and a specified period the Digest records:

- the **meter reference** (`meterRefs`) and **service-delivery-point reference** (`serviceDeliveryPointRefs`)
- the **period** the readings cover
- the **readings** — either raw profiles (`INTERVAL`, `DAILY`, `MONTHLY`) or derived **summaries** (`SUMMARY_TOTAL`, `SUMMARY_PEAK`, `SUMMARY_TOD`)
- the **data quality** metadata (estimation flags, missing intervals)
- the **issuer** block (DISCOM `did:web`) and the **proof**

Granularity options today: `RAW_15M` (15-minute interval data), `DAILY`, `MONTHLY`, plus derived summaries. Maximum period typically 24 months for `MONTHLY`, 90 days for `RAW_15M`.

## 3. How Each Item is Identified

Reuses the identifier scheme from [Consumer Energy Passport §3](../consumer-energy-passport/README.md#id-3.-how-each-item-is-identified).

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (issuer) | `did:web` on owned domain | `did:web:ies.tpddl.in` |
| Consumer (holder) | `did:key` (wallet) | `did:key:z6MkjVQ8r4f3rPuY…` |
| Meter | `did:web` under issuer domain | `did:web:ies.tpddl.in:assets:meter:NM-44091234` |
| Service delivery point | `did:web` under issuer domain | `did:web:ies.tpddl.in:connections:CON-90234` |

The meter identifier in the Digest **matches** the meter identifier in the consumer's [Consumer Energy Passport](../consumer-energy-passport/README.md); a verifier sees the Passport and the Digest as a coherent pair.

## 4. Definitions

- **Holder-bound** — issued to a specific holder's wallet (`credentialSubject.id` = wallet DID).
- **READING** — register value at a point in time (cumulative; strictly increasing for cumulative registers).
- **USAGE** — delta or consumed amount over a period (used for energy block consumption and for demand registers).
- **OBIS** — Object Identification System code (IEC 62056 / IS 15959) identifying a physical quantity at a meter register.
- **Summary** — a derived aggregate (total, peak, time-of-day bucket) computed from raw readings; carried in the Digest alongside or instead of the raw profile.

For the underlying meter-data terminology see **[IES Meter Data Model](../smart-meter-data-exchange/ies-meter-data-model.md)**.

## 5. Basis of Standards

Same precedence as the rest of IES: **IS → CEA → IEC → IEEE**.

Metering reads conform directly to Indian standards: **IS 15959** (DLMS/COSEM companion specification; OBIS codes) for the underlying meter data, and **IS 16444** for the meter device. The credential envelope is **W3C VC Data Model 2.0**.

## 6. Where Indian Standards Do Not Yet Exist

The credential envelope (W3C VC) and the underlying data model (DDM / IES MeterData compact profiles) have no Indian equivalent; international standards are used. The MeterData v0.6 compact-profile shapes are an IES specification on top of IEC 62056 / IS 15959.

## 7. The Record

The Digest defines **one record**: a Verifiable Credential wrapping a MeterData profile. Unlike the [Passport](../consumer-energy-passport/README.md), the Digest is a **point-in-time snapshot** with a short `validUntil` (hours to days) — the consumer re-requests when they need fresh data.

It is **holder-bound**. The consumer holds it in DigiLocker or a DID wallet. The consumer can present the same Digest to multiple verifiers within its validity window.

Revocation rarely matters in practice (Digests typically expire faster than they would need revocation), but the same DeDi-hash revocation flow is available.

## 8. Schedule I — Static Fields of the Credential

The full, authoritative field tables are in the schema:

→ **[MeterDataCredential v0.6 — Field reference](../../schemas/MeterDataCredential/v0.6/README.md)**

The credential envelope (`@context`, `id`, `type`, `issuer`, `credentialSubject`, `proof`) is identical to any W3C VC. The payload (`meterReference`, `period`, `readings`, `summary`, `dataQuality`) follows the MeterData v0.6 compact-profile schema:

→ **[MeterData v0.6 — Field reference](../../schemas/MeterData/v0.6/README.md)**

## 9. Schedule II

Not applicable as a populated report template.

The closest analogue is the **summary** profile, which derives `SUMMARY_TOTAL`, `SUMMARY_PEAK` or `SUMMARY_TOD` aggregates from the raw `INTERVAL` / `DAILY` / `MONTHLY` profile. The derivation is documented per summary kind in the schema.

## 10. How It Fits Together

```
Consumer (wallet)         DISCOM
─────────────────         ──────

  │── request via ──────>│
  │   DigiLocker /        ├─ verify consumer is entitled
  │   consented app       │  (Consumer Energy Passport or
  │                       │   minimal customer credential)
  │                       │
  │                       ├─ pull readings from MDM
  │                       │  for requested meter + period
  │                       │
  │                       ├─ build MeterData/v0.6 payload
  │                       │  (INTERVAL / DAILY / MONTHLY,
  │                       │   or derived SUMMARY_*)
  │                       │
  │                       ├─ wrap in MeterDataCredential v0.6:
  │                       │  credentialSubject.id = wallet DID
  │                       │  validUntil = 24h to 7d
  │                       │
  │<── signed Digest ─────│
  │   delivered to wallet │

  │── present Digest ────> Verifier (bank, marketplace, …)
  │   (offline verify)
```

The Digest is **point-in-time**. The consumer re-requests when they need fresh data.

## 11. Points for Confirmation

1. **Maximum-range policy** by granularity (typical: 24 months for `MONTHLY`, 90 days for `RAW_15M`); to be tightened per use case.
2. **Summary-derivation schema** — the precise formula for each `SUMMARY_*` kind, especially ToD bucket boundaries that may vary by SERC.
3. **Latency budget** — consumer flows need a Digest within seconds; MDM read-path performance is the binding constraint.

---

## Schemas Used in This Use Case

The Digest is the holder-bound issuance of a single schema — **[MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md)** — which itself wraps a payload conforming to **[MeterData v0.6](../../schemas/MeterData/v0.6/README.md)**. The consumer's entitlement to request the Digest is typically proven by their **[Consumer Energy Passport](../consumer-energy-passport/README.md)** (or a minimal customer credential).

## Value Unlock

The consumer can prove their **actual consumption history**, signed by the DISCOM, in a form a bank, EV-charger installer, rooftop-solar quoter or marketplace can verify in seconds with no DISCOM callback. The DISCOM cuts the steady drip of bill-verification calls and gains a clean, consented data sharing surface. Verifiers gain a much higher-trust input than emailed PDF bills.

---

## Setup: Register → Discover → Exchange

Built on the four implementation steps in **[How you implement IES](../../how-you-implement-ies/README.md)**. Use-case-specific items only below.

### Register — base in place

- [ ] [Identity setup](../../how-you-implement-ies/setup-register.md) complete
- [ ] [Consumer Energy Passport](../consumer-energy-passport/README.md) issued to the same consumer (or a minimal customer credential) — used to prove entitlement to request the Digest

### Discover — consumer-pull endpoint

- [ ] [Discovery setup](../../how-you-implement-ies/setup-discovery.md) complete
- [ ] Beckn `DatasetItem` for the pull endpoint published on your BPP (`accessMethod: INLINE`)
- [ ] `requiredCredential` restricts callers to a valid [Consumer Energy Passport](../consumer-energy-passport/README.md) (or minimal customer credential)
- [ ] `granularityOptions` / `maxRange` agreed with internal compliance

### Exchange — MDM read path and issuance

- [ ] [Adapter built](../../how-you-implement-ies/build-adapter.md) for [MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md) / [MeterData v0.6](../../schemas/MeterData/v0.6/README.md)
- [ ] Read access tested for the granularities you'll support (`RAW_15M`, `DAILY`, `MONTHLY`, derived summaries)
- [ ] Max-range policy decided (e.g. 24 months for `MONTHLY`, 90 days for `RAW_15M`)
- [ ] Latency budget understood — consumer flows need a Digest in seconds
- [ ] `credentialSubject.id` = wallet DID; `schemaId` = `MeterDataCredential/v0.6`
- [ ] `validUntil` short — 24h for loan portals, up to 7d for less time-sensitive flows
- [ ] Schema validation passes against [MeterDataCredential v0.6 schema.json](../../schemas/MeterDataCredential/v0.6/schema.json)
- [ ] DigiLocker pull tested end-to-end → [DigiLocker delivery](../../what-ies-provides/energy-credentials/digilocker.md)
- [ ] One direct DID-push path tested for non-DigiLocker wallets
- [ ] Verification rehearsed with one verifier (bank / marketplace / housing society / EV installer)
- [ ] If you emit derived `summary` outputs, share the schema + description with verifiers up front
- [ ] Revocation flow tested (even though Digests usually expire before needing it)

### Team

- [ ] IT SPOC (MDM read path + BPP catalogue)
- [ ] Customer-ops SPOC (wallet support)
- [ ] Governance / Compliance SPOC (data-disclosure policy)

---

## Dev kits and code

- **Schema source** — [`schemas/MeterDataCredential/v0.6/attributes.yaml`](../../schemas/MeterDataCredential/v0.6/attributes.yaml)
- **JSON Schema** — [`schema.json`](../../schemas/MeterDataCredential/v0.6/schema.json) (credential wrapper) + [`MeterData/v0.6/schema.json`](../../schemas/MeterData/v0.6/schema.json) (payload)
- **JSON-LD context** — [`context.jsonld`](../../schemas/MeterDataCredential/v0.6/context.jsonld)
- **Example payloads** — [`examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterDataCredential/v0.6/examples) (customer profile; interval profile; monthly profile)
- **Validation** — `python3 scripts/validate_schema.py schemas/MeterDataCredential/v0.6/schema.json <your-output.json>`
- **MDM read-path guidance** — [MeterData v0.6 — User Guide](../../schemas/MeterData/v0.6/UserGuide.md)
- **OBIS / IS 15959 / CIM mapping** — [IES Meter Data Model](../smart-meter-data-exchange/ies-meter-data-model.md)

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 15959 (Parts 1–3) | DLMS/COSEM data-exchange companion specification; OBIS codes |
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IEC 62056 | DLMS/COSEM; OBIS (IS 15959 is the Indian companion) |
| IEC 61968-9 | CIM — meter reading and control |
| W3C VC Data Model 2.0; W3C DID Core | Verifiable Credential envelope; decentralized identifiers |
| RFC 3339 / ISO 8601 | Date-time format for `period.from` / `period.to` |

## Annexure B — Example Payload

Example payloads for each profile shape are in the schema repository:

- **[`example-customer-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-customer-profile.json)** — customer / service-point metadata
- **[`example-interval-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-interval-profile.json)** — 15-minute block load survey
- **[`example-monthly-profile.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterDataCredential/v0.6/examples/example-monthly-profile.json)** — monthly billing reset

## Annexure C — JSON Schema

- Canonical reference: `https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/`
- **[`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/schema.json)** — bundled JSON Schema (Draft 2020-12)
- **[`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/context.jsonld)**
- **[`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/vocab.jsonld)**

The MeterData payload schema (referenced from the credential): **[MeterData v0.6](../../schemas/MeterData/v0.6/README.md)**.
