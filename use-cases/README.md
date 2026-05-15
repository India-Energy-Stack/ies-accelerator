# Use Cases

This section documents the **flagship end-to-end use cases** that the India Energy Stack (IES) building blocks come together to deliver. Each guide is self-contained: it names the actors, identifies which building blocks are used, and walks an implementer through the steps to stand the use case up — from identifier issuance to a working data or credential exchange.

If the [Identifiers](../identifiers/README.md), [Registries](../registries/README.md), [Energy Credentials](../energy-credentials/README.md), and [Data Exchange](../data-exchange/README.md) chapters describe **the building blocks**, this section describes **what you can build with them**.

---

## The Five Use Cases

| # | Use Case | What it does | Primary actors | Building blocks |
|---|---|---|---|---|
| 1 | [Smart Meter Data Exchange](smart-meter-data-exchange/README.md) | Standard, audit-trailed API for sharing smart-meter data between AMISP, DISCOM, regulator, and consented third parties. | AMISP, DISCOM, SERC | Identifiers · Registries · Data Exchange |
| 2 | [Consumer Meter Digest](consumer-meter-digest.md) | Consumer pulls their own granular meter readings on demand as a signed credential and shares them with a third party of their choice. | Consumer, DISCOM, Third-party app | Identifiers · Registries · Energy Credentials · Data Exchange |
| 3 | [Consumer Energy Passport](consumer-energy-passport.md) | Wallet-held credential binding consumer identity to their connection, meter, sanctioned load, and DER/storage assets — issued by the DISCOM, verifiable everywhere. | Consumer, DISCOM, Verifier (bank, marketplace, society) | Identifiers · Registries · Energy Credentials |
| 4 | [DISCOM Regulatory Filing](discom-regulatory-filing.md) | Aggregate Revenue Requirement (ARR) and compliance filings delivered as structured, signed, machine-verifiable objects from DISCOM to SERC. | DISCOM, SERC | Identifiers · Registries · Data Exchange |
| 5 | [Tariff Intelligence](tariff-intelligence.md) | Tariff orders (slab billing, time-of-day, deviation penalties) and data-exchange rules published as policy-as-code that billing systems, apps, and meters can consume directly. | SERC, DISCOM, App developer | Identifiers · Registries · Energy Credentials · Data Exchange |

> **DER Visibility** — tracking rooftop solar, batteries and EV chargers per feeder using IES identifiers — is a sixth flagship use case and is documented separately (out of scope for this section for now).

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

## Maturity Snapshot (as of 2026-05)

| Component | Status |
|---|---|
| Identifier patterns and DeDi registries | Stable |
| Energy credential schemas — `CustomerCredential` | Stable |
| Energy credential schema — `ConsumerEnergyPassport` (composite) | Draft — see [credential docs](../energy-credentials/consumer-energy-passport.md) |
| Energy credential schema — `ConsumerMeterDigest` | Draft — see [credential docs](../energy-credentials/consumer-meter-digest.md) |
| Data exchange protocol (Beckn + DDM envelope) | Stable; shipped in devkit |
| `IES_Report` (meter telemetry) schema | **Draft — being finalised** |
| `IES_ARR_Filing` schema | **Draft — being finalised** |
| `IES_Policy` (tariff) schema | Stable |
| Tariff publication via data exchange | Shipped in devkit |

The two open items (`IES_Report` and `IES_ARR_Filing`) do not block implementation — the example payloads in the devkit are stable enough to integrate against. Treat the field names as subject to minor renames until the canonical schemas land in `India-Energy-Stack`.
