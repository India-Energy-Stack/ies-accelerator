# Discover

> **Step 2 of the three IES steps.** Interaction protocol. Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. *No bilateral arrangement is needed.*

Once participants are [Registered](register.md) (Step 1), they need a way to **find each other, negotiate terms, and produce a signed audit trail** of what was agreed — without anyone phoning anyone. IES uses the open **[Beckn Protocol v2](https://github.com/beckn/protocol-specifications-v2)** for this.

Discover belongs to the **data exchange** capability — B2B exchange of structured datasets between registered organisations. The other IES capability, **[Energy Credentials](energy-credentials/README.md)**, does not need this step: a credential is issued and verified against the issuer's published key, with no Beckn network involved.

---

## Two rails, two kinds of trust

| | **B2B data exchange** (this page + [Exchange](exchange.md)) | **B2C credentials** ([Issue Credentials](../how-you-implement-ies/issue-credentials.md)) |
|---|---|---|
| **What moves** | Structured datasets — meter telemetry, regulatory filings, tariff data, trade offers | Signed attestations — a consumer's connection record, a meter digest |
| **Between whom** | Two **registered organisations** that know who they are transacting with | An issuer and **any third party** — a bank, a marketplace, a housing society — that the issuer has never met |
| **Trust layer** | **Bilateral, anchored in DeDi.** Each side resolves the other's subscriber record, verifies its message signature, and checks that both belong to the same curated network. The network operator (NFO) maintains that membership boundary. | **Unilateral, anchored in `did:web`.** The issuer signs once; any verifier, anywhere, fetches the issuer's published key over HTTPS and checks the signature — no membership, no prior relationship, no callback to the issuer. |
| **Channel** | Must ride a **trust-bounded open network** — IES uses [Beckn Protocol v2](https://github.com/beckn/protocol-specifications-v2) — because discovery, negotiation, consent and the signed audit trail are part of the exchange itself | **Any channel** — DigiLocker, a web portal, email, SMS, chat. The trust travels inside the credential, not the pipe. |
| **Typical use cases** | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md), [Regulatory Filing](../use-cases/discom-regulatory-filing/README.md), [P2P Trading](../use-cases/p2p-energy-trading/README.md) | [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md), [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) |

The rest of this page covers how the B2B rail's two registered parties find each other, agree terms, and sign — the *Discover* step. What they actually exchange once agreed — the Taxonomy and, where needed, verifiable credentials — is *Exchange*, covered on its own page.

---

## Find, agree, and sign without a pre-negotiated integration

Energy data in India moves through bespoke point-to-point channels today — PDF filings, vendor-locked exports, one-off API integrations. A bespoke REST API per counterparty is exactly the n×m problem IES is solving. (Note: the *trust* here is still bilateral — each side verifies the other — but the wiring is not; you build to the protocol once, not to each partner.) Beckn is a single, open, **asynchronous and peer-to-peer** interaction protocol that any party builds to once and uses against every counterparty:

| Concern | What Beckn provides |
|---|---|
| Discovery | Either party can publish a catalogue of what it offers (datasets, credentials, dispatch programmes) and other parties can query it. |
| Negotiation | A standard `select` / `init` round-trip lets the two sides agree on quantity, price, SLA, delivery method. |
| Commitment | A signed `confirm` / `on_confirm` round-trip **is the contract**. The signed envelope is the non-repudiable record of agreement. |
| Status and delivery | `status` / `on_status` carry asynchronous fulfilment — including payload delivery, pagination, settlement updates. |
| Consent and audit | Every message is signed; every leg leaves a tamper-evident receipt. |

There is no central broker: the network operator curates the membership list, but every message flows directly between participants. The wire and the lifecycle are the same whether the payload is meter telemetry, a regulatory filing, a tariff order, or a peer-to-peer energy trade.

### The lifecycle at a glance

| Phase | BAP — the consumer side ([Beckn Application Platform](../glossary.md#bap)) calls | BPP — the provider side ([Beckn Provider Platform](../glossary.md#bpp)) responds | When you need it |
|---|---|---|---|
| Discovery | `discover` | `on_discover` | Consumer doesn't yet know which provider to contract with |
| Negotiation | `select` / `init` | `on_select` / `on_init` | Terms need agreeing before commitment |
| Commitment | `confirm` | `on_confirm` | **The minimal flow** — payload can be delivered inline here |
| Delivery | `status` | `on_status` | Payload prepared asynchronously, or paged across messages |
| Post-fulfilment | `update` | `on_update` | Amendments, credential rotation |

**Minimal viable exchange:** `confirm` → `on_confirm`, with the dataset embedded in the callback. Everything else is optional; each [use-case guide](../use-cases/README.md) lists which actions it actually exercises. Small datasets ride **inline** in the message (the IES default — end-to-end verifiable); large ones hand off to an established channel (signed URL, MQTT, Kafka, SFTP) agreed inside the same contract, so every exchange gets the same signed-audit story. Wire-level detail — message envelope, correlation rules, pagination, `accessMethod` values — is in the [Setup Discovery appendices](../how-you-implement-ies/setup-discovery.md#appendices).

## The IES networks

IES currently operates three Beckn networks (each with a `test-` twin for onboarding and certification) under the `indiaenergystack.in` namespace: **data sharing**, **P2P trading**, and **DER integration**. Membership is per-network and per-environment; the adapter rejects messages from outside the configured boundary. The registry mechanics are in [Register — The directory: DeDi](register.md#the-directory-dedi); how to get listed is [Setup Register §1.7](../how-you-implement-ies/setup-register.md#id-1.7-beckn-participants-get-referenced-into-an-ies-network).

---

## What you set up under Discover

For an IES participant, Discover means running a Beckn adapter — the **[ONIX](../glossary.md#onix)** reference software — and publishing your subscriber record:

1. **ONIX deployment** — one Docker container per side (BAP and / or BPP). Handles signing, signature verification, registry lookup, callback routing. **Same software for everyone** — you do not modify it.
2. **Beckn subscriber record** — a small entry in your DeDi namespace declaring your callback URL, role (`BAP` / `BPP`), and Ed25519 message-signing public key. Other Beckn nodes look this up to verify your signatures.
3. **Network reference** — the IES network operator (acting as Network Facilitator Organisation, NFO) writes a *reference* into the network registry pointing at your subscriber record. This is the membership boundary.

For the step-by-step setup, follow **[How you implement IES → Setup Discovery](../how-you-implement-ies/setup-discovery.md)**.

---

## Where this fits

| Step | Page |
|---|---|
| Step 1 — [Register](register.md) | Identity + directory |
| Step 2 — Discover *(this page)* | — |
| Step 3 — [Exchange](exchange.md) | Taxonomy + verifiable credentials |

To set up Beckn ONIX hands-on: **[Setup Discovery](../how-you-implement-ies/setup-discovery.md)**.
