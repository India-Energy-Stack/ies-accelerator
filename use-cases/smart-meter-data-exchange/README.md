# Smart Meter Data Exchange

A standard, audit-trailed way to exchange smart-meter telemetry between an AMISP, a DISCOM, a State regulator, and consented third parties — over [IES Data Exchange](../../what-ies-provides/data-exchange/README.md), carrying the [MeterData](../../schemas/MeterData/v0.6/README.md) payload.

| | |
|---|---|
| **Document** | IES/SMDX-PROFILE/0.6 |
| **Status** | Live in pilot |
| **Applicability** | All AMISPs, DISCOMs and SERCs |
| **This version** | Smart Meter Data Exchange built on [MeterData v0.6](../../schemas/MeterData/v0.6/README.md), [MeterDataRequest v0.6](../../schemas/MeterDataRequest/v0.6/README.md) and (optional) [MeterDataRequestCredential v0.1](../../schemas/MeterDataRequestCredential/v0.1/README.md) over Beckn. |

> For consumer-pull of *their own* meter data (one-meter, on-demand, wallet-shareable), see **[Consumer Meter Digest](../consumer-meter-digest/README.md)**. This guide is the bulk, scheduled, machine-to-machine flow.

---

## 1. Scope and Purpose

The **stakeholders** are the DISCOM (data fiduciary), the AMISP (data processor) and any authorised third party. Today every DISCOM-AMISP pair builds a **bespoke integration**: a one-time historical dump, then incremental files over a shared folder or FTP, or a project-specific API. Each pairing is negotiated and built from scratch.

This document defines the **Smart Meter Data Exchange** — a one-to-many, standard data shape (the MeterData v0.6 compact profiles) carried over a one-to-many discovery and contracting layer (Beckn). A TSP integrates once and the same pattern works across DISCOMs. Every exchange leaves a verifiable record.

IES standardises **the interface where parties exchange data**. It does **not** change how any party stores or moves data internally.

## 2. What It Records / Covers

Four things, and only these four:

| | |
|---|---|
| **The contract** | How a data request is discovered and agreed |
| **Consent and scope** | How consent, scope and duration are recorded |
| **The data shape** | The shape of the meter data on the wire — the IES MeterData schema |
| **Receipts and audit** | The receipts and audit trail that prove what was exchanged |

**What stays exactly as it is.** The meter keeps speaking DLMS-COSEM / IS 15959. The head-end and MDM keep working as they do. The AMISP keeps its existing systems. IES sits at the external interface where data leaves the MDM toward an authorised recipient. **None of this is replaced.**

The eight MeterData v0.6 compact profile shapes cover every smart-meter cadence:

| Profile | Carries |
|---|---|
| `CUSTOMER` | Slow-changing customer / service-point / meter installation metadata |
| `INTERVAL` | Block load survey at 15- or 30-minute resolution |
| `DAILY` | Daily accumulated load survey |
| `MONTHLY` | Monthly billing resets (cumulative kWh, ToU buckets, MD) |
| `BILL_DETAILS` | Utility-side billing computed details |
| `INSTANTANEOUS` | Real-time snapshot of V / A / P / Q |
| `EVENT` | IS 15959 diagnostic / tamper events |
| `ALARM` | Real-time active alerts |

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (data fiduciary) | `did:web` on owned domain | `did:web:ies.tpddl.in` |
| AMISP / TSP (data processor) | `did:web` on owned domain | `did:web:np.example.com` |
| Meter | `did:web` under DISCOM domain | `did:web:ies.tpddl.in:assets:meter:NM-44091234` |
| Distribution transformer | `did:web` under DISCOM domain | `did:web:ies.tpddl.in:assets:dt:DT-11KV-F02-452` |
| Feeder | `did:web` under DISCOM domain | `did:web:ies.tpddl.in:assets:feeder:F02` |

> **There are no new IDs to allocate.** Existing meter SLNOs, DT codes, feeder codes and substation codes are the IDs of record and stay exactly as they are. The IES convention is a `did:web` wrapper that reuses those existing IDs so they can be referenced across the network. Adoption of the `did:web` form is *nice to have* for first deployment — initial flows can use bare IDs inside MeterData payloads and adopt the `did:web` form incrementally.

## 4. Definitions

- **DLMS-COSEM** — the wire protocol between a smart meter and the AMI head-end (also referred to as **IS 15959** in India).
- **OBIS** — Object Identification System code (IEC 62056 / IS 15959) identifying a physical quantity at a meter register.
- **HES** (Head-End System) — the AMI software layer that talks to smart meters over the field network.
- **MDM / MDMS** — Meter Data Management System; the utility's system of record for meter readings.
- **AMISP** — Advanced Metering Infrastructure Service Provider; the entity that deploys, owns and operates smart meters and the HES on behalf of a DISCOM.
- **TSP** — Technology Service Provider (e.g. an AMISP or analytics provider).
- **READING vs USAGE** — `READING` is the physical register value at a point in time; `USAGE` is the delta or consumed amount over a period.

## 5. Basis of Standards

IES order of preference: **IS → CEA → IEC → IEEE**.

For meter data, IES follows **IS 16444** (smart meter spec) and **IS 15959 / IEC 62056** (DLMS-COSEM companion specification, OBIS codes) directly. The IES MeterData v0.6 compact profiles are an IES specification on top of these — they standardise the JSON shape that carries DLMS-COSEM readings over the wire.

CEA / RDSS AMI interoperability guidance names **IEC 61968 / IEC 61968-100** alongside MultiSpeak and Web Services for HES↔MDMS integration. IES uses CIM (IEC 61968-9) for master data and the CustomerProfile shape.

## 6. Where Indian Standards Do Not Yet Exist

The compact-profile **JSON shape** carrying DLMS-COSEM readings is an IES specification — no Indian or international standard predates it. The Beckn protocol layer (open, asynchronous, peer-to-peer discovery and contracting) is also an IES choice, not a sector-mandated standard.

For event codes, IES MeterData v0.6 follows **IS 15959** event-code allocations directly.

## 7. The Record

The Smart Meter Data Exchange does not produce a Verifiable Credential by default. The artefacts produced per exchange are:

1. A **signed Beckn contract** — discovery, consent scope, parties, time-bound authorisation
2. A **signed MeterData v0.6 payload** — the readings themselves (inline or via signed-URL handoff)
3. A **signed receipt** — who received what, under whose authorisation, for how long

Together these form a **verifiable audit trail** sufficient for DPDP accountability and dispute resolution.

If the use case needs a durable, holder-bound record (a consumer sharing their own data with a bank, a regulator receiving a long-lived attestation), use the wrapping **[MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md)** — see [Consumer Meter Digest](../consumer-meter-digest/README.md).

## 8. Schedule I — Static Fields of the Data Exchange

The full, authoritative field tables are in the schemas:

- **[MeterData v0.6 — Field reference](../../schemas/MeterData/v0.6/README.md)** — the payload shape (eight compact profiles)
- **[MeterDataRequest v0.6 — Field reference](../../schemas/MeterDataRequest/v0.6/README.md)** — the query / capabilities shape
- **[MeterDataRequestCredential v0.1 — Field reference](../../schemas/MeterDataRequestCredential/v0.1/README.md)** — the optional VC carrying authorisation

For the Indian-terminology mapping (OBIS codes, IS 15959 event IDs, CIM master-data fields) see the companion page **[IES Meter Data Model](ies-meter-data-model.md)**.

## 9. Schedule II — Reportee templates (optional)

Several deployments produce **derived reports** from the raw MeterData stream — feeder-aggregated profiles, anonymised telemetry responses, custom billing summaries. These are documented as separate example payloads in the schema repository, not as schemas in their own right.

Examples: `AggregatedFeeder.json`, `Anonymised_Telemetry_Response.json`, `CustomerBillingSummary.json`, `BillDetails.json`. See **[`MeterData/v0.6/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.6/examples)**.

## 10. How It Fits Together

```
Today (without IES)                       With IES

DISCOM ─bespoke─ AMISP-1                  DISCOM ─┐
       ─bespoke─ AMISP-2                          ├── one MeterData v0.6 ──── AMISP-1
       ─bespoke─ analytics provider                │   over Beckn          ── AMISP-2
       ─bespoke─ consented third party            ┴                       ── analytics
                                                                          ── third party
n × m bespoke integrations                One published interface;
                                          n + m connections, not n × m
```

**Roles do not change. The record makes them explicit.**

| | |
|---|---|
| **DISCOM** | Remains the data fiduciary. Authorises a TSP once, in a way that is recorded, scoped and time-bound. Internal systems (MDM, head-end, billing) are not re-engineered. |
| **AMISP** | Remains the processor. Processes data on behalf of the DISCOM. IES does not alter who owns or controls the data. Because IES sits at the external interface, the head-end, meters and MDM are not touched by an IES integration. |
| **TSP** | Integrates once. Conforms to the IES interface once, and the same discovery, contract and data shape apply across DISCOMs that have adopted IES. Receives data in the IES MeterData schema, so the parser is written once. |

Every exchange leaves a signed receipt: who received what, under whose authorisation, and for how long. This record supports DPDP accountability and dispute resolution.

## 11. Points for Confirmation

1. **Chunking convention** for bulk historical pulls (daily / monthly / quarterly) is being agreed across deployments.
2. **Quality flags** — the v0.6 `validationStatus` enum is stable; the recommended profile of allowed values per cadence is being tightened.
3. **Aggregator-controlled DERs** — the consent + control flow for a TSP that wants to *act* on a DER (not just observe) is being specified separately under the DER Flexibility use case.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| **[MeterData v0.6](../../schemas/MeterData/v0.6/README.md)** | The payload shape on the wire — eight compact profiles covering every smart-meter cadence |
| **[MeterDataRequest v0.6](../../schemas/MeterDataRequest/v0.6/README.md)** | The query / capabilities shape — what the seeker is asking for |
| **[MeterDataRequestCredential v0.1](../../schemas/MeterDataRequestCredential/v0.1/README.md)** *(optional)* | A W3C VC the seeker attaches at `confirm` time; provider verifies offline |

## Value Unlock

**For DISCOMs and AMISPs** — one published interface replaces bespoke pair-by-pair integration; weeks-to-months of bilateral work become days. New AMISPs or technology vendors plug in without renegotiating the data shape.

**For regulators and analytics providers** — telemetry arrives in one consistent format, with a verifiable audit trail of consent and scope. Comparable analysis across DISCOMs becomes possible.

**For the consumer** — when consented third parties (banks, energy apps) can read meter data on standard rails, downstream services they value (green loans, automated solar quotes, demand-shift offers) become viable.

---

## Setup: Register → Discover → Exchange

Built on the four implementation steps in **[Part 3 — Implementing IES](../../how-you-implement-ies/README.md)**. Use-case-specific items only below.

### Register — network identity

- [ ] [Identity setup](../../how-you-implement-ies/setup-register.md) complete (DeDi namespace + signing key on both sides — BAP and BPP)
- [ ] Meter / DT / feeder identifier convention agreed (existing IDs wrapped, not replaced)

### Discover — catalogue and contract

- [ ] [Discovery setup](../../how-you-implement-ies/setup-discovery.md) complete (ONIX running on both sides; subscriber records published)
- [ ] BPP publishes a Beckn catalogue entry for the `MeterData/v0.6` dataset offered — `programID`, geographic scope, refresh cadence, `accessMethod` (`INLINE` for ≤MB chunks; `SIGNED_URL` / `KAFKA` / `SFTP` for bulk and streaming), required credentials
- [ ] Pre-agreed bilateral subscriptions (where used) skip `discover` and go straight to `confirm`
- [ ] Test exchange completed against sandbox: `confirm` → `on_confirm` → `on_status`

### Exchange — adapter and data flow

- [ ] [Adapter built](../../how-you-implement-ies/build-adapter.md) for [MeterData v0.6](../../schemas/MeterData/v0.6/README.md)
- [ ] Meter population, geography, granularity, counterparty for Phase 1 agreed
- [ ] Source system mapped (HES / MDM endpoint, owner team, SLA)
- [ ] Indian-OBIS → MeterData v0.6 mapping verified for every reading and event you ship (see [IES Meter Data Model](ies-meter-data-model.md))
- [ ] Data-quality flags (missing / estimated) handled per the v0.6 `validationStatus` enum
- [ ] (If third-party access in scope) MeterDataRequestCredential verification wired into the BPP — type, validity, DeDi status, scope ⊆ contract
- [ ] Live exchange completed end-to-end with a real counterparty

### Team

- [ ] IT / data SPOC (HES / MDM read path; BPP handler)
- [ ] Authorised Signatory (network onboarding)
- [ ] Compliance SPOC (DPDP accountability; consent scope)

---

## Dev kits and code

- **Schema source** — [`schemas/MeterData/v0.6/attributes.yaml`](../../schemas/MeterData/v0.6/attributes.yaml)
- **JSON Schema** — [`schema.json`](../../schemas/MeterData/v0.6/schema.json)
- **OBIS code registry** — [`IES codes.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/MeterData/v0.6/IES%20codes.json)
- **User Guide** — [`UserGuide.md`](../../schemas/MeterData/v0.6/UserGuide.md)
- **Reference Guide** — [`ReferenceGuide.md`](../../schemas/MeterData/v0.6/ReferenceGuide.md)
- **Example payloads** — [`examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.6/examples) (24 examples covering all eight profile shapes)
- **Validation** — `make test` (from repo root) runs the validator against every example
- **Data Exchange devkit** — `git clone https://github.com/beckn/DEG.git && cd DEG/devkits/data-exchange/install && docker compose up -d`
- **Indian-terminology mapping** — [IES Meter Data Model](ies-meter-data-model.md)

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IS 15959 (Parts 1–3) | DLMS/COSEM data-exchange companion specification; OBIS codes; event codes |
| IEC 62056 | DLMS/COSEM |
| IEC 61968-9 | CIM — meter reading and control |
| IEC 61968-100 | Web service implementation profile (named in CEA AMI interoperability guidance) |
| CEA (Installation and Operation of Meters) Regulations, 2006 | Metering legal framework |
| RDSS — Revamped Distribution Sector Scheme | Policy context for current AMI deployment |
| DPDP Act 2023 | Consent and accountability framework for consumer data |
| W3C VC Data Model 2.0; W3C DID Core | (Optional — for MeterDataRequestCredential authorisation) |

## Annexure B — Example Payloads

24 example payloads ship with the schema, covering every profile shape and several derived report templates:

→ **[`schemas/MeterData/v0.6/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.6/examples)**

Highlights:

- `CustomerProfile.json` — customer / service-point / meter installation
- `IntervalProfile.json` / `IntervalProfile_Elaborated.json` — 15-min block load
- `DailyProfile.json` / `MonthlyProfile.json` — daily / monthly accumulators
- `MultiMeterBulkDataset.json` / `MultiMeterBulkDatasetShortCodes.json` — bulk with OBIS codes and short codes
- `EventProfile.json` / `AlarmProfile.json` — IS 15959 events and active alarms
- `AggregatedFeeder.json` — feeder-aggregated derived report

## Annexure C — JSON Schema

- Canonical reference: `https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/`
- **[`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/schema.json)** — bundled JSON Schema (Draft 2020-12)
- **[`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld)**
- **[`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/vocab.jsonld)**
- **[`IES codes.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/IES%20codes.json)** — OBIS code registry
