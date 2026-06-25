# Customer Credential

> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.0/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.0/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.0/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.0/vocab.jsonld) · [examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.0/examples)

> **Mirror.** Files in this directory are mirrored verbatim from [`beckn/DEG/specification/schema/ElectricityCredential/v1.0/`](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential/v1.0). Upstream is canonical.

## Overview

The **Customer Credential** is a unified W3C Verifiable Credential (VC Data Model 2.0) that combines five equal-level profile sections into a single `credentialSubject` object. The customer's DID (`id`) is optional per the W3C VC Data Model, and the five profiles sit as equal-level sibling properties.

This credential is issued per meter — each meter will have its own credential.

## Credential Structure

```
credentialSubject
├── id                    (optional customer DID)
├── customerProfile       (required — identity: meter, customer number, idRef)
├── customerDetails       (required — name, address, connection date)
├── consumptionProfile    (optional — premises, connection type, load, tariff)
├── generationProfile     (optional — DER type, capacity, commissioning)
└── storageProfile        (optional — battery capacity, power rating, type)
```

## Issuer

The credential is issued by energy providers. The issuer object contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | URI | Yes | DID or URL of the issuing provider |
| `name` | string | Yes | Name of the provider |
| `idRef` | object | No | (Any) Identity reference — see [idRef](#idref) |

Example:
```json
"issuer": {
  "id": "did:web:bescom.karnataka.gov.in",
  "name": "BESCOM - Bangalore Electricity Supply Company",
  "idRef": {
    "issuedBy": "did:web:kerc.karnataka.gov.in",
    "subjectId": "kerc.karnataka.gov.in:AABPC12345"
  }
}
```

## Validity Period

Per the [W3C VC Data Model 2.0 validity period](https://www.w3.org/TR/2025/REC-vc-data-model-2.0-20250515/#validity-period), this credential uses:

- **`validFrom`** (required) — date-time from which the credential is valid
- **`validUntil`** (optional) — date-time until which the credential is valid

All date-time values include an explicit timezone offset (e.g., `2025-01-13T10:30:00-05:00`).

## Revocation

Credential revocation is managed via DeDi. See [Energy Credentials — Revoke](../../../energy-credentials/README.md#id-4.-revoke) for the publication flow.

## Profile Sections

### customerProfile

Core customer identity fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customerNumber` | string | Yes | Full customer account number assigned by the utility |
| `meterNumber` | string | Yes | Unique meter serial number |
| `meterType` | enum | Yes | Type of meter — see [meterType enum](#metertype-enum) |
| `idRef` | object | No | External identity reference (e.g., government ID) — see [idRef](#idref) |

#### meterType enum

Values derived from Green Button / ESPI meter kind classifications:

| Value | Description |
|-------|-------------|
| `AMR` | Automated Meter Reading |
| `AMI` | Advanced Metering Infrastructure (smart meter) |
| `Electromechanical` | Traditional electromechanical meter |
| `Forward` | Forward-only (import) meter |
| `Reverse` | Reverse-only (export) meter |
| `Bidirectional` | Bidirectional meter (import + export) |
| `Prepaid` | Prepaid/token-based meter |
| `NetMeter` | Net metering meter |
| `Other` | Other meter type |

### customerDetails

Personal and address information:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fullName` | string | Yes | Full name of the customer as per ID proof |
| `installationAddress` | object | Yes | Address of the installation (see below) |
| `serviceConnectionDate` | date-time | Yes | Date and time when the electricity connection was activated |

#### installationAddress

Follows the [beckn Location schema](https://github.com/beckn/protocol-specifications/blob/master/schema/Location.yaml) with an additional `openLocationCode` field.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | No | Unique identifier for the location |
| `descriptor` | object | No | Physical description of the location (`name`, `code`, `short_desc`, `long_desc`) |
| `map_url` | string (uri) | No | URL to the map of the location |
| `gps` | string | No | GPS coordinates as `"lat,lng"` string (e.g., `"12.9716,77.5946"`) |
| `address` | string | Yes | Complete postal address of the installation |
| `city` | object | No | City — `{ name: string, code: string }` |
| `district` | string | No | District or county name |
| `state` | object | No | State — `{ name: string, code: string }` |
| `country` | object | Yes | Country — `{ name: string, code: string }` (ISO 3166-1 alpha-2 code required) |
| `area_code` | string | Yes | Area code or postal/ZIP code |
| `circle` | object | No | Circular geo-fence — `{ gps: string, radius: Scalar }` |
| `polygon` | string | No | Boundary polygon of the location |
| `3dspace` | string | No | Three dimensional region describing the location |
| `rating` | string | No | Rating of the location |
| `openLocationCode` | string | No | Open Location Code (OLC) for the installation location |

The address object aligns with the [beckn protocol Location schema](https://github.com/beckn/protocol-specifications/blob/master/schema/Location.yaml) and reuses [schema.org](https://schema.org/) vocabulary where applicable.

### consumptionProfile

Connection and consumption characteristics:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `premisesType` | enum | Yes | `Residential`, `Commercial`, `Industrial`, or `Agricultural` |
| `connectionType` | enum | Yes | `Single-phase` or `Three-phase` |
| `sanctionedLoadKW` | number | Yes | Sanctioned electrical load in kW |
| `tariffCategoryCode` | string | Yes | Billing/tariff category code |

### generationProfile

DER generation capability:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assetId` | string | No | Unique identifier for the generation asset |
| `generationType` | enum | Yes | `Solar`, `Wind`, `MicroHydro`, or `Other` |
| `capacityKW` | number | Yes | Installed generation capacity in kW |
| `commissioningDate` | date-time | Yes | Date and time when the system was activated |
| `manufacturer` | string | No | Equipment manufacturer |
| `modelNumber` | string | No | Equipment model number |

### storageProfile

Battery/energy storage capability:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assetId` | string | No | Unique identifier for the storage asset |
| `storageCapacityKWh` | number | Yes | Storage capacity in kWh |
| `powerRatingKW` | number | Yes | Charge/discharge power rating in kW |
| `commissioningDate` | date-time | Yes | Date and time when the system was activated |
| `storageType` | enum | No | `LithiumIon`, `LeadAcid`, `FlowBattery`, or `Other` |

## idRef

A reusable identity reference pattern. In this credential it appears in:

- **`issuer.idRef`** — the utility's regulatory registration
- **`customerProfile.idRef`** — the customer's external identity

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `issuedBy` | URI (DID) | Yes | DID of the authority that issued the identity |
| `subjectId` | string | Yes | Identifier in the format `authority-domain:id-value` |

Example (customer's government ID):
```json
"idRef": {
  "issuedBy": "did:web:ssa.gov",
  "subjectId": "ssa.gov:XXX-XX-1234"
}
```

## Files

| File | Description |
|------|-------------|
| `context.jsonld` | JSON-LD context defining semantic mappings for all five profile sections |
| `schema.json` | JSON Schema (draft 2020-12) for credential validation |
| `example.json` | Sample credential with all five profiles populated |


---

<!-- FIELD-TABLE:START — auto-generated by scripts/generate_field_tables.py from schema.json; do not edit by hand -->
## Field reference

_Auto-generated from `schema.json`. **Field**, **Type**, and **Status** are derived from the schema; **Standard** comes from each field's `x-standard` annotation (`—` when unset). One table per object._

### ElectricityCredential Schema

| Field | Type | Standard | Status |
|---|---|---|---|
| `id` | uri | — | Mandatory |
| `type` | list of text | — | Mandatory |
| `issuer` | object | — | Mandatory |
| `validFrom` | date-time | — | Mandatory |
| `validUntil` | date-time | — | Optional |
| `credentialStatus` | object | — | Optional |
| `credentialSubject` | object | — | Mandatory |
| `proof` | object | — | Optional |

### CustomerProfile

| Field | Type | Standard | Status |
|---|---|---|---|
| `customerNumber` | text | — | Mandatory |
| `meterNumber` | text | — | Mandatory |
| `meterType` | AMR / AMI / Electromechanical / Forward / Reverse / Bidirectional / Prepaid / NetMeter / Other | — | Mandatory |
| `idRef` | object | — | Optional |

### CustomerDetails

| Field | Type | Standard | Status |
|---|---|---|---|
| `fullName` | text | — | Mandatory |
| `installationAddress` | object | — | Mandatory |
| `serviceConnectionDate` | date-time | — | Mandatory |

### ConsumptionProfile

| Field | Type | Standard | Status |
|---|---|---|---|
| `id` | uri | — | Mandatory |
| `consumerNumber` | text | — | Mandatory |
| `fullName` | text | — | Mandatory |
| `premisesType` | Residential / Commercial / Industrial / Agricultural | — | Mandatory |
| `connectionType` | Single-phase / Three-phase | — | Mandatory |
| `sanctionedLoadKW` | number | — | Mandatory |
| `tariffCategoryCode` | text | — | Mandatory |
| `meterNumber` | text | — | Optional |

### GenerationProfile

| Field | Type | Standard | Status |
|---|---|---|---|
| `id` | uri | — | Mandatory |
| `consumerNumber` | text | — | Mandatory |
| `fullName` | text | — | Optional |
| `meterNumber` | text | — | Optional |
| `assetId` | text | — | Optional |
| `generationType` | Solar / Wind / MicroHydro / Other | — | Mandatory |
| `capacityKW` | number | — | Mandatory |
| `commissioningDate` | date | — | Mandatory |
| `manufacturer` | text | — | Optional |
| `modelNumber` | text | — | Optional |

### StorageProfile

| Field | Type | Standard | Status |
|---|---|---|---|
| `id` | uri | — | Mandatory |
| `consumerNumber` | text | — | Mandatory |
| `fullName` | text | — | Optional |
| `meterNumber` | text | — | Optional |
| `assetId` | text | — | Optional |
| `storageCapacityKWh` | number | — | Mandatory |
| `powerRatingKW` | number | — | Mandatory |
| `commissioningDate` | date | — | Mandatory |
| `storageType` | LithiumIon / LeadAcid / FlowBattery / Other | — | Optional |

<!-- FIELD-TABLE:END -->
