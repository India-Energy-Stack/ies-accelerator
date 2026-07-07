# DISCOM Regulatory Filing

A DISCOM's Aggregate Revenue Requirement (ARR), true-up, FPPCA or compliance filing submitted to its State Electricity Regulatory Commission (SERC) as a structured, signed object — the **[ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5)** payload carried over **[IES Data Exchange](../../what-ies-provides/data-exchange/README.md)**.

| | |
|---|---|
| **Document** | IES/DRF-PROFILE/0.5 |
| **Status** | Live or staged |
| **Applicability** | All distribution licensees and SERCs |
| **This version** | DISCOM Regulatory Filing built on [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) over Beckn. Replaces PDF/Excel submission with a machine-verifiable JSON-LD object signed by the DISCOM's `did:web`. |

---

## 1. Scope and Purpose

The **stakeholders** are the distribution licensee (DISCOM) and the SERC. Every DISCOM in India submits an ARR petition each year — a detailed projection of power-purchase, transmission, O&M, depreciation and return-on-equity costs that justifies the tariff it wants approved. The same DISCOMs file true-ups, FPPCA reconciliations, multi-year tariff petitions, and compliance returns through the year.

Today these arrive as **PDFs and Excel workbooks**. SERC staff manually re-key the numbers into analysis spreadsheets. There is no canonical machine-readable form — so no cross-DISCOM comparison, no automated trend analysis, no straight-through validation.

This document defines the **DISCOM Regulatory Filing** — a structured `ArrFiling` payload, signed by the DISCOM and delivered to the SERC over Beckn Data Exchange. The SERC ingests it directly. The signed envelope is the non-repudiable record of submission.

It does **not** change what is filed, when it is filed, or which regulatory order it answers. It standardises the **shape on the wire** and the **trust path** for that submission.

## 2. What It Records / Covers

For one filing the record carries:

- the **filing identity** — `filingId`, `licensee`, `regulatoryCommission`, `filingType` (`MYT` / `ANNUAL` / `TRUE_UP` / `REVISED`), `controlPeriodStart` / `controlPeriodEnd`, `currency`, `unitScale`;
- one or more **fiscal years** (`fiscalYears[]`), each tagged with `yearType` (`BASE_YEAR` / `CONTROL_PERIOD` / `HISTORICAL`) and `amountBasis` (`AUDITED` / `APPROVED` / `PROPOSED` / `TRUED_UP`);
- per-year **line items** (`lineItems[]`) for every cost, revenue, subtotal and adjustment heading on the regulatory form — `category` (`VARIABLE` / `FIXED` / `INCOME` / `SUB_TOTAL` / `ARR` / `ADJUSTMENT`), `subCategory`, `head`, `particulars`, `amount`, `formReference`, `componentOf`, and (for subtotals) a human-readable `formula`.

Supporting workbooks — when used — ride as separate signed datasets in the same Beckn exchange, linked by `filingId`.

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (filer) | `did:web` on owned domain | `did:web:ies.discom.example` |
| SERC (recipient) | `did:web` on owned domain | `did:web:ies.serc.example` |
| Filing | `filingId` — DISCOM-minted, stable across versions | `DISCOM-ARR-2026-27` |
| Tariff order this filing answers | `policyID` — from [Tariff Intelligence](../tariff-intelligence/README.md) | `TARIFF-ORDER-2025-26` |
| Line item | `lineItemId` — kebab-case, stable across years | `power-purchase-cost` |

The DISCOM and SERC subscriber records on the Beckn fabric resolve through the **[IES DISCOMs](../../what-ies-provides/registries/README.md#reference-allow-lists-industry-coordination)** and **[Regulators reference registries](../../what-ies-provides/registries/README.md#reference-allow-lists-industry-coordination)** for public-key lookup. Resubmissions reuse the same `filingId`; versioning lives on the Beckn envelope (`updatedAt`), not the ID.

## 4. Definitions

- **ARR** (Aggregate Revenue Requirement) — the annual revenue a DISCOM seeks recovery for, summing power-purchase, transmission, O&M, depreciation, interest and return on equity.
- **True-up** — reconciliation of actuals against amounts previously approved by the SERC.
- **FPPCA** (Fuel and Power Purchase Cost Adjustment) — quarterly / monthly pass-through reconciliation for fuel and power-purchase cost variations.
- **MYT** (Multi-Year Tariff) — a tariff regulation framework where SERCs approve costs and tariffs for a multi-year control period.
- **Control period** — the span of fiscal years covered by an MYT order.
- **Line item** — one row in the regulatory form; the smallest costed unit in the filing.
- **`amountBasis`** — declares whether a year's numbers are `AUDITED`, `APPROVED`, `PROPOSED`, or `TRUED_UP`.

## 5. Basis of Standards

IES order of preference: **IS → CEA → IEC → IEEE**. None apply to the filing itself — regulatory filings are governed by SERC tariff regulations, not standards. The IES choices on top are:

- **Electricity Act 2003, Sections 61–62 / 64** — statutory basis for tariff filings and their classes.
- **SERC tariff regulations** — each commission's MYT / Annual Tariff regulations define the form, the cost categories, and the timetable. `ArrFiling` is a **superset** of category enumerations across SERCs; mapping notes per state are tracked in the schema.
- **Beckn protocol v2** — the wire (discovery, contracting, audit).
- **W3C VC Data Model 2.0** / **W3C DID Core** — used for the issuer key (`did:web`) and signature on the Beckn envelope.

## 6. Where Indian Standards Do Not Yet Exist

The JSON shape that carries an ARR filing is an IES specification — no Indian or international standard predates it. The SERCs' cost taxonomies vary; `ArrFiling`'s `category` / `subCategory` enums are an IES superset with per-SERC mapping. The category enumeration is the live area of work.

## 7. The Records

The DISCOM Regulatory Filing produces **three signed artefacts** per submission:

1. A **signed Beckn contract** — discovery, parties (DISCOM as BPP, SERC as BAP), time-bound consent and scope;
2. A **signed `ArrFiling` v0.5 payload** — the filing itself, JSON-LD validated against `schema.json`, delivered inline (filings are small) or via signed URL when supporting workbooks accompany;
3. A **signed receipt** — who delivered what, to whom, when.

Together they form a **non-repudiable audit trail** sufficient for regulatory accountability and dispute resolution. The SERC archives the original signed envelope as the record of submission.

The filing is **not a holder-bound credential** — it does not need to be carried in a wallet. If a stakeholder (consumer-rep, researcher) needs to consume the same filing under public-disclosure norms, the SERC republishes it via its own BPP — same schema, same wire, settlement value `0`.

## 8. Schedule I — Static Fields of the Filing

The full, authoritative field tables are in the schema:

→ **[ArrFiling v0.5 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5#field-reference)**

Three tables: `ArrFiling` (root — filing identity, parties, currency, status), `ArrFiscalYear` (per-year basis and line items), `ArrLineItem` (the rows themselves). Each row carries `Field`, `Type`, the standard(s) it is **Based on**, and `Status` (Mandatory / Optional).

## 9. Schedule II — Report Templates

Not applicable as a populated downstream template. The filing is the report.

The closest interdependence is the **tariff order** the filing answers (`policyID` in [Tariff Intelligence](../tariff-intelligence/README.md)) and any **prior-year filing** it trues-up against. Both are references inside the filing, not derived templates.

## 10. How It Fits Together

```
Today                                With IES

DISCOM ── PDF/Excel ── email ── SERC ── re-key by hand
                                         ──► spreadsheet ──► tariff analysis

DISCOM ── ArrFiling v0.5 ──► Beckn ──► SERC ── ingest directly
       (signed, schema-valid)                 ──► database  ──► tariff analysis
                                              ──► archive   ──► audit trail
```

The DISCOM is the **BPP** (provider). The SERC is the **BAP** (consumer) — the inverse of the Smart Meter Data Exchange topology, but the Beckn protocol is symmetric and the ONIX stack is the same on both sides. The same identity, the same signing, the same registry — all reused. The only new thing per filing is the `ArrFiling` payload.

A SERC ingesting from multiple DISCOMs sees one schema, not n bespoke spreadsheets. Cross-DISCOM comparison becomes a database query.

## 11. Points for Confirmation

1. **Cost-category superset** — `ArrFiling` `category` / `subCategory` enums are converging across SERCs. Expect additions, not breaking renames.
2. **Workbook attachments** — convention for supporting Excel models (separate `DatasetItem` per workbook vs. embedded base64) is being agreed.
3. **Cross-filing references** — a standard shape for *"this filing answers SERC Order X"* is being aligned with the [Tariff Intelligence](../tariff-intelligence/README.md) `policyID` pattern.
4. **Public-disclosure republication** — the catalogue convention for SERC-side republication (settlement `0`) is being formalised with the Forum of Regulators.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| **[ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5)** | The payload — filing identity, fiscal years, line items |
| **[DatasetItem](../../what-ies-provides/data-exchange/README.md)** (DDM) | The Beckn envelope on the wire (`accessMethod: INLINE` for the filing; `SIGNED_URL` for any large workbook attachments) |

## Value Unlock

**For SERCs** — direct ingest replaces manual re-keying. Comparable analysis across DISCOMs becomes a single query. The signed envelope is a non-repudiable record of submission, with no PDF round-trip.

**For DISCOMs** — one canonical shape across all SERCs; the same finance-system extract serves every state once the local category mapping is signed off. Resubmissions and revisions are versioned cleanly.

**For consumer-rep parties and researchers** — when SERCs republish filings under public-disclosure norms, every objection and analysis works off the same machine-readable record, not a re-typed PDF.

---

## Setup: Register → Discover → Exchange

Built on the four implementation steps in **[How you implement IES](../../how-you-implement-ies/README.md)**. Use-case-specific items only below.

### Register — both sides

- [ ] [Identity setup](../../how-you-implement-ies/setup-register.md) complete on the DISCOM side and on the SERC side
- [ ] DISCOM in the [IES DISCOMs reference registry](../../what-ies-provides/registries/README.md#reference-allow-lists-industry-coordination)
- [ ] SERC in the [IES Regulators reference registry](../../what-ies-provides/registries/README.md#reference-allow-lists-industry-coordination)
- [ ] `filingId` minting convention agreed (typical: `<DISCOM>-ARR-<FY>` / `<DISCOM>-TRUEUP-<FY>`)

### Discover — catalogue the filing

- [ ] [Discovery setup](../../how-you-implement-ies/setup-discovery.md) complete on both sides
- [ ] DISCOM BPP publishes a Beckn catalogue entry per filing — `descriptor.name`, `filingType` (`ARR` / `TRUE_UP` / `FPPCA` / `COMPLIANCE`), `policyContext` (the SERC orders the filing answers), `accessMethod` (`INLINE` typical; `SIGNED_URL` for workbook attachments)
- [ ] Pre-agreed bilateral subscription (where the SERC subscribes to the DISCOM's filings ahead of time) skips `discover` and goes straight to `confirm`

### Exchange — adapter and submission

- [ ] [Adapter built](../../how-you-implement-ies/build-adapter.md) for [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5)
- [ ] DISCOM finance-system categories mapped to the `ArrFiling` `category` / `subCategory` enums (signed off by regulatory affairs + finance)
- [ ] Tariff-order references (`policyID`) tracked per filing so each cites the order it answers
- [ ] One prior-year filing converted, schema-validated, and reconciled line-item-by-line-item against the source PDF
- [ ] Test `confirm` → `on_confirm` → `on_status` against sandbox; both sides verify signatures
- [ ] Workbook-attachment policy decided (separate dataset / embedded / omitted)
- [ ] SERC archive stores the original signed envelope as the non-repudiation record
- [ ] Re-submission policy agreed (`updatedAt`, same `filingId`)
- [ ] One real production submission completed end-to-end
- [ ] (Optional) Public-disclosure catalogue entry published by SERC if mandated

### Team

- [ ] (DISCOM) Regulatory / finance SPOC
- [ ] (DISCOM) IT SPOC
- [ ] (SERC) IT / data SPOC
- [ ] (Both) Authorised Signatory

---

## Dev kits and code

- **Schema source** — [`schemas/ArrFiling/v0.5/attributes.yaml`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/attributes.yaml)
- **JSON Schema** — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/schema.json)
- **JSON-LD context** — [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/context.jsonld)
- **Example payloads** — [`examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ArrFiling/v0.5/examples)
- **Validation** — `python3 scripts/validate_schema.py schemas/ArrFiling/v0.5/schema.json <your-filing.json>`
- **Data Exchange devkit** — `git clone https://github.com/beckn/DEG.git && cd DEG/devkits/data-exchange/install && docker compose up -d`
- **UC2 regulatory-data Postman collection** — [`devkits/data-exchange/uc2-regulatory-data/postman/`](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc2-regulatory-data/postman)

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| Electricity Act 2003 (Sections 61–62, 64) | Statutory basis for tariff petitions and classes of filings |
| SERC MYT / Annual Tariff Regulations (state-specific) | The form, cost categories and timetable for each commission |
| Beckn Protocol v2 | Discovery, contracting and signed audit on the wire |
| W3C VC Data Model 2.0; W3C DID Core | Issuer key (`did:web`); signature on the Beckn envelope |
| JSON-LD 1.1 | Wire format and semantic resolution |

## Annexure B — Example Payloads

Example payloads (per-state filing shapes) are in the schema repository:

→ **[`schemas/ArrFiling/v0.5/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ArrFiling/v0.5/examples)**

## Annexure C — JSON Schema

- Canonical reference: `https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/`
- **[`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/schema.json)** — bundled JSON Schema (Draft 2020-12)
- **[`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/context.jsonld)**
- **[`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/vocab.jsonld)**
