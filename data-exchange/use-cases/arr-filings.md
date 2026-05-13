# Use Case 2 — ARR Filings

**Regulatory data exchange: a DISCOM submits its Aggregate Revenue Requirement (ARR) filing to a State Electricity Regulatory Commission (SERC).**

---

## Scenario

Every year, DISCOMs submit an ARR (Aggregate Revenue Requirement) filing to their state regulator — a detailed breakdown of projected costs (power purchase, transmission, O&M, depreciation, return on equity) that justifies their proposed tariff for the coming fiscal year. Today these are submitted as PDFs or Excel sheets, manually re-keyed by regulators.

IES Data Exchange makes this machine-readable: the DISCOM publishes a structured `IES_ARR_Filing` dataset, the regulator's system consumes it directly, and the submission is logged, signed, and auditable.

---

## Roles

| Role | Organisation | What they do |
|---|---|---|
| BAP (consumer) | APERC (Andhra Pradesh Electricity Regulatory Commission) | Requests and receives the ARR filing |
| BPP (provider) | BESCOM (DISCOM) | Publishes and delivers the `IES_ARR_Filing` dataset |

Note: Unlike Use Case 1, here the **DISCOM is the BPP** (data provider) and the **regulator is the BAP** (data consumer). The protocol is symmetric.

---

## Dataset — IES_ARR_Filing

The `IES_ARR_Filing` schema carries structured cost data for one or more fiscal years.

### Structure

```json
{
  "filingId": "BESCOM-ARR-2026-27",
  "licensee": "BESCOM",
  "state": "Karnataka",
  "regulatoryCommission": "KERC",
  "submissionDate": "2026-01-15",
  "fiscalYears": [
    {
      "year": "2026-27",
      "totalRevenueRequirementCrINR": 18432.5,
      "lineItems": [
        {
          "category": "Power Purchase Cost",
          "subcategory": "Long-term PPAs",
          "amountCrINR": 12450.5,
          "notes": "Includes 1200 MW coal + 800 MW solar"
        },
        {
          "category": "Transmission Charges",
          "subcategory": "PGCIL charges",
          "amountCrINR": 1823.2
        },
        {
          "category": "O&M Expenses",
          "subcategory": "Employee costs",
          "amountCrINR": 892.7
        },
        {
          "category": "Depreciation",
          "amountCrINR": 634.1
        },
        {
          "category": "Return on Equity",
          "amountCrINR": 632.0
        }
      ]
    }
  ]
}
```

| Field | Description |
|---|---|
| `filingId` | Unique identifier for this filing |
| `licensee` | DISCOM submitting the filing |
| `regulatoryCommission` | Target SERC |
| `fiscalYears[]` | One entry per fiscal year covered |
| `lineItems[]` | Cost breakdown — each item is a standard ARR cost category |
| `amountCrINR` | Amount in INR Crores |

The schema maps directly to the standard ARR format prescribed by most SERCs, making it straightforward for DISCOMs to generate from existing financial systems.

---

## Proposal: OpenADR 3 Standardized Format

To align with global grid standards and enable automated processing by generic regulatory tools, the ARR filing can be represented using the **OpenADR 3.0 REPORT** format.

### Mapping Strategy
| Custom Schema Concept | OpenADR 3 Mapping | Rationale |
|---|---|---|
| **Fiscal Year** | `intervalPeriod` | A 1-year duration (`P1Y`) starting from April 1st. |
| **ARR Categories** | `resourceName` | Each cost or energy heading is treated as a logical resource. |
| **Financial Values** | `payloadType: PRICE` | Standard type for financial/cost data (Units: `INR_CRORES`). |
| **Energy Quantities** | `payloadType: USAGE` | Standard type for energy volumes (Units: `MU` for Million Units). |
| **Projections** | `readingType: FORECAST` | Used for the coming year's estimated Aggregate Revenue Requirement. |
| **Historical Actuals** | `readingType: SUMMED` | Used for "True-up" sections showing actual historical costs. |

### OpenADR 3 JSON Example
This example shows how the "Power Purchase Cost" and "Total Energy" for a fiscal year are represented as resources within a single Report.

```json
{
  "objectType": "REPORT",
  "reportID": "BESCOM-ARR-2026-27",
  "programID": "regulatory-arr-filing",
  "reportPayloadDescriptors": [
    {
      "payloadType": "PRICE",
      "readingType": "FORECAST",
      "units": "INR_CRORES"
    },
    {
      "payloadType": "USAGE",
      "readingType": "FORECAST",
      "units": "MU"
    }
  ],
  "resources": [
    {
      "resourceName": "Power Purchase Cost",
      "intervalPeriod": {
        "start": "2026-04-01T00:00:00Z",
        "duration": "P1Y"
      },
      "intervals": [
        {
          "id": 0,
          "payloads": [{"type": "PRICE", "values": [12450.5]}]
        }
      ]
    },
    {
      "resourceName": "Total Energy Requirement",
      "intervalPeriod": {
        "start": "2026-04-01T00:00:00Z",
        "duration": "P1Y"
      },
      "intervals": [
        {
          "id": 0,
          "payloads": [{"type": "USAGE", "values": [15200.0]}]
        }
      ]
    }
  ]
}
```

##### Historical Actuals (True-up for 2024-25)
This example uses `readingType: SUMMED` to indicate actual historical values rather than projections.

```json
{
  "objectType": "REPORT",
  "reportID": "BESCOM-TRUE-UP-2024-25",
  "programID": "regulatory-arr-filing",
  "reportPayloadDescriptors": [
    {
      "payloadType": "PRICE",
      "readingType": "SUMMED",
      "units": "INR_CRORES"
    }
  ],
  "resources": [
    {
      "resourceName": "Power Purchase Cost",
      "intervalPeriod": {
        "start": "2024-04-01T00:00:00Z",
        "duration": "P1Y"
      },
      "intervals": [
        {
          "id": 0,
          "payloads": [{"type": "PRICE", "values": [11820.3]}]
        }
      ]
    }
  ]
}
```

---

## Transaction Flow

UC2 exercises **`confirm` → `on_confirm` → `status` → `on_status`** — the contract is acknowledged in `on_confirm` and the filing arrives asynchronously in `on_status`. Discovery and negotiation actions are available but optional for the regulator/DISCOM bilateral scenario.

The filing is carried inside `message.contract.commitments[].resources[].resourceAttributes`:

```json
"resources": [{
  "id": "ds-bescom-arr-filing-2026-27",
  "descriptor": { "name": "BESCOM ARR Filing 2026-27" },
  "resourceAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1.1/context.jsonld",
    "@type": "DatasetItem",
    "accessMethod": "INLINE",
    "dataPayload": { /* IES_ARR_Filing — see snippet above */ }
  }
}]
```

Full request/response examples live in [uc2-regulatory-data/examples/](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc2-regulatory-data/examples).

---

## Why This Matters

| Current State | With IES Data Exchange |
|---|---|
| Filing arrives as PDF / Excel | Filing arrives as structured JSON — machine-parseable |
| Regulator manually re-keys data into their system | Regulator's system ingests directly |
| No standard schema — different DISCOMs format differently | Uniform `IES_ARR_Filing` schema across all DISCOMs |
| No audit trail on submission | Every exchange is signed, timestamped, and logged in Beckn |
| Filing disputes require going back to paper trail | Cryptographically signed payload is non-repudiable |
| Proprietary schemas limit interoperability | OpenADR 3 alignment allows use of standard grid management tools |

---

## Running This Use Case

```bash
cd DEG/devkits/data-exchange/install
docker compose up -d
```

Then import the BAP collection at `uc2-regulatory-data/postman/data-exchange-uc2-regulatory-data.BAP-DEG.postman_collection.json` into Postman, set `bap_host_root` and `bpp_host_root` to `http://beckn-router:9000`, and fire `confirm`. Inspect callbacks:

```bash
docker logs sandbox-bap 2>&1 | grep -E 'on_(confirm|status)' | tail -10
```

See the [Quick Start](../quick-start.md) for the full step-by-step.

---

## Reference

- [IES_ARR_Filing Schema definitions](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/arr) *(currently on the `ies-specs` branch; will move to India-Energy-Stack — see [Concepts § IES Data Schemas](../concepts.md#ies-data-schemas))*
- [Example payloads](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc2-regulatory-data/examples)
