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

IES Data Exchange uses the **Beckn Protocol** — an open, decentralised, peer-to-peer commerce protocol — adapted for energy data. Instead of goods or services, the "items" being exchanged are structured energy datasets.

```
Data Consumer (BAP)              Data Provider (BPP)
e.g. DISCOM requesting           e.g. AMISP publishing
meter telemetry                  smart meter data

     │── select ───────────────────────────────────────>│
     │<── on_select (catalog + terms) ─────────────────│
     │── init ────────────────────────────────────────>│
     │<── on_init (ready) ─────────────────────────────│
     │── confirm ─────────────────────────────────────>│
     │<── on_confirm (active) ─────────────────────────│
     │── status ──────────────────────────────────────>│
     │<── on_status (data delivered inline) ───────────│
```

Data is delivered **inline** in the `on_status` response — embedded directly in the Beckn message rather than via an external download URL. This makes the exchange verifiable and auditable end-to-end.

> Steps before `confirm` and after `on_confirm` are optional. A minimal exchange is `confirm` → `on_confirm`, with the payload carried in the callback. Add `select`/`init` when terms need negotiating, `publish-catalog`/`discover` when the consumer doesn't yet know the provider, and `status`/`on_status` when delivery is asynchronous. See [Quick Start](./quick-start.md) for picking the right shape.

---

## What Data Can Be Exchanged

IES Data Exchange currently supports three dataset types:

| Schema | Description | Typical Flow |
|---|---|---|
| `IES_Report` | Smart meter telemetry — 15-minute interval kWh readings in OpenADR 3.1.0 format | AMISP → DISCOM |
| `IES_ARR_Filing` | Aggregate Revenue Requirement — cost line items by fiscal year | DISCOM → SERC |
| `IES_Policy` + `IES_Program` | Tariff rate structures — energy slabs, time-of-day surcharges | SERC → DISCOM |

---

## Key Components

| Component | Role |
|---|---|
| **ONIX Adapter** | Beckn-compatible adapter that handles signing, routing, and schema validation. Runs as a Docker service. |
| **BAP** | Beckn Application Platform — the data-consuming side. Your application calls the BAP adapter. |
| **BPP** | Beckn Provider Platform — the data-providing side. Your server receives requests and delivers data. |
| **IES Networks** | Two networks anchored at the `indiaenergystack.in` DeDi namespace: `indiaenergystack.in/test-ies-data-sharing-network` for pre-production / certification, and `indiaenergystack.in/ies-data-sharing-network` for live exchange. The devkit sandbox is local-only and uses placeholder identities. |
| **sandbox-bpp** | A pre-built provider stub that auto-responds with real IES test data — bundled in the devkit for local development. |

---

## Sections in This Chapter

| Page | What you'll learn |
|---|---|
| [Quick Start](./quick-start.md) | Run a complete exchange in under 10 minutes — clone, start, send `confirm`, see `on_confirm`. Includes onboarding checklist. |
| [Core Concepts](./concepts.md) | DEG primitives, DatasetItem, inline delivery, context invariants |
| [Architecture](./architecture.md) | Stack topology, generic Beckn ladder, `transactionId`/`messageId` rules |
| [Registry Setup](./registry-setup.md) | Going beyond sandbox identity — DeDi namespace, subscriber record, ONIX config |
| [Use Cases](./use-cases/README.md) | Detailed walkthroughs for each dataset type |

---

## Mock BPP (cloud sandbox) — planned

The devkit ships a local `sandbox-bpp` container for development. A separate **cloud-hosted Mock BPP** is planned as additional scope outside the devkit — a long-lived sandbox provider that BAP implementors can transact against without running anything locally, and that the network can use for **automated conformance testing and certification** of new BAPs.

Details (URL, supported use cases, conformance suite) — TBD.

---

## Related Repositories

- [DEG Devkits — Data Exchange](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange)
- [DDM DatasetItem Schema](https://github.com/beckn/DDM/tree/main/specification/schema/DatasetItem/v1)
- [ies-docs Implementation Guide](https://github.com/India-Energy-Stack/ies-docs/tree/main/implementation-guides/data_exchange)
