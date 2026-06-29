# Discover

> **Step 2 of the three IES steps.** Interaction protocol. Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. *No bilateral arrangement is needed.*

Once both parties are registered (Step 1), they need a way to **find each other, negotiate terms, and produce a signed audit trail** of what was agreed — without anyone phoning anyone. IES uses the open **[Beckn Protocol v2](https://becknprotocol.io)** for this.

| Concern | What Beckn provides |
|---|---|
| Discovery | Either party can publish a catalogue of what it offers (datasets, credentials, dispatch programmes) and other parties can query it. |
| Negotiation | A standard `select` / `init` round-trip lets the two sides agree on quantity, price, SLA, delivery method. |
| Commitment | A signed `confirm` / `on_confirm` round-trip is the contract. The signed envelope is the non-repudiable record of agreement. |
| Status and delivery | `status` / `on_status` carry asynchronous fulfilment — including payload delivery, pagination, settlement updates. |
| Consent and audit | Every message is signed; every leg leaves a tamper-evident receipt. |

Beckn is **asynchronous and peer-to-peer**: there is no central broker. The IES "network operator" curates the membership list (the allow-list of valid Beckn subscribers), but every message flows directly between participants.

---

## What you set up under Discover

For an IES participant, Discover means running a Beckn adapter — the **Beckn ONIX reference software** — and publishing your subscriber record:

1. **ONIX deployment** — one Docker container per side (BAP and / or BPP). Handles signing, signature verification, registry lookup, callback routing. **Same software for everyone** — you do not modify it.
2. **Beckn subscriber record** — a small entry in your DeDi namespace declaring your callback URL, role (`BAP` / `BPP`), and Ed25519 message-signing public key. Other Beckn nodes look this up to verify your signatures.
3. **Network reference** — the IES network operator (acting as Network Facilitator Organisation, NFO) writes a *reference* into the network registry pointing at your subscriber record. This is the membership boundary.

For the step-by-step setup, follow **[How you implement IES → Setup Discovery](../how-you-implement-ies/setup-discovery.md)**.

---

## Why Beckn, not a REST API

A bespoke REST API per integration is exactly the n×m problem IES is solving. Beckn is a single, open, asynchronous interaction protocol that any party can build to once and use against every counterparty. Discovery, negotiation, signing, audit and consent are built in. The wire and the lifecycle are the same whether the payload is meter telemetry, a regulatory filing, a tariff order, or a peer-to-peer energy trade.

---

## Detail pages

- **[Data Exchange — Beckn lifecycle](data-exchange/README.md#appendix-a-beckn-protocol-lifecycle)** — the `discover` / `select` / `init` / `confirm` / `status` round-trips.
- **[Data Exchange — ONIX deployment](data-exchange/README.md)** — Docker stack, message signing, registry lookup, two-environment (test + prod) topology.
- **[Registries — Beckn subscriber registries](registries/README.md#registry-tags-used-in-ies)** — the `beckn_subscriber` and `beckn_subscriber_reference` tags.

---

## Where this fits

| Step | Page |
|---|---|
| Step 1 — [Register](register.md) | Identity + directory |
| Step 2 — Discover *(this page)* | — |
| Step 3 — [Exchange](exchange.md) | Schemas, credentials, taxonomy |

To set up Beckn ONIX hands-on: **[Setup Discovery](../how-you-implement-ies/setup-discovery.md)**.
