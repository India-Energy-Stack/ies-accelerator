# Checklist — Energy Trading

> **Status — work in progress.** Track the [Energy Trading use case](./README.md) page for moves. This checklist captures what is stable enough to plan against today.

*Plain-English rollout checklist for a trading platform vendor (BAP or BPP), a regulated Ledger Provider (LP), or a discom standing up [Energy Trading](./README.md) on the IES network. Items are use-case-specific additions on top of the canonical [Data Exchange — Onboarding Checklist](../../checklists/data-exchange-checklist.md); follow that one first.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ Buyer TP (BAP) &nbsp; ☐ Seller TP (BPP) &nbsp; ☐ Ledger Provider (LP) &nbsp; ☐ DISCOM

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Network identity in place (shared with Data Exchange)

If you have already onboarded any Beckn flow on this network, reuse the same identity. New entrants follow [Required Registries — minimum to get started](../../registries/required-registries.md#onboarding-quick-guide-minimum-to-get-started).

- [ ] DeDi subscriber record under the right network namespace
- [ ] Signing key in a secrets manager, never in config files

### 2. Devkit running end-to-end on your machine

Goal: prove the four-actor topology and the Phase-3 cascade before integrating real systems.

- [ ] `devkits/p2p-trading-ies-wave2/install/docker compose up -d` healthy
- [ ] Role-specific Postman collection imported from `uc1/postman/`; `/select` → `/init` → `/confirm` → `/status` completes end-to-end

### 3. Schemas mapped

Map your application data to the DEG schema family.

- [ ] [`P2PTrade`](https://schema.beckn.io/P2PTrade/) and [`DEGContract`](https://schema.beckn.io/DEGContract/) envelope mapped (the four roles, the policy URL)
- [ ] [`EnergyTradeOffer`](https://schema.beckn.io/EnergyTradeOffer/) populated for your catalogue (price, quantity, validity, source type)
- [ ] [`BecknTimeSeries`](https://schema.beckn.io/BecknTimeSeries/) descriptors declared for every `payloadType` you emit (`PRICE_PER_KWH` in INR, `AVAILABLE_QTY` / `REQUESTED_QTY` / `*_ALLOC` in kWh)
- [ ] (LP only) [`DiscomLedgerProvider`](https://schema.beckn.io/DiscomLedgerProvider/) entry registered (`utilityId`, `ledgerUrl`)

### 4. `degledgerrecorder` cascade configured

You do not write the cascade — you configure the plugin. Match the wave-2 patterns in the devkit ONIX configs and only edit the `participants` block.

- [ ] Plugin enabled in your ONIX config with `ledgerUriSource: payload`, `ledgerApi: beckn`
- [ ] Rule 1 (seller-side `on_confirm` cascade to your LP) — verified on the devkit
- [ ] Rule 2a (peer-TP forward at `/bap/receiver`) — verified
- [ ] Rule 2b (own-discom cascade at `/bap/receiver` when `context.bppId` does not match) — verified
- [ ] No loops: every Rule 2a path terminates at a discom (Rule 2b is the terminal sink)

### 5. Policy bundle resolved

Both bundles are published on DeDi by the network operator. Your job is to fetch, verify, and evaluate locally.

- [ ] Network policy bundle URL (`policyUrl`) resolves and signature verifies
- [ ] Settlement / revenue-flow bundle URL resolves and signature verifies
- [ ] Local OPA eval wired into the BPP / LP path: rejects payloads that fail the network rules; computes revenue flows from the final allocation
- [ ] Policy bundle version pinned per contract (so a mid-trade bundle change does not retroactively change outcomes)

### 6. DISCOM ↔ LP meter-data sub-transaction (Phase 5)

The DISCOM emits meter quantities to its contracted LP during Phase 5 as input to allocation. This reuses the **`BecknTimeSeries` payload** shape that the trade-negotiation legs already use — same envelope inside `message.contract`, just a different payloadType vocabulary for the meter-quantity values. The `MeterData` schema and the DDM `DatasetItem` envelope are **not** involved.

- [ ] (DISCOM only) Meter quantities published to the LP as `BecknTimeSeries` matching the descriptor-then-payload pattern used by the trade legs
- [ ] (LP only) Meter-quantity payloadTypes wired into the allocation function — keyed by meter ID and interval index in the descriptor

### 7. Production cut-over (shared with Data Exchange)

- [ ] HTTPS endpoint live; signing keys in a secrets manager
- [ ] Monitoring, alerting, on-call set up for the BAP / BPP / LP role you operate
- [ ] One real production trade completed and reconciled end-to-end
- [ ] Operations runbook: key rotation, policy-bundle upgrades, dispute handling

### 8. Team nominated

- [ ] IT / data SPOC (name, email, phone)
- [ ] Commercial / settlement SPOC (name, email, phone)
- [ ] Authorised Signatory (name, email, phone)

---

*Once these eight items are in place for your role and you have completed the same checklist against the counterparties on the other side of the trade, you can transact energy on IES with full audit, signed contracts, signed allocations, and signed revenue-flow computations — no central exchange, no bilateral spreadsheets. See the [Energy Trading use case](./README.md) for the protocol detail and the [Data Exchange chapter](../../data-exchange/README.md) for the underlying wire.*
