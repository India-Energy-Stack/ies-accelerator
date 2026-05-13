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

The minimal-flow framing, the optional phases, and the `transactionId` / `messageId` correlation rules all live in [Concepts § Beckn Protocol Lifecycle](./concepts.md#beckn-protocol-lifecycle).

---

## Endpoints — sandbox vs production

| Concern | Devkit sandbox | Real network |
|---|---|---|
| BAP-side caller (where your code POSTs `confirm`, etc.) | `http://localhost:9000/bap/caller` *(from Postman on your laptop)* or `http://beckn-router:9000/bap/caller` *(in-stack)* | Your ONIX deployment URL behind TLS |
| BPP-side caller | `http://localhost:9000/bpp/caller` or `http://beckn-router:9000/bpp/caller` *(in-stack)* | Your ONIX deployment URL behind TLS |
| Callback URLs in payload `bapUri`/`bppUri` | `http://beckn-router:9000/{bap,bpp}/receiver` *(docker-internal hostname; resolved by ONIX, not by Postman)* | Your public `bapUri` / `bppUri` published in your DeDi subscriber record |
| `networkId`, `bapId`/`bppId`, `allowedNetworkIDs` | placeholder values shipped in `config/` | See [Registry Setup](./registry-setup.md) |

`beckn-router` is a docker-network hostname — only reachable from inside the `bap_side`/`bpp_side` networks. From Postman on your laptop, hit `localhost:9000`. From within ONIX, `beckn-router` resolves and is the correct value to bake into payload `bapUri`/`bppUri`.

ONIX configuration lives in [config/local-simple-{bap,bpp}.yaml](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/config). The DeDi → ONIX field mapping is on [Registry Setup](./registry-setup.md).

---

## Further reading

- [Devkit README — stack topology, hosting, multi-network](https://github.com/beckn/DEG/blob/main/devkits/README.md)
- [Beckn ONIX](https://github.com/beckn/beckn-onix) — the protocol adapter
- [Beckn protocol spec v2.0.0](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0)
- [docs.nfh.global/beckn](https://docs.nfh.global/beckn) — network and registry primitives
