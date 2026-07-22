# Use Case Overviews

Before the step-by-step implementation guide, each IES use case gets one plain-language page here — the problem it solves, who's involved, the standards basis, and where it still has open questions. This is the same **IES Documentation Template** used for [Schemas Overview](../what-ies-provides/schemas-overview/README.md) (sections 1–11, condensed Schedule I/II, Annexures A–C), applied to a use case built on top of one or more schemas.

Read one of these before the [Use Case Implementation Guide](../use-cases/README.md) if you want the *why* before the *how*.

| Use case | What it is | Status |
|---|---|---|
| **[Consumer Energy Passport](consumer-energy-passport.md)** | Holder-bound ElectricityCredential v1.2 — a consumer's verifiable proof of their connection and assets | Live in pilot |
| **[Consumer Meter Digest](consumer-meter-digest.md)** | Holder-bound MeterDataCredential v0.6 — a consumer's own meter readings, on demand | Live in pilot |
| **[Smart Meter Data Exchange](smart-meter-data-exchange.md)** | Bulk, audit-trailed MeterData v0.6 exchange between AMISP, DISCOM, SERC and consented third parties | Live in pilot |
| **[DER Visibility](der-visibility.md)** | Grid-side, PII-free ElectricityCredential v1.2 issuance — per-feeder DER visibility for operators and aggregators | Live in pilot |
| **[DISCOM Regulatory Filing](discom-regulatory-filing.md)** | Structured ArrFiling v0.5 — ARR, true-up and compliance filings from DISCOM to SERC | Live or staged |
| **[Tariff Intelligence](tariff-intelligence.md)** | Tariff orders and other policy published once, as code | Live or staged |
| **[P2P Energy Exchange](p2p-energy-trading.md)** | Two prosumers on different DISCOMs execute a direct, signed energy trade over Beckn — regulated Ledger Providers, signed-Rego settlement, no central exchange | In progress |

---

## How each page is organised

Every page follows the same eleven numbered sections as a schema overview, minus the setup checklist (that lives in the matching [implementation guide](../use-cases/README.md)):

1. **Scope and Purpose** — the problem, in plain words
2. **What It Records / Covers** — what is captured
3. **How Each Item is Identified** — DIDs, identifier patterns
4. **Definitions** — terms and acronyms
5. **Basis of Standards** — BIS → CEA → IEC → IEEE precedence
6. **Where Indian Standards Do Not Yet Exist** — gaps and the international standards used
7. **The Record(s)** — what the use case produces
8. **Schedule I — Field Reference (summary)** — linking to the full auto-generated table
9. **Schedule II** — whether this use case wraps or depends on another
10. **How It Fits Together** — diagram or short narrative
11. **Points for Confirmation** — genuinely open questions
- **Schemas Used in This Use Case**, **Value Unlock**
- **Annexure A — Standards Referenced**, **Annexure B — Example Payloads**, **Annexure C — JSON Schema**

---

## Where this fits

This section sits alongside [What IES Provides](../what-ies-provides/README.md) (the specifications) and the [Use Case Implementation Guides](../use-cases/README.md) (the step-by-step build). Read Overview → Implementation Guide → Schemas, in that order, if you're new to a use case.
