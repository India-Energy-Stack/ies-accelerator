# IES Data Exchange

**IES Data Exchange** is a federated, policy-governed protocol for discovering and exchanging structured energy datasets across the Indian power sector. It enables AMISPs, DISCOMs, SERCs, and other sector participants to share data — telemetry, regulatory filings, tariff orders — in a standardised, auditable, and credential-gated way.

---

## The Problem It Solves

Today, energy data in India moves through bespoke bilateral channels:

- Regulatory filings arrive as PDFs, independently re-implemented across the sector
- Smart meter telemetry is locked inside proprietary MDMS systems
- Tariff policies are interpreted differently by each DISCOM
- There is no standard for discovery, access terms, or audit trails

IES Data Exchange replaces these ad-hoc arrangements with a **single, open protocol stack** based on Beckn Protocol v2.0 and IES schemas.

---

## How It Works

IES Data Exchange uses the **Beckn Protocol** — an open, decentralised, peer-to-peer protocol — adapted for energy data. Instead of goods or services, the "items" being exchanged are structured energy datasets.

The **minimal exchange** is a single round-trip:

```
Data Consumer (BAP)                          Data Provider (BPP)
e.g. DISCOM consuming                        e.g. AMISP publishing
meter telemetry                              smart meter data

     │── confirm ──────────────────────────────────────────>│
     │<── on_confirm (payload delivered inline) ────────────│
```

That's enough for a pre-agreed bilateral exchange. The full Beckn lifecycle adds optional phases on top: `publish-catalog`/`discover` (consumer doesn't know the provider yet), `select`/`init` (terms need negotiating), `status`/`on_status` (payload prepared asynchronously after `on_confirm`), `update`/`on_update` (credential rotation). See [Concepts § Beckn Protocol Lifecycle](./concepts.md#beckn-protocol-lifecycle) for the full picture.

Data delivery supports multiple modes — **inline** (dataset embedded directly in the Beckn callback, end-to-end signed and verifiable, best for moderate-sized datasets), **signed download URL** (typical for larger datasets — the callback carries a URL and checksum), or transport-specific streaming credentials (MQTT, Kafka, S3 datalake, REST API) carried inline. The `accessMethod` field on the DatasetItem declares which mode applies. See [Concepts § The DatasetItem Schema](./concepts.md#the-datasetitem-schema) for the full list.

---

## What Data Can Be Exchanged

The devkit ships **prebuilt schemas** for three IES dataset types — the sector's most common shapes:

| Schema | Description | Typical Flow |
|---|---|---|
| `IES_Report` | Smart meter telemetry — 15-minute interval kWh readings in OpenADR 3.1.0 format | AMISP → DISCOM |
| `IES_ARR_Filing` | Aggregate Revenue Requirement — cost line items by fiscal year | DISCOM → SERC |
| `IES_Policy` + `IES_Program` | Tariff rate structures — energy slabs, time-of-day surcharges | SERC → DISCOM |

**Any JSON payload can be exchanged** — the wire envelope carries arbitrary data inside `dataPayload`. If your payload is **self-describing** (declares a JSON-LD `@context` and `@type`), the ONIX adapter automatically validates it against the schema published at that context URL. Payloads without `@context` flow through unvalidated — useful for ad-hoc or evolving data shapes. See [Concepts § How schema validation works](./concepts.md#how-schema-validation-works) for the dispatch mechanics.

---

## Key Components

| Component | Role |
|---|---|
| **BAP** (data consumer) | Your application on the consuming side — DISCOM, regulator, VAS provider. Beckn calls it the Beckn Application Platform. |
| **BPP** (data provider) | Your server on the providing side — AMISP, DISCOM, SERC, data custodian. Beckn calls it the Beckn Provider Platform. |
| **ONIX Adapter** | The Beckn protocol adapter — signs and verifies messages, routes between BAP and BPP, validates payload schemas. Your code talks to ONIX; ONIX talks Beckn. Runs as a Docker service. See [Architecture](./architecture.md) for details. |
| **IES Networks** | Two networks anchored at the `indiaenergystack.in` DeDi namespace: `test-ies-data-sharing-network` for pre-production / certification and `ies-data-sharing-network` for live exchange. The devkit sandbox is local-only and uses placeholder identities. See [Registry Setup](./registry-setup.md). |
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
