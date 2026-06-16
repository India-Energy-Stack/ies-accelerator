# Checklist — P2P Energy Trading

> **Status — work in progress.** Track the [P2P Energy Trading use case](./README.md) page for moves. This checklist captures what is stable enough to plan against today.

*Plain-English rollout checklist for a trading platform vendor (BAP or BPP), a regulated Ledger Provider (LP), or a discom standing up [P2P Energy Trading](./README.md) on the IES network. Items are P2P-specific additions on top of the canonical [Data Exchange — Onboarding Checklist](../../checklists/data-exchange-checklist.md); follow that one first.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ Buyer TP (BAP) &nbsp; ☐ Seller TP (BPP) &nbsp; ☐ Ledger Provider (LP) &nbsp; ☐ DISCOM

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Scope agreed

Pick the smallest first slice that exercises the four-actor topology end-to-end. A single one-hour solar slot, one buyer, one seller, one inter-discom hop is enough for Phase 1.

- [ ] Trade window agreed (one-hour / one-day / one-week slots)
- [ ] Counterparties identified (which TP, which LP on each side, which discom)
- [ ] Intra-discom or inter-discom — confirmed (intra collapses the two LPs into one)

### 2. Network identity in place (shared with Data Exchange)

If you have already onboarded any Beckn flow on this network, reuse the same identity. New entrants follow [Required Registries — minimum to get started](../../registries/required-registries.md#onboarding-quick-guide-minimum-to-get-started).

- [ ] `did:web` published on a DeDi runtime (or self-hosted) for your role
- [ ] DeDi subscriber record under the right network namespace
- [ ] Signing key in a secrets manager, never in config files

### 3. Devkit running end-to-end on your machine

Goal: prove the four-actor topology and the Phase-3 cascade before integrating real systems.

- [ ] `devkits/p2p-trading-ies-wave2/install/docker compose up -d` healthy
- [ ] `uc1/workflows/run-arazzo.sh -w select-through-settlement -v` completes green
- [ ] You can replay the run via the role-specific Postman collection

### 4. Schemas mapped

Map your application data to the DEG schema family. Don't invent — these schemas are stable.

- [ ] [`P2PTrade`](https://github.com/beckn/DEG/tree/main/specification/schema/P2PTrade) and [`DEGContract`](https://github.com/beckn/DEG/tree/main/specification/schema/DEGContract) envelope mapped (the four roles, the policy URL)
- [ ] [`EnergyTradeOffer`](https://github.com/beckn/DEG/tree/main/specification/schema/EnergyTradeOffer) populated for your catalogue (price, quantity, validity, source type)
- [ ] [`BecknTimeSeries`](https://github.com/beckn/DEG/tree/main/specification/schema/BecknTimeSeries) descriptors declared for every `payloadType` you emit (`PRICE_PER_KWH` in INR, `AVAILABLE_QTY` / `REQUESTED_QTY` / `*_ALLOC` in kWh)
- [ ] (LP only) [`DiscomLedgerProvider`](https://github.com/beckn/DEG/tree/main/specification/schema/DiscomLedgerProvider) entry registered (`utilityId`, `ledgerUrl`)

### 5. `degledgerrecorder` cascade configured

You do not write the cascade — you configure the plugin. Match the wave-2 patterns in the devkit ONIX configs and only edit the `participants` block.

- [ ] Plugin enabled in your ONIX config with `ledgerUriSource: payload`, `ledgerApi: beckn`
- [ ] Rule 1 (seller-side `on_confirm` cascade to your LP) — verified on the devkit
- [ ] Rule 2a (peer-TP forward at `/bap/receiver`) — verified
- [ ] Rule 2b (own-discom cascade at `/bap/receiver` when `context.bppId` does not match) — verified
- [ ] No loops: every Rule 2a path terminates at a discom (Rule 2b is the terminal sink)

### 6. Policy bundle resolved

Both bundles are published on DeDi by the network operator. Your job is to fetch, verify, and evaluate locally.

- [ ] Network policy bundle URL (`policyUrl`) resolves and signature verifies
- [ ] Settlement / revenue-flow bundle URL resolves and signature verifies
- [ ] Local OPA eval wired into the BPP / LP path: rejects payloads that fail the network rules; computes revenue flows from the final allocation
- [ ] Policy bundle version pinned per contract (so a mid-trade bundle change does not retroactively change outcomes)

### 7. Allocation logic

Keep it simple for Phase 1 — pro-rata across the customer's trades in the delivery window is enough. The same `/status` flow supports multiple rounds (provisional → final → true-up) by repeating with a fresh `BecknTimeSeries` payload; that is a follow-on iteration, not a Phase-1 blocker.

- [ ] (LP only) Allocation function implemented (pro-rata as the simplest case)
- [ ] (TP only) `FINAL_ALLOC = min(BUYER_DISCOM_ALLOC, SELLER_DISCOM_ALLOC)` computed and written back
- [ ] (LP only) Settled qty written to your ledger after the TPs exchange allocations

### 8. Meter-data sub-transaction

The settlement-side meter data comes off the discom over Beckn — the same pattern as [Smart Meter Data Exchange](../smart-meter-data-exchange/README.md), used as a sub-transaction inside Phase 5. When the network policy requires it, the LP attaches a [`MeterDataRequestCredential`](../../schemas/MeterDataRequestCredential/README.md) at `confirm`.

- [ ] (LP only) `MeterData` ingestion from your contracted discom over Beckn
- [ ] (LP only) `MeterDataRequestCredential` issued / verified for the consent hop
- [ ] (Discom only) `MeterData` BPP exposing your LP's meters only — scope locked to LP↔discom contract

### 9. Production cut-over (shared with Data Exchange)

- [ ] HTTPS endpoint live; signing keys in a secrets manager
- [ ] Monitoring, alerting, on-call set up for the BAP / BPP / LP role you operate
- [ ] One real production trade completed and reconciled end-to-end
- [ ] Operations runbook: key rotation, policy-bundle upgrades, dispute handling

### 10. Team nominated

- [ ] IT / data SPOC (name, email, phone)
- [ ] Commercial / settlement SPOC (name, email, phone)
- [ ] Authorised Signatory (name, email, phone)

---

*Once these ten items are in place for your role and you have completed the same checklist against the counterparties on the other side of the trade, you can transact P2P energy on IES with full audit, signed contracts, signed allocations, and signed revenue-flow computations — no central exchange, no bilateral spreadsheets. See the [P2P Energy Trading use case](./README.md) for the protocol detail and the [Data Exchange chapter](../../data-exchange/README.md) for the underlying wire.*
