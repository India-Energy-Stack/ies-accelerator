# Use Case Implementation Guides

Practical, step-by-step guides for standing up each use case — actors, the dataset or credential on the wire, setup steps, and a checklist. For the *why* behind each use case (standards basis, full field schedules, value unlock), see **[Use Case Overviews](../use-cases-overview/README.md)**.

If [Identifiers](../what-ies-provides/identifiers/README.md), [Registries](../what-ies-provides/registries/README.md), [Energy Credentials](../what-ies-provides/energy-credentials/README.md) and [Data Exchange](../what-ies-provides/data-exchange/README.md) are **the building blocks**, this section is **what you build with them**.

---

## The Seven Use Cases

| # | Use Case | What it does | Primary actors | Building blocks |
|---|---|---|---|---|
| 1 | [Smart Meter Data Exchange](smart-meter-data-exchange/README.md) ([data model](smart-meter-data-exchange/ies-meter-data-model.md)) | Standard, audit-trailed exchange of `MeterData` telemetry between AMISP, DISCOM, regulator and consented third parties. | AMISP, DISCOM, SERC | Identifiers · Registries · Data Exchange · Energy Credentials (optional consent) |
| 2 | [Consumer Meter Digest](consumer-meter-digest/README.md) | Consumer pulls their own meter readings on demand as a signed credential and shares it with a third party of their choice. | Consumer, DISCOM, third-party app | Identifiers · Registries · Energy Credentials · Data Exchange |
| 3 | [Consumer Energy Passport](consumer-energy-passport/README.md) | Wallet-held credential binding consumer identity to their connection, meter, sanctioned load, and DER/storage assets — issued by the DISCOM, verifiable everywhere. | Consumer, DISCOM, verifier (bank, marketplace, society) | Identifiers · Registries · Energy Credentials |
| 4 | [DER Visibility](der-visibility/README.md) | Grid-side, PII-free issuance of the same credential schema — per-feeder view of connected DERs for the grid operator and aggregators. | DISCOM, grid operator, aggregator | Identifiers · Registries · Energy Credentials |
| 5 | [DISCOM Regulatory Filing](discom-regulatory-filing/README.md) | ARR and compliance filings delivered as structured, signed, machine-verifiable objects from DISCOM to SERC. | DISCOM, SERC | Identifiers · Registries · Data Exchange |
| 6 | [Tariff Intelligence](tariff-intelligence/README.md) | Tariff orders and data-exchange rules published once, as code, and consumed directly by billing systems, apps and meters. | SERC, DISCOM, app developer | Identifiers · Registries · Data Exchange |
| 7 | [P2P Energy Trading](p2p-energy-trading/README.md) | Inter-DISCOM prosumer-to-prosumer energy trade carried as a signed contract, settled through regulated Ledger Providers. | Prosumer, trading platform, Ledger Provider, DISCOM | Identifiers · Registries · Data Exchange · Energy Credentials |

---

## How to Read These Guides

1. **Scope** — the real-world problem this solves, and who's involved
2. **Building blocks used** — which parts of [What IES Provides](../what-ies-provides/README.md) you'll touch, and why
3. **The dataset / credential** — the data object flowing through the use case
4. **Setup: Register → Discover → Exchange** — ordered steps from cold start to a working exchange, linking to [How you implement IES](../how-you-implement-ies/README.md) for the generic mechanics
5. **Checklist** — everything, in one place, with checkboxes
6. **References** — schemas, devkit examples, further reading

---

## Maturity Snapshot

| Component | Status |
|---|---|
| Identifiers, registries, energy credentials, data exchange | Stable |
| `ElectricityCredential v1.2` (Consumer Energy Passport, DER Visibility) | Stable |
| `MeterData v0.6` / `MeterDataCredential v0.6` (Smart Meter Data Exchange, Consumer Meter Digest) | Stable |
| `ArrFiling v0.5` (DISCOM Regulatory Filing) | Draft for technical review |
| `IES_Policy` family (Tariff Intelligence) | Stable upstream; moving to `schemas/Tariff/` in this repo |
| P2P Energy Trading schemas and settlement Rego bundle | Schema stable; settlement rules in progress |

See **[Use Case Overviews](../use-cases-overview/README.md)** for the full standards basis and field schedules behind each use case.
