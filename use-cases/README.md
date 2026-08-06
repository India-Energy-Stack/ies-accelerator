# Use Case Implementation Guides

Each guide takes a real outcome and shows how to ship it on IES — what schemas it uses, what your adapter needs to do, who is involved, and what good looks like at the end.

Every guide follows the same **IES Documentation Template** (eleven numbered sections + use-case extras), and every guide's **Setup** section is organised by the same **[Register → Discover → Exchange](../README.md#how-it-works-three-steps)** spine that runs through the whole GitBook. Once you have read one guide, you know where to look in any other.

---

## Piloted in the 30-day Challenge

These four use cases were [demonstrated by the four pilot DISCOMs](../README.md#pilots-and-status) in the 30-day Challenge — a completed, historical outcome; see **[Status](../STATUS.md)** for current status.

| Use case | Issuer / Provider | Audience | Schema |
|---|---|---|---|
| **[Consumer Energy Passport](consumer-energy-passport/README.md)** | DISCOM | Consumer (held in DigiLocker) | [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) (holder-bound) |
| **[Consumer Meter Digest](consumer-meter-digest/README.md)** | DISCOM | Consumer (held in DigiLocker) | [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) (holder-bound) |
| **[Smart Meter Data Exchange](smart-meter-data-exchange/README.md)** | AMISP / DISCOM | DISCOM / SERC / consented third party | [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) |
| **[DER Visibility](der-visibility/README.md)** | DISCOM | Grid operator, aggregator | [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) energyResources, per consumer today; a PII-free per-feeder aggregate is an illustrative future profile, not yet its own schema |

## Work in progress (WIP)

These guides are still being finalised and may change.

| Use case | Issuer / Provider | Audience | Schema |
|---|---|---|---|
| **[DISCOM Regulatory Filing](discom-regulatory-filing/README.md)** | DISCOM | SERC | [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) |
| **[Policy as Code](tariff-intelligence/README.md)** | SERC | DISCOMs, applications | (tariff schema — in progress) |

## In progress

| Use case | Schema | Status |
|---|---|---|
| **[P2P Energy Transaction](p2p-energy-trading/README.md)** | [External — Energy Trading](../schemas/external/README.md) | Schema published; pilot integrations being staged |

> **OutageNotification** — the schema is published ([v0.1](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1)), but there is no IES use-case guide for outage visibility yet. See the [OutageNotification family page](../schemas/OutageNotification/README.md) for the plain-language walkthrough of what the schema covers.

---

## How each guide is organised

Each guide is a build sequence, not a specification. It runs:

1. **Scenario** — the situation the use case answers
2. **How it differs from** the neighbouring use case, where they could be confused
3. **Actors and roles** — who does what
4. **Building blocks used** — the schemas and network pieces you will need
5. **Setup: Register → Discover → Exchange** — the steps, in order
6. **Checklist** — what "done" looks like
7. **Open items** and **References**

The numbered eleven-section **IES Documentation Template** — including the field-level **Schedule I** (static fields exchanged) and **Schedule II** (live fields exchanged) — belongs to the matching [Use Case Overview](../use-cases-overview/README.md), not to these guides. Read the overview for *what* the record contains; read the guide for *how* to build it.

---

## Picking a first use case

If you are a DISCOM implementing IES for the first time, the [Build your Internal-facing Adapter guide](../how-you-implement-ies/build-adapter.md#pick-your-first-use-case) has a decision table — which use case to ship first based on what internal data is easiest for you to expose.

---

## See also

- **[Register](../what-ies-provides/register.md)** · **[Discover](../what-ies-provides/discover.md)** · **[Exchange](../what-ies-provides/exchange.md)** — the three IES steps each use case combines.
- **[How you implement IES](../how-you-implement-ies/README.md)** — the one-time setup that supports every use case.
- **[Schemas](../schemas/README.md)** — schema map showing which schemas each use case combines.
