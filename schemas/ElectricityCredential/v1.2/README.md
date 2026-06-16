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

## EnergyResourceCommonAttributes

Inherited by all seven kinds via `allOf`. All power fields are `QVPower {value, unit: W|kW|MW}`.

| Field | Type | Description |
|-------|------|-------------|
| `make` | string | Manufacturer name |
| `model` | string | Model number |
| `ratedPower` | QVPower | Nameplate peak power — kept for backward compatibility; prefer `maxExport` |
| `maxExport` | QVPower | Max power injected to grid (generates/discharges). Always ≥0. unit: W\|kW\|MW |
| `maxImport` | QVPower | Max power drawn from grid (absorbs/charges). Always ≥0. unit: W\|kW\|MW |
| `telemetryProvider` | string | Vendor API / data-source for telemetry |
| `commissioningDate` | date-time | ISO 8601 commissioning date-time |
| `location` | object | `geo` (GeoJSONGeometry) + optional `address` (PostalAddress) |
| `serialNumber` | string | Equipment-nameplate device serial. CIM `EndDeviceInfo.serialNumber` (IEC 61968-9). Distinct from the network DID in `id`. |
| `inspection` | object | Commissioning / safety inspection record: `{date, result: pass\|fail\|conditional, inspectorId}`. IEEE 1547-2018 Cl. 11; CEA Connectivity Regs 2013. |
| `aggregator` | object | Third-party demand-flex enrolment: `{id (URI), name, controllable (bool), enrolledOn (date)}`. `controllable:false` = observation-only. IEEE 2030.5 / IEC 61850-7-420. |

## Kind-specific attributes

### EnergyResourceMeter (type: `METER`)

| Field | Type | Description |
|-------|------|-------------|
| `meterCapability` | enum | `Electromechanical` · `CMRI` · `AMR` · `AMI` |
| `energyDirection` | enum | `Forward` (default) · `Reverse` · `Bidirectional` · `Net` |
| `functions` | array of enum | `ToU` · `NetMetering` · `MaxDemand` · `LoadControl` · `TamperDetection` · `PowerQuality` · `EventLogging` |
| `feeder` | string | Feeder identifier |
| `bus` | string | Busbar identifier |
| `communicationTechnology` | enum | `PLC` · `RF_Mesh` · `GPRS` · `NB-IoT` · `LoRa` · `ZigBee` · `Other` |
| `applicationProtocol` | enum | `DLMS_COSEM` · `ANSI_C12_18` · `IEC_61850` · `Modbus` · `Other` |

### EnergyResourceGenerator (type: `SOLAR_PV` | `WIND` | `HYDRO` | `BIOGAS` | `CHP` | `FUEL_CELL`)

| Field | Type | Description |
|-------|------|-------------|
| `nominalPower` | QVPower | Nominal output power, unit: W\|kW\|MW |
| `efficiency` | number (0–100) | Conversion efficiency, % |
| `dcArrayCapacity` | QVPower | DC-side PV array nameplate at STC (industry "kWp"). SOLAR_PV. Distinct from AC `maxExport`. unit: W\|kW\|MW. IS 16221; IEC 61727. |

### EnergyResourceStorage (type: `BESS`)

`storageCapacity` is **exclusive to this kind**. Discharge: `maxExport`. Charge: `maxImport`.

| Field | Type | Description |
|-------|------|-------------|
| `storageCapacity` | QVEnergy | Rated energy capacity, unit: kWh\|MWh |
| `storageType` | enum | LithiumIon, LeadAcid, FlowBattery, NaS, NiCd, Flywheel, Other |
| `stateOfHealthPct` | number (0–100) | Battery SoH as % of original capacity |
| `roundTripEfficiencyPct` | number (0–100) | AC-to-AC round-trip efficiency over a full charge/discharge cycle. IEC 62933-2-1. |

### EnergyResourceEVCharger (type: `EV_CHARGER` | `EV_V2G`)

EV charging station (EVSE) — a **flexible load**, not a storage resource. `EV_V2G` adds ISO 15118-20 / OCPP 2.1 BPT bidirectional capability.

| Field | Type | Description |
|-------|------|-------------|
| `connectorType` | enum | Type1, Type2, CCS1, CCS2, CHAdeMO, GB_T, NACS, Other |
| `controlProtocol` | enum | OCPP_1.6, OCPP_2.0.1, OCPP_2.1, ISO_15118_2, ISO_15118_20, Other |
| `v2xProtocol` | enum | CHAdeMO_V2G, CCS_BPT, ISO_15118_20_AC_BPT, ISO_15118_20_DC_BPT, Other |

### EnergyResourceInverter (type: `INVERTER`)

Grid-connected power-electronics converter. IEEE 1547-2018 / SunSpec DER Models 702–714.

| Field | Type | Description |
|-------|------|-------------|
| `ratedApparentPower` | QVApparentPower | Rated apparent power, unit: kVA\|MVA |
| `maxReactivePower` | QVReactivePower | Max reactive power injection (leading), unit: kVAR\|MVAR. Always ≥0. |
| `minReactivePower` | QVReactivePower | Max reactive power absorption (lagging); value typically negative, unit: kVAR\|MVAR |
| `rideThroughCategory` | enum | CategoryI / CategoryII / CategoryIII (IEEE 1547-2018) |
| `operatingMode` | enum | GridFollowing / GridForming / Standby |
| `voltVarEnabled` | boolean | Volt-VAr curve active |
| `freqDroopEnabled` | boolean | Frequency-Watt droop active |
| `enterServiceRampTimeSec` | number | Ramp-up time after reconnect, seconds |

### EnergyResourceLoad (type: `SMART_HVAC` | `SMART_WATER_HEATER` | `CONTROLLABLE_LOAD`)

| Field | Type | Description |
|-------|------|-------------|
| `controlProtocol` | enum | OpenADR_2.0b, OCPP_2.0.1, SunSpec_Modbus, EEBus, Modbus, Other |
| `loadCategory` | enum | Heating, Cooling, WaterHeating, Lighting, EV, Industrial, Other |

### EnergyResourceNetwork (type: `DT` | `BUS` | `FEEDER` | `MICROGRID`)

| Field | Type | Description |
|-------|------|-------------|
| `nominalVoltage` | QVVoltage | Nominal voltage, unit: V\|kV |
| `zone` | string | Operating zone / region identifier |
| `substationId` | string | Parent substation identifier |
| `feederCode` | string | Feeder code per utility records |

## ConsumptionProfile (MeterServiceProfile/v1.1)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `meterId` | string | Yes | Matches `id` of a METER entry in `energyResources[]` |
| `sanctionedLoad` | QVPower | Yes | Utility-approved load, unit: W\|kW\|MW |
| `sanctionedExportLoad` | QVPower | No | Sanctioned grid export limit, unit: W\|kW\|MW |
| `billingCycleDay` | integer (1–31) | No | Day of month the billing cycle resets |
| `contractMaxDemand` | QVPower | No | Maximum demand contracted with the utility, unit: W\|kW\|MW |
| `tariffCategoryCode` | string | Yes | Billing/tariff category code |
| `premisesType` | enum | No | Residential, Commercial, Industrial, Agricultural |
| `connectionType` | enum | No | Single-phase, Three-phase |
| `paymentMode` | enum | No | POSTPAID, PREPAID |
| `serviceStatus` | enum | No | `active`, `suspended`, `closed`. CIM `UsagePoint.status`. State of the service connection, not of the meter device. |

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
