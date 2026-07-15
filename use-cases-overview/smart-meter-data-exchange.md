# Smart Meter Data Exchange

*A standard, audit-trailed way to exchange smart-meter telemetry between an AMISP, a DISCOM, a State regulator, and consented third parties — over [IES Data Exchange](../what-ies-provides/discover.md), carrying the [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) payload.*

**[Implementation Guide →](../use-cases/smart-meter-data-exchange/README.md)**

| Field | Value |
|---|---|
| Document | IES/SMDX-PROFILE/0.6 |
| Status | Live in pilot |
| Applicability | All AMISPs, DISCOMs and SERCs |
| This version | Built on MeterData v0.6, MeterDataRequest v0.6 and (optional) MeterDataRequestCredential v0.1 over Beckn. |

> For consumer-pull of *their own* meter data, see **[Consumer Meter Digest](consumer-meter-digest.md)**. This is the bulk, scheduled, machine-to-machine flow.

---

## 1. Scope and Purpose

The stakeholders are the DISCOM (data fiduciary), the AMISP (data processor) and any authorised third party. Today every DISCOM-AMISP pair builds a bespoke integration — a one-time dump, then incremental files over FTP, or a project-specific API — negotiated and built from scratch each time.

This document defines **Smart Meter Data Exchange** — a one-to-many, standard data shape (MeterData v0.6) carried over a one-to-many discovery and contracting layer (Beckn). A TSP integrates once and the same pattern works across DISCOMs. IES standardises **the interface where parties exchange data** — it does not change how any party stores or moves data internally.

## 2. What It Records / Covers

Four things, and only these four: **the contract** (how a request is discovered and agreed), **consent and scope** (how consent, scope, duration are recorded), **the data shape** (the MeterData wire format), **receipts and audit** (proof of what was exchanged). The meter keeps speaking DLMS-COSEM / IS 15959; the head-end, MDM and AMISP's systems are unchanged.

Eight MeterData v0.6 compact profiles cover every cadence:

| Profile | Carries |
|---|---|
| `CUSTOMER` | Slow-changing customer / service-point / meter installation metadata |
| `INTERVAL` | Block load survey at 15- or 30-min resolution |
| `DAILY` | Daily accumulated load survey |
| `MONTHLY` | Monthly billing resets (cumulative kWh, ToU, MD) |
| `BILL_DETAILS` | Utility-side billing computed details |
| `INSTANTANEOUS` | Real-time snapshot of V/A/P/Q |
| `EVENT` | IS 15959 diagnostic / tamper events |
| `ALARM` | Real-time active alerts |

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (data fiduciary) | `did:web` on owned domain | `did:web:ies.discom.example` |
| AMISP / TSP (data processor) | `did:web` on owned domain | `did:web:np.example.com` |
| Meter / DT / Feeder | `did:web` under DISCOM domain | `did:web:ies.discom.example:assets:meter:NM-44091234` |

**No new IDs to allocate.** Existing meter SLNOs, DT codes and feeder codes stay exactly as they are; the `did:web` wrapper reuses them. Adoption is *nice to have* for a first deployment — bare IDs work in payloads initially.

## 4. Definitions

Terms used here (DLMS-COSEM, OBIS, HES, MDM/MDMS, AMISP, READING vs USAGE) are defined once on the schema overview — see **[MeterData — Definitions](../what-ies-provides/schemas-overview/meter-data.md#id-4.-definitions)** and the [Glossary](../glossary.md).

## 5. Basis of Standards

IES follows a fixed precedence (IS → CEA → IEC → IEEE); the standards MeterData is built on are documented once on the schema overview — see **[MeterData — Basis of Standards](../what-ies-provides/schemas-overview/meter-data.md#id-5.-basis-of-standards)**.

## 6. Where Indian Standards Do Not Yet Exist

The compact-profile JSON shape and Beckn discovery/contracting are IES choices; this is documented once on the schema overview — see **[MeterData — Where Indian Standards Do Not Yet Exist](../what-ies-provides/schemas-overview/meter-data.md#id-6.-where-indian-standards-do-not-yet-exist)**.

## 7. The Record

No Verifiable Credential by default. Each exchange produces: a **signed Beckn contract** (discovery, scope, parties, time-bound authorisation), a **signed MeterData v0.6 payload** (inline or signed-URL), and a **signed receipt**. Together: a verifiable audit trail for DPDP accountability and dispute resolution. For a durable, holder-bound record, wrap in **[MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6)** — see [Consumer Meter Digest](consumer-meter-digest.md).

## 8. Schedule I — Static Fields of the Data Exchange

- **[MeterData v0.6 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6)** — the payload (eight compact profiles)
- **[MeterDataRequest v0.6 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6)** — the query shape
- **[MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1)** — the optional authorisation VC

For Indian-terminology mapping, see **[IES Meter Data Model](../use-cases/smart-meter-data-exchange/ies-meter-data-model.md)**.

## 9. Schedule II — Reportee Templates (optional)

Several deployments produce derived reports from the raw stream — feeder-aggregated profiles, anonymised responses, billing summaries — documented as example payloads, not separate schemas. See [`MeterData/v0.6/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.6/examples).

## 10. How It Fits Together

```
Today: DISCOM ─bespoke─ AMISP-1 / AMISP-2 / analytics / third party  (n × m integrations)
With IES: DISCOM ── one MeterData v0.6 over Beckn ──► AMISP-1 / AMISP-2 / analytics / third party  (n + m)
```

**Roles don't change; the record makes them explicit.** The DISCOM remains the data fiduciary (authorises a TSP once, scoped, time-bound); the AMISP remains the processor (IES doesn't alter ownership); the TSP integrates once (same discovery/contract/shape across every adopting DISCOM). Every exchange leaves a signed receipt for DPDP accountability.

## 11. Points for Confirmation

1. **Chunking convention** for bulk historical pulls — being agreed across deployments.
2. **Quality flags** — the v0.6 `validationStatus` enum is stable; the per-cadence recommended profile is being tightened.
3. **Aggregator-controlled DERs** — the consent/control flow for *acting* on (not just reading) a DER is specified separately.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) | The payload — eight compact profiles |
| [MeterDataRequest v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6) | The query / capabilities shape |
| [MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) *(optional)* | Seeker authorisation VC |

## Value Unlock

**DISCOMs/AMISPs** — one interface replaces bespoke pair-by-pair integration; months become days. **Regulators/analytics** — one consistent format with a verifiable audit trail; comparable analysis across DISCOMs. **Consumers** — consented third parties reading meter data on standard rails unlocks green loans, automated solar quotes and demand-shift offers.

---

## Annexure A — Standards Referenced

The full standards table for the MeterData payload lives on the schema overview — see **[MeterData — Standards Referenced](../what-ies-provides/schemas-overview/meter-data.md#annexure-a-standards-referenced)**. DPDP Act 2023 (consent/accountability) and Beckn v2 (the exchange wire) additionally apply to this use case.

## Annexure B — Example Payloads

26 examples covering every profile shape and derived reports at **[`schemas/MeterData/v0.6/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.6/examples)** — highlights: `CustomerProfile.json`, `IntervalProfile.json`, `DailyProfile.json` / `MonthlyProfile.json`, `MultiMeterBulkDataset*.json`, `EventProfile.json` / `AlarmProfile.json`, `AggregatedFeeder.json`.

## Annexure C — JSON Schema

Canonical: `https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/` — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/schema.json), [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld), [`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/vocab.jsonld), [`IES codes.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/IES%20codes.json) (OBIS registry).
