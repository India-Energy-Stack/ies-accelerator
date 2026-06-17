# Use Cases

This section documents the **flagship end-to-end use cases** that the India Energy Stack (IES) building blocks come together to deliver. Each guide is self-contained: it names the actors, identifies which building blocks are used, and walks an implementer through the steps to stand the use case up — from identifier issuance to a working data or credential exchange.

If the [Identifiers](../identifiers/README.md), [Registries](../registries/README.md), [Energy Credentials](../energy-credentials/README.md), and [Data Exchange](../data-exchange/README.md) chapters describe **the building blocks**, this section describes **what you can build with them**.

---

## The Six Use Cases

| # | Use Case | What it does | Primary actors | Building blocks |
|---|---|---|---|---|
| 1 | [Smart Meter Data Exchange](smart-meter-data-exchange/README.md) ([data model](smart-meter-data-exchange/ies-meter-data-model.md)) | Standard, audit-trailed exchange of `MeterData` telemetry between AMISP, DISCOM, regulator, and consented third parties over IES Data Exchange. | AMISP, DISCOM, SERC | Identifiers · Registries · Data Exchange · Energy Credentials (optional consent) |
| 2 | [Consumer Meter Digest](consumer-meter-digest/README.md) ([checklist](consumer-meter-digest/checklist.md)) | Consumer pulls their own granular meter readings on demand as a signed credential and shares them with a third party of their choice. | Consumer, DISCOM, Third-party app | Identifiers · Registries · Energy Credentials · Data Exchange |
| 3 | [Consumer Energy Passport](consumer-energy-passport/README.md) ([checklist](consumer-energy-passport/checklist.md)) | Wallet-held credential binding consumer identity to their connection, meter, sanctioned load, and DER/storage assets — issued by the DISCOM, verifiable everywhere. | Consumer, DISCOM, Verifier (bank, marketplace, society) | Identifiers · Registries · Energy Credentials |
| 4 | [DISCOM Regulatory Filing](discom-regulatory-filing/README.md) ([checklist](discom-regulatory-filing/checklist.md)) | Aggregate Revenue Requirement (ARR) and compliance filings delivered as structured, signed, machine-verifiable objects from DISCOM to SERC. | DISCOM, SERC | Identifiers · Registries · Data Exchange |
| 5 | [Tariff Intelligence](tariff-intelligence/README.md) ([checklist](tariff-intelligence/checklist.md)) | Tariff orders (slab billing, time-of-day, deviation penalties) and data-exchange rules published as policy-as-code that billing systems, apps, and meters can consume directly. | SERC, DISCOM, App developer | Identifiers · Registries · Energy Credentials · Data Exchange |
| 6 | [P2P Energy Trading](p2p-energy-trading/README.md) ([checklist](p2p-energy-trading/checklist.md)) — **WIP** | Inter-discom prosumer-to-prosumer energy trade carried as a signed contract over IES Data Exchange. Variant of Data Exchange: same wire, the payload is `DEGContract` + `EnergyTradeDelivery` instead of `DatasetItem`. Network rules and revenue flows enforced by signed Rego bundles hosted on DeDi. | Prosumer, Trading Platform (BAP/BPP), Ledger Provider, DISCOM | Identifiers · Registries · Data Exchange · Energy Credentials |

> **DER Visibility** — tracking rooftop solar, batteries and EV chargers per feeder using IES identifiers — is a seventh flagship use case and is documented separately (out of scope for this section for now).

---

## How to Read These Guides

Each use case page follows the same structure so you can navigate quickly:

1. **Scenario** — the real-world problem this solves
2. **Actors and roles** — who is the BAP / BPP / Issuer / Holder / Verifier
3. **Building blocks used** — which IES chapters you'll touch and why
4. **Schemas and payloads** — the data objects flowing through the use case
5. **Setup steps** — ordered checklist from cold start to working exchange
6. **Operate** — how to run, observe, and verify the use case end-to-end
7. **Open items** — what is still being finalised upstream
8. **References** — canonical schemas, devkit examples, ies-docs links

---

## Maturity Snapshot (as of 2026-06)

| Component | Status |
|---|---|
| Identifier patterns and DeDi registries | Stable |
| Energy credential schemas — `ElectricityCredential v1.2` | Stable |
| Energy credential schema — `ConsumerEnergyPassport` (composite) | Draft — see [credential docs](../energy-credentials/consumer-energy-passport.md) |
| Energy credential schema — `ConsumerMeterDigest` | Draft — see [credential docs](../energy-credentials/consumer-meter-digest.md) |
| Data exchange protocol (Beckn + DDM envelope) | Stable; shipped in devkit |
| `MeterData v0.6` (meter telemetry) schema | Current canonical — supersedes the earlier `IES_Report` working name |
| `MeterDataRequest v0.6` + `MeterDataRequestCredential v0.1` | Current |
| `ArrFiling` schema | **Draft — being finalised** |
| Tariff policy schema | Stable |
| Tariff publication via data exchange | Shipped in devkit |
| P2P trade schemas (`P2PTrade`, `DEGContract`, `EnergyTradeOffer`, `EnergyTradeDelivery`, `DiscomLedgerProvider`, `BecknTimeSeries`) | Stable in DEG `p2p-trading-ies-wave2` devkit |
| P2P Rego bundle — network rules | Stable; carried by `policyUrl` on the contract |
| P2P Rego bundle — settlement / revenue flows | **Draft — wheeling and penalty placeholders pending** |

The open items (`ArrFiling`, the wheeling / penalty rules in the P2P settlement bundle, and the auto-`revenueflows` middleware in the wave-2 ONIX config) do not block implementation — the example payloads in the devkit are stable enough to integrate against, and the rego bundles can be updated independently of code via DeDi.
