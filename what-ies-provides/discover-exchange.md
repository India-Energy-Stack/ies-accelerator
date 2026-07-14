# Discover+Exchange

> **Steps 2 and 3 of the three IES steps.** *Discover*: before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms — no one-off, pre-negotiated integration needed. *Exchange*: the data then moves using agreed field names and structure — the **Taxonomy** — and, where the use case needs a durable record, as a **verifiable credential** the holder keeps and can re-present anywhere.

Once participants are [Registered](register.md) (Step 1), IES gives them two ways to move data. They solve different problems, and a participant adopts whichever its use cases need.

---

## Two rails, two kinds of trust

| | **B2B data exchange** (this page) | **B2C credentials** ([Issue Credentials](../how-you-implement-ies/issue-credentials.md)) |
|---|---|---|
| **What moves** | Structured datasets — meter telemetry, regulatory filings, tariff data, trade offers | Signed attestations — a consumer's connection record, a meter digest |
| **Between whom** | Two **registered organisations** that know who they are transacting with | An issuer and **any third party** — a bank, a marketplace, a housing society — that the issuer has never met |
| **Trust layer** | **Bilateral, anchored in DeDi.** Each side resolves the other's subscriber record, verifies its message signature, and checks that both belong to the same curated network. The network operator (NFO) maintains that membership boundary. | **Unilateral, anchored in `did:web`.** The issuer signs once; any verifier, anywhere, fetches the issuer's published key over HTTPS and checks the signature — no membership, no prior relationship, no callback to the issuer. |
| **Channel** | Must ride a **trust-bounded open network** — IES uses [Beckn Protocol v2](https://becknprotocol.io) — because discovery, negotiation, consent and the signed audit trail are part of the exchange itself | **Any channel** — DigiLocker, a web portal, email, SMS, chat. The trust travels inside the credential, not the pipe. |
| **Typical use cases** | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md), [Regulatory Filing](../use-cases/discom-regulatory-filing/README.md), [P2P Trading](../use-cases/p2p-energy-trading/README.md) | [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md), [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) |

The rest of this page covers the B2B rail — the Beckn interaction and the Taxonomy that both rails share. The credential rail's concepts (lifecycle, variants, trust model) are in **[Energy Credentials](../how-you-implement-ies/energy-credentials/README.md)**.

---

## Discover — find, agree, and sign without a pre-negotiated integration

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

**Minimal viable exchange:** `confirm` → `on_confirm`, with the dataset embedded in the callback. Everything else is optional; each [use-case guide](../use-cases/README.md) lists which actions it actually exercises. Small datasets ride **inline** in the message (the IES default — end-to-end verifiable); large ones hand off to an established channel (signed URL, MQTT, Kafka, SFTP) agreed inside the same contract, so every exchange gets the same signed-audit story. Wire-level detail — message envelope, correlation rules, pagination, `accessMethod` values — is in the [Setup Discovery+Exchange appendices](../how-you-implement-ies/setup-discovery-exchange.md#appendices).

### The IES networks

IES currently operates three Beckn networks (each with a `test-` twin for onboarding and certification) under the `indiaenergystack.in` namespace: **data sharing**, **P2P trading**, and **DER integration**. Membership is per-network and per-environment; the adapter rejects messages from outside the configured boundary. The registry mechanics are in [Register — The directory: DeDi](register.md#the-directory-dedi); how to get listed is [Setup Register §1.7](../how-you-implement-ies/setup-register.md#id-1.7-beckn-participants-get-referenced-into-an-ies-network).

---

## Exchange — the Taxonomy

Whichever rail data moves on, it uses agreed field names and structure:

| Part | Purpose | IES choice |
|---|---|---|
| **[Taxonomy](../schemas/README.md)** | The master vocabulary of IES — every domain object, what it is for, which use cases combine it, how it evolves and how new ones are proposed. The shape of each object is described by its **schema**: field names, types, units, optionality — one canonical schema per object. | IES-published JSON Schema + JSON-LD context, built on public standards |
| **Verifiable Credentials** | Where the use case needs a durable record — a Passport, a Digest — a W3C Verifiable Credential is issued that the holder keeps in DigiLocker or any wallet. | W3C VC Data Model 2.0; W3C DID Core |

**IES does not write new standards.** It picks the right open standard for each domain — DLMS/COSEM for meter data, IEEE 2030.5 for solar and storage, OpenADR for demand response, CIM for grid models — and publishes a faithful schema on top. A schema is valid whether or not the payload ever travels over Beckn: the same `MeterData` object can ride a Beckn `on_confirm`, sit inside a signed `MeterDataCredential`, or be validated standalone.

### Schemas grouped by use case

The same set of schemas combines in different ways to deliver each use case.

**Pilot use cases (live):**

| Use case | Schemas combined |
|---|---|
| [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) | [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) (holder-bound) |
| [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) | [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) wrapping [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6); often paired with the consumer's [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) |
| [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) | [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) + [MeterDataRequest v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6) + optionally [MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) |
| [DER Visibility](../use-cases/der-visibility/README.md) | [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) building blocks (PII-free `energyResources[]` + `consumptionProfiles[]` arrays per feeder) |

**Live or staged:**

| Use case | Schemas combined |
|---|---|
| [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md) | [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) over Beckn |
| [Tariff Intelligence](../use-cases/tariff-intelligence/README.md) | `IES_Policy` family (upstream; in progress) |

**In progress:**

| Use case | Schemas combined |
|---|---|
| [P2P Energy Trading](../use-cases/p2p-energy-trading/README.md) | DEG `P2PTrade` family — [P2PTrade, DEGContract, EnergyTradeOffer, EnergyCustomer, RevenueFlow, BecknTimeSeries](../schemas/external/README.md#energy-trading-p2p) |

> **OutageNotification** (schema published, [v0.1](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1)) and the **DEG demand-flex family** (`DemandFlexNeed`, `DemandFlexBuyOffer`, `DemandFlexPerformance` — see [external schemas](../schemas/external/README.md#demand-flexibility)) are published schemas without an IES use-case guide yet.

The wire envelope accepts any JSON payload; validation is opt-in per object, driven by the payload's own `@context` / `@type` declaration. The families above are the ones IES ships pre-built and validated.

### Verifiable credentials on the Exchange step

A subset of Exchange payloads are issued as W3C Verifiable Credentials — durable, holder-bound records the consumer or another stakeholder keeps independently of IES:

| Credential | What it carries |
|---|---|
| [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) | Static facts of a consumer's connection — sanctioned load, tariff, assets behind the meter |
| [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) | A signed envelope around a MeterData payload — the consumer's own readings for a window |
| [MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) | A signed proof-of-right-to-ask that a seeker presents to a meter-data provider — the one credential that rides *inside* a Beckn message |

Concepts, variants, and the trust model: **[Energy Credentials](../how-you-implement-ies/energy-credentials/README.md)**. Issue / verify / revoke operations: **[Issue Credentials](../how-you-implement-ies/issue-credentials.md)**.

---

## What you set up

For an IES participant, this page turns into three pieces of work, all in **[How you implement IES](../how-you-implement-ies/README.md)**:

1. **A Beckn adapter** — the ready-made [ONIX](../glossary.md#onix) reference software (the standard software every participant runs to speak Beckn), plus your subscriber identity and network membership: [Setup Discovery+Exchange](../how-you-implement-ies/setup-discovery-exchange.md) (network identity itself is part of [Setup Register §1.5–1.7](../how-you-implement-ies/setup-register.md#id-1.5-beckn-participants-generate-your-beckn-signing-keypair)).
2. **A credential engine**, if your use cases issue credentials — [Issue Credentials](../how-you-implement-ies/issue-credentials.md).
3. **An internal-facing mapping** — the small adapter layer that translates between your internal systems (CIS, MDM, billing, DERMS) and the IES schemas, feeding ONIX and/or OpenCred: [Build your Internal-facing Adapter](../how-you-implement-ies/build-adapter.md).

For how schemas evolve and how to propose a new one: **[Taxonomy](../schemas/README.md)**.

---

## Where this fits

| Step | Page |
|---|---|
| Step 1 — [Register](register.md) | Identity + directory |
| Steps 2+3 — Discover+Exchange *(this page)* | — |
