# ArrFiling v0.5

*A structured, machine-readable version of the Aggregate Revenue Requirement (ARR) filing a distribution licensee submits to its state electricity regulator.*

| Field | Value |
|---|---|
| Document | IES/ARR/0.5 |
| Status | Draft for technical review. The line-item `category`/`subCategory` enumeration is an IES superset still converging across State Electricity Regulatory Commissions (SERCs); it is expected to gain additions, not stabilise as final, in this version. |
| Applicability | Issued (filed) by a distribution licensee (DISCOM); consumed by the State Electricity Regulatory Commission (SERC) or Joint Electricity Regulatory Commission that receives the filing. |
| This version | Covers the ARR filing payload only — filing metadata, per-fiscal-year basis, and line items — defined in [ArrFiling v0.5 schema.json](../../schemas/ArrFiling/v0.5/schema.json). |

## 1. Scope and Purpose

The stakeholders are the DISCOM that prepares and files its revenue requirement, and the SERC that receives, reviews and rules on it. Today, every state uses its own spreadsheet format for this filing, so a SERC that wants to compare cost structures or trends across DISCOMs — or across states — cannot do so without manually re-keying each filing, and a DISCOM operating (or a body analysing DISCOMs) across states cannot reuse a single extract from its finance system.

This document explains the **ArrFiling v0.5** schema: it does not define a new schema, it explains the existing one.

## 2. What It Records / Covers

For one regulatory filing, ArrFiling captures:

- **Identity of the filing** — a regulatory filing reference number, the filing date, and what kind of filing it is (a multi-year tariff filing, a single annual filing, a true-up, or a revised/amended filing).
- **Who is filing and to whom** — the licensee's full name and short code, the state, and the regulatory commission receiving the filing.
- **The period covered** — the control-period start and end years for multi-year filings.
- **How amounts are expressed** — the currency (fixed to INR) and the unit scale (crore, lakh, or absolute) that every amount in the filing uses.
- **Status in the regulatory process** — draft, submitted, under review, approved, or rejected.
- **Per-year detail** — for each fiscal year covered, whether it is a base year, a control-period year, or a historical year, and whether its figures are audited actuals, SERC-approved amounts, DISCOM-proposed amounts, trued-up reconciled amounts, or not yet filed.
- **The individual cost, revenue and adjustment lines** — each with its category (variable cost, fixed cost, income credit, computed subtotal, the final aggregate revenue requirement, or a true-up adjustment), a finer functional sub-classification for cross-DISCOM comparison, the heading and description as it appears on the regulatory form, the amount itself, and how each line rolls up into subtotals.

## 3. How Each Item is Identified

ArrFiling does not use decentralised identifiers (DIDs) for the objects inside the payload itself. Instead it uses two plain, stable reference schemes grounded directly in regulatory practice:

- The **filing** as a whole carries a `filingId` — the regulatory filing reference number already used by the DISCOM and SERC — plus a `licenseeCode` identifying the DISCOM.
- Each **line item** carries a `lineItemId` — a stable, kebab-case identifier (for example `power-purchase-cost`) that is reused across fiscal years so the same cost line can be tracked and compared year over year — and a `serialNumber` matching the display order on the regulatory form itself.

The payload schema itself defines no DID scheme for these identifiers. However, when an ArrFiling payload is exchanged over Beckn Data Exchange, the envelope carrying it is signed using the DISCOM's `did:web` key, so the filing as a whole is tied to a verifiable issuer identity at the transport level even though the identifiers inside the payload are plain regulatory references.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **did:web** — a DID method anchored to a domain the participant controls; the DID document (`did.json`) is fetched over HTTPS from that domain. Used here to sign the Beckn envelope carrying an ArrFiling payload.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer. ArrFiling itself is not a VC; only the transport envelope is signed.
- **Beckn Protocol** — the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks). ArrFiling payloads travel over Beckn Data Exchange.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers; the filer of an ArrFiling.
- **SERC/CERC** — State/Central Electricity Regulatory Commission, the tariff and licensing regulator for the power sector; the recipient of an ArrFiling.
- **MYT (Multi-Year Tariff)** — a filing type spanning a control period of several years, mixing actual and proposed data.
- **True-up** — a filing type that reconciles actuals against amounts previously approved by the SERC.
- **ARR (Aggregate Revenue Requirement)** — the total revenue a DISCOM is entitled to recover through tariffs; the final net line item in the schema's line-item hierarchy.

## 5. Basis of Standards

The IES order of preference is fixed, always the same:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

ArrFiling itself does not follow a metering or asset-modelling standard in this order, because it is not a technical/electrical schema — it is a regulatory-filing structure. It follows each state's own **SERC tariff regulations** (each commission's MYT / Annual Tariff Regulations define the filing form, the cost categories and the filing timetable); ArrFiling's `category`/`subCategory` enumeration is built as a superset across these SERC regulations. On the wire, it follows the **Beckn Protocol** for discovery and delivery, and **W3C VC Data Model 2.0** / **W3C DID Core** for the issuer key and signature on the Beckn envelope that carries the payload.

## 6. Where Indian Standards Do Not Yet Exist

The JSON shape that carries an ARR filing is itself an IES specification — no Indian or international standard predates a machine-readable ARR filing format. The gap this schema fills is structural, not electrical: SERCs' cost taxonomies vary state to state, so ArrFiling's `category`/`subCategory` enums are an IES-defined superset, with per-SERC mapping notes tracked in the schema. This is the live area of work referenced in the Status row above, rather than a case of an international standard substituting for a missing Indian one.

## 7. The Record(s)

ArrFiling defines one filing built from three nested, relational record types:

- **ArrFiling (root)** — issued once per regulatory submission by the DISCOM. It changes each time the DISCOM files, resubmits or revises (`filingType` covers MYT, ANNUAL, TRUE_UP and REVISED). It is the parent record: it carries the filing's identity, the parties, the currency/scale, and the overall status as the filing moves through the regulatory process (draft through submitted, under review, approved or rejected).
- **ArrFiscalYear** — one entry per fiscal year covered by the filing, nested inside ArrFiling. It changes as a year moves from proposed, to trued-up, to historical across successive filings.
- **ArrLineItem** — one entry per cost, revenue, subtotal or adjustment row, nested inside each fiscal year. Line items are the most granular and most frequently referenced record: their `lineItemId` is designed to stay stable across years so the same cost line can be compared and tracked over time, and they reference each other (via `componentOf` and `formula`) to express how subtotals and the final ARR are computed.

ArrFiling relates to other IES records at the transport level: it is carried as the payload inside a Beckn Data Exchange envelope, alongside signed contract and receipt artefacts that together form the non-repudiable audit trail of the submission — but those envelope-level artefacts are not part of the ArrFiling schema itself.

## 8. Schedule I — Field Reference (summary)

ArrFiling is built from three logical blocks:

- **ArrFiling** — global filing metadata: filing identity, licensee and regulator, control period, currency/scale, status, and the list of fiscal years.
- **ArrFiscalYear** — one fiscal year's classification (base year, control-period year, or historical) and amount basis (audited, approved, proposed, trued-up, or not filed), plus its list of line items.
- **ArrLineItem** — one cost, revenue, subtotal or adjustment row: its category and sub-category, its form heading and description, its amount, and how it rolls up into other line items.

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [ArrFiling v0.5 — Field reference](../../schemas/ArrFiling/v0.5/README.md#field-reference).

## 9. Schedule II

ArrFiling is stand-alone. It is a payload schema in its own right and does not wrap or depend on another IES schema. It is not a Verifiable Credential and defines no VC wrapper; when it travels over Beckn Data Exchange, the signature is applied to the transport envelope, not to a credential structure defined by ArrFiling itself.

## 10. How It Fits Together

ArrFiling is the payload at the centre of the DISCOM Regulatory Filing use case: a DISCOM prepares an ArrFiling v0.5 object from its finance-system extract, and delivers it as a signed, schema-validated payload over Beckn Data Exchange to the SERC, which ingests it directly rather than receiving a PDF or spreadsheet. In that exchange, the DISCOM acts as the provider (BPP) and the SERC as the consumer (BAP) — the reverse of the roles in the Smart Meter Data Exchange use case, though the same identity, signing and registry infrastructure is reused on both sides. ArrFiling itself carries only the filing content; the surrounding Beckn envelope (discovery, contract, signed receipt) is what makes the submission a non-repudiable regulatory record. Supporting workbooks, where a filing needs them, ride as separate signed datasets in the same exchange, linked back to the filing by `filingId`, rather than being embedded inside ArrFiling.

## 11. Points for Confirmation

1. **Cost-category convergence.** The `category`/`subCategory` enumeration on `ArrLineItem` is an IES superset across SERC tariff regulations, still converging; further additions are expected as more states are mapped, rather than a settled final list.
2. **Per-SERC category mapping.** Each DISCOM's mapping from its own finance-system categories to the schema's `category`/`subCategory` enums needs to be agreed and signed off (regulatory affairs and finance) before the schema can be relied on for cross-DISCOM comparison.
3. **Large workbook attachments.** The schema and its examples cover the structured filing itself; how supporting workbooks are packaged and referenced alongside an ArrFiling payload in the Beckn envelope is a delivery-layer detail outside this schema's scope, not fully specified here.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| SERC tariff regulations (state-specific MYT / Annual Tariff Regulations) | Define the filing form, cost categories and filing timetable that ArrFiling's enumerations are built to cover as a superset |
| Beckn Protocol | Discovery, negotiation and delivery of the ArrFiling payload over IES Data Exchange |
| W3C VC Data Model 2.0; W3C DID Core | Issuer key (`did:web`) and signature applied to the Beckn envelope carrying the payload |

### Annexure B — Example Payloads

Example ArrFiling payloads are at [schemas/ArrFiling/v0.5/examples/](../../schemas/ArrFiling/v0.5/examples).

### Annexure C — JSON Schema

The authoritative schema definitions are [schemas/ArrFiling/v0.5/schema.json](../../schemas/ArrFiling/v0.5/schema.json) and [schemas/ArrFiling/v0.5/attributes.yaml](../../schemas/ArrFiling/v0.5/attributes.yaml).
