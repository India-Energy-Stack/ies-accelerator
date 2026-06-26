> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/vocab.jsonld) · [examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.2/examples)

> **Mirror.** Files in this directory are mirrored verbatim from [`beckn/DEG/specification/schema/ElectricityCredential/v1.2/`](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential/v1.2). Upstream is canonical.

# ElectricityCredential v1.2

W3C Verifiable Credential (VC Data Model 2.0) issued per meter by electricity distribution utilities.

v1.2 introduces a **composable EnergyResource hierarchy**: each entry in `energyResources[]` is discriminated by `type` into one of seven typed kinds, each with a typed `attributes` bag. All power and capacity fields use **QuantitativeValue `{value, unit}`** with short unit aliases (`kW`, `kWh`, `kVA`, `kVAR`, `kV`, `MW`, `MWh`, `MVA`, `MVAR`, `V`, `W`) mapped to QUDT IRIs via JSON-LD context.

## Structure

```
credentialSubject
├── id                         (optional — customer DID)
├── customerProfile            (required — non-PII)
│   ├── customerNumber         (required — CA number)
│   ├── idRef                  (optional — external identity reference)
│   ├── energyResources[]      (required — all physical assets, min 1)
│   │   ├── id                 (meter serial for METER; stable id for DERs)
│   │   ├── type               (discriminator — see kinds below)
│   │   ├── attributes         (kind-specific bag inheriting EnergyResourceCommonAttributes)
│   │   ├── subResources[]     (child resource ids or inline objects)
│   │   └── parentResources[]  (parent resource ids — e.g. the meter a DER sits behind)
│   └── consumptionProfiles[]  (optional — tariff/load per meter, linked via meterId)
└── customerDetails            (optional — PII)
    ├── fullName               (PII — only here)
    ├── installationAddress
    └── serviceConnectionDate
```

## EnergyResource kinds

| Kind | `type` values | CIM class (IEC 61970/61968) |
|------|---------------|-----------------------------|
| `EnergyResourceMeter` | `METER` | `cim:Meter` / `cim:EndDevice` (IEC 61968-9) |
| `EnergyResourceGenerator` | `SOLAR_PV`, `WIND`, `HYDRO`, `BIOGAS`, `CHP`, `FUEL_CELL` | `cim:GeneratingUnit` subtypes (IEC 61970-302) |
| `EnergyResourceStorage` | `BESS` | `cim:BatteryUnit` (IEC 61970-302) |
| `EnergyResourceEVCharger` | `EV_CHARGER`, `EV_V2G` | `cim:ElectricVehicleChargingStation` (CIM17+) |
| `EnergyResourceInverter` | `INVERTER` | `cim:PowerElectronicsConnection` (IEC 61970-302) |
| `EnergyResourceLoad` | `SMART_HVAC`, `SMART_WATER_HEATER`, `CONTROLLABLE_LOAD` | `cim:EnergyConsumer` / `cim:ConformLoad` (IEC 61970-301) |
| `EnergyResourceNetwork` | `DT`, `BUS`, `FEEDER`, `MICROGRID` | `cim:PowerTransformer`, `cim:BusbarSection`, `cim:Feeder`, `cim:Substation` (IEC 61970-301) |

**Deprecated type aliases** (still valid for backward compatibility): `SOLAR` → use `SOLAR_PV`; `BATTERY` → use `BESS`.

## v1.1 → v1.2 migration

| Change | v1.1 (scalar) | v1.2 (QuantitativeValue) |
|--------|---------------|--------------------------|
| Power fields | `ratedPowerKw`, `maxExportKw`, `maxImportKw` (number) | `ratedPower`, `maxExport`, `maxImport` (`{value, unit: W\|kW\|MW}`) |
| Generator nameplate | `nominalPowerKw` (number) | `nominalPower` (`{value, unit: W\|kW\|MW}`) |
| Storage capacity | `storageCapacityKwh` (number) | `storageCapacity` (`{value, unit: kWh\|MWh}`) |
| Apparent power | `ratedApparentPowerKva` (number) | `ratedApparentPower` (`{value, unit: kVA\|MVA}`) |
| Reactive power | `maxReactivePowerKvar`, `minReactivePowerKvar` (number) | `maxReactivePower`, `minReactivePower` (`{value, unit: kVAR\|MVAR}`) |
| Network voltage | `nominalVoltageKv` (number) | `nominalVoltage` (`{value, unit: V\|kV}`) |
| Tariff load | `sanctionedLoadKw`, `contractMaxDemandKw` (number) | `sanctionedLoad`, `contractMaxDemand` (`{value, unit: W\|kW\|MW}`) |

## Files

| File | Description |
|------|-------------|
| `attributes.yaml` | OpenAPI 3.1.1 schema with composable EnergyResource hierarchy |
| `schema.json` | Bundled JSON Schema (draft 2020-12) — self-contained |
| `context.jsonld` | JSON-LD context with unit aliases (kW→qudt:KiloW, kWh→qudt:KiloW-HR, etc.) |
| `vocab.jsonld` | RDF vocabulary with CIM class alignments |
| `examples/example.json` | Single meter + SOLAR_PV + WIND + 2× BESS |
| `examples/example-submetering.json` | Building main meter + 2 tenant sub-meters + rooftop solar |
| `examples/example-parallel-metering.json` | Import meter + export meter (solar FIT) |

For full documentation see the [upstream README](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential/v1.2/README.md).


---

<!-- FIELD-TABLE:START — auto-generated by scripts/generate_field_tables.py from schema.json; do not edit by hand -->
## Field reference

_Auto-generated from `schema.json`. **Field**, **Type** (with units for QuantitativeValue models), and **Description** are derived from the schema; the description is prefixed with the field's **Mandatory**/**Optional** status. **Standard** comes from each field's `x-standard` annotation (`—` when unset). One table per object._

### ElectricityCredential v1.2

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | uri | — | **Mandatory** |
| `type` | list of text | — | **Mandatory** |
| `issuer` | object | — | **Mandatory** |
| `validFrom` | date-time | — | **Mandatory** |
| `validUntil` | date-time | — | **Optional** |
| `credentialStatus` | object | — | **Optional** |
| `credentialSubject` | object | — | **Mandatory** |
| `proof` | object | — | **Optional** |

### CustomerDetails

| Field | Type | Standard | Description |
|---|---|---|---|
| `fullName` | text | CIM (IEC 61968-1 Customer.name) | **Mandatory** — Full name of the customer as per ID proof. |
| `careOf` | list of object | — | **Optional** — Care-of (c/o) reference person(s) used to uniquely identify / disambiguate a customer who may share the same fullName with others in a locality (e.g. a village). Each entry pairs a name with an optional, gender-neutral relationship. |
| `installationAddress` | Location | GeoJSON RFC 7946; schema.org PostalAddress; CIM (IEC 61968-1 ServiceLocation) | **Mandatory** — Physical location of the metered installation. geo (GeoJSON Point, coordinates [longitude, latitude]) is required; address (schema.org PostalAddress fields) is optional. |
| `serviceConnectionDate` | date-time | CIM (IEC 61968-1 ServiceLocation activation date) | **Mandatory** — Date and time the service connection was activated, with timezone offset (ISO 8601). |

### Location

| Field | Type | Standard | Description |
|---|---|---|---|
| `geo` | GeoJSONGeometry | — | **Mandatory** |
| `address` | Address | — | **Optional** |

### GeoJSONGeometry

| Field | Type | Standard | Description |
|---|---|---|---|
| `bbox` | list of number | — | **Optional** — Optional bounding box `[west, south, east, north]` in degrees. |
| `coordinates` | list of — | — | **Optional** — Coordinates per RFC 7946 for all types **except** GeometryCollection. Order is **[lon, lat, (alt)]**. For Polygons, this is an array of linear rings; each ring is an array of positions. |
| `geometries` | list of GeoJSONGeometry | — | **Optional** — Member geometries when `type` is **GeometryCollection**. |
| `type` | Point / LineString / Polygon / MultiPoint / MultiLineString / MultiPolygon / GeometryCollection | — | **Mandatory** |

### Address

| Field | Type | Standard | Description |
|---|---|---|---|
| `addressCountry` | text | — | **Optional** — Country name or ISO-3166-1 alpha-2 code. |
| `addressLocality` | text | — | **Optional** — City/locality. |
| `addressRegion` | text | — | **Optional** — State/region/province. |
| `extendedAddress` | text | — | **Optional** — Address extension (apt/suite/floor, C/O). |
| `postalCode` | text | — | **Optional** — Postal/ZIP code. |
| `streetAddress` | text | — | **Optional** — Street address (building name/number and street). |

### CustomerProfile

| Field | Type | Standard | Description |
|---|---|---|---|
| `customerNumber` | text | — | **Mandatory** — Utility customer account (CA) number. |
| `idRef` | IdRef | — | **Optional** |
| `energyResources` | list of EnergyResource | — | **Mandatory** — All physical energy assets for this account. Each entry is discriminated by 'type' into one of seven composable kinds. |
| `consumptionProfiles` | list of ConsumptionProfile | — | **Optional** — Tariff and load characteristics per meter connection. Each entry links to a METER via meterId. |

### IdRef

| Field | Type | Standard | Description |
|---|---|---|---|
| `issuedBy` | uri | — | **Mandatory** — DID or URI of the issuing authority. |
| `subjectId` | text | — | **Mandatory** — Subject identifier in authority-domain:id-value format. |

### EnergyResourceMeter

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | text | — | **Mandatory** — Stable identifier for this resource. For METER resources the meter serial number is conventional. |
| `type` | text | — | **Mandatory** — Asset-class discriminator. Must be "METER". CIM cim:Meter (IEC 61968-9). |
| `subResources` | list of text or EnergyResource | — | **Optional** — Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. |
| `parentResources` | list of text | — | **Optional** — Upward topology — ids of parent resources. |
| `attributes` | EnergyResourceMeterAttributes | — | **Optional** |

### EnergyResourceCommon

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | text | — | **Optional** — Stable identifier for this resource. For METER resources the meter serial number is conventional. |
| `type` | text | — | **Optional** — Asset class discriminator. Constrained to a kind-specific enum or const in each typed kind schema. |
| `subResources` | list of text or EnergyResource | — | **Optional** — Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. |
| `parentResources` | list of text | — | **Optional** — Upward topology — ids of parent resources. |
| `attributes` | EnergyResourceCommonAttributes | — | **Optional** — Attribute bag. Inherits EnergyResourceCommonAttributes via allOf plus kind-specific fields. |

### EnergyResourceCommonAttributes

| Field | Type | Standard | Description |
|---|---|---|---|
| `make` | text | — | **Optional** — Manufacturer (free text). |
| `model` | text | — | **Optional** — Model (free text). |
| `ratedPower` | QVPower (W / kW / MW) | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | **Optional** — Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. |
| `maxExport` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | **Optional** — Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. |
| `maxImport` | QVPower (W / kW / MW) | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | **Optional** — Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. |
| `telemetryProvider` | text | — | **Optional** — Vendor API / data source identifier for telemetry. |
| `commissioningDate` | date-time | — | **Optional** — ISO 8601 date-time the asset was commissioned. |
| `location` | Location | — | **Optional** — Physical location of this asset. |
| `serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | **Optional** — Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). |
| `inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | **Optional** — Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. |
| `aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | **Optional** — Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. |

### QVPower

| Field | Type | Standard | Description |
|---|---|---|---|
| `value` | number | — | **Mandatory** |
| `unit` | W / kW / MW | — | **Mandatory** |

### EnergyResourceMeterAttributes

| Field | Type | Standard | Description |
|---|---|---|---|
| `make` | text | — | **Optional** — Manufacturer (free text). |
| `model` | text | — | **Optional** — Model (free text). |
| `ratedPower` | QVPower (W / kW / MW) | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | **Optional** — Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. |
| `maxExport` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | **Optional** — Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. |
| `maxImport` | QVPower (W / kW / MW) | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | **Optional** — Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. |
| `telemetryProvider` | text | — | **Optional** — Vendor API / data source identifier for telemetry. |
| `commissioningDate` | date-time | — | **Optional** — ISO 8601 date-time the asset was commissioned. |
| `location` | Location | — | **Optional** — Physical location of this asset. |
| `serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | **Optional** — Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). |
| `inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | **Optional** — Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. |
| `aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | **Optional** — Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. |
| `meterCapability` | Electromechanical / CMRI / AMR / AMI | CIM (IEC 61968-9 AmiBillingReadyKind) | **Optional** — Communication/automation generation. Electromechanical: induction-disc. CMRI: manual optical-port (India legacy). AMR: one-way automated read. AMI: two-way smart meter. |
| `energyDirection` | Forward / Reverse / Bidirectional / Net | CIM (FlowDirectionKind); ESPI NAESB REQ.21 | **Optional** — Energy flow direction metered at this point. |
| `functions` | list of ToU / NetMetering / MaxDemand / LoadControl / TamperDetection / PowerQuality / EventLogging | CIM (IEC 61968-9 EndDeviceFunction) | **Optional** — Active meter capabilities. |
| `feeder` | text | — | **Optional** — Feeder identifier this meter is supplied from. |
| `bus` | text | — | **Optional** — Busbar identifier at the meter's connection point. |
| `communicationTechnology` | PLC / RF_Mesh / GPRS / NB-IoT / LoRa / ZigBee / Other | — | **Optional** — Last-mile physical-layer communication technology. |
| `applicationProtocol` | DLMS_COSEM / ANSI_C12_18 / IEC_61850 / Modbus / Other | — | **Optional** — Application-layer protocol for meter data. DLMS_COSEM: IEC 62056, mandatory for India AMI per BIS IS 16444. ANSI_C12_18: North American. Orthogonal to communicationTechnology (physical layer). |

### EnergyResourceGenerator

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | text | — | **Mandatory** — Stable identifier for this resource. For METER resources the meter serial number is conventional. |
| `type` | SOLAR_PV / SOLAR / WIND / HYDRO / BIOGAS / CHP / FUEL_CELL | — | **Mandatory** — Asset-class discriminator. SOLAR is deprecated — use SOLAR_PV. |
| `subResources` | list of text or EnergyResource | — | **Optional** — Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. |
| `parentResources` | list of text | — | **Optional** — Upward topology — ids of parent resources. |
| `attributes` | EnergyResourceGeneratorAttributes | — | **Optional** |

### EnergyResourceGeneratorAttributes

| Field | Type | Standard | Description |
|---|---|---|---|
| `make` | text | — | **Optional** — Manufacturer (free text). |
| `model` | text | — | **Optional** — Model (free text). |
| `ratedPower` | QVPower (W / kW / MW) | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | **Optional** — Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. |
| `maxExport` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | **Optional** — Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. |
| `maxImport` | QVPower (W / kW / MW) | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | **Optional** — Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. |
| `telemetryProvider` | text | — | **Optional** — Vendor API / data source identifier for telemetry. |
| `commissioningDate` | date-time | — | **Optional** — ISO 8601 date-time the asset was commissioned. |
| `location` | Location | — | **Optional** — Physical location of this asset. |
| `serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | **Optional** — Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). |
| `inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | **Optional** — Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. |
| `aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | **Optional** — Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. |
| `nominalPower` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.nominalP) | **Optional** — Nominal (nameplate) power output. Use when distinct from maxExport (peak). |
| `efficiency` | number | — | **Optional** — Conversion efficiency as a percentage (0–100). Most relevant for FUEL_CELL and CHP resources. |
| `dcArrayCapacity` | QVPower (W / kW / MW) | IS 16221 (PV module qualification); IEC 61727 (PV grid interface) | **Optional** — DC-side nameplate capacity of a photovoltaic array at Standard Test Conditions (industry term: "kWp"). For PV systems this is typically larger than the AC-side maxExport because of inverter clipping and DC-to-AC ratios. Relevant for SOLAR_PV resources. The unit is the standard QUDT power alias kW — the STC/peak semantic is documented here, not encoded in the unit string. |

### EnergyResourceStorage

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | text | — | **Mandatory** — Stable identifier for this resource. For METER resources the meter serial number is conventional. |
| `type` | BESS / BATTERY | — | **Mandatory** — Asset-class discriminator. BATTERY is deprecated — use BESS. CIM: BatteryUnit (IEC 61970-302). |
| `subResources` | list of text or EnergyResource | — | **Optional** — Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. |
| `parentResources` | list of text | — | **Optional** — Upward topology — ids of parent resources. |
| `attributes` | EnergyResourceStorageAttributes | — | **Optional** |

### EnergyResourceStorageAttributes

| Field | Type | Standard | Description |
|---|---|---|---|
| `make` | text | — | **Optional** — Manufacturer (free text). |
| `model` | text | — | **Optional** — Model (free text). |
| `ratedPower` | QVPower (W / kW / MW) | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | **Optional** — Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. |
| `maxExport` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | **Optional** — Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. |
| `maxImport` | QVPower (W / kW / MW) | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | **Optional** — Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. |
| `telemetryProvider` | text | — | **Optional** — Vendor API / data source identifier for telemetry. |
| `commissioningDate` | date-time | — | **Optional** — ISO 8601 date-time the asset was commissioned. |
| `location` | Location | — | **Optional** — Physical location of this asset. |
| `serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | **Optional** — Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). |
| `inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | **Optional** — Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. |
| `aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | **Optional** — Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. |
| `storageCapacity` | QVEnergy (kWh / MWh) | CIM (IEC 61970-302 BatteryUnit.ratedE) | **Optional** — Rated stored-energy capacity. Replaces storageCapacityKwh from v1.0. |
| `storageType` | LithiumIon / LeadAcid / FlowBattery / NaS / NiCd / Flywheel / Other | — | **Optional** — Battery storage technology type. |
| `stateOfHealthPct` | number | — | **Optional** — Battery state-of-health as a percentage (0–100). |
| `roundTripEfficiencyPct` | number | IEC 62933-2-1 (performance test method) | **Optional** — AC-to-AC round-trip efficiency as a percentage (0–100): the fraction of energy returned to the grid relative to energy drawn during a full charge/discharge cycle. Distinct from stateOfHealthPct (cumulative life indicator) and from inverter conversion efficiency. |

### QVEnergy

| Field | Type | Standard | Description |
|---|---|---|---|
| `value` | number | — | **Mandatory** |
| `unit` | kWh / MWh | — | **Mandatory** |

### EnergyResourceEVCharger

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | text | — | **Mandatory** — Stable identifier for this resource. For METER resources the meter serial number is conventional. |
| `type` | EV_CHARGER / EV_V2G | — | **Mandatory** — Asset-class discriminator. EV_CHARGER: EVSE hardware. EV_V2G: Vehicle-to-Grid capable EVSE with ISO 15118-20 / OCPP 2.1 BPT. |
| `subResources` | list of text or EnergyResource | — | **Optional** — Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. |
| `parentResources` | list of text | — | **Optional** — Upward topology — ids of parent resources. |
| `attributes` | EnergyResourceEVChargerAttributes | — | **Optional** |

### EnergyResourceEVChargerAttributes

| Field | Type | Standard | Description |
|---|---|---|---|
| `make` | text | — | **Optional** — Manufacturer (free text). |
| `model` | text | — | **Optional** — Model (free text). |
| `ratedPower` | QVPower (W / kW / MW) | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | **Optional** — Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. |
| `maxExport` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | **Optional** — Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. |
| `maxImport` | QVPower (W / kW / MW) | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | **Optional** — Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. |
| `telemetryProvider` | text | — | **Optional** — Vendor API / data source identifier for telemetry. |
| `commissioningDate` | date-time | — | **Optional** — ISO 8601 date-time the asset was commissioned. |
| `location` | Location | — | **Optional** — Physical location of this asset. |
| `serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | **Optional** — Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). |
| `inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | **Optional** — Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. |
| `aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | **Optional** — Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. |
| `connectorType` | Type1 / Type2 / CCS1 / CCS2 / CHAdeMO / GB_T / NACS / Other | — | **Optional** — Physical connector standard. Type1: IEC 62196-2 Type 1 (J1772). Type2: IEC 62196-2 Type 2 (Mennekes). CCS1/CCS2: Combined Charging System DC fast charge. CHAdeMO: CHAdeMO DC fast charge. GB_T: GB/T 20234. NACS: SAE J3400. |
| `controlProtocol` | OCPP_1.6 / OCPP_2.0.1 / OCPP_2.1 / ISO_15118_2 / ISO_15118_20 / Other | — | **Optional** — EVSE control and smart-charging protocol. |
| `v2xProtocol` | CHAdeMO_V2G / CCS_BPT / ISO_15118_20_AC_BPT / ISO_15118_20_DC_BPT / Other | — | **Optional** — Vehicle-to-Grid / V2X protocol. Present only for EV_V2G resources. |

### EnergyResourceInverter

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | text | — | **Mandatory** — Stable identifier for this resource. For METER resources the meter serial number is conventional. |
| `type` | text | — | **Mandatory** — Asset-class discriminator. Must be "INVERTER". CIM: PowerElectronicsConnection (IEC 61970-302). |
| `subResources` | list of text or EnergyResource | — | **Optional** — Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. |
| `parentResources` | list of text | — | **Optional** — Upward topology — ids of parent resources. |
| `attributes` | EnergyResourceInverterAttributes | — | **Optional** |

### EnergyResourceInverterAttributes

| Field | Type | Standard | Description |
|---|---|---|---|
| `make` | text | — | **Optional** — Manufacturer (free text). |
| `model` | text | — | **Optional** — Model (free text). |
| `ratedPower` | QVPower (W / kW / MW) | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | **Optional** — Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. |
| `maxExport` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | **Optional** — Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. |
| `maxImport` | QVPower (W / kW / MW) | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | **Optional** — Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. |
| `telemetryProvider` | text | — | **Optional** — Vendor API / data source identifier for telemetry. |
| `commissioningDate` | date-time | — | **Optional** — ISO 8601 date-time the asset was commissioned. |
| `location` | Location | — | **Optional** — Physical location of this asset. |
| `serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | **Optional** — Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). |
| `inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | **Optional** — Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. |
| `aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | **Optional** — Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. |
| `ratedApparentPower` | QVApparentPower (kVA / MVA) | SunSpec DER Model 702 (maxVA); CIM (IEC 61970-302 PowerElectronicsConnection.ratedS) | **Optional** — Rated apparent power. Replaces ratedApparentPowerKva from v1.0. |
| `maxReactivePower` | QVReactivePower (kVAR / MVAR) | SunSpec DER Model 702 (maxVar); CIM (IEC 61970-302 PowerElectronicsConnection.maxQ) | **Optional** — Maximum reactive power injection (leading / over-excited). Replaces maxReactivePowerKvar from v1.0. |
| `minReactivePower` | QVReactivePower (kVAR / MVAR) | SunSpec DER Model 702 (maxVarNeg); CIM (IEC 61970-302 PowerElectronicsConnection.minQ) | **Optional** — Maximum reactive power absorption (lagging / under-excited). Value is typically negative. Replaces minReactivePowerKvar from v1.0. |
| `rideThroughCategory` | CategoryI / CategoryII / CategoryIII | IEEE 1547-2018 (ride-through category) | **Optional** — Abnormal operating performance category. CategoryI: basic. CategoryII: enhanced for distribution-connected DER. CategoryIII: advanced for large/transmission-connected DER. |
| `operatingMode` | GridFollowing / GridForming / Standby | CIM (IEC 61970-302 PowerElectronicsConnection.inverterMode) | **Optional** — Inverter grid-interaction mode. GridFollowing: PLL-based sync. GridForming: own V/f reference (microgrid islanding, black-start). Standby: energised but not injecting. |
| `voltVarEnabled` | yes / no | IEEE 2030.5 (opModVoltVar); SunSpec DER Model 705 | **Optional** — Volt-VAr curve active. |
| `freqDroopEnabled` | yes / no | IEEE 1547-2018; SunSpec DER Model 711 | **Optional** — Frequency-Watt droop active. |
| `enterServiceRampTimeSec` | number | SunSpec DER Model 703 (ESRmpTms) | **Optional** — Seconds to ramp from 0 to rated power after reconnection. |

### QVApparentPower

| Field | Type | Standard | Description |
|---|---|---|---|
| `value` | number | — | **Mandatory** |
| `unit` | kVA / MVA | — | **Mandatory** |

### QVReactivePower

| Field | Type | Standard | Description |
|---|---|---|---|
| `value` | number | — | **Mandatory** |
| `unit` | kVAR / MVAR | — | **Mandatory** |

### EnergyResourceLoad

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | text | — | **Mandatory** — Stable identifier for this resource. For METER resources the meter serial number is conventional. |
| `type` | SMART_HVAC / SMART_WATER_HEATER / CONTROLLABLE_LOAD | — | **Mandatory** — Asset-class discriminator. CIM: EnergyConsumer / ConformLoad (IEC 61970-301). |
| `subResources` | list of text or EnergyResource | — | **Optional** — Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. |
| `parentResources` | list of text | — | **Optional** — Upward topology — ids of parent resources. |
| `attributes` | EnergyResourceLoadAttributes | — | **Optional** |

### EnergyResourceLoadAttributes

| Field | Type | Standard | Description |
|---|---|---|---|
| `make` | text | — | **Optional** — Manufacturer (free text). |
| `model` | text | — | **Optional** — Model (free text). |
| `ratedPower` | QVPower (W / kW / MW) | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | **Optional** — Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. |
| `maxExport` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | **Optional** — Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. |
| `maxImport` | QVPower (W / kW / MW) | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | **Optional** — Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. |
| `telemetryProvider` | text | — | **Optional** — Vendor API / data source identifier for telemetry. |
| `commissioningDate` | date-time | — | **Optional** — ISO 8601 date-time the asset was commissioned. |
| `location` | Location | — | **Optional** — Physical location of this asset. |
| `serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | **Optional** — Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). |
| `inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | **Optional** — Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. |
| `aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | **Optional** — Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. |
| `controlProtocol` | OpenADR_2.0b / OCPP_2.0.1 / SunSpec_Modbus / EEBus / Modbus / Other | — | **Optional** — Demand-response / control protocol supported by this load device. |
| `loadCategory` | Heating / Cooling / WaterHeating / Lighting / EV / Industrial / Other | CIM (IEC 61970-301 ConformLoad classification) | **Optional** — Functional category of this load. |

### EnergyResourceNetwork

| Field | Type | Standard | Description |
|---|---|---|---|
| `id` | text | — | **Mandatory** — Stable identifier for this resource. For METER resources the meter serial number is conventional. |
| `type` | DT / BUS / FEEDER / MICROGRID | — | **Mandatory** — Asset-class discriminator. DT → PowerTransformer, BUS → BusbarSection, FEEDER → Feeder (EquipmentContainer), MICROGRID → Substation / microgrid container (IEC 61970-301). |
| `subResources` | list of text or EnergyResource | — | **Optional** — Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. |
| `parentResources` | list of text | — | **Optional** — Upward topology — ids of parent resources. |
| `attributes` | EnergyResourceNetworkAttributes | — | **Optional** |

### EnergyResourceNetworkAttributes

| Field | Type | Standard | Description |
|---|---|---|---|
| `make` | text | — | **Optional** — Manufacturer (free text). |
| `model` | text | — | **Optional** — Model (free text). |
| `ratedPower` | QVPower (W / kW / MW) | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | **Optional** — Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. |
| `maxExport` | QVPower (W / kW / MW) | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | **Optional** — Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. |
| `maxImport` | QVPower (W / kW / MW) | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | **Optional** — Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. |
| `telemetryProvider` | text | — | **Optional** — Vendor API / data source identifier for telemetry. |
| `commissioningDate` | date-time | — | **Optional** — ISO 8601 date-time the asset was commissioned. |
| `location` | Location | — | **Optional** — Physical location of this asset. |
| `serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | **Optional** — Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). |
| `inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | **Optional** — Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. |
| `aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | **Optional** — Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. |
| `nominalVoltage` | QVVoltage (V / kV) | CIM (IEC 61970-301 BaseVoltage.nominalVoltage) | **Optional** — Nominal operating voltage. Replaces nominalVoltageKv from v1.0. |
| `zone` | text | — | **Optional** — Operating zone or region identifier used by the utility. |
| `substationId` | text | — | **Optional** — Parent substation identifier per utility records. |
| `feederCode` | text | — | **Optional** — Feeder code per utility records. Relevant for FEEDER and DT resources. |

### QVVoltage

| Field | Type | Standard | Description |
|---|---|---|---|
| `value` | number | — | **Mandatory** |
| `unit` | V / kV | — | **Mandatory** |

### ConsumptionProfile

| Field | Type | Standard | Description |
|---|---|---|---|
| `meterId` | text | — | **Mandatory** — Matches the id of a METER entry in customerProfile.energyResources[]. |
| `sanctionedLoad` | QVPower (W / kW / MW) | CIM (IEC 61968-9 UsagePoint) | **Mandatory** — Sanctioned/approved import load. |
| `sanctionedExportLoad` | QVPower (W / kW / MW) | — | **Optional** — Sanctioned/approved grid export limit. |
| `billingCycleDay` | integer | — | **Optional** — Day of month on which the billing cycle resets. |
| `contractMaxDemand` | QVPower (W / kW / MW) | — | **Optional** — Maximum demand contracted with the utility for this connection. |
| `tariffCategoryCode` | text | CIM (IEC 61968-9 UsagePoint.serviceCategory) | **Mandatory** — Billing/tariff category code assigned by the utility. |
| `premisesType` | Residential / Commercial / Industrial / Agricultural | — | **Optional** — Type of premises at the metering point. |
| `connectionType` | Single-phase / Three-phase | CIM (IEC 61968-9 UsagePoint.phaseCode) | **Optional** — Electrical connection type. |
| `paymentMode` | POSTPAID / PREPAID | CIM (IEC 61968-9 AmiBillingReadyKind, ESPI) | **Optional** — Billing/payment modality. POSTPAID: consume now, pay later. PREPAID: pay-before-use. |
| `serviceStatus` | active / suspended / closed | CIM (IEC 61968-9 UsagePoint.status) | **Optional** — Lifecycle state of the service connection (the UsagePoint), not of the meter device itself. 'active' = currently energised and billable; 'suspended' = temporarily disconnected (non-payment, inspection, fault) with the contract still on record; 'closed' = permanently terminated. Distinct from the meter device's operational state. |

<!-- FIELD-TABLE:END -->
