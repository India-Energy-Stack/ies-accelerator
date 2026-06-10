> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/vocab.jsonld) · [examples/](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/examples)

> **Mirror.** Files in this directory are mirrored verbatim from [`beckn/DEG/specification/schema/ElectricityCredential/v1.2/`](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential/v1.2). Upstream is canonical.

# ElectricityCredential v1.2

W3C Verifiable Credential (VC Data Model 2.0) issued per meter by electricity distribution utilities.

v1.2 introduces a **composable EnergyResource hierarchy**: each entry in `energyResources[]` is discriminated by `type` into one of **seven** typed kinds, each with a typed `attributes` bag.

| Kind | `type` values |
|------|--------------|
| `EnergyResourceMeter` | `METER` |
| `EnergyResourceGenerator` | `SOLAR_PV`, `WIND`, `HYDRO`, `BIOGAS`, `CHP`, `FUEL_CELL` |
| `EnergyResourceStorage` | `BESS` |
| `EnergyResourceEVCharger` | `EV_CHARGER`, `EV_V2G` |
| `EnergyResourceInverter` | `INVERTER` |
| `EnergyResourceLoad` | `SMART_HVAC`, `SMART_WATER_HEATER`, `CONTROLLABLE_LOAD` |
| `EnergyResourceNetwork` | `DT`, `BUS`, `FEEDER`, `MICROGRID` |

## Key changes from v1.1

| Change | v1.1 | v1.2 |
|--------|------|------|
| EnergyResource structure | Single flat schema | `oneOf` 7 composable kinds |
| EV charger / V2G | Grouped with Storage | Own kind `EnergyResourceEVCharger` |
| Inverter | — | New `EnergyResourceInverter` kind (IEEE 1547-2018 / SunSpec) |
| Power fields | `ratedPowerKw` | `maxExportKw` + `maxImportKw` (directional, both ≥ 0) |
| Meter type | `meterType` flat enum | `meterCapability` + `energyDirection` + `functions[]` (orthogonal) |
| Application protocol | — | `applicationProtocol` enum (DLMS_COSEM, ANSI_C12_18, …) |
| Storage capacity field | `energyCapacityKwh` | `storageCapacityKwh` (Storage kind only) |
| `gps` / location | `gps: "lat,lng"` string | `location: {geo: GeoJSONGeometry, address: Address}` |
| ConsumptionProfile | Inline in credential | External `MeterServiceProfile/v1.0` (alias kept for backward compat) |
| `billingMode` | on meter | `paymentMode` on `MeterServiceProfile` (POSTPAID/PREPAID) |
| `sanctionedLoadKW` | uppercase KW | `sanctionedLoadKw` (SI casing) |
| New generator fields | — | `nominalPowerKw`, `efficiency` |
| New load fields | — | `controlProtocol`, `loadCategory` |
| New network fields | — | `nominalVoltageKv`, `zone`, `substationId`, `feederCode` |
| SOLAR deprecated | `type: "SOLAR"` | `type: "SOLAR_PV"` (preferred) |
| BATTERY deprecated | `type: "BATTERY"` | `type: "BESS"` (preferred) |

## Files

| File | Description |
|------|-------------|
| `attributes.yaml` | OpenAPI 3.1.1 schema with composable EnergyResource hierarchy |
| `schema.json` | Bundled JSON Schema (draft 2020-12) — self-contained |
| `context.jsonld` | JSON-LD context |
| `vocab.jsonld` | RDF vocabulary with CIM class alignments |
| `examples/example.json` | Single meter + SOLAR_PV + WIND + 2× BESS |
| `examples/example-submetering.json` | Building main meter + 2 tenant sub-meters + rooftop solar |
| `examples/example-parallel-metering.json` | Import meter + export meter (solar FIT) |

For full documentation see the [upstream README](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential/v1.2/README.md).
