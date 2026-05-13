# Architecture — Data Exchange

A minimum-viable picture of how a data exchange runs end-to-end. For the authoritative stack reference (hosting patterns, ngrok over the public internet, multi-network ONIX, TLS), see the [devkit README](https://github.com/beckn/DEG/blob/main/devkits/README.md).

---

## Stack topology

Each side (BAP and BPP) is a self-contained set of containers. The only bridge between them is a Caddy router on `:9000`. The same image runs unchanged whether you're hitting it locally or through a public tunnel.

```
                    beckn-router :9000   (Caddy — the only bridge)
                    /                  \
        /bap/*    <                      >    /bpp/*
                  /                      \
   ─── bap_side ──┘                        └── bpp_side ───
   onix-bap     :8081                       onix-bpp     :8082
   sandbox-bap  :3001                       sandbox-bpp  :3002
   redis                                    redis
```

| Component | Role |
|---|---|
| `onix-bap` / `onix-bpp` | Beckn protocol adapter — signs, verifies, routes, validates `dataPayload` against the declared schema, manages async callbacks |
| `sandbox-bap` | BAP webhook receiver. Logs every `on_*` callback so you can inspect responses |
| `sandbox-bpp` | Reference BPP — auto-responds with the example payloads in `uc{1,2}-*/examples/` |
| `beckn-router` | Caddy bridging the two side networks; the public entrypoint when deployed |
| `redis` | Per-side message cache used by ONIX |

---

## Generic Beckn flow

Every action is a separate HTTP POST that returns an immediate `ACK`; the paired `on_*` callback arrives asynchronously at the caller's webhook. Which steps you actually run depends on the use case:

```
BAP App      ONIX BAP      beckn-router      ONIX BPP      BPP Server
   │             │              │                 │             │
   │  (optional) publish-catalog & discover/on_discover         │
   │             │              │                 │             │
   │  (optional) select / init  →  on_select / on_init          │
   │             │              │                 │             │
   │─ confirm ──>│─────────────>│────────────────>│────────────>│
   │<── ACK ─────│              │                 │<── ACK ─────│
   │             │<───────────────  on_confirm  ───────────────│   ★ minimal flow ends here
   │<─ on_confirm                │                 │             │
   │             │              │                 │             │
   │  (optional) status / on_status — async delivery            │
   │  (optional) update / on_update — credential rotation       │
```

The **minimal viable exchange** is just `confirm` → `on_confirm`, with the dataset (or, for streaming, the connection credentials) carried in `on_confirm`. Every other step is opt-in:

- **Discovery** (`publish-catalog`, `discover`/`on_discover`) — when the consumer doesn't yet know which provider to contract with.
- **Negotiation** (`select`/`init`) — when terms (price, SLA, delivery mode) must be agreed before commitment.
- **Polled delivery** (`status`/`on_status`) — when payload is prepared after `on_confirm`.
- **Post-fulfilment** (`update`/`on_update`) — credential rotation, contract amendments.

---

## Context invariants

Two `context` rules govern message correlation. ONIX rejects messages that violate either.

- **`transactionId` is constant across one exchange.** Every message — from the first `discover`/`select`/`confirm` through the final `on_status` or `on_update` — carries the same UUID. It is how all parties (and registry-level audit trails) stitch the conversation together.
- **`messageId` is the same on a request and its paired callback.** `confirm` and its matching `on_confirm` share one `messageId`; a later `status` gets a *new* `messageId`, which its `on_status` reuses. Treat each request/callback pair as one logical message with two hops.

In addition, every message must include `schemaContext` pointing at the JSON-LD context of the schema being carried in the payload — without it, ONIX validation fails.

Authoritative reference: [beckn/protocol-specifications-v2 — `api/v2.0.0`](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0).

---

## Network configuration

| Parameter | Local devkit (sandbox) | Real network |
|---|---|---|
| `networkId` | `nfh.global/testnet-deg` | Your DeDi-issued `<nfo-domain>/<registry>` — see [Registry Setup](./registry-setup.md) |
| `bapId` / `bppId` | `bap.example.com` / `bpp.example.com` | Your DeDi `subscriberId` |
| Caller URLs | `http://beckn-router:9000/{bap,bpp}/caller` (in-stack) or `http://localhost:8081 \| 8082/{bap,bpp}/caller` (direct) | Your ONIX deployment URL behind TLS |
| Callback URLs | `http://beckn-router:9000/{bap,bpp}/receiver` | Your public `bapUri` / `bppUri` published in the registry |

ONIX configuration lives in [config/local-simple-{bap,bpp}.yaml](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/config). The mapping from DeDi registry fields to ONIX config fields is on the [Registry Setup](./registry-setup.md) page.

---

## Mock BPP (cloud sandbox) — planned

`sandbox-bpp` in the diagram above is the **local** devkit container. Separately, a **cloud-hosted Mock BPP** is planned as additional scope outside the devkit — a long-lived sandbox provider that BAP implementors can transact against without running anything locally, and that the network can use for automated conformance testing and certification of new BAPs. URL, supported use cases, and conformance suite — TBD.

---

## Further reading

- [Devkit README — stack topology, hosting, multi-network](https://github.com/beckn/DEG/blob/main/devkits/README.md)
- [Beckn ONIX](https://github.com/beckn/beckn-onix) — the protocol adapter
- [Beckn protocol spec v2.0.0](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0)
- [docs.nfh.global/beckn](https://docs.nfh.global/beckn) — network and registry primitives
