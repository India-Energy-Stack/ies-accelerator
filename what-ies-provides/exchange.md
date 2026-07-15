# Exchange

> **Step 3 of the three IES steps.** The Taxonomy and verifiable credentials. Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, a **verifiable credential** is issued that the holder keeps and can re-present anywhere.

Once two parties have [Registered](register.md) and [Discovered](discover.md) each other (or, for credentials, once the issuer alone is registered), the data itself moves using agreed field names and structure — the **Taxonomy**. Exchange has two parts:

| Part | Purpose | IES choice |
|---|---|---|
| **[Taxonomy](taxonomy.md)** | The master vocabulary of IES — every domain object, what it is for, which use cases combine it, how it evolves and how new ones are proposed. The shape of each object is described by its **schema**: field names, types, units, optionality — one canonical schema per object. | IES-published JSON Schema + JSON-LD context, built on public standards (DLMS/COSEM, IEEE 2030.5, OpenADR, CIM, etc.) |
| **Verifiable Credentials** | Where the use case needs a durable record — a Passport, a Digest — a W3C Verifiable Credential is issued that the holder keeps in DigiLocker or an EntityLocker. | W3C VC Data Model 2.0; W3C DID Core |

**IES does not write new standards.** It picks the right open standard for each domain — DLMS/COSEM for meter data, IEEE 2030.5 for solar and storage, OpenADR for demand response — and publishes a faithful schema on top. A schema is valid whether or not the payload ever travels over Beckn: the same `MeterData` object can ride a Beckn `on_confirm`, sit inside a signed `MeterDataCredential`, or be validated standalone.

Exchange happens over two kinds of rail, and a use case picks whichever fits:

- **B2B data exchange** — structured payloads moving between organisations, after the parties are **Registered** and have **[Discovered](discover.md)** each other. IES recommends the Beckn protocol here for its built-in discovery, consent, contract and audit trail.
- **Credential flows** — issued with [OpenCred](../glossary.md#opencred) and verified offline against the issuer's published key, credentials stand on their own and **do not require a Beckn network**. Consumer-facing (B2C) delivery happens over DigiLocker, a web portal, or any channel the issuer already runs.

---

## Don't hand-map schemas to use cases here

That lives in one place: the **[Taxonomy schema map](taxonomy.md#schema-map)** (which schema, which use cases, current version) and the plain-language **[Schemas Overview](schemas-overview/README.md)** pages (the *why* before the field-level reference). The wire envelope itself accepts any JSON payload; validation is opt-in per object, driven by the payload's own `@context` / `@type` declaration.

## Verifiable Credentials

A subset of Exchange payloads are issued as W3C Verifiable Credentials — durable, holder-bound records the consumer or another stakeholder keeps independently of IES and can re-present anywhere. A credential is verified against the issuer's published key, so issuing, holding and verifying one involves no Beckn network at all. One credential, `MeterDataRequestCredential`, is the exception that rides *inside* a Beckn message (a seeker's proof-of-right-to-ask). The three credential schemas today:

| Credential | What it carries |
|---|---|
| [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) | Static facts of a consumer's connection — sanctioned load, tariff, assets behind the meter |
| [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) | A signed envelope around a MeterData payload — consumer's own readings for a window |
| [MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) | A signed proof-of-right-to-ask that a seeker presents to a meter-data provider |

For the concept, trust model and issuance operations, see **[Energy Credentials](energy-credentials/README.md)**; to issue them, **[Issue Credentials](../how-you-implement-ies/issue-credentials.md)**.

---

## What you set up under Exchange

For an IES participant, Exchange means writing the **Part-2 mapping** — the small adapter layer that translates between your internal systems and the IES schemas:

1. Pick the use case you want to ship first.
2. Map each IES field to the corresponding column / API field / file format in your internal systems (CIS, MDM, billing, DERMS, etc.).
3. Hook the mapping into your ONIX as a BPP handler (or BAP callback), and/or into OpenCred as an issuance feed if your use case issues credentials.
4. Validate the output against the canonical JSON Schema.

For the step-by-step setup, follow **[How you implement IES → Build your Internal-facing Adapter](../how-you-implement-ies/build-adapter.md)**. If your use case issues credentials, also see **[Issue Credentials](../how-you-implement-ies/issue-credentials.md)**.

The schema canonical references — JSON Schema, JSON-LD context, RDF vocabulary, example payloads — are in the **[Taxonomy](../schemas/README.md)**.

---

## Detail pages

- **[Energy Credentials](energy-credentials/README.md)** — issuance / verification / revocation operations using OpenCred; credential variants; trust model; DigiLocker delivery.
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
