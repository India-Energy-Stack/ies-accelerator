# P2P Energy Transaction

*Two prosumers on different DISCOMs execute a direct, signed energy trade over the same Beckn wire that carries dataset exchanges — the payload is a contract and its fulfilment, not a dataset. Each DISCOM is represented in the protocol by a regulated **Ledger Provider**, and settlement is computed by signed Rego policy, with no central exchange.*

**[Implementation Guide →](../use-cases/p2p-energy-trading/README.md)**

| | |
|---|---|
| **Document** | IES/P2PEX-PROFILE/2.0 |
| **Status** | Piloted — see [Status](../STATUS.md) (schema stable in DEG wave-2 devkit) |
| **Applicability** | Trading platforms, regulated Ledger Providers, DISCOMs |
| **This version** | Built on the DEG `P2PTrade` / `DEGContract` / `BecknTimeSeries` family (canonical at [schema.beckn.io](https://schema.beckn.io)) over Beckn, with signed Rego policies governing the network and contract rules. Mirrored in [External Schemas — Energy Trading](../schemas/external/README.md). |

> **Current deployment.** The architecture supports one Ledger Provider per DISCOM, but to start with **all trading platforms connect to a single Ledger Provider**, hosted at `ies-p2p-energy-ledger.beckn.io` — the two LPs in the diagrams below collapse into one (the intra-DISCOM topology; same protocol, fewer hops). The network namespaces are `indiaenergystack.in/test-ies-p2p-trading-network` (test) and `indiaenergystack.in/ies-p2p-trading-network` (production).

> **Where to go next.** This page is the *why* and the *what*. For the step-by-step build — what each actor does per phase, the ONIX config, the ledger interfaces, the payload snapshots and the setup checklist — read the **[Implementation Guide](../use-cases/p2p-energy-trading/README.md)**.

---

## 1. Scope and Purpose

The **stakeholders** are two prosumers (buyer and seller) on potentially different DISCOMs, their respective trading platforms (TPs), and the regulated Ledger Provider (LP) contracted by each DISCOM. Today, peer-to-peer energy trade requires bespoke bilateral integrations, ad-hoc settlement spreadsheets, and a central exchange-style intermediary — none of which exist in the form Indian DISCOMs need.

This document defines **P2P Energy Transaction** — a one-to-many discovery, contracting and settlement pattern carried over the same Beckn wire that carries dataset exchanges. The contract is a `DEGContract` with a `P2PTrade` body. Allocation and reconciliation flow as `BecknTimeSeries` inside the same envelope. Network rules are enforced by a **signed Rego network policy** in the adapter, and settlement terms by the seller-DISCOM's **contract policy** — a signed Rego bundle published on DeDi. Any participant evaluates locally; no central exchange.

A trading platform integrates once. The same pattern works inter-DISCOM (two LPs, one peer leg) and intra-DISCOM (one LP, the two LPs collapse).

## 2. What It Records / Covers

For one peer-to-peer trade the records carry:

| Records | Detail | Source |
|---|---|---|
| The contract | Agreed quantity, price per kWh, delivery window, the four roles (buyer / seller / buyer's DISCOM / seller's DISCOM), and the `policyUrl` for the Rego bundle in force | `DEGContract` / `P2PTrade` (DEG) |
| The offer | The seller's price, available quantity, validity window, source-type constraint (e.g. no GRID-sourced energy) | `EnergyTradeOffer` (DEG) |
| Per-interval time series | `PRICE_PER_KWH`, `AVAILABLE_QTY`, `REQUESTED_QTY`, `BUYER_DISCOM_ALLOC`, `SELLER_DISCOM_ALLOC`, `FINAL_ALLOC` | `BecknTimeSeries` (DEG) |
| LP↔DISCOM binding | Each LP's `utilityId` and ledger endpoint | `DiscomLedgerProvider` (DEG) |
| Meter-data sub-transactions | Per-DISCOM actual injected / consumed quantities per interval, supplied during reconciliation by the DISCOM to its contracted LP as input to allocation — rides inside the same `message.contract` envelope as `BecknTimeSeries`, **not** a separate `MeterData` exchange | `BecknTimeSeries` (DEG) |
| Revenue flows | Computed from the final allocation by the seller-DISCOM's **contract policy** Rego, recorded inside the contract (wire key `revenueFlows`, type `RevenueFlow`; injected by the `contractpolicyenforcer` ONIX step) | `RevenueFlow` (DEG) |

Customer PII and raw meter data stay with the customer's own DISCOM and TP. Both LPs record the confirmed contract — including the agreed price — and the cascaded allocation and settled-quantity updates.

## 3. How Each Item is Identified

Participants are identified by their plain **network subscriber IDs** — the `participantId` under which they are registered in the network registry (DeDi). No `did:web` (or any other DID scheme) is required for participants; the subscriber ID is a hostname-style string and is what appears in `context.bapId` / `context.bppId` and in the contract's `roles[]`.

| Subject | Identifier method | Example |
|---|---|---|
| Trading platform (BAP / BPP) | Network subscriber ID | `buyerapp.example.com` |
| Ledger Provider (LP) | Network subscriber ID | `seller-discom-ledger.example.com` |
| DISCOM | Network subscriber ID; bound to its LP by `utilityId` in the `DiscomLedgerProvider` block | `buyerdiscom.example.com` (`utilityId: TEST_DISCOM_BUYER`) |
| Buyer / Seller (prosumer) | Represented by their TP — the contract's `roles[buyer/seller]` carry the TP's subscriber ID; the prosumer is pinned by their meter reference | `roles[buyer].participantId = buyerapp.example.com` |
| Meter / DT / feeder referenced in the trade | Existing utility asset ID wrapped as `did:web:<discom-id>:meters:<meter-number>` (per [Register — Identifier patterns](../what-ies-provides/register.md#identifier-patterns)) | `did:web:buyerdiscom.example.com:meters:NM-44091234` |
| Network policy | Rego file loaded by the adapter (`opapolicychecker` step) from `specification/policies/` | [`p2p-trading-ies-wave2-networkpolicy.rego`](https://github.com/beckn/DEG/blob/main/specification/policies/p2p-trading-ies-wave2-networkpolicy.rego) |
| Contract policy | DeDi-published Rego record URL (`contractAttributes.policy.url`) | `https://api.dedi.global/dedi/lookup/indiaenergystack.in/ies-policies/ies-p2p-network-settlement-rego-policy-v1` |

No new identifier scheme. The four-actor topology reuses the same subscriber-registry machinery as every other IES use case; public keys resolve from the same DeDi record the subscriber ID names.

## 4. Definitions

- **Prosumer** — a consumer who can both inject (sell) and consume (buy) energy.
- **TP** (Trading Platform) — the BAP or BPP that represents a prosumer on the network and runs the matching engine.
- **LP** (Ledger Provider) — a regulated service that holds each DISCOM's slice of the trade record. Each DISCOM contracts exactly one LP; two DISCOMs may share an LP.
- **Inter-DISCOM** — buyer and seller served by different DISCOMs; two LPs involved.
- **Intra-DISCOM** — buyer and seller served by the same DISCOM; the two LPs collapse into one.
- **Discovery service** — the network service that answers `discover` queries against catalogs that provider nodes have listed via `publish-catalog`.
- **`BecknTimeSeries`** — the per-interval payload carrier; declares `payloadDescriptors` (each column's `payloadType` and `insertedBy`) and per-interval `payloads[]`.
- **Cascade** — the auto-routing by which contract and settled-quantity messages reach both TPs and both LPs in the right order; implemented by the `degledgerrecorder` ONIX plugin (see [Auto-routing of contracts and allocations](../use-cases/p2p-energy-trading/README.md#auto-routing-of-contracts-and-allocations) in the Implementation Guide).
- **Policy-as-code** — the network and contract rules as signed Rego policies, evaluated locally with OPA.

## 5. Basis of Standards

IES order of preference: **IS → CEA → IEC → IEEE**. Indian standards do not yet exist for peer-to-peer energy trade as a protocol. The IES choices:

| Standard | Role here |
|---|---|
| **Beckn Protocol v2** | The discovery / contracting / status lifecycle (`discover` → `select` → `init` → `confirm` → `status`); providers list offers to the Catalog service via `publish-catalog`, consumers query the Discovery service with `discover` |
| **DEG schema family** | `P2PTrade`, `EnergyTradeOffer`, `EnergyTradeDelivery`, `DEGContract`, `DiscomLedgerProvider`, `BecknTimeSeries` — canonical at [schema.beckn.io](https://schema.beckn.io) |
| **OPA / Rego** | The policy bundle format (standardised by CNCF) |
| **W3C VC Data Model 2.0 / W3C DID Core** | Issuer key, signing |
| **JSON-LD 1.1** | Wire format and semantic resolution |

Meter data referenced by the trade conforms to **IS 16444** and **IS 15959** — the same standards as the [Smart Meter Data Exchange](smart-meter-data-exchange.md).

## 6. Where Indian Standards Do Not Yet Exist

The whole protocol — the four-actor topology, the `BecknTimeSeries` payload vocabulary for trade negotiation, the cascaded routing, the policy-as-code framework — is an IES choice with no Indian standard predating it. The CERC Innovation Sandbox order (2023) is the regulatory umbrella; CEA / CERC standards specific to peer-to-peer trade are expected and will inform future versions.

## 7. The Records

The P2P Energy Transaction flow produces three distinct kinds of signed artefact per trade:

1. The **contract** — `DEGContract` carrying a `P2PTrade` body. Recorded by both TPs and both LPs at confirm time (each LP receives it as a blocking `on_confirm` forward from its TP).
2. The **per-interval allocation series** — `BecknTimeSeries` carrying buyer-DISCOM allocation, seller-DISCOM allocation, final allocation. Recorded by both LPs and both TPs as Phase 5 cascades.
3. The **revenue-flow record** — computed from the final allocation by the seller-DISCOM's contract policy via the `contractpolicyenforcer` ONIX step; signed by the policy author and stored in `message.contract.consideration[id=auto-settlement-flows].considerationAttributes` (wire key `revenueFlows`, type `RevenueFlow`).

Together they form a **complete, attributable audit trail** of the trade — from offer to settlement — with no central exchange.

If the use case needs a holder-bound credential — e.g. a prosumer carrying a credit-worthiness attestation in a wallet — that uses the [Consumer Energy Passport](consumer-energy-passport.md) or [Consumer Meter Digest](consumer-meter-digest.md) separately.

## 8. Schedule I — Static Fields of the Exchange

Schedule I is a use-case profile table over DEG's externally governed schema family, canonical at [schema.beckn.io](https://schema.beckn.io) and mirrored in [External Schemas — Energy Trading](../schemas/external/README.md#energy-trading-p2p). Because these fields are not maintained in this repository, the schema-qualified names below identify the upstream contract rather than local JSON-Schema paths. **Upstream Requires** follows the mirrored v2.0 field tables; **P2P Guidance** is informative use-case guidance.

### 8.1 Contract Roles and Policy

| **Upstream Field** | **Type / Allowed Value** | **Upstream Requires** | **P2P Guidance** *(informative)* |
|---|---|---|---|
| `P2PTrade` | EnergyContract subclass | Inherits its fields; defines no additional fields in the mirrored table | Contract body identifying the P2P trade profile |
| `DEGContract.roles[]` | array of role objects | Required | Carry the participant-binding roles used by the trade |
| `DEGContract.roles[].role` | text | Required per role | Network policy expects buyer, seller, buyer-DISCOM and seller-DISCOM roles |
| `DEGContract.roles[].participantId` | text or `null` | Key required per role; value may be null before binding | Bind to the registered subscriber/compound participant ID at select/init |
| `DEGContract.policy` | policy object | Required | Points to the signed Rego contract policy in force |
| `DEGContract.policy.url` / `.queryPath` | URI / text | Both required | Resolve only from the configured trusted DeDi policy prefixes |
| `DEGContract.revenueFlows[]` | array of signed role/value/currency rows | Optional legacy shape | Wave-2 settlement uses the `RevenueFlow` consideration shape in §8.4 instead |
| inherited `Contract.participants[]` | Beckn/DEG participant objects | Defined by the parent Contract schema | Carry participant attributes such as meter and utility identity; consult the canonical parent schema |

### 8.2 Offer, Customer and Order Item

| **Upstream Field** | **Type** | **Upstream Requires** | **P2P Guidance** *(informative)* |
|---|---|---|---|
| `EnergyTradeOffer.validityWindow` | time period | Optional | Expire the offer before its earliest delivery interval |
| `EnergyTradeOffer.contractAttributes` | JSON-LD object | Optional | At catalog publication, declare known roles and the contract-policy terms |
| `EnergyTradeOffer.contractAttributes.@type` | text | Required when the object is used | Normally `DEGContract` |
| `EnergyTradeOffer.commitmentAttributes` | `BecknTimeSeries` JSON-LD object | Optional | Carries seller price/available-quantity columns and their descriptor contract |
| `EnergyTradeOffer.commitmentAttributes.@type` | constant `TimeSeries` | Required when the object is used | Use the BecknTimeSeries v1.0 context |
| `EnergyCustomer.meterId` | text (`der://meter/{id}` in the upstream description) | Required | Pins the represented buyer or seller to a meter |
| `EnergyCustomer.sanctionedLoad` | number (kW) | Optional | Use only where network/contract policy evaluates the approved load |
| `EnergyCustomer.utilityCustomerId` / `.utilityId` | text / text | Optional | Utility account and service-territory binding; minimise disclosure outside regulated participants |
| `EnergyCustomer.platformUrl` | base URI | Optional | Base address for cascade sub-transactions |
| `EnergyOrderItem.providerAttributes` | object | Required | Carries the `EnergyCustomer` identity for the order item |
| `EnergyOrderItem.fulfillmentAttributes` | object | Optional | Populate only in status/update responses for delivery tracking |

### 8.3 Per-interval Negotiation and Allocation (`BecknTimeSeries`)

| **Upstream Field / Payload Type** | **Type** | **Upstream Requires** | **Writer / Role in the Trade** *(informative)* |
|---|---|---|---|
| `intervalPeriod` | ISO 8601 start + duration | Required | Defines the delivery slots |
| `payloadDescriptors[]` | event/report payload descriptors | Required | Declares every column's type, unit/currency and responsible writer |
| `intervals[]` | interval rows | Required | Carries the typed values for each slot |
| `resourceName` / `clientName` | text / text | Optional | Identifies the source resource and reporting participant |
| `PRICE_PER_KWH` | event payload, INR | Profile-required at offer/confirm | Seller platform |
| `AVAILABLE_QTY` | event payload, kWh | Profile-required in the published offer | Seller platform |
| `REQUESTED_QTY` | event payload, kWh | Profile-required after buyer selection | Buyer platform |
| `BUYER_DISCOM_ALLOC` / `BUYER_DISCOM_STATUS` | report payloads | Required by the reconciliation profile when buyer allocation is reported | Buyer DISCOM |
| `SELLER_DISCOM_ALLOC` / `SELLER_DISCOM_STATUS` | report payloads | Required by the reconciliation profile when seller allocation is reported | Seller DISCOM |
| `FINAL_ALLOC` | report payload, kWh | Required by the settled profile | Seller DISCOM; network policy enforces `FINAL_ALLOC ≤ min(buyer allocation, seller allocation)` |

Every `payloadType` used in an interval must be declared by the profile's descriptor contract. The full schema uses OpenADR's open-string payload convention; the governed P2P names above are profile constraints enforced by the network/contract policies, not a closed enum in base `BecknTimeSeries`.

### 8.4 Settlement Revenue Flow

| **Upstream Field** | **Type** | **Upstream Requires** | **P2P Guidance** *(informative)* |
|---|---|---|---|
| `consideration[].considerationAttributes.@type` | constant `RevenueFlow` in this profile | Required by the P2P settlement profile | Store policy output in the `auto-settlement-flows` consideration entry |
| `RevenueFlow.revenueFlows[]` | array of role/value/currency objects | Required | Contract-policy output must balance to zero across rows |
| `revenueFlows[].role` | text | Required | Names the buyer/seller platform or DISCOM role |
| `revenueFlows[].value` | signed number | Required | Positive receives; negative pays |
| `revenueFlows[].currency` | ISO 4217 code | Required | Use `INR` for this profile |
| `revenueFlows[].description` | text | Optional | Explain energy, wheeling, platform or shortfall components |

### 8.5 Resource and Meter-actual Binding

| **Record Surface** | **Shape** | **Contract Status** | **P2P Treatment** |
|---|---|---|---|
| Offered energy resource | `EnergyResource` discriminated union | Upstream shared schema | Minimal P2P use is stable `id` + `type`; add attributes only when policy needs them |
| Trade-side meter identity | `EnergyCustomer.meterId` | Required upstream field | Identifies the prosumer endpoint used by the trade |
| Daily injected/consumed actuals | `BecknTimeSeries` report payload types | Governed by the P2P reconciliation profile | Supplied by each DISCOM to its LP inside the contract-status flow |
| MeterData v0.6 | Separate IES telemetry schema | **Not embedded as a MeterData profile in this trade contract** | A DISCOM may derive actuals from its MeterData system, but the trade-side wire shape remains BecknTimeSeries |
| Ledger-provider binding | `DiscomLedgerProvider` upstream schema | Defined only at schema.beckn.io | Associates a regulated ledger endpoint with its DISCOM/utility ID |

## 9. Schedule II — Report Templates

Schedule II contains derived operational views; none is a separate populated IES schema.

| **Derived View** | **Schedule I Sources** | **Schema Status** | **Treatment** |
|---|---|---|---|
| Per-DISCOM monthly bill adjustment | settled `FINAL_ALLOC`, revenue-flow rows and the applicable policy | Derived | Exclude traded volume/include charges according to the signed policy and local billing rules |
| Trading-platform book of trades | confirmed contracts plus allocation/status history | Derived | Preserve contract and interval identifiers so every row traces to signed evidence |
| Ledger reconciliation statement | both LP copies, DISCOM allocation series and final allocation | Derived | Differences are exceptions; do not overwrite either signed source |
| Prosumer statement | price, requested/final quantity and applicable charges | Presentation only | May be rendered for the consumer; the signed contract and revenue flow remain authoritative |
| Network performance report | trade counts, delivery ratios and policy failures | Derived aggregate | Must not expose raw customer identifiers or meter data |
| Holder-bound credit/energy credential | Consumer Energy Passport or Consumer Meter Digest | Separate schema/use case | Do not repurpose the P2P contract as a wallet credential |

## 10. How It Fits Together

Everything buyer-side mirrors everything seller-side: a buyer prosumer and their trading platform (BAP) on one side, a seller prosumer and their trading platform (BPP) on the other, the two platforms meeting over the `select / init / confirm / status` leg. Each DISCOM is represented by one regulated Ledger Provider, and each LP pulls metered actuals daily from its own DISCOM as the input to allocation. The two LPs — one per DISCOM — never speak to each other directly; the two TPs are the only liaison between them. No central exchange. Discovery goes through the network's Discovery service: the SellerTP lists offers via `publish-catalog`, the BuyerTP queries with `discover`.

> **The block-topology diagram and the full six-phase sequence diagram** (with the automated ONIX legs shaded) live in the **[Implementation Guide → What each actor does, per phase](../use-cases/p2p-energy-trading/README.md#what-each-actor-does-per-phase)** — placed there so a developer has the topology, the wire sequence and the per-actor build steps in one place.

### The six phases

This is the inter-DISCOM flow. Intra-DISCOM (buyer and seller behind the same DISCOM) collapses Phase 2's optional limit check and Phase 5 into a single ledger. The wire sequence is drawn — with the automated (ONIX) legs shaded — in the [Implementation Guide](../use-cases/p2p-energy-trading/README.md#what-each-actor-does-per-phase); in words:

1. **Discovery** — SellerTP lists an `EnergyTradeOffer` catalog (`publish-catalog`); BuyerTP queries the Discovery service with `discover` and a JSONPath intent filter.
2. **Select and init** — quantity and price refined; optional LP headroom pre-check.
3. **Confirm** — the buyer's `confirm` is answered by the seller's `on_confirm`; as that `on_confirm` travels, each TP's `degledgerrecorder` forwards a rewritten copy to its own LP and **blocks until the LP ACKs** — seller-side before the `on_confirm` leaves for the buyer, buyer-side before the buyer app receives it. The LPs do not emit an `on_confirm` of their own; their sync ACK is the record receipt.
4. **Delivery** — seller injects, buyer consumes.
5. **Allocation and reconciliation** — **daily**, each LP asks its own DISCOM (a `status` request on the LP's `/bap/caller`) for metered actuals covering the meters and intervals that still carry an **unallocated trade**; the DISCOM answers with an `on_status` bearing those actuals, and the LP allocates its side. Either TP may then **poll** for the peer's latest allocation with a `status` request — which the peer TP's adapter auto-cascades to its own ledger before that ledger answers with a fresh `on_status`. Every allocation and settled-quantity `on_status` then cascades **symmetrically** through the two TPs to the opposite LP (an automatic forward at one TP, an automatic record at the other): buyer-side updates run `BuyerLP → BuyerTP → SellerTP → SellerLP`, seller-side updates run the mirror chain, so all four parties converge on `FINAL_ALLOC`. The `contractpolicyenforcer` step computes the revenue flows as the settled `on_status` passes the seller TP.
6. **Billing and settlement** — buyer pays seller (off-ledger via TPs); DISCOM monthly bills are adjusted accordingly.

The allocation logic on each LP can be as simple as **pro-rata across the customer's trades in the delivery window**. The same Phase-5 message flow supports multiple rounds — a provisional allocation, a final allocation after meter-data finalisation, a deviation true-up — by repeating the `/status` round-trip with a fresh `BecknTimeSeries` payload. Iteration is a payload concern, not a protocol concern.

The cascade rules, the four ledger interfaces, and the payload snapshots that make this flow concrete are in the **[Implementation Guide](../use-cases/p2p-energy-trading/README.md)**.

## 11. Points for Confirmation

1. **Wheeling / penalty tariff values** — the rates in force are whatever the seller-DISCOM's published contract policy defines; each DISCOM sets production values per its tariff order by publishing its own policy version.
2. **`contractpolicyenforcer` ONIX step** — ships in the wave-2 seller-TP config (computes revenue flows on `on_status` from the DeDi-resolved contract policy); being aligned across LP implementations.
3. **TEST → PROD `utilityId` allow-list** — the network bundle's production rules check approved IDs only; the production allow-list is governance-pending.
4. **CERC sandbox graduation** — production-grade network policy bundle awaits CERC sign-off post-sandbox.
5. **Intra-DISCOM topology** — collapsing the two LPs into one is supported and lighter; the configuration convention is in the wave-2 devkit, being formalised.
6. **Daily meter-data pull cadence** — the LP→DISCOM actuals pull is modelled as a daily job over meters and intervals with unallocated trades; the exact cadence and the retry/true-up window are per-DISCOM and being formalised.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| **[P2PTrade](https://schema.beckn.io/P2PTrade/)** | The contract `@type` — agreed quantity, price, delivery window, the four roles, the policy URL |
| **[EnergyTradeOffer](https://schema.beckn.io/EnergyTradeOffer/)** | The seller's offer block |
| **[EnergyTradeDelivery](https://schema.beckn.io/EnergyTradeDelivery/)** | The performance block populated during reconciliation |
| **[DEGContract](https://schema.beckn.io/DEGContract/)** | The envelope — roles, the rego policy URL, computed revenue flows |
| **[DiscomLedgerProvider](https://schema.beckn.io/DiscomLedgerProvider/)** | The LP↔DISCOM binding (`utilityId`, `ledgerUrl`) |
| **[BecknTimeSeries](https://schema.beckn.io/BecknTimeSeries/)** | Per-interval payload carrier — declares `payloadDescriptors` and `payloads[]` |
| **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)** *(optional)* | Seller's attestation of meter / sanctioned-load / DER details backing the offer |

A consolidated field reference is in **[External Schemas — Energy Trading](../schemas/external/README.md#energy-trading-p2p)**.

## Value Unlock

**For prosumers** — peer-to-peer trade becomes a real channel for distributed energy, with cryptographic settlement and no central exchange.

**For trading platforms** — one integration; same protocol intra- and inter-DISCOM; allocation and settlement done by signed Rego, not custom code.

**For DISCOMs** — wheeling charges and deviation penalties are the output of a signed function over a signed contract — not a bilateral spreadsheet. Visibility into peer-to-peer trade is a by-product, not a separate reporting effort.

**For regulators** — the network rules are themselves the regulation. A policy change is a new signed bundle on DeDi, picked up by every participant on next contract.

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| CERC Innovation Sandbox Order, 2023 | Regulatory umbrella for peer-to-peer trade pilots |
| Beckn Protocol v2 | Discovery, contracting, status, signed audit |
| DEG `P2PTrade` / `DEGContract` / `BecknTimeSeries` family | The payload schema family on the wire |
| OPA / Rego (CNCF) | Policy-as-code format for network and settlement bundles |
| IS 16444 (Parts 1, 2) | AC smart meter — specification (for trade-side meter quantities) |
| IS 15959 (Parts 1–3) | DLMS/COSEM data-exchange companion specification; OBIS codes |
| W3C VC Data Model 2.0; W3C DID Core | Issuer keys; signing |
| JSON-LD 1.1 | Wire format and semantic resolution |

## Annexure B — Example Payloads

The wave-2 devkit ships example payloads for every phase, per role:

→ **[`devkits/p2p-trading-ies-wave2/uc1/`](https://github.com/beckn/DEG/tree/main/devkits/p2p-trading-ies-wave2/uc1)**

## Annexure C — JSON Schema

Canonical references at **[schema.beckn.io](https://schema.beckn.io)**:

- **[P2PTrade/v2.0](https://schema.beckn.io/P2PTrade/v2.0)**
- **[DEGContract/v2.0](https://schema.beckn.io/DEGContract/v2.0)**
- **[EnergyTradeOffer/v2.0](https://schema.beckn.io/EnergyTradeOffer/v2.0)**
- **[EnergyTradeDelivery/v2.0](https://schema.beckn.io/EnergyTradeDelivery/v2.0)**
- **[DiscomLedgerProvider/v2.0](https://schema.beckn.io/DiscomLedgerProvider/v2.0)**
- **[BecknTimeSeries/v1.0](https://schema.beckn.io/BecknTimeSeries/v1.0)**

A consolidated field reference for the trade schemas (except `DiscomLedgerProvider` and `EnergyTradeDelivery`, defined only at schema.beckn.io) is in **[External Schemas — Energy Trading](../schemas/external/README.md#energy-trading-p2p)**.
