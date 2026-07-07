# Exchange

> **Step 3 of the three IES steps.** Schema, taxonomy and verifiable credentials. Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, the exchange also produces a **verifiable credential** the holder keeps and can re-present anywhere.

Once parties are **Registered** and have **Discovered** each other on Beckn, the actual data moves in this step. Exchange has three parts:

| Part | Purpose | IES choice |
|---|---|---|
| **Schemas** | The agreed shape of the data on the wire — field names, types, units, optionality. One canonical shape per domain object. | IES-published JSON Schema + JSON-LD context, built on public standards (DLMS/COSEM, IEEE 2030.5, OpenADR, CIM, etc.) |
| **Verifiable Credentials** | Where the use case needs a durable record — a Passport, a Digest, a Filing — the exchange produces a W3C Verifiable Credential the holder keeps in DigiLocker or an EntityLocker. | W3C VC Data Model 2.0; W3C DID Core |
| **Taxonomy** | The master vocabulary that ties everything together — what each schema is for, which use cases use which schemas, how schemas evolve and how new ones are proposed. | The [IES Taxonomy](taxonomy.md) |

**IES does not write new standards.** It picks the right open standard for each domain — DLMS/COSEM for meter data, IEEE 2030.5 for solar and storage, OpenADR for demand response — and publishes a faithful schema on top.

---

## Schemas grouped by use case

The same set of schemas combines in different ways to deliver each use case. Each table cell links to the schema and to the use case that combines them.

### Pilot use cases (live)

| Use case | Schemas combined |
|---|---|
| [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) | [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) (holder-bound) |
| [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) | [MeterDataCredential v0.6](../schemas/MeterDataCredential/v0.6/README.md) wrapping [MeterData v0.6](../schemas/MeterData/v0.6/README.md); often paired with the consumer's [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) |
| [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) | [MeterData v0.6](../schemas/MeterData/v0.6/README.md) + [MeterDataRequest v0.6](../schemas/MeterDataRequest/v0.6/README.md) + optionally [MeterDataRequestCredential v0.1](../schemas/MeterDataRequestCredential/v0.1/README.md) |
| [DER Visibility](../use-cases/der-visibility/README.md) | [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) (grid-side issuance: `energyResources[]` only, no PII) |

### Live or staged

| Use case | Schemas combined |
|---|---|
| [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md) | [ArrFiling v0.5](../schemas/ArrFiling/v0.5/README.md) over Beckn |
| [Tariff Intelligence](../use-cases/tariff-intelligence/README.md) | `IES_Policy` family (upstream; in progress) |

### In progress

| Use case | Schemas combined |
|---|---|
| [P2P Energy Exchange](../use-cases/p2p-energy-exchange/README.md) | DEG `P2PTrade` family — [P2PTrade, DEGContract, EnergyTradeOffer, EnergyCustomer, RevenueFlow, BecknTimeSeries](../schemas/external/README.md#energy-trading-p2p) |

> **OutageNotification** (schema published, [v0.1](../schemas/OutageNotification/v0.1/README.md)) and the **DEG demand-flex family** (`DemandFlexNeed`, `DemandFlexBuyOffer`, `DemandFlexPerformance` — see [external schemas](../schemas/external/README.md#demand-flexibility)) are published schemas without an IES use-case guide yet.

---

## What you set up under Exchange

For an IES participant, Exchange means writing the **Part-2 mapping** — the small adapter layer that translates between your internal systems and the IES schemas:

1. Pick the use case you want to ship first.
2. Map each IES field to the corresponding column / API field / file format in your internal systems (CIS, MDM, billing, DERMS, etc.).
3. Hook the mapping into your ONIX as a BPP handler (or BAP callback).
4. Validate the output against the canonical JSON Schema.

For the step-by-step setup, follow **[How you implement IES → Build your Internal-facing Adapter](../how-you-implement-ies/build-adapter.md)**.

The schema canonical references — JSON Schema, JSON-LD context, RDF vocabulary, example payloads — are in **[Schemas](../schemas/README.md)**.

---

## Verifiable Credentials

A subset of Exchange payloads are issued as W3C Verifiable Credentials — durable, holder-bound records the consumer or another stakeholder keeps independently of IES and can re-present anywhere. The three credential schemas today:

| Credential | What it carries |
|---|---|
| [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) | Static facts of a consumer's connection — sanctioned load, tariff, assets behind the meter |
| [MeterDataCredential v0.6](../schemas/MeterDataCredential/v0.6/README.md) | A signed envelope around a MeterData payload — consumer's own readings for a window |
| [MeterDataRequestCredential v0.1](../schemas/MeterDataRequestCredential/v0.1/README.md) | A signed proof-of-right-to-ask that a seeker presents to a meter-data provider |

For OpenCred-based issuance, verification and revocation operations, see **[Energy Credentials](energy-credentials/README.md)**.

---

## Detail pages

- **[Energy Credentials](energy-credentials/README.md)** — issuance / verification / revocation operations using OpenCred; credential variants; trust model; DigiLocker delivery.
- **[Data Exchange — payload shapes](data-exchange/README.md#what-you-can-exchange-schema-families)** — what schemas ride on the Beckn wire, inline vs handoff.
- **[Schemas Overview](schemas-overview/README.md)** — the plain-language walkthrough of each schema, before the field-by-field reference.
- **[Schemas](../schemas/README.md)** — every schema family, every version, every example payload.
- **[External Schemas](../schemas/external/README.md)** — DEG-published schemas (P2PTrade, DemandFlex*) referenced by IES use cases.

---

## Where this fits

| Step | Page |
|---|---|
| Step 1 — [Register](register.md) | Identity + directory |
| Step 2 — [Discover](discover.md) | Beckn-protocol interaction |
| Step 3 — Exchange *(this page)* | — |

To set up the Part-2 mapping hands-on: **[Build your Internal-facing Adapter](../how-you-implement-ies/build-adapter.md)**.

For how schemas evolve and how to propose a new one: **[Taxonomy](taxonomy.md)**.
