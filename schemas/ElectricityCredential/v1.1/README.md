> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.1/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.1/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.1/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.1/vocab.jsonld) · [examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.1/examples)

> **Mirror.** Files in this directory are mirrored verbatim from [`beckn/DEG/specification/schema/ElectricityCredential/v1.1/`](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential/v1.1). Upstream is canonical.

# ElectricityCredential v1.1

W3C Verifiable Credential (VC Data Model 2.0) issued per meter by electricity distribution utilities.

## Structure

```
credentialSubject
├── id                         (optional — customer DID)
├── customerProfile            (required — non-PII)
│   ├── customerNumber         (required — CA number)
│   ├── idRef                  (optional — external identity reference)
│   ├── energyResources[]      (required — all physical assets, min 1)
│   │   ├── id                 (meter serial number for METER; any stable id for DERs)
│   │   ├── type               (enum: METER, DT, BUS, FEEDER, SOLAR, WIND, BATTERY, BESS, EV_CHARGER, …)
│   │   ├── attributes         (open bag — all non-topological properties)
│   │   │   ├── CommonResourceAttributes: make, model, ratedPowerKw, energyCapacityKwh, telemetryProvider
│   │   │   └── type-specific: meterType, gps, location / commissioningDate / storageType / …
│   │   ├── subResources[]     (child resource ids or inline objects)
│   │   └── parentResources[]  (parent resource ids — e.g., the meter a DER sits behind)
│   └── consumptionProfiles[]  (optional — tariff/load per meter, linked via meterId)
└── customerDetails            (optional — PII)
    ├── fullName               (PII — only here)
    ├── installationAddress
    └── serviceConnectionDate
```

## Multiple topologies

A single `customerNumber` can span arbitrary asset topologies.

**Submetering** — building main meter + tenant sub-meters:
```json
"energyResources": [
  {"id": "MET-BLDG-001", "type": "METER", "attributes": {"meterType": "AMI"}, "parentResources": ["BAN-NR-F22"]},
  {"id": "MET-UNIT-101", "type": "METER", "attributes": {"meterType": "AMR"}, "parentResources": ["MET-BLDG-001"]},
  {"id": "MET-UNIT-102", "type": "METER", "attributes": {"meterType": "AMR"}, "parentResources": ["MET-BLDG-001"]},
  {"id": "ROOFTOP-101",  "type": "SOLAR", "attributes": {"ratedPowerKw": 2},   "parentResources": ["MET-UNIT-101"]}
]
```

**Parallel metering** — import meter + export meter for solar FIT:
```json
"energyResources": [
  {"id": "MET-IMPORT", "type": "METER", "attributes": {"meterType": "AMI"}, "parentResources": ["DEL-F08"]},
  {"id": "MET-EXPORT", "type": "METER", "attributes": {"meterType": "Reverse"}},
  {"id": "SOLAR-001",  "type": "SOLAR", "attributes": {"ratedPowerKw": 5}, "parentResources": ["MET-EXPORT"]}
],
"consumptionProfiles": [
  {"meterId": "MET-IMPORT", "sanctionedLoadKW": 10, "tariffCategoryCode": "DS-I"},
  {"meterId": "MET-EXPORT", "sanctionedLoadKW": 5,  "tariffCategoryCode": "FIT-SOLAR-01"}
]
```

## customerProfile

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customerNumber` | string | Yes | Utility CA number |
| `idRef` | object | No | External identity linkage (`issuedBy` DID + `subjectId`) |
| `energyResources` | array | Yes | EnergyResource/v2.0 entries (min 1) |
| `consumptionProfiles` | array | No | Tariff/load profiles, one per meter |

## EnergyResource — top-level fields

| Field | Description |
|-------|-------------|
| `id` | Stable identifier. For METER: meter serial number. For DERs: any stable scheme. |
| `type` | Enum asset class. Grid: `METER`, `DT`, `BUS`, `FEEDER`. Generation: `SOLAR`, `SOLAR_PV`, `WIND`, `HYDRO`, `BIOGAS`, `CHP`, `FUEL_CELL`. Storage: `BATTERY`, `BESS`. Loads: `EV_CHARGER`, `EV_V2G`, `SMART_HVAC`, `SMART_WATER_HEATER`, `CONTROLLABLE_LOAD`. System: `MICROGRID`. |
| `attributes` | Open bag — all non-topological properties (see below) |
| `subResources` | Child resource ids or inline EnergyResource objects |
| `parentResources` | Parent resource ids — e.g., the meter a DER sits behind |

## EnergyResource.attributes

All non-topological fields go here.

**CommonResourceAttributes** (all resource types):

| Field | Type | Description |
|-------|------|-------------|
| `make` | string | Manufacturer |
| `model` | string | Model |
| `ratedPowerKw` | number | Rated peak power, kW |
| `energyCapacityKwh` | number | Stored-energy capacity, kWh (storage-class only) |
| `telemetryProvider` | string | Vendor API / data source for telemetry |

**METER-specific** (`type: METER`):

| Field | Type | Description |
|-------|------|-------------|
| `meterType` | enum | AMR, AMI, Electromechanical, Forward, Reverse, Bidirectional, Prepaid, NetMeter, Other |
| `gps` | string | `"lat,lng"` coordinates of the meter |
| `location` | object | Postal location (beckn Location shape) |

Grid topology (feeder, bus, DT) is expressed via `parentResources[]` — reference the id of a `FEEDER`, `BUS`, or `DT` resource.

**DER-specific examples** (open — any field can be added):

| Field | Applies to | Description |
|-------|-----------|-------------|
| `commissioningDate` | SOLAR, WIND, BATTERY | Date the asset was commissioned |
| `storageType` | BATTERY, BESS | LithiumIon, LeadAcid, FlowBattery, … |
| `vin` | EV_CHARGER, EV_V2G | Vehicle identification number |

## ConsumptionProfile

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `meterId` | string | Yes | Matches `id` of a METER entry in `energyResources[]` |
| `sanctionedLoadKW` | number | Yes | Utility-approved load in kW |
| `contractMaxDemandKw` | number | No | Maximum demand contracted with the utility, kW |
| `tariffCategoryCode` | string | Yes | Billing/tariff category code |
| `premisesType` | enum | No | Residential, Commercial, Industrial, Agricultural |
| `connectionType` | enum | No | Single-phase, Three-phase |

## customerDetails (PII)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fullName` | string | Yes | Full name — **only here** |
| `installationAddress` | object | Yes | Beckn Location shape |
| `serviceConnectionDate` | date-time | Yes | Connection activation date (with timezone) |

## Minimal valid credential

```json
{
  "@context": ["https://www.w3.org/ns/credentials/v2", "https://schema.beckn.io/ElectricityCredential/v1.1/context.jsonld"],
  "id": "urn:uuid:…",
  "type": ["VerifiableCredential", "ElectricityCredential"],
  "issuer": {"id": "did:web:ies.discom.example", "name": "Example Distribution Company"},
  "validFrom": "2025-01-13T10:30:00+05:30",
  "credentialSubject": {
    "customerProfile": {
      "customerNumber": "UTIL-2025-001234567",
      "energyResources": [
        {"id": "MET2025789456123", "type": "METER", "attributes": {"meterType": "AMI"}}
      ]
    }
  }
}
```

## v1.0 → v1.1 migration

| v1.0 field | v1.1 location |
|------------|---------------|
| `customerProfile.meterNumber` | `energyResources[METER].id` |
| `customerProfile.meterType` | `energyResources[METER].attributes.meterType` |
| `consumptionProfiles[].sanctionedLoadKW` | `consumptionProfiles[].sanctionedLoadKW` |
| `consumptionProfiles[].tariffCategoryCode` | `consumptionProfiles[].tariffCategoryCode` |
| `generationProfiles[].assetId` | `energyResources[DER].id` |
| `generationProfiles[].capacityKW` | `energyResources[DER].attributes.ratedPowerKw` |
| `generationProfiles[].manufacturer` | `energyResources[DER].attributes.make` |
| `generationProfiles[].commissioningDate` | `energyResources[DER].attributes.commissioningDate` |
| `storageProfiles[].storageCapacityKWh` | `energyResources[DER].attributes.energyCapacityKwh` |
| `storageProfiles[].storageType` | `energyResources[DER].attributes.storageType` |
| `fullName` (duplicated per entry) | `customerDetails.fullName` (once) |

## Files

| File | Description |
|------|-------------|
| `attributes.yaml` | OpenAPI 3.1.1 schema |
| `schema.json` | Bundled JSON Schema (draft 2020-12) — self-contained |
| `context.jsonld` | JSON-LD context |
| `vocab.jsonld` | RDF vocabulary |
| `examples/example.json` | Single meter + 2 generation + 2 storage DERs |
| `examples/example-submetering.json` | Building main meter + 2 tenant sub-meters |
| `examples/example-parallel-metering.json` | Import meter + export meter (solar FIT) |


---

<!-- FIELD-TABLE:START — auto-generated by scripts/generate_field_tables.py from schema.json; do not edit by hand -->
## Field reference

_Auto-generated from `schema.json`. A field name in **bold** with a trailing **\*** is required; all others are optional. **Type** shows units for QuantitativeValue models. Where a field is derived from a standard, its description begins with **Based on** and the standard reference (from the field's `x-standard` annotation). One table per object._

### ElectricityCredential v1.1

| Field | Type | Description |
|----|-------|-----------------|
| **`id`** \* | uri | — |
| **`type`** \* | list of text | — |
| **`issuer`** \* | object | — |
| **`validFrom`** \* | date-time | — |
| `validUntil` | date-time | — |
| `credentialStatus` | object | — |
| **`credentialSubject`** \* | object | — |
| `proof` | object | — |

### IdRef

| Field | Type | Description |
|----|-------|-----------------|
| **`issuedBy`** \* | uri | — |
| **`subjectId`** \* | text | — |

### CustomerProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`customerNumber`** \* | text | — |
| `idRef` | IdRef | — |
| **`energyResources`** \* | list of EnergyResource | — |
| `consumptionProfiles` | list of ConsumptionProfile | — |

### ConsumptionProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`meterId`** \* | text | — |
| **`sanctionedLoadKw`** \* | number | — |
| `contractMaxDemandKw` | number | — |
| `sanctionedExportLoadKw` | number | Sanctioned/approved grid export limit in kW. |
| **`tariffCategoryCode`** \* | text | — |
| `premisesType` | `Residential` / `Commercial` / `Industrial` / `Agricultural` | — |
| `connectionType` | `Single-phase` / `Three-phase` | — |
| `paymentMode` | `PREPAID` / `POSTPAID` | Indicates if the connection is prepaid or postpaid. |
| `billingCycleDay` | integer | Day of month on which the billing cycle resets. |

### CustomerDetails

| Field | Type | Description |
|----|-------|-----------------|
| **`fullName`** \* | text | — |
| **`installationAddress`** \* | Location | — |
| **`serviceConnectionDate`** \* | date-time | — |

### EnergyResource

| Field | Type | Description |
|----|-------|-----------------|
| `id` | text | — |
| `type` | `METER` / `DT` / `BUS` / `FEEDER` / `SOLAR` / `SOLAR_PV` / `WIND` / `HYDRO` / `BIOGAS` / `CHP` / `FUEL_CELL` / `BATTERY` / `BESS` / `EV_CHARGER` / `EV_V2G` / `SMART_HVAC` / `SMART_WATER_HEATER` / `CONTROLLABLE_LOAD` / `MICROGRID` | — |
| `attributes` | object | All non-topological attributes. CommonResourceAttributes (make, model, ratedPowerKw, energyCapacityKwh, telemetryProvider) plus type-specific fields (meterType, gps, location, feeder, bus, commissioningDate, storageType, …). |
| `subResources` | list of text or EnergyResource | — |
| `parentResources` | list of text | — |

### Location

| Field | Type | Description |
|----|-------|-----------------|
| **`geo`** \* | GeoJSONGeometry | — |
| `address` | Address | — |

### Address

| Field | Type | Description |
|----|-------|-----------------|
| `streetAddress` | text | Building name/number and street. |
| `extendedAddress` | text | Apt, suite, floor, or C/O. |
| `addressLocality` | text | City or locality. |
| `addressRegion` | text | State, region or province. |
| `addressCountry` | text | ISO 3166-1 alpha-2 country code. |
| `postalCode` | text | Postal or ZIP code. |

### GeoJSONGeometry

| Field | Type | Description |
|----|-------|-----------------|
| **`type`** \* | `Point` / `LineString` / `Polygon` / `MultiPoint` / `MultiLineString` / `MultiPolygon` / `GeometryCollection` | — |
| `coordinates` | list of — | Coordinates per RFC 7946. For a Point: [longitude, latitude]. |
| `geometries` | list of GeoJSONGeometry | Member geometries when type is GeometryCollection. |
| `bbox` | list of number | Bounding box [west, south, east, north] in degrees. |

<!-- FIELD-TABLE:END -->
