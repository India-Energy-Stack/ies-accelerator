# Architecture — Data Exchange

This page describes the full technical architecture of IES Data Exchange: components, transaction flow, network topology, and configuration.

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     IES Data Exchange Network                    │
│                      (nfh.global/testnet-deg)                   │
└─────────────────────────────────────────────────────────────────┘
         ↑ discover / route                    ↑ discover / route
         │                                     │
┌────────┴──────────┐                 ┌─────────┴──────────┐
│   BAP Side        │                 │   BPP Side         │
│                   │                 │                    │
│  ┌─────────────┐  │                 │  ┌──────────────┐  │
│  │  Your App   │  │                 │  │  Your Server │  │
│  │  (BAP app)  │  │                 │  │  (BPP impl.) │  │
│  └──────┬──────┘  │                 │  └──────┬───────┘  │
│         │ REST    │                 │         │ HTTP     │
│  ┌──────▼──────┐  │  Beckn msgs    │  ┌──────▼───────┐  │
│  │  ONIX BAP  │◄──┼────────────────┼──►  ONIX BPP   │  │
│  │  Adapter   │  │                 │  │  Adapter     │  │
│  │  :8081     │  │                 │  │  :8082       │  │
│  └─────────────┘  │                 │  └──────────────┘  │
│                   │                 │                    │
│  ┌─────────────┐  │                 │  ┌──────────────┐  │
│  │  Redis      │  │                 │  │  Redis       │  │
│  │  :6379      │  │                 │  │  :6379       │  │
│  └─────────────┘  │                 │  └──────────────┘  │
└───────────────────┘                 └────────────────────┘
```

In local development, both sides run on a single machine. In production, BAP and BPP are separate organisations with separate deployments.

---

## Transaction Flow

Every data exchange follows the Beckn four-step lifecycle. Here is the complete flow with all participants:

```
BAP App     ONIX BAP    IES Network    ONIX BPP     BPP Server
   │            │             │             │             │
   │──select──>│             │             │             │
   │           │──select────>│             │             │
   │<── ACK ───│             │──select────>│             │
   │           │             │             │──select────>│
   │           │             │             │<── ACK ─────│
   │           │             │<──on_select─│             │
   │           │<──on_select─│             │             │
   │<──on_select             │             │             │
   │            (catalog: available datasets + access terms)
   │                         │             │             │
   │──init────>│             │             │             │
   │           │──init──────>│──init──────>│──init──────>│
   │<── ACK ───│             │             │<── ACK ─────│
   │           │<──on_init───────────────────────────────│
   │<──on_init │             │             │             │
   │            (contract ready)           │             │
   │                         │             │             │
   │──confirm─>│             │             │             │
   │           │──confirm───>│──confirm───>│──confirm───>│
   │<── ACK ───│             │             │<── ACK ─────│
   │           │<──on_confirm────────────────────────────│
   │<──on_confirm            │             │             │
   │            (contract active, order_id confirmed)   │
   │                         │             │             │
   │──status──>│             │             │             │
   │           │──status────>│──status────>│──status────>│
   │<── ACK ───│             │             │             │
   │           │             │             │  (prepare dataPayload)
   │           │             │             │<── ACK ─────│
   │           │<──on_status─────────────────────────────│
   │<──on_status             │             │             │
   │   dataPayload: { IES_Report | IES_ARR_Filing | IES_Policy }
```

---

## ONIX Adapter

ONIX is the Beckn protocol adapter that shields your application from protocol-level concerns.

### What ONIX Does

| Function | Details |
|---|---|
| **Signing** | Signs every outbound Beckn message with your Ed25519 private key |
| **Verification** | Verifies signatures on inbound Beckn messages |
| **Routing** | Routes messages to the correct BPP/BAP via the IES network registry |
| **Schema validation** | Validates that `dataPayload` conforms to the declared IES schema |
| **Async handling** | Manages the request/callback asynchrony; your app sends synchronous calls |
| **Retry** | Retries failed deliveries with exponential backoff |

### ONIX API Surface (BAP side)

```
POST http://localhost:8081/bap/caller/select    ← send select
POST http://localhost:8081/bap/caller/init      ← send init
POST http://localhost:8081/bap/caller/confirm   ← send confirm
POST http://localhost:8081/bap/caller/status    ← send status
GET  http://localhost:8081/health               ← health check

Callbacks received at:
POST {your_bap_webhook}/bap/receiver/on_select
POST {your_bap_webhook}/bap/receiver/on_init
POST {your_bap_webhook}/bap/receiver/on_confirm
POST {your_bap_webhook}/bap/receiver/on_status
```

### ONIX API Surface (BPP side)

```
GET  http://localhost:8082/health               ← health check

Inbound calls from network (ONIX routes these to your BPP server):
POST {your_bpp_server}/select
POST {your_bpp_server}/init
POST {your_bpp_server}/confirm
POST {your_bpp_server}/status

Your BPP server calls ONIX to send callbacks:
POST http://localhost:8082/bpp/caller/on_select
POST http://localhost:8082/bpp/caller/on_init
POST http://localhost:8082/bpp/caller/on_confirm
POST http://localhost:8082/bpp/caller/on_status
```

---

## Network Configuration

| Parameter | Local Development | Production |
|---|---|---|
| Network ID | `nfh.global/testnet-deg` | `nfh.global/deg` (contact IES team) |
| BAP ID | `bap.example.com` | Your registered BAP ID |
| BPP ID | `bpp.example.com` | Your registered BPP ID |
| BAP adapter URL | `http://localhost:8081/bap/caller` | Your deployed BAP adapter URL |
| BPP adapter URL | `http://localhost:8082/bpp/caller` | Your deployed BPP adapter URL |

---

## Mock BPP

For development and bootcamp purposes, the devkit includes a **Mock BPP** — a FastAPI application that:

1. Receives Beckn requests routed from the ONIX BPP adapter
2. Detects which dataset is being requested from resource IDs in the message
3. Tracks transaction state: `DRAFT → SELECTED → INITIALIZED → CONFIRMED → DELIVERED`
4. Responds with real IES test data embedded in the `on_status` dataPayload

The key difference from the sandbox BPP: the sandbox just logs requests and returns ACK. The Mock BPP actually responds with data, simulating a real provider.

Source: [`devkits/data-exchange/mock-bpp/app.py`](https://github.com/Beckn-One/DEG/blob/main/devkits/data-exchange/mock-bpp/app.py)

---

## Data Delivery Modes

| Mode | How data arrives | When to use |
|---|---|---|
| `INLINE` | Embedded directly in `on_status` Beckn message | Most IES use cases — provides end-to-end auditability |
| `DOWNLOAD` | `on_status` contains a signed download URL + checksum | Large datasets (>50MB) |
| `DATA_ENCLAVE` | Data accessible within a secure compute environment only | Sensitive/regulated data |
| `OFF_CHANNEL` | Delivery agreed bilaterally, Beckn only handles discovery+contract | Legacy systems |

---

## Schema Context and Validation

ONIX validates that the `dataPayload` conforms to the schema declared in the item's `descriptor.code`. The schema context URL must be present in the request context:

```json
{
  "context": {
    "schemaContext": "https://ies.energy/schemas/v1"
  }
}
```

Missing `schemaContext` causes a validation error. The Mock BPP strips any nested `@context` fields from `dataPayload` automatically to avoid ONIX's regex engine issue with OpenADR duration patterns (see [beckn-onix#655](https://github.com/beckn/beckn-onix/issues/655)).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `connection refused` on port 8081/8082 | Wait 10–15s for ONIX to initialise. Check `docker logs onix-bap` |
| ACK returned but no `on_*` callback arrives | Check `docker logs mock-bpp`. Verify routing config in `config/` |
| Schema validation errors | Ensure `schemaContext` is present in request context |
| `domain not allowed` errors | ONIX rejects nested `@context` URLs in dataPayload — use a BPP that strips them |
| Signatures not verifying | Confirm signing key in `config/` matches the key registered on the testnet |
