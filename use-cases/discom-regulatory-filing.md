# DISCOM Regulatory Filing

**A DISCOM submits its Aggregate Revenue Requirement (ARR), tariff petition, true-up, or other compliance filing to a State Electricity Regulatory Commission (SERC) as a structured, signed, machine-verifiable object.**

---

## Scenario

Every year, every DISCOM in India submits an ARR filing to its state regulator — a detailed projection of power-purchase, transmission, O&M, depreciation, and return-on-equity costs that justifies the tariff it wants the SERC to approve. The same DISCOMs file true-up petitions, FPPCA reconciliations, multi-year tariff petitions, and various compliance returns through the year.

Today these arrive as **PDFs and Excel sheets**. SERC staff manually re-key the numbers into their analysis spreadsheets. Stakeholders and consumer-rep parties can only object on the same PDFs. There is no canonical machine-readable form, so no cross-DISCOM comparison, no automated trend analysis, no straight-through validation.

This use case replaces the PDF round-trip with a structured `IES_ARR_Filing` payload delivered over the IES Data Exchange protocol — signed by the DISCOM, ingested directly by the SERC, archived with a non-repudiable audit trail.

---

## Actors and Roles

| Role | Organisation (example) | What they do |
|---|---|---|
| **BPP** — data provider | DISCOM (e.g. BESCOM) | Generates and submits the filing |
| **BAP** — data consumer | SERC (e.g. KERC, APERC) | Receives, validates, and archives the filing |
| **Optional secondary consumers** | Consumer-rep parties, research orgs, Forum of Regulators | Receive the published filing via the same protocol, gated by public-disclosure norms |

Note: unlike Smart Meter Data Exchange, here the **DISCOM is the BPP** (data provider) and the **regulator is the BAP**. The Beckn protocol is symmetric — the same Docker stack and adapter run both directions.

---

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../identifiers/README.md) | The DISCOM and SERC each have a `did:web` identity registered in the IES registries; the filing object carries identifiers for the filing, the fiscal year, the regulatory order it responds to, and the cost line items. |
| [Registries](../registries/README.md) | DISCOM looked up in [IES DISCOMs Reference Registry](../registries/required-registries.md#discoms-registry); SERC in [IES Regulators Reference Registry](../registries/required-registries.md#regulators-registry). |
| [Data Exchange](../data-exchange/README.md) | The Beckn-based protocol carries the `IES_ARR_Filing` payload from BPP (DISCOM) to BAP (SERC), with the same `confirm` / `on_confirm` / `status` / `on_status` lifecycle as the meter-data flow. |
| [Energy Credentials](../energy-credentials/README.md) | *Not used for the filing itself* — the filing is signed by the Beckn message envelope. Credentials enter the picture only if a consumer-rep needs an attested DISCOM identity letter, which is the [Consumer Energy Passport / DISCOM-side analogue](../energy-credentials/README.md), not part of the filing flow. |

---

## The Dataset — `IES_ARR_Filing`

The `IES_ARR_Filing` schema carries structured cost data for one or more fiscal years. Two equivalent representations are supported:

### A. Native IES shape

The shape most DISCOMs will generate directly from their financial systems:

```json
{
  "filingId": "BESCOM-ARR-2026-27",
  "licensee": "BESCOM",
  "state": "Karnataka",
  "regulatoryCommission": "KERC",
  "submissionDate": "2026-01-15",
  "fiscalYears": [{
    "year": "2026-27",
    "totalRevenueRequirementCrINR": 18432.5,
    "lineItems": [
      { "category": "Power Purchase Cost",  "subcategory": "Long-term PPAs", "amountCrINR": 12450.5, "notes": "1200 MW coal + 800 MW solar" },
      { "category": "Transmission Charges", "subcategory": "PGCIL",          "amountCrINR":  1823.2 },
      { "category": "O&M Expenses",         "subcategory": "Employee costs", "amountCrINR":   892.7 },
      { "category": "Depreciation",                                           "amountCrINR":   634.1 },
      { "category": "Return on Equity",                                       "amountCrINR":   632.0 }
    ]
  }]
}
```

The `category` values follow the standard ARR cost categories prescribed by most SERCs, which keeps the schema natural for DISCOM finance teams.

### B. OpenADR 3 REPORT representation

For alignment with global grid-data tooling and the same OpenADR 3 envelope used by meter telemetry:

| Custom concept | OpenADR 3 mapping | Why |
|---|---|---|
| Fiscal year | `intervalPeriod` (`P1Y` starting 1 Apr) | Standard interval semantics |
| ARR cost categories | `resourceName` | Each cost heading is a logical resource |
| Financial values | `payloadType: PRICE` (units `INR_CRORES`) | Standard type for cost data |
| Energy quantities | `payloadType: USAGE` (units `MU`) | Standard type for energy volumes |
| Projections | `readingType: FORECAST` | Next-year ARR |
| Historical actuals | `readingType: SUMMED` | True-up sections |

```json
{
  "objectType": "REPORT",
  "reportID": "BESCOM-ARR-2026-27",
  "programID": "regulatory-arr-filing",
  "reportPayloadDescriptors": [
    { "payloadType": "PRICE", "readingType": "FORECAST", "units": "INR_CRORES" },
    { "payloadType": "USAGE", "readingType": "FORECAST", "units": "MU" }
  ],
  "resources": [
    {
      "resourceName": "Power Purchase Cost",
      "intervalPeriod": { "start": "2026-04-01T00:00:00+05:30", "duration": "P1Y" },
      "intervals": [{ "id": 0, "payloads": [{ "type": "PRICE", "values": [12450.5] }] }]
    },
    {
      "resourceName": "Total Energy Requirement",
      "intervalPeriod": { "start": "2026-04-01T00:00:00+05:30", "duration": "P1Y" },
      "intervals": [{ "id": 0, "payloads": [{ "type": "USAGE", "values": [15200.0] }] }]
    }
  ]
}
```

Either shape can be exchanged; the BAP declares which it expects in the catalogue entry, and the BPP serialises accordingly. Both share the same `filingId` so downstream archives can cross-reference.

> **Status — `IES_ARR_Filing` schema is being finalised.** The category enumeration is the open item: SERCs use slightly different cost taxonomies and the IES schema is converging on a superset with mapping notes. Integrate against the devkit examples; expect small enum additions, not breaking renames.

---

## Setup Steps

### 1. Register the DISCOM and the SERC

Both parties need DeDi entries:

- DISCOM in [`ies-discoms-reference-registry`](../registries/required-registries.md#discoms-registry) under `india-energy-stack:<discom-short-code>`.
- SERC in [`ies-regulators-reference-registry`](../registries/required-registries.md#regulators-registry) under `india-energy-stack:<serc-short-code>`.

Each registration pins a `did:web` and the public key for Beckn message signing. See [Registry Creation](../registries/registry-creation.md).

### 2. Identifier hygiene

Mint a single canonical `filingId` per submission (typical pattern: `<DISCOM>-ARR-<FY>` or `<DISCOM>-TRUEUP-<FY>`). The same `filingId` should appear on any subsequent re-submissions or revisions — versioning lives on the data-exchange envelope (`updatedAt`), not on the ID.

If the filing responds to a specific tariff order, include the `policyID` of that order (see [Tariff Intelligence](tariff-intelligence.md)) so the SERC's archive can stitch order ↔ petition ↔ true-up automatically.

### 3. Stand up the data-exchange adapters

The DISCOM runs a BPP adapter; the SERC runs a BAP adapter. The local devkit gives both:

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

For production, follow [Registry Setup](../data-exchange/registry-setup.md) and point the adapter at the IES registry endpoint and your `did:web` keys.

### 4. Catalogue the filing as a published dataset

The DISCOM publishes the filing through its BPP catalogue with:

- `descriptor.name` — human-readable filing title (e.g. *"BESCOM ARR Filing 2026-27"*)
- `category` — `ARR`, `TRUE_UP`, `FPPCA`, `COMPLIANCE` (one of the agreed regulatory categories)
- `accessMethod` — typically `INLINE` (filings are small) or `SIGNED_URL` if supporting workbooks accompany it
- `policyContext` — references to the SERC orders the filing responds to

### 5. Exercise the flow

The flow is `confirm` → `on_confirm` → `status` → `on_status`, with the regulator (BAP) initiating `confirm` against the catalogue entry:

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

Both messages are signed; the SERC's archive stores the original signed envelope as the non-repudiable record of submission.

### 6. (Optional) Open the filing for public consumption

If the SERC mandates public disclosure of filings, the same dataset is republished from the SERC's BPP under the public-disclosure catalogue. Consumer-rep parties and researchers become BAPs against that catalogue, with settlement value `0` per public-disclosure norms.

---

## Operate

```bash
# Import the regulatory-filing BAP collection
#   DEG/devkits/data-exchange/uc2-regulatory-data/postman/
# Set bap_host_root + bpp_host_root to http://beckn-router:9000
# Fire `confirm`.

docker logs sandbox-bap 2>&1 | grep -E 'on_(confirm|status)' | tail -10
```

The signed envelope received by the SERC is what should be persisted — re-validating the signature against the DISCOM's registry-published key is the audit-trail check.

---

## Why This Matters

ARR filings arrive today as PDFs/Excel sheets that regulators manually re-key. Delivering them as structured `IES_ARR_Filing` JSON — signed, timestamped, schema-validated — replaces re-keying with direct ingest, gives a non-repudiable audit trail, and lets every DISCOM submit in the same canonical shape. The OpenADR 3 representation additionally makes the same data legible to grid-management tooling.

---

## Open Items

- **`IES_ARR_Filing` schema canonicalisation.** The schema currently lives on `beckn/DEG:ies-specs`; it will move to `India-Energy-Stack`. The cost-category enumeration is the active conversation — expect additions, not breaking renames.
- **Workbook attachments.** Many filings ship with supporting Excel models; the convention for attaching them (separate `DatasetItem` per workbook vs. embedded base64) is being agreed.
- **Cross-filing references.** A standard reference shape for *"this filing responds to SERC Order X"* is being aligned with the [Tariff Intelligence](tariff-intelligence.md) `policyID` pattern.

---

## References

- [Basic Checklist](./discom-regulatory-filing-basic-checklist.md) — plain-English rollout checklist
- [`IES_ARR_Filing` schema (upstream)](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/arr)
- [Example payloads (devkit)](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc2-regulatory-data/examples)
- [ies-docs ARR examples](https://github.com/India-Energy-Stack/ies-docs/tree/main/implementation-guides/data_exchange/examples)
- [Data Exchange — Architecture](../data-exchange/architecture.md)
- [Data Exchange — Quick Start](../data-exchange/quick-start.md)
