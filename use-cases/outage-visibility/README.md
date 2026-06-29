# Outage Visibility

A DISCOM publishes planned and unplanned **electricity outage** details — affected feeders / DTs, area, timing, cause, restoration — as a signed `OutageNotification` consumable as a website / outage-map feed and pushable to affected consumers.

| | |
|---|---|
| **Document** | IES/OV-PROFILE/0.1 |
| **Status** | Live in pilot (early draft v0.1 — subject to change) |
| **Applicability** | All distribution licensees |
| **This version** | Built on **[OutageNotification v0.1](../../schemas/OutageNotification/v0.1/README.md)** over Beckn. One canonical object — pull (catalogue feed) and push (CAP-aligned alert) carriage. |

> **WORK IN PROGRESS.** The schema is an early draft. Model names, enum values and the SD/BD/RS interpretation may change before a stable release. Do not depend on it for production integrations yet.

---

## 1. Scope and Purpose

The **stakeholders** are the DISCOM (issuer), affected consumers, third-party outage-map operators, and the SERC. Today, planned shutdowns are notified through ad-hoc SMS / newspaper / website PDFs; unplanned outages reach consumers via the complaint helpline. Cross-DISCOM comparison and SAIDI / SAIFI roll-ups depend on hand-stitched spreadsheets.

This document defines **Outage Visibility** — one signed, machine-readable record per outage, with **GIS-ready** geometry, **CAP-compatible** push semantics for alerts, and **MultiSpeak**-style provenance back to the smart-meter signal where the outage was auto-detected.

It standardises the **publication shape**. It does not change how the DISCOM detects, dispatches or restores an outage.

## 2. What It Records / Covers

For one outage the record carries:

- the **outage identity** — id, status (`NEW` / `UPDATE` / `RESTORED` / `CANCELLED`), class (planned shutdown / unplanned breakdown / load-shedding);
- the **cause** — IEEE 1782 category + subcategory, vendor-specific code (verbatim), free-text reason;
- the **affected assets** — feeder(s), DT(s), substation(s), lines, with optional geometry;
- the **network context** — DISCOM org hierarchy (Zone > Circle > Division > Subdivision > Substation);
- the **affected area** — CAP-style text + admin areas + GeoJSON polygon;
- the **timing** — window, ETR (estimated restoration), actual restoration, SLA target;
- the **impact** — customers affected, de-/energised UsagePoints (CIM);
- the **response** — back-feed, resource status, complaint count;
- the **public info** — CAP info block for web / push (`msgType`, `severity`, headline, instruction);
- the **provenance** — source (manual / auto), AMISP code, raw signal, alarm refs into `MeterData`.

Where an outage is auto-detected from smart-meter signals, `provenance` links back to the originating alarm in the [MeterData `AlarmProfile`](../smart-meter-data-exchange/README.md).

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (issuer) | `did:web` on owned domain | `did:web:ies.pvvnl.in` |
| Outage | DISCOM-minted ID (stable across UPDATEs and the final RESTORED record) | `PVVNL-OUTAGE-2026-06-29-0117` |
| Feeder / DT / substation | `did:web` under DISCOM domain (existing IDs wrapped) | `did:web:ies.pvvnl.in:assets:feeder:F02` |
| Alarm reference into MeterData | `meterRef` + `alarmRef` per the `AlarmProfile` | per [MeterData v0.6](../../schemas/MeterData/v0.6/README.md) |

References to **affected meters** are the same `did:web` IDs used by Smart Meter Data Exchange. References to **affected consumers** are kept aggregate (counts only) in the public record; consumer-level push goes through a separate channel with consent.

## 4. Definitions

- **Planned shutdown (SD)** — outage notified in advance for maintenance.
- **Unplanned breakdown (BD)** — fault-induced outage; cause unknown at the moment of detection.
- **Roster / load-shedding (RS)** — scheduled load-relief outage; aligned to a published roster.
- **CAP** (Common Alerting Protocol) — OASIS standard for emergency push alerts; the public-info block follows its shape.
- **SAIDI / SAIFI** — System Average Interruption Duration / Frequency Indices (IEEE 1366); computed from outage records.
- **ETR** — Estimated Time of Restoration.
- **CIM UsagePoint** — IEC 61968 concept; the connection point at which an outage is observed.
- **OMS** — Outage Management System; the DISCOM's source system.

## 5. Basis of Standards

IES order of preference: **IS → CEA → IEC → IEEE**. For outage publication, the standards compose by layer:

- **IEC 61968-3 (CIM)** — outage / UsagePoint data semantics, planned vs unplanned.
- **IEEE 1782** — cause categories (§4.4) and subcategories (§4.5); used with **IEEE 1366** for SAIDI / SAIFI.
- **OASIS CAP v1.2** (ITU-T X.1303) — push-alert envelope (`msgType`, `references`, `severity`, area + polygon, headline / instruction).
- **MultiSpeak** — AMI / MDMS → OMS detection flow and provenance.
- **GeoJSON (RFC 7946)** — GIS geometry, WGS84.
- **CEA / RDSS** — operational frame; restoration-time targets.

Beckn protocol v2 is the wire; W3C VC Data Model 2.0 / DID Core for issuer identity (`did:web`) and signature.

## 6. Where Indian Standards Do Not Yet Exist

No Indian standard defines an outage publication wire format. The combination above (CIM + IEEE 1782 / 1366 + CAP + MultiSpeak + GeoJSON) is an IES composition with no Indian equivalent.

The `outageClass` and `category` enums are **local** value sets (modelled on UPPCL OMS' "Down Info" vocabulary). Each enum's origin is declared in its `description` and a machine-readable `$comment` in the schema.

## 7. The Records

The Outage Visibility flow produces **one signed `OutageNotification` record per outage**, updated in place — `NEW` at detection, one or more `UPDATE` records as estimates change, `RESTORED` (or `CANCELLED`) at conclusion. Each version is signed.

Two carriage modes share the record:

1. **Pull** — the DISCOM's BPP exposes the active outages as a catalogue; outage-map operators, consumer apps and aggregators read the feed.
2. **Push** — CAP-aligned alert delivery to consumers / subscribers (consent-gated where applicable).

There is no separate "alert schema" — the push payload **is** the same `OutageNotification` record with the CAP info block populated.

## 8. Schedule I — Static Fields

The full, authoritative field tables are in the schema:

→ **[OutageNotification v0.1 — Field reference](../../schemas/OutageNotification/v0.1/README.md)**

Ten tables: `OutageNotification` (root), `OutageCause`, `OutageAsset`, `OutageNetworkContext`, `OutageAffectedArea`, `OutageImpact`, `OutageTiming`, `OutageResponse`, `OutagePublicInfo`, `OutageProvenance`. Each row carries `Field`, `Type`, the standard(s) it is **Based on**, and `Status`.

## 9. Schedule II — Report Templates

The **SAIDI / SAIFI roll-up** (IEEE 1366) is a derived report computed by the SERC or aggregator over a time window of `OutageNotification` records — using `OutageImpact.customersAffected` and `OutageTiming.actualRestoration - eventStart`. Methodology is in the schema's implementation note.

A second derived report is the **outage-map feed** — typically rendered by the DISCOM website or a third-party app from the live catalogue.

Neither is a separate IES schema.

## 10. How It Fits Together

```
Detection layer                       Publication layer

Smart meter                           DISCOM BPP
  AlarmProfile (LAST_GASP)              ├── OutageNotification feed (pull) ──► Outage-map operator
   │                                    │                                       Consumer app
   ▼                                    │                                       Aggregator
DISCOM OMS                              │
   │                                    └── OutageNotification push (CAP)  ──► Affected consumers
   ▼                                                                           (consent-gated)
OutageNotification draft   ─────────►   Sign + publish
(NEW)
   │
   ├── UPDATE (ETR change, scope change)
   └── RESTORED  (final)
```

A separate **feeder-status ingest** API (the [`FeederStatusIngest` OpenAPI spec](../../schemas/OutageNotification/v0.1/FeederStatusIngest.openapi.yaml)) standardises the *detection* layer between AMI / SCADA and the OMS, so that the publication layer has clean input. That layer is optional — DISCOMs whose OMS already has a clean detection feed can publish directly.

## 11. Points for Confirmation

1. **SD / BD / RS interpretation** — the precise mapping from OMS class codes to `outageClass` is per-state and being formalised.
2. **`category` value set** — currently UPPCL-modelled; will be widened as PVVNL and other pilot DISCOMs come online.
3. **Push delivery channel** — CAP envelope is decided; the underlying transport (Beckn push topic vs SMS gateway vs OEM app push) is per-DISCOM.
4. **Consumer-affected granularity** — counts only in the public record; consumer-level push depends on existing CIS contact data and consent.
5. **SAIDI / SAIFI methodology** — IEEE 1366 alignment with the SERC's existing computation needs to be reconciled state-by-state.

---

## Schemas Used in This Use Case

A **single schema** — **[OutageNotification v0.1](../../schemas/OutageNotification/v0.1/README.md)**.

Optionally, the **[`FeederStatusIngest` OpenAPI spec](../../schemas/OutageNotification/v0.1/FeederStatusIngest.openapi.yaml)** for the detection layer, and references back into **[MeterData v0.6](../../schemas/MeterData/v0.6/README.md)** for auto-detected outages (alarm references in `provenance`).

## Value Unlock

**For consumers** — a single trustworthy source for "is my supply out, why, and when will it be back?" — across DISCOMs.

**For outage-map operators and third-party apps** — one schema, one feed, every DISCOM that has adopted IES.

**For DISCOMs** — public communication on outages becomes a by-product of running the OMS, not a parallel manual process.

**For the SERC** — SAIDI / SAIFI become computable directly from signed records, comparable across licensees.

---

## Setup: Register → Discover → Exchange

Built on the four implementation steps in **[Part 3 — Implementing IES](../../how-you-implement-ies/README.md)**. Use-case-specific items only below.

### Register — DISCOM identity and feeder map

- [ ] [Identity setup](../../how-you-implement-ies/setup-register.md) complete
- [ ] Feeder / DT / substation identifier convention confirmed
- [ ] Network-context hierarchy (Zone > Circle > Division > Subdivision > Substation) registered

### Discover — outage feed catalogue

- [ ] [Discovery setup](../../how-you-implement-ies/setup-discovery.md) complete
- [ ] BPP catalogue entry published for the active-outage feed — `accessMethod: INLINE`
- [ ] (Optional) Push channel registered with the OEM consumer app / SMS gateway

### Exchange — OMS adapter and detection layer

- [ ] [Adapter built](../../how-you-implement-ies/build-adapter.md) for [OutageNotification v0.1](../../schemas/OutageNotification/v0.1/README.md)
- [ ] OMS class codes mapped to `outageClass` / `category` / `cause.category` / `cause.subcategory`
- [ ] (Optional) `FeederStatusIngest` ingest live; AMI alarm → OMS auto-detect proven
- [ ] One planned shutdown notified end-to-end (`NEW` → `UPDATE` → `RESTORED`)
- [ ] One unplanned breakdown notified end-to-end with `provenance` set
- [ ] SAIDI / SAIFI computation rehearsed against a back-test window
- [ ] Revocation / cancellation flow tested

### Team

- [ ] Operations / OMS SPOC
- [ ] IT SPOC
- [ ] Public-comms / consumer-affairs SPOC

---

## Dev kits and code

- **Schema source** — [`schemas/OutageNotification/v0.1/attributes.yaml`](../../schemas/OutageNotification/v0.1/attributes.yaml)
- **JSON Schema** — [`schema.json`](../../schemas/OutageNotification/v0.1/schema.json)
- **Design note** — [`OutageNotification_Design.md`](../../schemas/OutageNotification/v0.1/OutageNotification_Design.md)
- **Implementation guide** — [`OutageNotification_Implementation.md`](../../schemas/OutageNotification/v0.1/OutageNotification_Implementation.md)
- **Feeder-status ingest** — [`FeederStatusIngest.openapi.yaml`](../../schemas/OutageNotification/v0.1/FeederStatusIngest.openapi.yaml)
- **UPPCL fault-reason crosswalk** — [`fault_reason_crosswalk.json`](../../schemas/OutageNotification/v0.1/fault_reason_crosswalk.json)
- **PVVNL planned-shutdown CSV tools** — [`tools/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/OutageNotification/v0.1/tools)
- **Example payloads** — [`examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/OutageNotification/v0.1/examples) (planned multi-feeder shutdown; unplanned breakdown with provenance; restoration UPDATE)
- **Validation** — `python3 scripts/validate_schema.py schemas/OutageNotification/v0.1/schema.json <your-outage.json>`

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IEC 61968-3 (CIM) | Outage / UsagePoint data semantics; planned vs unplanned |
| IEEE 1782-2022 §4.4 / §4.5 | Cause categories and subcategories |
| IEEE 1366 | SAIDI / SAIFI computation |
| OASIS CAP v1.2 (ITU-T X.1303) | Push-alert envelope shape |
| MultiSpeak | AMI / MDMS → OMS detection flow |
| GeoJSON (RFC 7946) | GIS geometry; WGS84 |
| RDSS / CEA operational guidance | Restoration-time targets, operational frame |
| Beckn Protocol v2 | Pull catalogue + push delivery on the wire |
| W3C VC Data Model 2.0; W3C DID Core | Issuer identity; signature |

## Annexure B — Example Payloads

→ **[`schemas/OutageNotification/v0.1/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/OutageNotification/v0.1/examples)**

## Annexure C — JSON Schema

- Canonical reference: `https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/`
- **[`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/schema.json)** — bundled JSON Schema (Draft 2020-12)
- **[`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/context.jsonld)**
- **[`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/vocab.jsonld)**
