# DISCOM Regulatory Filing

**In a hurry?** Jump to the [Checklist](#checklist). For the standards basis and full field schedule, see the **[Overview](../../use-cases-overview/discom-regulatory-filing.md)**.

**A DISCOM submits its Aggregate Revenue Requirement (ARR), tariff petition, true-up, or other compliance filing to a State Electricity Regulatory Commission (SERC) as a structured, signed, machine-verifiable [ArrFiling v0.5](../../schemas/ArrFiling/v0.5/README.md) object.**

---

## Scenario

Every year, every DISCOM in India submits an ARR filing to its state regulator — a detailed projection of power-purchase, transmission, O&M, depreciation, and return-on-equity costs that justifies the tariff it wants the SERC to approve. The same DISCOMs file true-up petitions, FPPCA reconciliations, multi-year tariff petitions, and various compliance returns through the year.

Today these arrive as **PDFs and Excel sheets**. SERC staff manually re-key the numbers into their analysis spreadsheets. There is no canonical machine-readable form, so no cross-DISCOM comparison, no automated trend analysis, no straight-through validation.

This use case replaces the PDF round-trip with a structured `ArrFiling` payload delivered over IES Data Exchange — signed by the DISCOM, ingested directly by the SERC, archived with a non-repudiable audit trail.

---

## Actors and Roles

| Role | Organisation (example) | What they do |
|---|---|---|
| **BPP** — data provider | DISCOM | Generates and submits the filing |
| **BAP** — data consumer | SERC | Receives, validates, and archives the filing |
| **Optional secondary consumers** | Consumer-rep parties, research orgs, Forum of Regulators | Receive the published filing via the same protocol, gated by public-disclosure norms |

Unlike Smart Meter Data Exchange, here the **DISCOM is the BPP** (data provider) and the **regulator is the BAP**. The Beckn protocol is symmetric — the same ONIX adapter runs both directions.

---

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../../what-ies-provides/register.md) | The DISCOM and SERC each have a `did:web` identity. The filing carries identifiers for the filing (`filingId`), each fiscal year, and each cost line item. |
| [Registries](../../what-ies-provides/register.md#the-directory-dedi) | For Beckn message-signature verification: DISCOM and SERC subscriber records resolved via DeDi. The [IES DISCOMs](../../what-ies-provides/register.md#the-directory-dedi) and [Regulators reference registries](../../what-ies-provides/register.md#the-directory-dedi) provide the Beckn network trust boundary. |
| [Data Exchange](../../what-ies-provides/discover-exchange.md) | Carries the `ArrFiling` payload from BPP (DISCOM) to BAP (SERC), with the same `confirm` / `on_confirm` / `status` / `on_status` lifecycle as the meter-data flow. |

---

## The Dataset — `ArrFiling v0.5`

The [`ArrFiling`](../../schemas/ArrFiling/v0.5/README.md) schema carries structured cost data for one or more fiscal years. Root fields: `filingId`, `filingType` (`MYT` / `ANNUAL` / `TRUE_UP` / `REVISED`), `licensee`, `regulatoryCommission`, `controlPeriodStart` / `controlPeriodEnd`, `currency`, `unitScale` (`CRORE` / `LAKH` / `ABSOLUTE`), `status`, and `fiscalYears[]`.

Each fiscal year (`ArrFiscalYear`) carries `yearType` (`BASE_YEAR` / `CONTROL_PERIOD` / `HISTORICAL`), `amountBasis` (`AUDITED` / `APPROVED` / `PROPOSED` / `TRUED_UP` / `NOT_FILED`), and `lineItems[]`. Each line item (`ArrLineItem`) carries `lineItemId`, `category` (`VARIABLE` / `FIXED` / `INCOME` / `SUB_TOTAL` / `ARR` / `ADJUSTMENT`), `subCategory` (e.g. `POWER_PURCHASE`, `NETWORK_COST`, `O_AND_M`, `DEPRECIATION`), `head`, `amount`, and a `formReference` back to the source regulatory form.

```json
{
  "objectType": "ARR_FILING",
  "filingId": "ABRC/ARR/XXDCL/MYT/2024-29",
  "filingType": "MYT",
  "licensee": "Alpha State Distribution Company Limited",
  "regulatoryCommission": "ABERC",
  "controlPeriodStart": "FY 2024-25",
  "controlPeriodEnd": "FY 2028-29",
  "currency": "INR",
  "unitScale": "CRORE",
  "status": "SUBMITTED",
  "fiscalYears": [{
    "fiscalYear": "FY 2023-24",
    "yearType": "BASE_YEAR",
    "amountBasis": "AUDITED",
    "lineItems": [
      { "lineItemId": "transmission-cost", "category": "FIXED", "subCategory": "NETWORK_COST",
        "head": "Transmission Cost", "amount": 873.52, "formReference": "Form 1.1" }
    ]
  }]
}
```

The `category` / `subCategory` enums follow the standard ARR cost categories most SERCs use, converging on a superset with per-state mapping notes.

> **Status — `ArrFiling` schema is a draft for technical review.** The category enumeration is the open item: SERCs use slightly different cost taxonomies and the schema is converging on a superset. Integrate against the schema's own example (`arr_filings.json`); expect small enum additions, not breaking renames.

---

## Setup: Register → Discover → Exchange

### 1. Register — both parties

- DISCOM in the [IES DISCOMs reference registry](../../what-ies-provides/register.md#the-directory-dedi); SERC in the [Regulators reference registry](../../what-ies-provides/register.md#the-directory-dedi) → **[Setup Register](../../how-you-implement-ies/setup-register.md)**.
- Mint a single canonical `filingId` per submission (typical pattern: `<COMMISSION>/ARR/<DISCOM>/<TYPE>/<FY-range>`). The same `filingId` should appear on any resubmissions — versioning lives on the data-exchange envelope, not the ID.
- If the filing responds to a specific tariff order, reference the `policyID` of that order (see [Tariff Intelligence](../tariff-intelligence/README.md)).

### 2. Discover — stand up the data-exchange adapters

The DISCOM runs a BPP adapter; the SERC runs a BAP adapter → **[Setup Discovery](../../how-you-implement-ies/setup-discovery-exchange.md)**.

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

### 3. Exchange — catalogue and submit

The DISCOM publishes the filing through its BPP catalogue with `descriptor.name`, `category` (`ARR` / `TRUE_UP` / `FPPCA` / `COMPLIANCE`), `accessMethod` (`INLINE` for filings; `SIGNED_URL` if supporting workbooks accompany it), and `policyContext` (the SERC orders the filing responds to). The regulator (BAP) initiates `confirm` against the catalogue entry; both messages are signed, and the SERC's archive stores the original signed envelope as the non-repudiable record of submission.

### 4. (Optional) Open the filing for public consumption

If the SERC mandates public disclosure, the same dataset is republished from the SERC's BPP under a public-disclosure catalogue, settlement value `0` — see [Tariff Intelligence](../tariff-intelligence/README.md) for the pattern.

---

## Why This Matters

ARR filings arrive today as PDFs/Excel sheets that regulators manually re-key. Delivering them as structured `ArrFiling` JSON — signed, timestamped, schema-validated — replaces re-keying with direct ingest, gives a non-repudiable audit trail, and lets every DISCOM submit in the same canonical shape.

---

## Open Items

- **`ArrFiling` cost-category enumeration** is converging across SERCs — expect additions, not breaking renames.
- **Workbook attachments.** The convention for supporting Excel models (separate dataset per workbook vs. embedded) is being agreed.
- **Cross-filing references.** A standard shape for *"this filing responds to SERC Order X"* is being aligned with the [Tariff Intelligence](../tariff-intelligence/README.md) `policyID` pattern.

---

## Checklist

For the DISCOM (filing) and the SERC (receiving). Role: ☐ DISCOM ☐ SERC ☐ Both.

**1. Decide which filings to start with.**

- [ ] Filing types selected (`ARR` / `TRUE_UP` / `FPPCA` / `COMPLIANCE`); source system identified for each

**2. Register both parties on the IES network.**

- [ ] DISCOM in the DISCOMs reference registry; SERC in the Regulators reference registry

**3. Agree the cost-category mapping.**

- [ ] Categories mapped to `ArrFiling` enums and signed off by regulatory affairs + finance
- [ ] Tariff-order references (`policyID`) tracked so each filing cites the order it answers

**4. Generate a sample filing as structured data.**

- [ ] One prior-year filing converted to `ArrFiling` and schema-validated against [`schema.json`](../../schemas/ArrFiling/v0.5/schema.json)
- [ ] Line-item parity confirmed against the source PDF

**5. Stand up the data-exchange adapters** — prove on the devkit first.

- [ ] Test `confirm` → `on_status` with the sample filing succeeds; both sides verify signatures

**6. Catalogue the filing and submit.**

- [ ] Catalogue entry published; SERC archives the signed envelope as the non-repudiation record
- [ ] Re-submission policy agreed (same `filingId`, new version on the envelope)

**7. (Optional) Open the filing for public consumption.**

- [ ] Public-disclosure catalogue entry published (settlement `0`), if mandated

**8. Production deployment and go-live.**

- [ ] One real production submission completed and verified

**9. Team.** [ ] Regulatory / finance SPOC · [ ] IT SPOC · [ ] Authorised Signatory

---

## References

- [`ArrFiling v0.5` schema](../../schemas/ArrFiling/v0.5/README.md)
- [Example payload](../../schemas/ArrFiling/v0.5/examples/arr_filings.json)
- [Overview — DISCOM Regulatory Filing](../../use-cases-overview/discom-regulatory-filing.md) — standards basis, definitions, full field schedule
- [Data Exchange chapter](../../what-ies-provides/discover-exchange.md)
- [Registries and Directories](../../what-ies-provides/register.md#the-directory-dedi)
- [Identifiers and Addressing](../../what-ies-provides/register.md)
