# Discover

> **Step 2 of the three IES steps.** Before every exchange, both systems look each other up, confirm authenticity, and agree terms. *No bilateral arrangement needed.*

Once registered (Step 1), parties need to **find each other, negotiate terms, and produce a signed audit trail** — without anyone phoning anyone. IES uses the open **[Beckn Protocol v2](https://becknprotocol.io)**.

Discover belongs to the **data exchange** capability — B2B exchange of structured datasets between registered organisations. The other IES capability, **[Energy Credentials](energy-credentials/README.md)**, does not need this step: a credential is issued and verified against the issuer's published key, with no Beckn network involved.

| Concern | What Beckn provides |
|---|---|
| Discovery | Either party can publish a catalogue of what it offers (datasets, credentials, dispatch programmes) and other parties can query it. |
| Negotiation | A standard `select` / `init` round-trip lets the two sides agree on quantity, price, SLA, delivery method. |
| Commitment | A signed `confirm` / `on_confirm` round-trip is the contract. The signed envelope is the non-repudiable record of agreement. |
| Status and delivery | `status` / `on_status` carry asynchronous fulfilment — including payload delivery, pagination, settlement updates. |
| Consent and audit | Every message is signed; every leg leaves a tamper-evident receipt. |

Beckn is **asynchronous and peer-to-peer**, with no central broker; the IES "network operator" curates the membership allow-list, but messages flow directly between participants.

---

## What you set up under Discover

For an IES participant, Discover means running the **Beckn ONIX reference software** and publishing your subscriber record:

1. **ONIX deployment** — one Docker container per side (BAP and/or BPP): signing, signature verification, registry lookup, callback routing. **Same software for everyone.**
2. **Beckn subscriber record** — an entry in your DeDi namespace with your callback URL, role (`BAP`/`BPP`), and Ed25519 signing key, for other nodes to verify your signatures.
3. **Network reference** — the IES network operator (NFO) points a *reference* in the network registry at your subscriber record — the membership boundary.

Step-by-step: **[How you implement IES → Setup Discovery](../how-you-implement-ies/setup-discovery.md)**.

---

## Why Beckn, not a REST API

A bespoke REST API per integration is the n×m problem IES avoids: Beckn is a single, open, asynchronous protocol built once and used against every counterparty, with discovery, negotiation, signing, audit and consent built in, whatever the payload — meter telemetry, a regulatory filing, a tariff order, or a peer-to-peer trade.

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
| Step 3 — [Exchange](exchange.md) | Taxonomy + verifiable credentials |

Hands-on: **[Setup Discovery](../how-you-implement-ies/setup-discovery.md)**.
