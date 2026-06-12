# Core Concepts — Data Exchange

Just enough theory to start building. Read this page, then go run the [Quick Start](./quick-start.md). Deeper reference material — the four ONIX endpoints, hostname/endpoint tables, validation dispatch mechanics, the full sequence diagram — lives in the [Appendix](./appendix.md).

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

Beckn is **asynchronous**: every call is answered by an `ACK` — produced by the receiving application and cascaded back through the adapters as the synchronous HTTP response — and the paired response arrives later as a callback (`on_*`) to the BAP's webhook. The [ONIX](../glossary.md#onix) adapter manages this asynchrony transparently.

### Message Structure

Every Beckn message shares the same envelope (v2.0 wire format, camelCase). This is what the **devkit sandbox** emits — on a real IES network, the `networkId`, IDs and URIs change to your DeDi-published values ([Quick Start § Swap in your real identity](./quick-start.md#swap-in-your-real-identity)):

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

Two correlation rules to remember (details in [Appendix § Context invariants](./appendix.md#context-invariants)):

- **`transactionId` stays constant** across every message in one exchange.
- **`messageId` is shared** by a request and its paired `on_*` callback; each new request gets a new one.

---

## Building Trust

Every message is **cryptographically signed** by the sender and verified by the receiver — ONIX handles both directions, so your application never touches keys. On each inbound message, ONIX resolves the sender in the **[DeDi](../glossary.md#dedi) registry** (getting their callback URL, public key, and network memberships), checks those memberships against its own `allowedNetworkIDs` config, and verifies the signature.

That combination is the **boundary of trust**: only participants registered in a network you accept can transact with you. The DeDi → ONIX identity field mapping (`subscriber_id` → `networkParticipant`, `record_id` → `keyId`, signing keypair) and the onboarding flow that produces those values are on [Registry Setup](./registry-setup.md); the inbound resolution steps are in [Appendix § Identity resolution](./appendix.md#identity-resolution-step-by-step).

---

## The DatasetItem Schema

In a data exchange, the **resource is a dataset**. **`DatasetItem`** (from DDM, Beckn's Decentralised Data Marketplace schema) is the per-dataset record shape that rides inside `message.contract.commitments[].resources[]`, qualified by `resourceAttributes`:

```json
"resources": [{
  "id": "ds-ami-meter-data-blr-zone-a-q1-2026",
  "descriptor": { "name": "IntelliGrid AMI Meter Data — Bengaluru Zone A — Q1 2026" },
  "resourceAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.1/context.jsonld",
    "@type": "DatasetItem",
    "accessMethod": "INLINE",
    "dataPayload": { /* inline MeterData, ArrFiling, ... */ }
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

## Schema families

The body inside `dataPayload` is one of the IES schema families maintained in this repo's [schemas/](../schemas/README.md) directory:

| Family | What it carries | Use case |
|---|---|---|
| [MeterData](../schemas/MeterData/README.md) | Smart meter telemetry compact profiles (interval reads, billing, events) | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) |
| [MeterDataCredential](../schemas/MeterDataCredential/README.md) | W3C Verifiable Credential wrapping MeterData for provenance attestation | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) (credentialed delivery) |
| [ArrFiling](../schemas/ArrFiling/README.md) | Aggregate Revenue Requirement line items by fiscal year | [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md) |
| `IES_Policy` (+ `IES_Program`) | Machine-readable tariff rate structures (energy slabs, ToD surcharges) | [Tariff Intelligence](../use-cases/tariff-intelligence/README.md) |

Related families — [MeterDataRequest](../schemas/MeterDataRequest/README.md) (query/authorisation shape) and [MeterDataRequestCredential](../schemas/MeterDataRequestCredential/README.md) (VC wrapping it) — cover the request side of meter-data flows. The full catalogue, with versions and provenance, is in [schemas/README.md](../schemas/README.md).

---

## How schema validation works

The wire envelope accepts arbitrary JSON inside `dataPayload`; validation is **opt-in per object**, driven by JSON-LD self-description:

- **Payload declares `@context` + `@type` → ONIX validates it.** ONIX fetches the OpenAPI 3.x **`attributes.yaml` that sits next to the `context.jsonld`** named in `@context` (same URL, different filename — every IES/Beckn schema family publishes the pair side by side), and validates the object against the `components.schemas` entry whose name matches the `@type` exactly (`DatasetItem`, `MeterData`, `ArrFiling`, …). A failed validation rejects the message.
- **Payload omits `@context` → ONIX passes it through.** Useful for prototyping a new dataset shape or exchanging vendor-specific data.

One operational gotcha: ONIX only fetches `@context` URLs from **allow-listed hosts** (out of the box: `raw.githubusercontent.com`, `schema.beckn.io`). Error messages, the allow-list config, and how to publish your own schema pair are in [Appendix § Schema validation reference](./appendix.md#schema-validation-reference).

---

## Architecture at a glance

Your application never speaks Beckn directly — it talks to **ONIX**, which exposes a `caller` endpoint (where your app hands it outbound messages to sign and dispatch) and a `receiver` endpoint (where the network delivers inbound messages, which ONIX verifies and forwards to your app's **webhook**). There is one caller/receiver pair per role — `/bap/caller`, `/bap/receiver`, `/bpp/caller`, `/bpp/receiver` — and one ONIX deployment can host any combination under one identity. Roles are configuration, not separate software.

The devkit simulates **two participants** (identities `bap.example.com` and `bpp.example.com`), so it runs two ONIX containers on mutually isolated docker networks:

```
                    beckn-router :9000   (Caddy reverse proxy — stands in for
                    /                  \    the internet + public hostnames)
        /bap/*    <                      >    /bpp/*
                  /                      \
   ─── bap_side ──┘                        └── bpp_side ───
   onix-bap     :8081                       onix-bpp     :8082
   sandbox-bap  :3001                       sandbox-bpp  :3002
   redis                                    redis
```

| Component | Role |
|---|---|
| `onix-bap` / `onix-bpp` | Beckn protocol adapter, one per simulated participant — signs, verifies, validates `dataPayload`, dispatches to the counterparty, forwards inbound messages to the app webhook |
| `sandbox-bap` | Consumer-side stand-in app — receives `on_*` callbacks on its webhook and logs them so you can inspect responses |
| `sandbox-bpp` | Provider-side stand-in app — receives requests on its webhook and auto-responds with the example payloads via `/bpp/caller` |
| `beckn-router` | Plain Caddy reverse proxy, the only container on both networks — routes by path (`/bap/*` → `onix-bap`, `/bpp/*` → `onix-bpp`) and carries the dummy participant hostnames as docker aliases. **Not a Beckn entity** — deployment plumbing: in production the local aliases (e.g. `bap.example.com`) are replaced by your publicly accessible URL (`https://<your-host>/b*p/receiver`), and Caddy can keep routing incoming calls to the right ONIX endpoint at the receiver's end |
| `redis` | Per-side message cache used by ONIX |

The hostnames in `bapUri`/`bppUri` are participant identities: dummy docker aliases locally, your real public URL (DeDi-published) in production. The full message path, the four-endpoint reference, and which URL goes where are in the [Appendix](./appendix.md#the-four-onix-endpoints).

---

## Where next

1. [Quick Start](./quick-start.md) — run the minimal exchange in under 10 minutes.
2. [Registry Setup](./registry-setup.md) — real identity on the IES networks.
3. [Onboarding Checklist](../checklists/data-exchange-checklist.md) — track your progression from devkit to production.
4. [Appendix](./appendix.md) — reference detail when you need it.
