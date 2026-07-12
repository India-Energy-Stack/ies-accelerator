# ArrFiling

*A structured, machine-readable version of the Aggregate Revenue Requirement (ARR) filing a distribution licensee submits to its state electricity regulator.*

**Status:** Draft for technical review (current: **v0.5**) · **Filed by** DISCOMs · **Received by** SERCs / Joint Electricity Regulatory Commissions

## What it records

One regulatory filing built from three nested models:

| Model | Purpose |
|-------|---------|
| `ArrFiling` | Root — filing ID, licensee, regulator, filing type (`MYT` / `ANNUAL` / `TRUE_UP` / `REVISED`), control period, currency (INR) + document-wide `unitScale`, status |
| `ArrFiscalYear` | One fiscal year — `yearType` (base / control-period / historical) crossed with `amountBasis` (audited / approved / proposed / trued-up / not-filed) |
| `ArrLineItem` | One cost, revenue, subtotal or adjustment row — category and cross-DISCOM `subCategory`, form heading, amount (nullable; negative = credit), roll-up via `componentOf` and optional human-readable `formula` |

The shape absorbs real cross-state variation: MYT wide-format and long-run historical filings, differing line-item granularity (one O&M line vs. three), and cost heads that appear or consolidate across years — without forcing filers into one fixed table.

## How things are identified

Plain regulatory references, not DIDs: the `filingId` the regulator already assigns, and stable kebab-case `lineItemId`s (`power-purchase-cost`) reused across fiscal years so lines can be compared year over year. Roll-ups are expressed through `componentOf` references rather than nesting.

## Standards basis

Each state's own **SERC tariff regulations** define the filing forms; ArrFiling's `category`/`subCategory` enums are an IES superset across them, still converging. No Indian or international standard predates a machine-readable ARR format — the gap this schema fills is structural.

## How it fits together

The payload of the **[DISCOM Regulatory Filing](../../use-cases/discom-regulatory-filing/README.md)** use case: the DISCOM (as provider) delivers the filing as a signed, schema-validated payload over the IES Beckn network to the SERC (as consumer), which ingests it directly instead of a PDF. Supporting workbooks ride as separate signed datasets linked by `filingId`.

## Open points

- The `category`/`subCategory` superset is expected to gain additions as more states are mapped; per-DISCOM mapping from finance-system categories needs sign-off before cross-DISCOM comparison.
- `formula` is optional and inconsistently populated — tooling that recomputes roll-ups must handle its absence.

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.5](v0.5/README.md) | **Current** | Three relational models: ArrFiling, ArrFiscalYear, ArrLineItem |
