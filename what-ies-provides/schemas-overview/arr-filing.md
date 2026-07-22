# ArrFiling v0.5

*A structured, machine-readable version of the Aggregate Revenue Requirement (ARR) filing a distribution licensee submits to its state electricity regulator.*

| Field | Value |
|---|---|
| Document | IES/ARR/0.5 |
| Status | Draft for technical review. The line-item `category`/`subCategory` enumeration is an IES superset still converging across State Electricity Regulatory Commissions (SERCs); it is expected to gain additions, not stabilise as final, in this version. |
| Applicability | Issued (filed) by a distribution licensee (DISCOM); consumed by the State Electricity Regulatory Commission (SERC) or Joint Electricity Regulatory Commission that receives the filing. |
| This version | Covers the ARR filing payload only — filing metadata, per-fiscal-year basis, and line items — defined in [ArrFiling v0.5 schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/schema.json). |

## 1. Scope and Purpose

The stakeholders are the DISCOM that prepares and files its revenue requirement, and the SERC that receives, reviews and rules on it. Today, every state uses its own spreadsheet format for this filing, so a SERC that wants to compare cost structures or trends across DISCOMs — or across states — cannot do so without manually re-keying each filing, and a DISCOM operating (or a body analysing DISCOMs) across states cannot reuse a single extract from its finance system.

The schema's own design notes (in `attributes.yaml`) name four concrete format mismatches it was built to unify: multi-year tariff (MYT) wide-format filings (the working example is a DISCOM's filing to its SERC), annual single-year filings that carry historical SERC-approved data going back over a decade (the working example is a filing to a Joint ERC), differing line-item granularity (some DISCOMs file one consolidated O&M line, others split it into Employee Costs / Admin & General / Repair & Maintenance; "Return" appears in different filings as Return on Net Fixed Assets, Return on Equity, or Return on Capital Base depending on which SERC regulation applies), and line items that evolve across years as new cost heads appear and old ones get consolidated. ArrFiling v0.5 is built to hold all four patterns in the same shape rather than forcing every filer into one fixed table.

This document explains the **ArrFiling v0.5** schema: it does not define a new schema, it explains the existing one.

## 2. What It Records / Covers

For one regulatory filing, ArrFiling captures:

| Records | Detail | Source |
|---|---|---|
| Filing identity | A filing reference number (`filingId`, e.g. `"SERC/ARR/DISCOM/MYT/2024-29"`), the filing date, and `filingType`: `MYT` (multi-year control-period, mixing actual and proposed years), `ANNUAL` (single year or a run of historical approved data), `TRUE_UP` (reconciliation of actuals against previously approved amounts), or `REVISED` (an amended filing) | ArrFiling v0.5 |
| Who is filing, and to whom | The licensee's full name (`licensee`) and short code (`licenseeCode`), the state (`stateProvince`), and the receiving `regulatoryCommission` (e.g. `"SERC"`) | ArrFiling v0.5 |
| Period covered | `controlPeriodStart` / `controlPeriodEnd`, populated only for MYT filings (e.g. `"FY 2024-25"` to `"FY 2028-29"`) | ArrFiling v0.5 |
| How amounts are expressed | Currency (fixed to `INR`) and a mandatory `unitScale` (`CRORE`, `LAKH`, or `ABSOLUTE`) applied to every amount — set once for the whole document, no per-line override | ArrFiling v0.5 |
| Status in the regulatory process | `DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, or `REJECTED` | ArrFiling v0.5 |
| Regulatory form traceability | An optional `formReference` at filing level (e.g. `"Form 1"`) and line-item level (e.g. `"Form 1.1"`), plus a free-text `notes` array for footnotes and regulatory-order references that make a cost line legally precise | ArrFiling v0.5 |
| Per-year detail | For each fiscal year, a `yearType` (`BASE_YEAR`, `CONTROL_PERIOD`, `HISTORICAL`) crossed with an `amountBasis` (`AUDITED`, `APPROVED`, `PROPOSED`, `TRUED_UP`, `NOT_FILED`) — it is the *combination* that carries meaning; `NOT_FILED` marks placeholder years inside a filed control period that have no data yet | ArrFiling v0.5 |
| Cost, revenue and adjustment lines | Each with a `category` (`VARIABLE`, `FIXED`, `INCOME`, `SUB_TOTAL`, `ARR`, `ADJUSTMENT`), an optional `subCategory` (twelve values, from `POWER_PURCHASE` and `O_AND_M` through `NON_TARIFF_INCOME` and `NET_ARR`), the `head` and `particulars` as on the form, the `amount` (nullable, or negative for a credit/deduction), and roll-up into subtotals via `componentOf` and a human-readable `formula` on subtotal/ARR rows | ArrFiling v0.5 |

A concrete illustration of the amount and adjustment conventions, drawn from a real MYT filing's proposed year: `power-purchase-cost` (`VARIABLE`, `11673.43`), an `ADJUSTMENT` row `fppca-adjustment` with amount `-1434.67` ("Prior-Year Fuel Cost Adjustment"), and another ADJUSTMENT row `pp-cost-adjustment` at `-60.95` ("Power Purchase Cost Adjustment per Tariff Order for FY 2025-26") — both negative because they reduce the supply-cost subtotal they roll into, exactly as the schema's field description for `amount` specifies ("Negative values represent credits, deductions, or adjustments that reduce ARR").

## 3. How Each Item is Identified

ArrFiling does not use decentralised identifiers (DIDs) for the objects inside the payload itself. Instead it uses two plain, stable reference schemes grounded directly in regulatory practice:

- The **filing** as a whole carries a `filingId` — the regulatory filing reference number already used by the DISCOM and SERC — plus a `licenseeCode` identifying the DISCOM. Sampled `filingId` values follow a state-specific convention already in use on paper, e.g. `"SERC/ARR/DISCOM/MYT/2024-29"` for a multi-year filing and `"SERC/ARR/DISCOM/HISTORICAL/2012-2024"`-style references for a long-run historical annual filing; the schema does not impose its own ID grammar, it just carries whatever reference the regulator already assigns.
- Each **line item** carries a `lineItemId` — a stable, kebab-case identifier (for example `power-purchase-cost`, `interest-working-cap`) that is reused across fiscal years so the same cost line can be tracked and compared year over year — and a `serialNumber` matching the display order on the regulatory form itself.
- A line item's position in the roll-up hierarchy is carried by `componentOf` (the `lineItemId` of the parent subtotal or ARR row it feeds into) rather than by nesting. Sampled data shows `componentOf` can point either at an intermediate `SUB_TOTAL` (e.g. five network-cost lines all set `componentOf: network-and-sldc-cost`) or, in a simpler historical filing with only one subtotal, directly at the final `ARR` row (`non-tariff-income`'s `componentOf` is `net-arr` with no intervening subtotal). `formula` is only meaningful on `SUB_TOTAL` and `ARR` rows, and even there it is not universally populated: one sampled historical year's `total-revenue-requirement` subtotal carries no `formula` string at all, while the `net-arr` row above it does (`"total-revenue-requirement + non-tariff-income"`) — so `formula` should be treated as an optional, human-readable annotation for cross-checking, not a guaranteed computable expression on every aggregation row.

The payload schema itself defines no DID scheme for these identifiers. However, when an ArrFiling payload is exchanged over Beckn Data Exchange, the envelope carrying it is signed using the DISCOM's `did:web` key, so the filing as a whole is tied to a verifiable issuer identity at the transport level even though the identifiers inside the payload are plain regulatory references.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **did:web** — a DID method anchored to a domain the participant controls; the DID document (`did.json`) is fetched over HTTPS from that domain. Used here to sign the Beckn envelope carrying an ArrFiling payload.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer. ArrFiling itself is not a VC; only the transport envelope is signed.
- **Beckn Protocol** — the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks). ArrFiling payloads travel over Beckn Data Exchange.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers; the filer of an ArrFiling.
- **SERC/CERC/JERC** — State/Central Electricity Regulatory Commission, or a Joint Electricity Regulatory Commission serving more than one state/UT, the tariff and licensing regulator for the power sector; the recipient of an ArrFiling. The schema's `regulatoryCommission` field is deliberately free text (not an enum) precisely so it can name any of these interchangeably.
- **MYT (Multi-Year Tariff)** — a filing type (`filingType: MYT`) spanning a control period of several years, mixing actual and proposed data; carries `controlPeriodStart`/`controlPeriodEnd`.
- **True-up** — a filing type (`filingType: TRUE_UP`) that reconciles actuals against amounts previously approved by the SERC; at the fiscal-year level, the corresponding `amountBasis` value is `TRUED_UP`.
- **ARR (Aggregate Revenue Requirement)** — the total revenue a DISCOM is entitled to recover through tariffs; the final net line item in the schema's line-item hierarchy, carrying `category: ARR` and (per the sampled examples) a `subCategory` of `NET_ARR`.
- **FPPCA** — Fuel and Power Purchase Cost Adjustment: a category of `ADJUSTMENT` line item the schema explicitly calls out (alongside true-up corrections and other pass-throughs) as the kind of correction the `ADJUSTMENT` category exists to hold.

## 5. Basis of Standards

The IES order of preference is fixed: **IS → CEA Regulations/IEGC → IEC → IEEE**. ArrFiling does not follow a metering or asset-modelling standard in this order — it is a regulatory-filing structure, not a technical/electrical schema, and `attributes.yaml` carries no `x-standard` annotations. Instead:

| Standard | Role here |
|---|---|
| **SERC tariff regulations** (per state) | The filing form, cost categories and timetable (each commission's MYT / Annual Tariff Regulations). ArrFiling's `category`/`subCategory` is a superset across these, absorbing cross-DISCOM variation — e.g. "Return" as Return on Net Fixed Assets, Return on Equity, or Return on Capital Base depending on the SERC (`return-on-nfa` and `return-on-equity` both appear as `lineItemId` values) |
| **Beckn Protocol** | Discovery and delivery on the wire |
| **W3C VC Data Model 2.0 / W3C DID Core** | Issuer key and signature on the Beckn envelope that carries the payload |

## 6. Where Indian Standards Do Not Yet Exist

The JSON shape that carries an ARR filing is itself an IES specification — no Indian or international standard predates a machine-readable ARR filing format. The gap this schema fills is structural, not electrical: SERCs' cost taxonomies vary state to state, so ArrFiling's `category`/`subCategory` enums are an IES-defined superset, with per-SERC mapping notes tracked in the schema. The two sampled example filings make the scale of this variation concrete rather than abstract: one DISCOM's own historical filings shift cost-head granularity release over release — splitting O&M into `employee-costs` / `admin-general-expenses` / `repair-maintenance` in an early year, then consolidating to a single `o-and-m` line from the next year onward, while later years introduce line items (`incentive-disincentive`, `om-sharing-gain-loss`) that simply did not exist on the form in earlier years. This is the live area of work referenced in the Status row above, rather than a case of an international standard substituting for a missing Indian one.

## 7. The Record(s)

ArrFiling defines one filing built from three nested, relational record types:

- **ArrFiling (root)** — issued once per regulatory submission by the DISCOM. It changes each time the DISCOM files, resubmits or revises (`filingType` covers MYT, ANNUAL, TRUE_UP and REVISED). It is the parent record: it carries the filing's identity, the parties, the currency/scale, and the overall status as the filing moves through the regulatory process (draft through submitted, under review, approved or rejected). Only `objectType`, `filingId`, `licensee`, `regulatoryCommission`, `currency`, `unitScale`, and `fiscalYears` are required at this level — `filingDate`, `filingType`, `licenseeCode`, `stateProvince`, `controlPeriodStart`/`End`, `status`, `formReference` and `notes` are all optional, which is what lets a sparse historical filing (no `filingDate`, no control period, no notes) validate just as cleanly as a fully-annotated MYT filing.
- **ArrFiscalYear** — one entry per fiscal year covered by the filing, nested inside ArrFiling (`fiscalYears`, minimum one entry). It changes as a year moves from proposed, to trued-up, to historical across successive filings. Only `fiscalYear`, `amountBasis` and `lineItems` are required; `yearType` itself is optional, so a filing can assert what the numbers *are* (audited, approved, proposed…) without always asserting *where in the tariff cycle* the year sits.
- **ArrLineItem** — one entry per cost, revenue, subtotal or adjustment row, nested inside each fiscal year (`lineItems`, minimum one entry per year). Line items are the most granular and most frequently referenced record: their `lineItemId` is designed to stay stable across years so the same cost line can be compared and tracked over time, and they reference each other (via `componentOf` and `formula`) to express how subtotals and the final ARR are computed. Only `lineItemId`, `category`, `head` and `amount` are required — `subCategory`, `particulars`, `formReference`, `serialNumber`, `componentOf` and `formula` are all optional, which is exactly why the two sampled filings can carry line items of very different richness (one filing's notes tie individual lines to specific corrigenda; the other's historical years carry none of that annotation) while both validate against the same schema.

A worked example of the full roll-up chain, taken from a real MYT filing's proposed year: five `FIXED`/`NETWORK_COST` lines (`transmission-cost`, `sldc-cost`, `net-distribution-cost`, `pgcil-expenses`, `uldc-charges`) each set `componentOf: network-and-sldc-cost`; the `network-and-sldc-cost` `SUB_TOTAL` row then carries `formula: "transmission-cost + sldc-cost + net-distribution-cost + pgcil-expenses + uldc-charges"`. A second group of eleven lines (power purchase, distribution cost attributable to supply, interest lines, provisions, and true-up/FPPCA adjustments) all set `componentOf: supply-cost`, and `supply-cost` carries the corresponding eleven-term formula. Finally the `aggregate-arr` row (`category: ARR`) sets `formula: "network-and-sldc-cost + supply-cost"` — a two-level roll-up expressed entirely through plain-text `lineItemId` references rather than nested objects.

ArrFiling relates to other IES records at the transport level: it is carried as the payload inside a Beckn Data Exchange envelope, alongside signed contract and receipt artefacts that together form the non-repudiable audit trail of the submission — but those envelope-level artefacts are not part of the ArrFiling schema itself.

## 8. Schedule I — Field Reference (summary)

ArrFiling is built from three logical blocks:

| Block | What it contains |
|---|---|
| **ArrFiling** | global filing metadata: filing identity, licensee and regulator, control period, currency/scale, status, and the list of fiscal years |
| **ArrFiscalYear** | one fiscal year's classification (base year, control-period year, or historical) and amount basis (audited, approved, proposed, trued-up, or not filed), plus its list of line items |
| **ArrLineItem** | one cost, revenue, subtotal or adjustment row: its category and sub-category, its form heading and description, its amount, and how it rolls up into other line items |

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [ArrFiling v0.5 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5#field-reference).

## 9. Schedule II

| Wrapping / dependency | Detail |
|---|---|
| Not applicable | ArrFiling is stand-alone. It is a payload schema in its own right and does not wrap or depend on another IES schema. |
| Not a Verifiable Credential | It defines no VC wrapper; when it travels over Beckn Data Exchange, the signature is applied to the transport envelope, not to a credential structure defined by ArrFiling itself. |

## 10. How It Fits Together

ArrFiling is the payload at the centre of the DISCOM Regulatory Filing use case: a DISCOM prepares an ArrFiling v0.5 object from its finance-system extract, and delivers it as a signed, schema-validated payload over Beckn Data Exchange to the SERC, which ingests it directly rather than receiving a PDF or spreadsheet. In that exchange, the DISCOM acts as the provider (BPP) and the SERC as the consumer (BAP) — the reverse of the roles in the Smart Meter Data Exchange use case, though the same identity, signing and registry infrastructure is reused on both sides. ArrFiling itself carries only the filing content; the surrounding Beckn envelope (discovery, contract, signed receipt) is what makes the submission a non-repudiable regulatory record.

Both sampled examples publish their JSON-LD wiring the same way — an `@context` pointing at the canonical `context.jsonld` URL and an `@type` of `ArrFiling` alongside the payload's own `objectType: ARR_FILING` — so a filing can be resolved as linked data by generic tooling while still validating as a plain JSON document against `schema.json`. Supporting workbooks, where a filing needs them, ride as separate signed datasets in the same exchange, linked back to the filing by `filingId`, rather than being embedded inside ArrFiling.

## 11. Points for Confirmation

1. **Cost-category convergence.** The `category`/`subCategory` enumeration on `ArrLineItem` is an IES superset across SERC tariff regulations, still converging; further additions are expected as more states are mapped, rather than a settled final list. The two sampled filings alone already use different `lineItemId` naming for functionally similar rows across years from the same DISCOM (`return-on-nfa` vs `return-on-equity`; `employee-costs`/`admin-general-expenses`/`repair-maintenance` vs a single `o-and-m`), which is a live illustration of the convergence problem rather than a settled mapping.
2. **Per-SERC category mapping.** Each DISCOM's mapping from its own finance-system categories to the schema's `category`/`subCategory` enums needs to be agreed and signed off (regulatory affairs and finance) before the schema can be relied on for cross-DISCOM comparison.
3. **`formula` is optional and inconsistently populated even within one filing.** One sampled historical filing has a `SUB_TOTAL` row (`total-revenue-requirement`) with no `formula` string at all, while the `ARR` row above it does carry one. Any tooling built to recompute or audit roll-ups from `formula` needs to handle the case where a subtotal's formula is simply absent, rather than assuming every `SUB_TOTAL`/`ARR` row is computably self-describing.
4. **Large workbook attachments.** The schema and its examples cover the structured filing itself; how supporting workbooks are packaged and referenced alongside an ArrFiling payload in the Beckn envelope is a delivery-layer detail outside this schema's scope, not fully specified here.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| SERC tariff regulations (state-specific MYT / Annual Tariff Regulations) | Define the filing form, cost categories and filing timetable that ArrFiling's enumerations are built to cover as a superset |
| Beckn Protocol | Discovery, negotiation and delivery of the ArrFiling payload over IES Data Exchange |
| W3C VC Data Model 2.0; W3C DID Core | Issuer key (`did:web`) and signature applied to the Beckn envelope carrying the payload |

### Annexure B — Example Payloads

Example ArrFiling payloads are at [schemas/ArrFiling/v0.5/examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ArrFiling/v0.5/examples). The bundled file contains two contrasting filings: an MYT control-period filing (six fiscal years spanning audited, approved, proposed and not-yet-filed years, with a rich multi-level subtotal roll-up and adjustment lines) and a long-run historical annual filing (thirteen consecutive fiscal years from the same DISCOM, showing how line-item granularity and naming shift release over release even without any change to the schema itself).

### Annexure C — JSON Schema

The authoritative schema definitions are [schemas/ArrFiling/v0.5/schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/schema.json) and [schemas/ArrFiling/v0.5/attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/attributes.yaml).
