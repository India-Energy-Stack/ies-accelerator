# IES Data Exchange

**IES Data Exchange** is a federated, policy-governed way for energy-sector participants — [AMISPs](../glossary.md#amisp), [DISCOMs](../glossary.md#discom), [SERCs](../glossary.md#serc), and others — to discover, contract, and exchange structured datasets. [Beckn](../glossary.md#beckn) always carries the **control plane** — discovery, offer, consent, contract, and audit. The **payload** has two equally valid modes, chosen per dataset:

- **Inline over Beckn** — for small, simple payloads (a single ARR row, a tariff slab, a small JSON document, a pre-agreed bilateral exchange) the dataset is embedded directly in the `on_confirm` callback. End-to-end signed, no second hop, no extra infrastructure to operate. This is the *easiest* path and is the right default whenever the payload fits comfortably in a signed message.
- **Access-pattern handoff via Beckn** — for bulky datasets, telemetry streams, or anything that already has an established sector channel (SFTP drop, Kafka topic, MQTT broker, signed S3 URL, OpenADR endpoint, an XBRL artifact), Beckn does the discovery / authentication / contract / consent / audit, and the `on_confirm` (or `on_status`) callback delivers the **access method** — endpoint, credentials, topic, URL — that the BAP uses to pull or subscribe over that existing channel.

Both modes use the same Beckn lifecycle and the same `accessMethod` field on the [DatasetItem](./concepts.md#the-datasetitem-schema) to declare which one applies.

---

## The Problem It Solves

Today, energy data in India moves through bespoke bilateral channels:

- Regulatory filings arrive as PDFs, independently re-implemented across the sector
- Smart meter telemetry is locked inside proprietary [MDMS](../glossary.md#mdms) systems
- Tariff policies are interpreted differently by each DISCOM
- There is no standard for discovery, access terms, or audit trails

IES Data Exchange replaces these ad-hoc arrangements with a **single coordination layer (Beckn Protocol v2.0 + IES schemas)** that handles discovery, terms, consent, contracts, and auditable records — and then either carries the payload **inline** in the same flow (for small / simple datasets) or hands off an **access method** to whatever channel the dataset class already standardises on ([DLMS-COSEM](../glossary.md#dlms-cosem), [IEC 61968](../glossary.md#iec-61968) / [CIM](../glossary.md#cim) / [MultiSpeak](../glossary.md#multispeak), [OpenADR](../glossary.md#openadr), [XBRL](../glossary.md#xbrl), [Akoma Ntoso](../glossary.md#akoma-ntoso), MQTT, Kafka, SFTP, signed URL).

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

The `on_confirm` callback delivers the payload in whichever mode was agreed at contract time:

- **Inline** — the dataset is embedded directly in the callback, end-to-end signed and verifiable. Best for small batches, a single regulatory record, a tariff slab, or any pre-agreed bilateral exchange where the payload fits in a signed message. *This is the simplest possible workflow — no second channel to operate.*
- **Signed download URL** — the callback carries a URL + checksum + short-lived token; the BAP fetches the bytes over HTTPS. Typical for files (XBRL filings, PDF/A annexures, CSV exports).
- **Transport-specific access pattern** — the callback carries the credential to use an established channel: an MQTT topic + token, a Kafka consumer config, an SFTP path + key, an S3 prefix, a REST endpoint, an OpenADR VEN binding. The BAP then pulls or subscribes over that channel.

The `accessMethod` field on the [DatasetItem](./concepts.md#the-datasetitem-schema) declares which mode applies, and the same field can be re-negotiated per contract — the *same* dataset class can be delivered inline to a small consumer and via Kafka to a large one.

That's enough for a pre-agreed bilateral exchange. The full Beckn lifecycle adds optional phases on top: `publish-catalog`/`discover` (consumer doesn't know the provider yet), `select`/`init` (terms need negotiating), `status`/`on_status` (delivery prepared asynchronously after `on_confirm` — common when the access pattern is provisioned just-in-time, e.g. a fresh signed URL or a freshly-scoped Kafka credential), `update`/`on_update` (credential rotation). See [Concepts § Beckn Protocol Lifecycle](./concepts.md#beckn-protocol-lifecycle) for the full picture.

### Choosing inline vs access-pattern handoff

**Both modes are first-class.** The decision is operational, not architectural:

| Use **inline over Beckn** when… | Use **access-pattern handoff** when… |
|---|---|
| Payload is small (kilobytes, single record, one filing row) | Payload is bulky (multi-MB XBRL, full-day interval reads, historical bulk) |
| You want the simplest possible integration — one signed message, no second channel | The dataset already lives in an established channel (Kafka, MQTT, SFTP, S3, OpenADR) and you don't want to duplicate that pipe |
| End-to-end signing of the payload bytes matters | The native channel already provides the signing / SLA / throughput guarantees |
| The exchange is occasional or event-driven | The exchange is high-volume, streaming, or already operated to an SLA |

The point of Beckn here is to give every exchange — inline or handoff — the same discovery, consent, contract, and audit story.

---

## What Data Can Be Exchanged

The devkit ships **prebuilt schemas** for three IES dataset types. The table below names common integration examples for each — *these are examples seen in utility integrations; confirm the actual interface with your AMISP / HES / vendor stack.*

| Dataset (`schema`) | Beckn role | Common integration examples | Transfer pattern | Confirm with your vendor |
|---|---|---|---|---|
| Smart meter telemetry ([MeterData](../schemas/MeterData/README.md)) | discovery + contract + consent + audit | Field: [DLMS-COSEM / IS 15959](../glossary.md#dlms-cosem). HES↔MDM and enterprise: [IEC 61968-9 / CIM / MultiSpeak v3.0](../glossary.md#iec-61968). Optional event / near-real-time adapter: [MQTT 5.0](../glossary.md#mqtt). [OpenADR 3.1.0](../glossary.md#openadr) for DR / DER events only — *not* generic interval reads. | Inline for small samples / single-meter pulls; signed URL or REST for bulk batches after MDM validation; MQTT or Kafka access pattern for subscribed near-real-time events | Which standard is actually deployed on your HES↔MDM interface and field network |
| ARR filing ([ArrFiling](../schemas/ArrFiling/README.md)) | discovery + contract + audit | [XBRL / iXBRL](../glossary.md#xbrl) (target). Current SERC portal practice: PDF/A + spreadsheet annexures. | Inline when filing fits in a signed message; HTTPS REST or signed object URL for full filings with annexures | Which annexure schema your SERC accepts today |
| Tariff policy (`IES_Policy` + `IES_Program`) | discovery + contract | Order text: [Akoma Ntoso / LegalDocML](../glossary.md#akoma-ntoso) XML. Schedules / slabs / [ToD](../glossary.md#tod) / subsidies: versioned CSV / JSON / JSON-LD with [DCAT 3](../glossary.md#dcat-3) metadata. | Inline for slab / ToD tables; HTTPS REST or signed artifact for full order documents | How your state publishes tariff orders today |

**Any JSON payload can be exchanged** beyond these three — the wire envelope carries arbitrary data inside `dataPayload`. If your payload is **self-describing** (declares a JSON-LD `@context` and `@type`), the ONIX adapter automatically validates it against the schema published at that context URL. Payloads without `@context` flow through unvalidated — useful for ad-hoc or evolving data shapes. See [Concepts § How schema validation works](./concepts.md#how-schema-validation-works) for the dispatch mechanics.

---

## Key Components

| Component | Role |
|---|---|
| **[BAP](../glossary.md#bap)** (data consumer) | Your application on the consuming side — DISCOM, regulator, VAS provider. Beckn calls it the Beckn Application Platform. |
| **[BPP](../glossary.md#bpp)** (data provider) | Your server on the providing side — AMISP, DISCOM, SERC, data custodian. Beckn calls it the Beckn Provider Platform. |
| **[ONIX](../glossary.md#onix) Adapter** | The Beckn protocol adapter — signs and verifies messages, routes between BAP and BPP, validates payload schemas. Your code talks to ONIX; ONIX talks Beckn. Runs as a Docker service. See [Concepts § Architecture at a glance](./concepts.md#architecture-at-a-glance). |
| **IES Networks** | Two networks anchored at the `indiaenergystack.in` [DeDi](../glossary.md#dedi) namespace: `test-ies-data-sharing-network` for pre-production / certification and `ies-data-sharing-network` for live exchange. The devkit sandbox is local-only and uses placeholder identities. See [Registry Setup](./registry-setup.md). |
| **sandbox-bpp / sandbox-bap** | Pre-built containers bundled in the devkit. `sandbox-bpp` auto-responds with IES test data; `sandbox-bap` logs every callback so you can inspect it. You replace these with your own application in production. |

---

## Sections in This Chapter

If you're new, read in this order: **Concepts → Quick Start → Registry Setup**, ticking off the [Onboarding Checklist](../checklists/data-exchange-checklist.md) as you go. The [Appendix](./appendix.md) is reference material to dip into when needed. End-to-end use cases that exercise this protocol — meter telemetry, ARR filings, tariff publication — live in the top-level [Use Cases](../use-cases/README.md) section.

| Page | What you'll learn |
|---|---|
| [Core Concepts](./concepts.md) | Just enough theory: Beckn lifecycle, the minimal flow, trust, DatasetItem, schema families, validation, stack topology |
| [Quick Start](./quick-start.md) | A complete exchange in under 10 minutes, then three phases: run locally → go over the public internet (ngrok) → make the sandbox your own |
| [Registry Setup](./registry-setup.md) | Going beyond sandbox identity — DeDi namespace, subscriber record, ONIX config, how to contact the IES NFO |
| [Onboarding Checklist](../checklists/data-exchange-checklist.md) | One staged checklist from devkit sandbox to production go-live |
| [Appendix](./appendix.md) | Reference detail — context invariants, validation dispatch, endpoints, sequence diagram |

---

## Related Repositories

- [DEG Devkits — Data Exchange](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange)
- [DDM DatasetItem Schema](https://github.com/beckn/DDM/tree/main/specification/schema/DatasetItem/v1)
- [ies-docs Implementation Guide](https://github.com/India-Energy-Stack/ies-docs/tree/main/implementation-guides/data_exchange)
