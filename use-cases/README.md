# Use Case Implementation Guides

Each guide takes a real outcome and shows how to ship it on IES — what schemas it uses, what your adapter needs to do, who is involved, and what good looks like at the end.

Every guide follows the same **IES Documentation Template** (eleven numbered sections + use-case extras), and every guide's **Setup** section is organised by the same **[Register → Discover → Exchange](../README.md#how-ies-works-three-steps)** spine that runs through the whole GitBook. Once you have read one guide, you know where to look in any other.

---

## Live in pilot

These four use cases were [demonstrated by the four pilot DISCOMs](../concepts/pilots.md) in the 30-day Challenge (21 May – 21 June 2026).

| Use case | Issuer / Provider | Audience | Schema |
|---|---|---|---|
| **[Consumer Energy Passport](consumer-energy-passport/README.md)** | DISCOM | Consumer (held in DigiLocker) | [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) (holder-bound) |
| **[Consumer Meter Digest](consumer-meter-digest/README.md)** | DISCOM | Consumer (held in DigiLocker) | [MeterDataCredential v0.6](../schemas/MeterDataCredential/v0.6/README.md) (holder-bound) |
| **[Smart Meter Data Exchange](smart-meter-data-exchange/README.md)** | AMISP / DISCOM | DISCOM / SERC / consented third party | [MeterData v0.6](../schemas/MeterData/v0.6/README.md) |
| **[DER Visibility](der-visibility/README.md)** | DISCOM | Grid operator, aggregator | [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) energyResources |

## Live or staged

| Use case | Issuer / Provider | Audience | Schema |
|---|---|---|---|
| **[DISCOM Regulatory Filing](discom-regulatory-filing/README.md)** | DISCOM | SERC | [ArrFiling v0.5](../schemas/ArrFiling/v0.5/README.md) |
| **[Tariff Intelligence](tariff-intelligence/README.md)** | SERC | DISCOMs, applications | (tariff schema — in progress) |

## In progress

| Use case | Schema | Status |
|---|---|---|
| **[P2P Energy Exchange](p2p-energy-exchange/README.md)** | [External — Energy Trading](../schemas/external/README.md) | Schema published; pilot integrations being staged |

> **OutageNotification** — the schema is published ([v0.1](../schemas/OutageNotification/v0.1/README.md)), but there is no IES use-case guide for outage visibility yet. See the [OutageNotification schema overview](../what-ies-provides/schemas-overview/outage-notification.md) for the plain-language walkthrough of what the schema covers.

---

## How each guide is organised

Every page follows the **IES Documentation Template** — eleven sections plus the use-case-specific extras:

1. **Scope and Purpose** — the problem, in plain words
2. **What It Records / Covers** — what is captured
3. **How Each Item is Identified** — DIDs, identifier patterns
4. **Definitions** — terms and acronyms
5. **Basis of Standards** — the standards this use case follows (BIS → CEA → IEC → IEEE precedence)
6. **Where Indian Standards Do Not Yet Exist** — gaps and the international standards used
7. **The Record(s)** — the artefacts produced
8. **Schedule I — Static Fields** — field reference (links to the schema for the full table)
9. **Schedule II — Report Templates** — where applicable
10. **How It Fits Together** — diagram or short narrative
11. **Points for Confirmation** — open decisions
- **Schemas Used in This Use Case** (use-case-specific extra)
- **Value Unlock** (use-case-specific extra)
- **Setup steps (Register → Discover → Exchange)** + **Checklist** + **Dev kits**

---

## Picking a first use case

If you are a DISCOM implementing IES for the first time, the [Build your Internal-facing Adapter guide](../how-you-implement-ies/build-adapter.md#pick-your-first-use-case) has a decision table — which use case to ship first based on what internal data is easiest for you to expose.

---

## See also

- **[Register](../what-ies-provides/register.md)** · **[Discover](../what-ies-provides/discover.md)** · **[Exchange](../what-ies-provides/exchange.md)** — the three IES steps each use case combines.
- **[How you implement IES](../how-you-implement-ies/README.md)** — the one-time setup that supports every use case.
- **[Taxonomy](../what-ies-provides/taxonomy.md)** — schema map showing which schemas each use case combines.
