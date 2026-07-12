# Exchange

> **Step 3 of the three IES steps.** The Taxonomy and verifiable credentials. Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, a **verifiable credential** is issued that the holder keeps and can re-present anywhere.

Exchange has two parts:

| Part | Purpose | IES choice |
|---|---|---|
| **[Taxonomy](../schemas/README.md)** | The master vocabulary of IES — every domain object, what it is for, which use cases combine it, how it evolves and how new ones are proposed. The shape of each object is described by its **schema**: field names, types, units, optionality — one canonical schema per object. | IES-published JSON Schema + JSON-LD context, built on public standards (DLMS/COSEM, IEEE 2030.5, OpenADR, CIM, etc.) |
| **Verifiable Credentials** | Where the use case needs a durable record — a Passport, a Digest — a W3C Verifiable Credential is issued that the holder keeps in DigiLocker or an EntityLocker. | W3C VC Data Model 2.0; W3C DID Core |

**IES does not write new standards.** It picks the right open standard for each domain — DLMS/COSEM for meter data, IEEE 2030.5 for solar and storage, OpenADR for demand response — and publishes a faithful schema on top.

Exchange happens over two kinds of rail, and a use case picks whichever fits:

- **B2B data exchange** — structured payloads moving between organisations, after the parties are **Registered** and have **Discovered** each other. IES recommends the [Beckn data-exchange flow](data-exchange/README.md) here for its built-in discovery, consent, contract and audit trail.
- **Credential flows** — issued with [OpenCred](../glossary.md#opencred) and verified offline against the issuer's published key, credentials stand on their own and **do not require a Beckn network**. Consumer-facing (B2C) delivery happens over DigiLocker, a web portal, or any channel the issuer already runs.

---

## Schemas grouped by use case

The same set of schemas combines in different ways to deliver each use case. Each table cell links to the schema and to the use case that combines them.

### Pilot use cases (live)

| Use case | Schemas combined |
|---|---|
| [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) | [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) (holder-bound) |
| [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) | [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) wrapping [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6); often paired with the consumer's [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) |
| [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) | [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) + [MeterDataRequest v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6) + optionally [MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) |
| [DER Visibility](../use-cases/der-visibility/README.md) | [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) (grid-side issuance: `energyResources[]` only, no PII) |

### Live or staged

| Use case | Schemas combined |
|---|---|
| [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md) | [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) over Beckn |
| [Tariff Intelligence](../use-cases/tariff-intelligence/README.md) | `IES_Policy` family (upstream; in progress) |

### In progress

| Use case | Schemas combined |
|---|---|
| [P2P Energy Trading](../use-cases/p2p-energy-trading/README.md) | DEG `P2PTrade` family — [P2PTrade, DEGContract, EnergyTradeOffer, EnergyCustomer, RevenueFlow, BecknTimeSeries](../schemas/external/README.md#energy-trading-p2p) |

> **OutageNotification** (schema published, [v0.1](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1)) and the **DEG demand-flex family** (`DemandFlexNeed`, `DemandFlexBuyOffer`, `DemandFlexPerformance` — see [external schemas](../schemas/external/README.md#demand-flexibility)) are published schemas without an IES use-case guide yet.

---

## What you set up under Exchange

For an IES participant, Exchange means writing the **Part-2 mapping** — the small adapter layer that translates between your internal systems and the IES schemas:

1. Pick the use case you want to ship first.
2. Map each IES field to the corresponding column / API field / file format in your internal systems (CIS, MDM, billing, DERMS, etc.).
3. Hook the mapping into your ONIX as a BPP handler (or BAP callback).
4. Validate the output against the canonical JSON Schema.

For the step-by-step setup, follow **[How you implement IES → Build your Internal-facing Adapter](../how-you-implement-ies/build-adapter.md)**.

The schema canonical references — JSON Schema, JSON-LD context, RDF vocabulary, example payloads — are in the **[Taxonomy](../schemas/README.md)**.

---

## Verifiable Credentials

A subset of Exchange payloads are issued as W3C Verifiable Credentials — durable, holder-bound records the consumer or another stakeholder keeps independently of IES and can re-present anywhere. A credential is verified against the issuer's published key, so issuing, holding and verifying one involves no Beckn network at all. The three credential schemas today:

| Credential | What it carries |
|---|---|
| [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) | Static facts of a consumer's connection — sanctioned load, tariff, assets behind the meter |
| [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) | A signed envelope around a MeterData payload — consumer's own readings for a window |
| [MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) | A signed proof-of-right-to-ask that a seeker presents to a meter-data provider |

For OpenCred-based issuance, verification and revocation operations, see **[Energy Credentials](energy-credentials/README.md)**.

---

## Detail pages

- **[Energy Credentials](energy-credentials/README.md)** — issuance / verification / revocation operations using OpenCred; credential variants; trust model; DigiLocker delivery.
- **[Data Exchange — payload shapes](data-exchange/README.md#what-you-can-exchange-schema-families)** — what schemas ride on the Beckn wire, inline vs handoff.
- **[Taxonomy](../schemas/README.md)** — the master schema map, plain-language overview of each schema, and every version's field reference and example payloads.
- **[External Schemas](../schemas/external/README.md)** — DEG-published schemas (P2PTrade, DemandFlex*) referenced by IES use cases.

---

## Where this fits

| Step | Page |
|---|---|
| Step 1 — [Register](register.md) | Identity + directory |
| Step 2 — [Discover](discover.md) | Beckn-protocol interaction |
| Step 3 — Exchange *(this page)* | — |

To set up the Part-2 mapping hands-on: **[Build your Internal-facing Adapter](../how-you-implement-ies/build-adapter.md)**.

For how schemas evolve and how to propose a new one: **[Taxonomy](../schemas/README.md)**.
