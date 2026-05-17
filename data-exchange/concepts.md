# Core Concepts — Data Exchange

This page explains the conceptual foundations of IES Data Exchange before you start integrating.

---

## The Digital Energy Grid (DEG) Primitives

IES Data Exchange is built on the broader **[Digital Energy Grid (DEG)](../glossary.md#deg)** architecture. For this chapter you only need to know that DEG models four things that surface in the wire format:

| Primitive | What it is | Where it shows up |
|---|---|---|
| **Energy Resource** | Any entity that produces, consumes, stores or manages energy — meters, generators, [DISCOMs](../glossary.md#discom), [SERCs](../glossary.md#serc), [AMISPs](../glossary.md#amisp). In a data exchange the [BAP](../glossary.md#bap) and [BPP](../glossary.md#bpp) are both Energy Resources. | `participants[]`, `provider` |
| **Energy Catalogue** | A BPP's listing of available datasets, with terms (price, SLA, delivery mode). | `publish-catalog` / `on_discover` |
| **Energy Contract** | The agreement created when a BAP commits to consume a catalogue entry. | `message.contract` (carries `commitments[]`, `consideration`, `performance[]`, `settlements[]`) |
| **Energy Credentials** | Verifiable attestations that may gate access (e.g. a regulatory-mandate credential the BPP requires before releasing data). | Not used in the basic flow; relevant to credential-gated use cases. |

[Energy Resource Address (ERA)](../glossary.md#era) and Energy Intent are additional DEG concepts not yet surfaced by the data-exchange use cases shipped today; you can read about them in the broader DEG specification when needed.

---

## Beckn Protocol Lifecycle

IES Data Exchange uses the **[Beckn Protocol v2.0](../glossary.md#beckn)** interaction model. The full set of actions:

| Phase | BAP calls | BPP responds | When you need it |
|---|---|---|---|
| Discovery | `discover` | `on_discover` | Consumer doesn't yet know which provider to contract with. Requires the BPP to have called `publish-catalog` earlier. |
| Negotiation | `select` / `init` | `on_select` / `on_init` | Terms (price, SLA, delivery mode) need to be agreed before commitment. |
| Commitment | `confirm` | `on_confirm` | **The minimal flow.** Payload can be delivered inline here. |
| Polled delivery | `status` | `on_status` | Payload is prepared asynchronously after `on_confirm`. |
| Post-fulfilment | `update` | `on_update` | Credential rotation, contract amendments. |

> **Minimal viable exchange:** `confirm` → `on_confirm`, with the dataset embedded in the callback. Everything else is optional.

Beckn is **asynchronous**: every call returns an immediate `ACK`, and the paired response arrives as a callback (`on_*`) to the BAP's webhook URL. The [ONIX](../glossary.md#onix) adapter manages this asynchrony transparently.

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

Two `context` rules govern message correlation across the network. These are protocol expectations from the Beckn v2.0 spec — every implementation that participates in the network is expected to honour them so that participants and audit trails can stitch related messages together:

- **`transactionId` is constant** across every message in one exchange. From the first `discover`/`select`/`confirm` to the final `on_status`/`on_update`, the same UUID flows through. It is how all parties (and registry-level audit trails) link the conversation.
- **`messageId` is the same on a request and its paired callback.** `confirm` and the matching `on_confirm` share one `messageId`; a subsequent `status` gets a *new* `messageId`, which its `on_status` reuses. Treat the pair as one logical message with two hops.

Authoritative reference: [beckn/protocol-specifications-v2 — `api/v2.0.0`](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0).

---

## Building Trust

Every Beckn message on the network is **cryptographically signed** by the sender, and every incoming message is verified by the receiver against the sender's published public key. ONIX does the heavy lifting on both sides — your application doesn't deal with signing or key management directly.

### How identity resolution works

When a message arrives, ONIX:

1. Reads the sender identifier from the message context (`bapId` on a forward request, `bppId` on a callback).
2. Looks the sender up in the **[DeDi](../glossary.md#dedi) registry** at a URL of the form:
   ```
   https://fabric.nfh.global/registry/dedi/lookup/<subscriber_id>/subscribers.beckn.one/<record_id>
   ```
   The lookup response carries the sender's published callback URL, signing public key, **parent namespaces** they belong to, and the **network memberships** they hold.
3. Cross-checks those network memberships against this ONIX's `allowedNetworkIDs` config. A sender that doesn't belong to any of the configured networks is treated as outside the boundary of trust.
4. Verifies the signature on the inbound message using the sender's published public key.

This combination — DeDi resolution plus `allowedNetworkIDs` — creates a **logical boundary of trust**: only participants registered in the networks you accept can transact with you. Two participants registered on different (or non-overlapping) networks cannot reach each other through their ONIX adapters.

### Identity fields, in DeDi and in ONIX

A Beckn subscriber record in DeDi has two identifiers you'll see throughout these docs. Both are present on a DeDi registry record whose registry is of type **`beckn-subscriber`**:

| Field | What it is |
|---|---|
| `subscriber_id` | Your unique participant identity on the network — typically tied to your verified DeDi namespace |
| `record_id` | The specific DeDi-assigned identifier of *this* subscriber record under your namespace; the handle ONIX uses to look up your key |

ONIX on your side needs to know **both of yours**, plus your **private signing key**, so it can stamp every outbound message with a valid signature. The corresponding ONIX config keys live under `modules[].handler.plugins.keyManager.config`:

| Yours, in DeDi | ONIX config key |
|---|---|
| `subscriber_id` | `networkParticipant` |
| `record_id` | `keyId` |
| Ed25519 private key (the half you keep) | `signingPrivateKey` |
| Ed25519 public key (the half you publish in DeDi) | `signingPublicKey` |

See [Registry Setup](./registry-setup.md) for the end-to-end onboarding flow that produces these values, and [Quick Start § Phase 2](./quick-start.md#phase-2--swap-in-your-real-identity) for the YAML snippet showing exactly where they sit in the adapter config.

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

The body inside `dataPayload` is one of the IES schemas; the relevant one for each use case is described on the corresponding [use-case page](../use-cases/README.md):

| Schema | Carried in | Use case |
|---|---|---|
| `IES_Report` (OpenADR 3.1.0) | 15-min interval meter readings | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) |
| `IES_ARR_Filing` | Aggregate Revenue Requirement line items by fiscal year | [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md) |
| `IES_Policy` (+ `IES_Program`) | Machine-readable tariff rate structures (energy slabs, ToD surcharges) | [Tariff Intelligence](../use-cases/tariff-intelligence/README.md) |

Canonical schema definitions today: [beckn/DEG — `ies-specs` branch](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies).

> **TBD — schema migration.** The IES schema family is currently hosted on a working branch under beckn/DEG. It will move to a public repository under the [India-Energy-Stack](https://github.com/India-Energy-Stack) GitHub organisation once stabilised. Links throughout these docs will be updated when the move happens.

---

## How schema validation works

The IES schemas above are convenient defaults — but the wire envelope itself accepts arbitrary JSON inside `dataPayload`. Validation is **opt-in per object**, driven by JSON-LD self-description:

- **Payload declares `@context` + `@type` → ONIX validates it.** Any object inside the message that carries both fields is dispatched to the Extended Schema validator.
- **Payload omits `@context` → ONIX passes it through.** Useful when you're prototyping a new dataset shape, exchanging vendor-specific data, or working with sources that don't publish JSON-LD contexts.

### The dispatch mechanic

When ONIX sees a self-describing object (such as `commitmentAttributes`, `resourceAttributes`, `performanceAttributes`, or the inner `dataPayload`), it:

1. Reads the object's `@context` URL — e.g. `https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.1/context.jsonld`.
2. Transforms it to the **sibling `attributes.yaml`** at the same path — `…/DatasetItem/v1.1/attributes.yaml`. By convention IES (and the broader Beckn schema family) keeps an OpenAPI 3.x schema file next to every JSON-LD context.
3. Fetches and caches that `attributes.yaml`.
4. Looks up an entry in `components.schemas` whose name **matches the `@type` value exactly** — `DatasetItem`, `IES_Report`, `IES_Policy`, `Organization`, `PriceSpecification`, `Payment`, etc.
5. Validates the object against that schema. If validation fails, the message is rejected.

Two failure modes are worth knowing:

- `no schema found for @type: XYZ` — the `attributes.yaml` doesn't define a schema with that name. Either the `@type` is wrong, or the schema file at the resolved URL doesn't include it.
- Schema validation error — the object is missing a required field, has the wrong type, or otherwise doesn't match the OpenAPI definition. ONIX includes the JSON path of the failure in the error.

### Domain allow-list

ONIX restricts which hosts it will fetch `@context` URLs from, via the `extendedSchema` plugin config. Out of the box that includes `raw.githubusercontent.com` and `schema.beckn.io`. To validate payloads using a context hosted elsewhere (your own schema repo, for instance), add the host to the allow-list in your ONIX config.

### Publishing your own schema

If you want ONIX to validate a custom dataset shape:

1. Author an OpenAPI 3.x `attributes.yaml` with your schemas in `components.schemas`.
2. Author a JSON-LD `context.jsonld` mapping your field names to URIs.
3. Host both at a URL ONIX is allowed to reach — they must sit at the same path (`<base>/context.jsonld` and `<base>/attributes.yaml`).
4. In your payload, set `@context` to the context URL and `@type` to the matching schema name.

ONIX then validates exactly as it does for `IES_Report` or `DatasetItem`. No code change needed; the dispatch is purely URL-driven. The shipped IES schemas under [beckn/DEG `ies-specs`](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies) and [beckn/DDM](https://github.com/beckn/DDM/tree/main/specification/schema/DatasetItem/v1.1) are working references for how to lay out the pair.

---

## ONIX Adapter and Network

**ONIX** is the Beckn protocol adapter — it signs, verifies, routes, and validates so your application never deals with protocol-level concerns. See [Architecture § Stack topology](./architecture.md#stack-topology).

IES operates two networks anchored at the `indiaenergystack.in` DeDi namespace (`test-ies-data-sharing-network` and `ies-data-sharing-network`). See [Registry Setup](./registry-setup.md) for joining either.
