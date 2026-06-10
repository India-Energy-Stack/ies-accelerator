# ArrFiling

Schema for Aggregate Revenue Requirement (ARR) filings made by electricity distribution licensees (DISCOMs) to State Electricity Regulatory Commissions (SERCs) in India. Standardises diverse state-level regulatory filing formats into a unified structure.

**Namespace prefix:** `ies:` → `https://schema.beckn.io/ies/`

**Tags:** `regulatory` · `arr` · `discom` · `serc` · `ies`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.5](v0.5/README.md) | **Current** | Three relational models: ArrFiling, ArrFiscalYear, ArrLineItem |

---

## Models

| Model | Purpose |
|-------|---------|
| `ArrFiling` | Root metadata — filing ID, DISCOM details, SERC, control period, currency, unit scale |
| `ArrFiscalYear` | Fiscal year entry — baseline/control-period classification, amount basis (actuals/approved/proposed) |
| `ArrLineItem` | Single line item — Power Purchase Cost, O&M Expenses, Net ARR, true-up adjustments |

---

## Usage

Used in the [Regulatory Data Exchange](../../data-exchange/) flow. DISCOMs publish ARR filings as structured Beckn catalog items; SERCs and downstream systems consume them via standard discovery and retrieval flows.
