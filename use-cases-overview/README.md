# Use Case Overviews

Before the step-by-step implementation guide, each IES use case gets one plain-language page here — the problem it solves, who's involved, the standards basis, and where it still has open questions. This is the same **IES Documentation Template** used for [Schemas Overview](../what-ies-provides/schemas-overview/README.md) (sections 1–11, condensed Schedule I/II, Annexures A–C), applied to a use case built on top of one or more schemas.

Read one of these before the [Use Case Implementation Guide](../use-cases/README.md) if you want the *why* before the *how*.

| Use case | What it is | Status |
|---|---|---|
| **[Consumer Energy Passport](consumer-energy-passport.md)** | Holder-bound ElectricityCredential v1.2 — a consumer's verifiable proof of their connection and assets | Piloted ([Status](../STATUS.md)) |
| **[Consumer Meter Digest](consumer-meter-digest.md)** | Holder-bound MeterDataCredential v0.6 — a consumer's own meter readings, on demand | Piloted ([Status](../STATUS.md)) |
| **[Smart Meter Data Exchange](smart-meter-data-exchange.md)** | Bulk, audit-trailed MeterData v0.6 exchange between AMISP, DISCOM, SERC and consented third parties | Piloted ([Status](../STATUS.md)) |
| **[DER Visibility](der-visibility.md)** | Per-consumer ElectricityCredential v1.2 today; a grid-side, PII-free per-feeder aggregate is an illustrative future profile, not yet its own schema | Piloted ([Status](../STATUS.md)) |
| **[DISCOM Regulatory Filing](../draft/use-cases-overview/discom-regulatory-filing.md)** | Structured ArrFiling v0.5 — ARR, true-up and compliance filings from DISCOM to SERC | 🚧 WIP |
| **[Policy as Code](../draft/use-cases-overview/tariff-intelligence.md)** | Tariff orders and other authority policy published once, as code (flagship sub-use-case: Tariff Intelligence) | 🚧 WIP |
| **[P2P Energy Transaction](p2p-energy-trading.md)** | Two prosumers on different DISCOMs execute a direct, signed energy trade over Beckn — regulated Ledger Providers, signed-Rego settlement, no central exchange | Piloted ([Status](../STATUS.md)) |

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
8. **Schedule I — the static fields exchanged** — every field whose value is fixed when the record is issued
9. **Schedule II — the live fields exchanged** — every field that keeps arriving after issuance; "not applicable" where the use case has none
10. **How It Fits Together** — diagram or short narrative
11. **Points for Confirmation** — genuinely open questions
- **Schemas Used in This Use Case**, **Value Unlock**
- **Annexure A — Standards Referenced**, **Annexure B — Example Payloads**, **Annexure C — JSON Schema**, **Annexure D — Derived Views** (where any exist)

---

## The rule for Schedule I and Schedule II

The two Schedules divide the same thing — **the fields this use case exchanges** — along one axis, and one only:

| | Schedule I | Schedule II |
|---|---|---|
| Contains | The **static** fields | The **live** fields |
| Test | Is the value fixed when the record is issued? | Does it keep arriving after issuance? |
| Example | Sanctioned load, DER capacity, tariff category, meter serial | A 15-minute interval reading, an instantaneous voltage, a settlement actual |

**The test is not "does the field carry a timestamp."** A fiscal-year amount in a regulatory filing carries a year and is still static: it is fixed when the filing is made. A meter reading is not fixed — a new one arrives every block, forever.

Three consequences follow, and they are binding on every page:

1. **A use case with no live data has no Schedule II.** It says "not applicable" and states why. That is informative, not empty — it tells an implementer they need no telemetry pipeline for this use case.
2. **A use case whose subject *is* live data still has a Schedule I.** The static half is the contract: which meter, which profile shapes, which period, under whose authorisation. The readings themselves belong in Schedule II.
3. **Neither Schedule holds anything that is not exchanged.** Totals, peak demand, rendered reports and dashboards are computed downstream by the recipient. They belong in **Annexure D — Derived Views**.

Where a use case draws on more than one exchange, each Schedule names its own source and transport — see [DER Visibility §10.1](der-visibility.md#id-10.1-where-each-schedules-data-comes-from) for the worked case.

### How this differs from the schema overviews

The [Schemas Overview](../what-ies-provides/schemas-overview/README.md) pages use the same eleven sections, but their Schedules answer a different question, because a schema describes a *shape* rather than an *exchange*: there, Schedule I is the field reference and Schedule II records **what the schema wraps or is wrapped by**. Both conventions are correct for what they describe. A use-case page follows the static/live rule above.

---

## Where this fits

This section sits alongside [What IES Provides](../what-ies-provides/README.md) (the specifications) and the [Use Case Implementation Guides](../use-cases/README.md) (the step-by-step build). Read Overview → Implementation Guide → Schemas, in that order, if you're new to a use case.
