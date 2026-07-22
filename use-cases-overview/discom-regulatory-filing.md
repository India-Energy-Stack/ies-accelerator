# DISCOM Regulatory Filing

*A DISCOM's Aggregate Revenue Requirement (ARR), true-up, FPPCA or compliance filing submitted to its SERC as a structured, signed object — the [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) payload carried over [IES Data Exchange](../what-ies-provides/discover.md).*

**[Implementation Guide →](../use-cases/discom-regulatory-filing/README.md)**

| Field | Value |
|---|---|
| Document | IES/DRF-PROFILE/0.5 |
| Status | Live or staged |
| Applicability | All distribution licensees and SERCs |
| This version | Built on ArrFiling v0.5 over Beckn. Replaces PDF/Excel submission with a machine-verifiable JSON-LD object signed by the DISCOM's `did:web`. |

---

## 1. Scope and Purpose

The stakeholders are the DISCOM and the SERC. Every DISCOM files an ARR petition each year — a detailed cost projection justifying the tariff it wants approved — plus true-ups, FPPCA reconciliations, MYT petitions and compliance returns through the year.

Today these arrive as **PDFs and Excel workbooks**; SERC staff manually re-key the numbers. No canonical machine-readable form means no cross-DISCOM comparison and no automated validation.

This document defines the **DISCOM Regulatory Filing** — a structured `ArrFiling` payload, signed by the DISCOM, delivered to the SERC over Beckn. The signed envelope is the non-repudiable record of submission. It does not change what is filed or when — it standardises the **shape on the wire** and the **trust path**.

## 2. What It Records / Covers

| Records | Detail | Source |
|---|---|---|
| Filing identity | `filingId`, `licensee`, `regulatoryCommission`, `filingType` (`MYT` / `ANNUAL` / `TRUE_UP` / `REVISED`), `controlPeriodStart/End`, `currency`, `unitScale` | ArrFiling v0.5 |
| Fiscal years | One or more `fiscalYears[]`, tagged `yearType` (`BASE_YEAR` / `CONTROL_PERIOD` / `HISTORICAL`) and `amountBasis` (`AUDITED` / `APPROVED` / `PROPOSED` / `TRUED_UP`) | ArrFiling v0.5 |
| Line items | Per-year `lineItems[]` — `category` (`VARIABLE` / `FIXED` / `INCOME` / `SUB_TOTAL` / `ARR` / `ADJUSTMENT`), `subCategory`, `head`, `amount`, `formReference`, `componentOf` | ArrFiling v0.5 |

Supporting workbooks ride as separate signed datasets in the same exchange, linked by `filingId`.

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (filer) | `did:web` on owned domain | `did:web:ies.discom.example` |
| SERC (recipient) | `did:web` on owned domain | `did:web:ies.serc.example` |
| Filing | `filingId` — DISCOM-minted, stable | `DISCOM-ARR-2026-27` |
| Line item | `lineItemId` — kebab-case, stable across years | `power-purchase-cost` |

Subscriber records resolve through the [IES DISCOMs](../what-ies-provides/register.md#the-directory-dedi) and [Regulators reference registries](../what-ies-provides/register.md#the-directory-dedi). Resubmissions reuse the same `filingId`; versioning lives on the Beckn envelope.

## 4. Definitions

- **ARR** — Aggregate Revenue Requirement.
- **True-up** — reconciliation of actuals against SERC-approved amounts.
- **FPPCA** — Fuel and Power Purchase Cost Adjustment, a periodic pass-through reconciliation.
- **MYT** — Multi-Year Tariff framework; **control period** — the fiscal-year span it covers.
- **Line item** — one costed row in the regulatory form.

## 5. Basis of Standards

**IS → CEA → IEC → IEEE.** None apply directly — filings are SERC instruments. IES adds: **Electricity Act 2003 §61–62/64** (statutory basis), **SERC tariff regulations** (form and category source; `ArrFiling` is a superset with per-state mapping), **Beckn protocol v2** (the wire), **W3C VC / DID Core** (issuer key and signature).

## 6. Where Indian Standards Do Not Yet Exist

The JSON shape carrying a filing is an IES specification. SERCs' cost taxonomies vary; `ArrFiling`'s category enums are an IES superset with per-SERC mapping — the live area of work.

## 7. The Records

Three signed artefacts per submission: a **signed Beckn contract** (parties, scope, consent), a **signed `ArrFiling` payload** (inline, or signed URL with workbooks), and a **signed receipt**. Together: a non-repudiable audit trail. Not a holder-bound credential — if public-disclosure norms require it, the SERC republishes via its own BPP, same schema, settlement value `0`.

## 8. Schedule I — Static Fields of the Filing

→ **[ArrFiling v0.5 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5#field-reference)**. Three tables: `ArrFiling` (root), `ArrFiscalYear` (per-year basis and items), `ArrLineItem` (the rows).

## 9. Schedule II — Report Templates

Not applicable — the filing is the report. The closest interdependence is the tariff order it answers (`policyID`, see [Policy as Code](tariff-intelligence.md)) and any prior-year filing it trues up against — both references, not derived templates.

## 10. How It Fits Together

```
Today: DISCOM ── PDF/Excel ── email ── SERC ── re-key by hand ──► tariff analysis
With IES: DISCOM ── ArrFiling v0.5 (signed) ──► Beckn ──► SERC ── ingest directly ──► database / archive / analysis
```

The DISCOM is the **BPP**; the SERC is the **BAP** — the inverse of Smart Meter Data Exchange, but Beckn is symmetric and the same ONIX stack, identity and registry are reused. Only the `ArrFiling` payload is new per filing. A SERC ingesting from multiple DISCOMs sees one schema, not n bespoke spreadsheets.

## 11. Points for Confirmation

1. **Cost-category superset** — `category`/`subCategory` enums are converging across SERCs; expect additions, not renames.
2. **Workbook attachments** — the convention (separate dataset vs. embedded) is being agreed.
3. **Cross-filing references** — aligning with the [Policy as Code](tariff-intelligence.md) `policyID` pattern.
4. **Public-disclosure republication** — being formalised with the Forum of Regulators.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) | The payload — identity, fiscal years, line items |
| DatasetItem (DDM) | The Beckn envelope (`accessMethod: INLINE` for the filing; `SIGNED_URL` for workbooks) |

## Value Unlock

**SERCs** — direct ingest replaces manual re-keying; comparable analysis becomes a single query; a non-repudiable submission record. **DISCOMs** — one canonical shape across every SERC; clean versioning for resubmissions. **Consumer-rep parties / researchers** — public-disclosure republication gives everyone the same machine-readable record.

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| Electricity Act 2003 (§61–62, 64) | Statutory basis for tariff petitions |
| SERC MYT / Annual Tariff Regulations (state-specific) | Form, cost categories, timetable |
| Beckn Protocol v2 | Discovery, contracting, signed audit |
| W3C VC Data Model 2.0; W3C DID Core | Issuer key; envelope signature |
| JSON-LD 1.1 | Wire format and semantic resolution |

## Annexure B — Example Payloads

→ **[`schemas/ArrFiling/v0.5/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ArrFiling/v0.5/examples)**

## Annexure C — JSON Schema

Canonical: `https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/` — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/schema.json) (Draft 2020-12), [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/context.jsonld), [`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ArrFiling/v0.5/vocab.jsonld).
