# Core Concepts — Data Exchange

This page explains the conceptual foundations of IES Data Exchange before you start integrating.

---

## The Digital Energy Grid (DEG) Primitives

IES Data Exchange is built on the **Digital Energy Grid (DEG)** architecture, which defines six primitives for energy transactions. Understanding these helps you model your data correctly.

### 1. Energy Resource

Any physical or logical entity that produces, consumes, stores, or manages energy. This includes:
- Generators (solar plants, wind farms)
- Storage systems (batteries)
- Consumption devices (EVs, appliances)
- Infrastructure (smart meters, transformers)
- Service providers (DISCOMs, AMISPs, SERCs)

In a data exchange, the **data provider (BPP)** and **data consumer (BAP)** are both Energy Resources.

### 2. Energy Resource Address (ERA)

A globally unique digital identifier for any Energy Resource — analogous to a domain name or IP address. ERAs enable discovery and addressing across federated networks.

```
meter-KA-98765432.amisp.bescom.in        ← smart meter
bescom.discom.karnataka.ies.in           ← DISCOM
aperc.regulator.andhra.ies.in           ← state regulator
```

### 3. Energy Credentials

Verifiable attestations about Energy Resources. In data exchange, credentials may gate access — a BPP can require the BAP to present a valid credential (e.g. a regulatory mandate credential) before delivering a dataset.

### 4. Energy Intent

A digital expression of what data a consumer needs — what dataset, from what source, for what time range, under what access terms.

### 5. Energy Catalogue

A structured listing of available datasets published by a BPP — including dataset type, time coverage, delivery mode, and pricing/terms.

### 6. Energy Contract

The formalized agreement that results from a BAP's intent matching a BPP's catalogue — the confirmed data exchange order.

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

Every Beckn message shares the same envelope. Field names follow the v2.0 wire format (camelCase):

```json
{
  "context": {
    "networkId": "indiaenergystack.in/test-ies-data-sharing-network",
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

### Context invariants

Two `context` rules govern correlation across the network — get either wrong and the adapter will reject the message:

- **`transactionId` is constant** across every message in one exchange. From the first `discover`/`select`/`confirm` to the final `on_status`/`on_update`, the same UUID flows through. It is how all parties (and registry-level audit trails) stitch the conversation together.
- **`messageId` is the same on a request and its paired callback.** `confirm` and the matching `on_confirm` share one `messageId`; a subsequent `status` gets a *new* `messageId`, which its `on_status` reuses. Treat the pair as one logical message with two hops.

Authoritative reference: [beckn/protocol-specifications-v2 — `api/v2.0.0`](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0).

---

## The DatasetItem Schema

IES describes exchangeable datasets with the **DDM DatasetItem schema** from [beckn/DDM](https://github.com/beckn/DDM/tree/main/specification/schema/DatasetItem/v1.1). On the wire, the dataset rides inside `message.contract.commitments[].resources[]` and is qualified by `resourceAttributes` carrying the `@context` of the DatasetItem schema:

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

Canonical schema definitions (today): [beckn/DEG — `ies-specs` branch](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies). They are currently hosted under the Beckn DEG repo on a working branch; **TBD: these will be migrated to a public repository under the [India-Energy-Stack](https://github.com/India-Energy-Stack) GitHub organisation** once the IES schema family is stabilised. Links from these docs will be updated when the move happens.

---

## ONIX Adapter

**ONIX** is the Beckn protocol adapter used by IES. It handles request signing (Ed25519), routing between BAP and BPP, schema validation (`dataPayload` against the declared IES schema), and async callback delivery — so your application never deals with protocol-level concerns.

In the devkit, ONIX runs as a Docker container behind `beckn-router` on `:9000`. See [Architecture](./architecture.md) for the topology, and [Registry Setup](./registry-setup.md) for the identity/configuration mapping.

---

## Network

IES Data Exchange participants transact on a Beckn network identified by a `networkId`:

| Parameter | Value |
|---|---|
| Network ID (test) | `indiaenergystack.in/test-ies-data-sharing-network` |
| Network ID (prod) | `indiaenergystack.in/ies-data-sharing-network` |
| Domain | `deg:data-exchange` |

Both networks are anchored at the `indiaenergystack.in` DeDi namespace. Membership in test does not imply membership in prod — every participant is referenced into each network's registry separately, and ONIX enforces the partition via its `allowedNetworkIDs` config. To join, see [Registry Setup](./registry-setup.md). The canonical network onboarding guide is at [docs.nfh.global/beckn](https://docs.nfh.global/beckn).
