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
| **IES Testnet** | The shared network (`nfh.global/testnet-deg`) for discovery and routing. |
| **Mock BPP** | A pre-built FastAPI server that auto-responds with real IES test data — for bootcamp and development. |

---

## Sections in This Chapter

| Page | What you'll learn |
|---|---|
| [Core Concepts](./concepts.md) | DEG primitives, Beckn lifecycle, inline data delivery |
| [Onboarding Guide](./onboarding.md) | Step-by-step setup for BAPs and BPPs |
| [Architecture](./architecture.md) | Full transaction flow, component diagram, network config |
| [Quick Start](./quick-start.md) | Run a complete exchange in under 10 minutes |
| [Use Cases](./use-cases/README.md) | Detailed walkthroughs for each dataset type |

---

## Related Repositories

- [DEG Devkits — Data Exchange](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange)
- [DDM DatasetItem Schema](https://github.com/beckn/DDM/tree/main/specification/schema/DatasetItem/v1)
- [ies-docs Implementation Guide](https://github.com/India-Energy-Stack/ies-docs/tree/main/implementation-guides/data_exchange)
