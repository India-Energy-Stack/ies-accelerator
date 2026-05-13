# Core Concepts — Data Exchange

This page explains the conceptual foundations of IES Data Exchange before you start integrating.

---

## The Digital Energy Grid (DEG) Primitives

IES Data Exchange is built on the broader **Digital Energy Grid (DEG)** architecture. For this chapter you only need to know that DEG models four things that surface in the wire format:

| Primitive | What it is | Where it shows up |
|---|---|---|
| **Energy Resource** | Any entity that produces, consumes, stores or manages energy — meters, generators, DISCOMs, SERCs, AMISPs. In a data exchange the BAP and BPP are both Energy Resources. | `participants[]`, `provider` |
| **Energy Catalogue** | A BPP's listing of available datasets, with terms (price, SLA, delivery mode). | `publish-catalog` / `on_discover` |
| **Energy Contract** | The agreement created when a BAP commits to consume a catalogue entry. | `message.contract` (carries `commitments[]`, `consideration`, `performance[]`, `settlements[]`) |
| **Energy Credentials** | Verifiable attestations that may gate access (e.g. a regulatory-mandate credential the BPP requires before releasing data). | Not used in the basic flow; relevant to credential-gated use cases. |

Energy Resource Address (ERA) and Energy Intent are additional DEG concepts not yet surfaced by the data-exchange use cases shipped today; you can read about them in the broader DEG specification when needed.

---

## Beckn Protocol Lifecycle

IES Data Exchange uses the **Beckn Protocol v2.0** interaction model. The full set of actions:

| Phase | BAP calls | BPP responds | When you need it |
|---|---|---|---|
| Discovery | `discover` | `on_discover` | Consumer doesn't yet know which provider to contract with. Requires the BPP to have called `publish-catalog` earlier. |
| Negotiation | `select` / `init` | `on_select` / `on_init` | Terms (price, SLA, delivery mode) need to be agreed before commitment. |
| Commitment | `confirm` | `on_confirm` | **The minimal flow.** Payload can be delivered inline here. |
| Polled delivery | `status` | `on_status` | Payload is prepared asynchronously after `on_confirm`. |
| Post-fulfilment | `update` | `on_update` | Credential rotation, contract amendments. |

> **Minimal viable exchange:** `confirm` → `on_confirm`, with the dataset embedded in the callback. Everything else is optional.

Beckn is **asynchronous**: every call returns an immediate `ACK`, and the paired response arrives as a callback (`on_*`) to the BAP's webhook URL. The ONIX adapter manages this asynchrony transparently.

### Message Structure

Every Beckn message shares the same envelope. Field names follow the v2.0 wire format (camelCase). The example below shows what the **devkit sandbox** emits — when you join a real IES network in [Phase 2](./quick-start.md#phase-2--swap-in-your-real-identity), `networkId`, `bapId`/`bppId` and `bapUri`/`bppUri` change to your DeDi-published values:

```json
{
  "context": {
    "networkId": "nfh.global/testnet-deg",
    "version": "2.0.0",
    "action": "confirm",
    "bapId": "bap.example.com",
    "bapUri": "http://beckn-router:9000/bap/receiver",
    "bppId": "bpp.example.com",
    "bppUri": "http://beckn-router:9000/bpp/receiver",
    "transactionId": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "messageId": "1e2f3a4b-5c6d-7890-4567-890123456789",
    "timestamp": "2026-04-01T09:25:00Z",
    "schemaContext": ["https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.1/context.jsonld"]
  },
  "message": { /* action-specific payload */ }
}
```

(`nfh.global/testnet-deg` is the placeholder the devkit example payloads ship with. Real participants on the IES test network emit `networkId: indiaenergystack.in/test-ies-data-sharing-network`.)

### Context invariants

Two `context` rules govern correlation across the network — get either wrong and the adapter will reject the message:

- **`transactionId` is constant** across every message in one exchange. From the first `discover`/`select`/`confirm` to the final `on_status`/`on_update`, the same UUID flows through. It is how all parties (and registry-level audit trails) stitch the conversation together.
- **`messageId` is the same on a request and its paired callback.** `confirm` and the matching `on_confirm` share one `messageId`; a subsequent `status` gets a *new* `messageId`, which its `on_status` reuses. Treat the pair as one logical message with two hops.

Authoritative reference: [beckn/protocol-specifications-v2 — `api/v2.0.0`](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0).

---

## The DatasetItem Schema

**DDM** (Decentralised Data Marketplace) is Beckn's generic dataset envelope schema; **`DatasetItem`** is the per-dataset record shape that IES uses inside Beckn's `resources[]` / `commitments[]` to carry an actual dataset payload. On the wire, the dataset rides inside `message.contract.commitments[].resources[]` and is qualified by `resourceAttributes` carrying the `@context` of the DatasetItem schema:

```json
"resources": [{
  "id": "ds-ami-meter-data-blr-zone-a-q1-2026",
  "descriptor": { "name": "IntelliGrid AMI Meter Data — Bengaluru Zone A — Q1 2026" },
  "resourceAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.1/context.jsonld",
    "@type": "DatasetItem",
    "accessMethod": "INLINE",
    "dataPayload": { /* inline IES_Report, IES_ARR_Filing, ... */ }
  }
}]
```

Full payloads live in the devkit: [uc1-meter-data/examples/on-status-response-ready-inline.json](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/uc1-meter-data/examples/on-status-response-ready-inline.json) and siblings.

The `accessMethod` field declares how data is delivered:

| Mode | Description |
|---|---|
| `INLINE` | Embedded in the Beckn callback message (typically `on_confirm` or `on_status`) |
| `DOWNLOAD` | BPP provides a signed download URL + checksum |
| `MQTT` / `KAFKA` / `API` / `DATA_LAKE` | Streaming transports — connection credentials delivered in `on_confirm.performance[].performanceAttributes` |
| `DATA_ENCLAVE` | Data accessible only within a secure compute environment |
| `OFF_CHANNEL` | Delivery through an agreed out-of-band channel |

IES Data Exchange today primarily uses `INLINE` — data arrives as part of the protocol message, making the exchange end-to-end verifiable.

---

## IES Data Schemas

The body inside `dataPayload` is one of the IES schemas; the relevant one for each use case is described on the corresponding [use-case page](./use-cases/README.md):

| Schema | Carried in | Use case |
|---|---|---|
| `IES_Report` (OpenADR 3.1.0) | 15-min interval meter readings | [Meter Telemetry](./use-cases/meter-telemetry/) |
| `IES_ARR_Filing` | Aggregate Revenue Requirement line items by fiscal year | [ARR Filings](./use-cases/arr-filings.md) |
| `IES_Policy` (+ `IES_Program`) | Machine-readable tariff rate structures (energy slabs, ToD surcharges) | [Tariff Policies](./use-cases/tariff-policies.md) |

Canonical schema definitions today: [beckn/DEG — `ies-specs` branch](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies).

> **TBD — schema migration.** The IES schema family is currently hosted on a working branch under beckn/DEG. It will move to a public repository under the [India-Energy-Stack](https://github.com/India-Energy-Stack) GitHub organisation once stabilised. Links throughout these docs will be updated when the move happens.

---

## ONIX Adapter and Network

**ONIX** is the Beckn protocol adapter — it signs, verifies, routes, and validates so your application never deals with protocol-level concerns. See [Architecture § Stack topology](./architecture.md#stack-topology).

IES operates two networks anchored at the `indiaenergystack.in` DeDi namespace (`test-ies-data-sharing-network` and `ies-data-sharing-network`). The `domain` field in every message is `deg:data-exchange`. See [Registry Setup](./registry-setup.md) for joining either.
