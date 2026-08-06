# DISCOM Regulatory Filing

*A DISCOM's Aggregate Revenue Requirement (ARR), true-up, FPPCA or compliance filing submitted to its SERC as a structured, signed object — the [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) payload carried over [IES Data Exchange](../what-ies-provides/discover.md).*

{% hint style="warning" %}
🚧 **Work in progress.** This section is still being finalised and may change before sign-off.
{% endhint %}

**[Implementation Guide →](../use-cases/discom-regulatory-filing/README.md)**

| Field | Value |
|---|---|
| Document | IES/DRF-PROFILE/0.5 |
| Status | 🚧 Work in progress (WIP) |
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

Fixed order of preference: **IS → CEA → IEC → IEEE** — none apply directly, as filings are SERC instruments. IES adds:

| Standard | Role here |
|---|---|
| **Electricity Act 2003, §61–62/64** | Statutory basis |
| **SERC tariff regulations** | Form and category source (`ArrFiling` is a superset with per-state mapping) |
| **Beckn Protocol v2** | The wire |
| **W3C VC / DID Core** | Issuer key and signature |

## 6. Where Indian Standards Do Not Yet Exist

The JSON shape carrying a filing is an IES specification. SERCs' cost taxonomies vary; `ArrFiling`'s category enums are an IES superset with per-SERC mapping — the live area of work.

## 7. The Records

Three signed artefacts per submission: a **signed Beckn contract** (parties, scope, consent), a **signed `ArrFiling` payload** (inline, or signed URL with workbooks), and a **signed receipt**. Together: a non-repudiable audit trail. Not a holder-bound credential — if public-disclosure norms require it, the SERC republishes via its own BPP, same schema, settlement value `0`.

## 8. Schedule I — Static Fields of the Filing

Schedule I is a field-and-status view over the real [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5#field-reference) schema. **Normative Path** is an actual JSON path and **Schema Requires** reflects the current schema. Standards and filing guidance are informative; they do not add fields to this WIP contract.

### 8.1 Filing Identity and Control Period

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **Regulatory Basis** *(informative)* | **Filing Guidance** *(informative)* |
|---|---|---|---|---|
| `@context` | text | Optional | JSON-LD 1.1 | Use the ArrFiling v0.5 context when publishing JSON-LD |
| `objectType` | constant `ARR_FILING` | Required | ArrFiling v0.5 | Identifies the payload family |
| `id` | text | Optional | IES identifier | Unique version/object identifier where the transport does not supply one |
| `filingId` | text | Required | SERC filing reference | Stable filing reference used across submission artefacts |
| `filingDate` | date | Optional | SERC procedure | Date the filing is submitted |
| `filingType` | `MYT`, `ANNUAL`, `TRUE_UP`, `REVISED` | Optional | Electricity Act; SERC tariff regulations | Populate to distinguish the filing process |
| `licensee` | text | Required | Electricity Act licence | Full distribution-licensee name |
| `licenseeCode` / `stateProvince` | text / text | Optional | SERC register | Use the regulator-recognised code and state |
| `regulatoryCommission` | text | Required | Electricity Act; SERC register | Commission receiving the filing |
| `controlPeriodStart` / `controlPeriodEnd` | fiscal-year labels | Optional | MYT regulations | Populate for MYT/control-period submissions |
| `currency` | constant `INR` | Required | ISO 4217 | All monetary rows use this currency |
| `unitScale` | `CRORE`, `LAKH`, `ABSOLUTE` | Required | Indian regulatory filing convention | Applies to every `amount` in the filing |
| `status` | `DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, `REJECTED` | Optional | SERC workflow | Do not infer approval from transport success |
| `formReference` | text | Optional | State-specific SERC form | Identifies the principal regulatory form |
| `notes[]` | array of text | Optional | SERC filing notes | Carry explanatory footnotes and order references |
| `fiscalYears[]` | non-empty array of `ArrFiscalYear` | Required | MYT / annual / true-up structure | Include every fiscal year in scope |

### 8.2 Fiscal-year Classification

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **Filing Guidance** *(informative)* |
|---|---|---|---|
| `fiscalYears[].fiscalYear` | text label | Required | Use the SERC's fiscal-year label consistently |
| `fiscalYears[].yearType` | `BASE_YEAR`, `CONTROL_PERIOD`, `HISTORICAL` | Optional | Distinguishes reference, projected/control-period and historical rows |
| `fiscalYears[].amountBasis` | `AUDITED`, `APPROVED`, `PROPOSED`, `TRUED_UP`, `NOT_FILED` | Required | States what the year's amounts represent; do not infer it from filing status |
| `fiscalYears[].lineItems[]` | non-empty array of `ArrLineItem` | Required | Preserve stable `lineItemId` values across years for comparison |

### 8.3 ARR Line Items

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **Regulatory Basis** *(informative)* | **Filing Guidance** *(informative)* |
|---|---|---|---|---|
| `lineItems[].lineItemId` | stable text identifier | Required | IES cross-year mapping | Use stable kebab-case identifiers across filings |
| `lineItems[].serialNumber` | integer ≥ 1 | Optional | SERC form order | Preserve display order from the source form |
| `lineItems[].category` | `VARIABLE`, `FIXED`, `INCOME`, `SUB_TOTAL`, `ARR`, `ADJUSTMENT` | Required | IES superset of SERC categories | Required analytical class |
| `lineItems[].subCategory` | governed enum | Optional | State-to-common taxonomy mapping | Use the nearest common category without discarding the original heading |
| `lineItems[].head` | text | Required | Source SERC form | Preserve the filing's original row heading |
| `lineItems[].particulars` | text | Optional | Source SERC form | Add detail when the heading alone is ambiguous |
| `lineItems[].amount` | number or `null` | Required | `currency` + `unitScale` at root | `null` means present but not filed/not applicable; it is not zero |
| `lineItems[].formReference` | text | Optional | Supporting form/schedule | Points to the supporting sub-form, not a URL attachment field |
| `lineItems[].componentOf` | parent `lineItemId` | Optional | IES roll-up mapping | Links a component row to its subtotal |
| `lineItems[].formula` | human-readable expression | Optional | Filing computation | Use on subtotal/ARR rows to disclose the roll-up; consumers must not treat it as executable code |

## 9. Schedule II

**Not applicable.** A regulatory filing is complete when it is filed. Every field in Schedule I — including the per-year amounts in `fiscalYears[]` — is fixed at submission and changes only through a revised or trued-up filing, which is a new record with its own `filingId`. Nothing in this use case keeps arriving after issuance, so there is no live half to map.

Year-tagged data is not live data: `fiscalYear` and `amountBasis` say which period an amount describes, not that the amount is still being measured.

Artefacts that travel alongside the filing, and their binding, are in [Annexure D](#annexure-d-related-artefacts-and-derived-views).

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

## Annexure D — Related Artefacts and Derived Views

Artefacts bound to the filing, and views computed from it downstream. None is a field of ArrFiling v0.5.

| **Related Artefact / Relationship** | **Inside ArrFiling v0.5?** | **How it is Bound** | **Status / Treatment** |
|---|---|---|---|
| Structured filing | Yes | `filingId` plus the Schedule I fields | Authoritative machine-readable payload |
| Signed Beckn contract | No | Exchange transaction identifiers and parties | Transport/audit envelope; ArrFiling defines no VC wrapper or `proof` field |
| Signed exchange receipt | No | Beckn request/response transaction | Evidence that the SERC received the payload, not evidence of approval |
| Supporting workbook or dataset | No | Operationally linked by `filingId`; row-level `formReference` may name the source form | Separate signed dataset or signed URL; no attachment field exists in ArrFiling v0.5 |
| Prior-year filing / true-up source | No explicit cross-filing field | Stable `lineItemId` values and filing metadata support comparison | A future explicit relationship field requires schema governance |
| Tariff order / Policy as Code record | No `policyID` field in ArrFiling v0.5 | May be cited in `notes[]` or exchange metadata | Reference is informative until a governed cross-schema field exists |
| Public-disclosure copy | Same ArrFiling payload | SERC republishes through its own channel/BPP | Publication does not turn the payload into a holder-bound credential |
