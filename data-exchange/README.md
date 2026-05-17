# IES Data Exchange

**IES Data Exchange** is a federated, policy-governed way for energy-sector participants — [AMISPs](../glossary.md#amisp), [DISCOMs](../glossary.md#discom), [SERCs](../glossary.md#serc), and others — to discover, contract, and exchange structured datasets. [Beckn](../glossary.md#beckn) is the **control plane**: it carries discovery, offer, consent, contract, and audit. The dataset bytes themselves move over the sector standard appropriate to each dataset class — a signed download URL for an [XBRL](../glossary.md#xbrl) filing, an [MQTT](../glossary.md#mqtt) topic for near-real-time telemetry, [OpenADR](../glossary.md#openadr) for DR events, and so on — handed off via Beckn's `accessMethod` field.

---

## The Problem It Solves

Today, energy data in India moves through bespoke bilateral channels:

- Regulatory filings arrive as PDFs, independently re-implemented across the sector
- Smart meter telemetry is locked inside proprietary [MDMS](../glossary.md#mdms) systems
- Tariff policies are interpreted differently by each DISCOM
- There is no standard for discovery, access terms, or audit trails

IES Data Exchange replaces these ad-hoc arrangements with **two complementary layers**:

1. **Control plane (Beckn Protocol v2.0 + IES schemas)** — how participants find each other, negotiate terms, give consent, sign contracts, and produce auditable records.
2. **Data plane (existing sector standards)** — how the bytes actually move, using whatever protocol the dataset class already standardises on ([DLMS-COSEM](../glossary.md#dlms-cosem), [IEC 61968](../glossary.md#iec-61968) / [CIM](../glossary.md#cim) / [MultiSpeak](../glossary.md#multispeak), [OpenADR](../glossary.md#openadr), [XBRL](../glossary.md#xbrl), [Akoma Ntoso](../glossary.md#akoma-ntoso), or a plain signed URL).

---

## How It Works

The **minimal exchange** is a single Beckn round-trip:

```
Data Consumer (BAP)                          Data Provider (BPP)
e.g. DISCOM consuming                        e.g. AMISP publishing
meter telemetry                              smart meter data

     │── confirm ──────────────────────────────────────────>│
     │<── on_confirm (carries the agreed accessMethod) ─────│
```

The `on_confirm` callback delivers either the dataset **inline** (small batches), a **signed download URL** (typical for files), or a **transport-specific credential** — an MQTT topic + token, a Kafka consumer config, an S3 prefix, a REST endpoint — that the BAP uses to fetch or stream the data over the appropriate sector protocol. The `accessMethod` field on the [DatasetItem](./concepts.md#the-datasetitem-schema) declares which mode applies.

That's enough for a pre-agreed bilateral exchange. The full Beckn lifecycle adds optional phases on top: `publish-catalog`/`discover` (consumer doesn't know the provider yet), `select`/`init` (terms need negotiating), `status`/`on_status` (delivery prepared asynchronously after `on_confirm`), `update`/`on_update` (credential rotation). See [Concepts § Beckn Protocol Lifecycle](./concepts.md#beckn-protocol-lifecycle) for the full picture.

### Why Beckn is not the payload wire

Wrapping every meter reading or every byte of a 50 MB filing in a signed Beckn message would be operationally heavy and would duplicate work the sector standards already do well. **Beckn coordinates; the existing protocols move bytes.** Expect **batch or near-real-time delivery after MDM validation** for smart-meter data; sub-minute streaming uses a transport credential handed off via Beckn, not Beckn itself.

---

## What Data Can Be Exchanged

The devkit ships **prebuilt schemas** for three IES dataset types. The table below names common integration examples for each — *these are examples seen in utility integrations; confirm the actual interface with your AMISP / HES / vendor stack.*

| Dataset (`schema`) | Beckn role | Common integration examples | Transfer pattern | Confirm with your vendor |
|---|---|---|---|---|
| Smart meter telemetry (`IES_Report`) | discovery + contract + consent + audit | Field: [DLMS-COSEM / IS 15959](../glossary.md#dlms-cosem). HES↔MDM and enterprise: [IEC 61968-9 / CIM / MultiSpeak v3.0](../glossary.md#iec-61968). Optional event / near-real-time adapter: [MQTT 5.0](../glossary.md#mqtt). [OpenADR 3.1.0](../glossary.md#openadr) for DR / DER events only — *not* generic interval reads. | Batch or near-real-time after MDM validation; signed URL or REST for bulk; MQTT for subscribed events | Which standard is actually deployed on your HES↔MDM interface and field network |
| ARR filing (`IES_ARR_Filing`) | discovery + contract + audit | [XBRL / iXBRL](../glossary.md#xbrl) (target). Current SERC portal practice: PDF/A + spreadsheet annexures. | HTTPS REST or signed object URL | Which annexure schema your SERC accepts today |
| Tariff policy (`IES_Policy` + `IES_Program`) | discovery + contract | Order text: [Akoma Ntoso / LegalDocML](../glossary.md#akoma-ntoso) XML. Schedules / slabs / [ToD](../glossary.md#tod) / subsidies: versioned CSV / JSON / JSON-LD with [DCAT 3](../glossary.md#dcat-3) metadata. | HTTPS REST or signed artifact | How your state publishes tariff orders today |

**Any JSON payload can be exchanged** beyond these three — the wire envelope carries arbitrary data inside `dataPayload`. If your payload is **self-describing** (declares a JSON-LD `@context` and `@type`), the ONIX adapter automatically validates it against the schema published at that context URL. Payloads without `@context` flow through unvalidated — useful for ad-hoc or evolving data shapes. See [Concepts § How schema validation works](./concepts.md#how-schema-validation-works) for the dispatch mechanics.

---

## Key Components

| Component | Role |
|---|---|
| **[BAP](../glossary.md#bap)** (data consumer) | Your application on the consuming side — DISCOM, regulator, VAS provider. Beckn calls it the Beckn Application Platform. |
| **[BPP](../glossary.md#bpp)** (data provider) | Your server on the providing side — AMISP, DISCOM, SERC, data custodian. Beckn calls it the Beckn Provider Platform. |
| **[ONIX](../glossary.md#onix) Adapter** | The Beckn protocol adapter — signs and verifies messages, routes between BAP and BPP, validates payload schemas. Your code talks to ONIX; ONIX talks Beckn. Runs as a Docker service. See [Architecture](./architecture.md) for details. |
| **IES Networks** | Two networks anchored at the `indiaenergystack.in` [DeDi](../glossary.md#dedi) namespace: `test-ies-data-sharing-network` for pre-production / certification and `ies-data-sharing-network` for live exchange. The devkit sandbox is local-only and uses placeholder identities. See [Registry Setup](./registry-setup.md). |
| **sandbox-bpp / sandbox-bap** | Pre-built containers bundled in the devkit. `sandbox-bpp` auto-responds with IES test data; `sandbox-bap` logs every callback so you can inspect it. You replace these with your own application in production. |

---

## Sections in This Chapter

If you're new, read in this order: **Concepts → Quick Start → Registry Setup**. Architecture is a deeper reference you can dip into when needed. End-to-end use cases that exercise this protocol — meter telemetry, ARR filings, tariff publication — live in the top-level [Use Cases](../use-cases/README.md) section.

| Page | What you'll learn |
|---|---|
| [Core Concepts](./concepts.md) | Beckn lifecycle, the minimal flow, DatasetItem, inline delivery, context invariants |
| [Quick Start](./quick-start.md) | Run a complete exchange in under 10 minutes — clone, start, send `confirm`, see `on_confirm`. Includes the BAP and BPP onboarding checklists. |
| [Registry Setup](./registry-setup.md) | Going beyond sandbox identity — DeDi namespace, subscriber record, ONIX config, how to contact the IES NFO |
| [Architecture](./architecture.md) | Stack topology, generic Beckn ladder, endpoints (sandbox vs production) |

---

## Mock BPP (cloud sandbox) — planned

The devkit ships a local `sandbox-bpp` container for development. A separate **cloud-hosted Mock BPP** is planned as additional scope outside the devkit — a long-lived sandbox provider that BAP implementors can transact against without running anything locally, and that the network can use for **automated conformance testing and certification** of new BAPs.

Details (URL, supported use cases, conformance suite) — TBD.

---

## Related Repositories

- [DEG Devkits — Data Exchange](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange)
- [DDM DatasetItem Schema](https://github.com/beckn/DDM/tree/main/specification/schema/DatasetItem/v1)
- [ies-docs Implementation Guide](https://github.com/India-Energy-Stack/ies-docs/tree/main/implementation-guides/data_exchange)
